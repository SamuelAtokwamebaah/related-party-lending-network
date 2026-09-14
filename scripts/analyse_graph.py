"""
Phase 2 - build the graph and run the analyses.

Reads db/graph.db, builds a directed multigraph in NetworkX, and answers four
investigator's questions. It writes docs/phase2/FINDINGS.md and a machine
-readable docs/phase2/metrics.json, and it reports what the evidence does not
support as plainly as what it does.

The framing follows the Phase 0 gate decision. The documented graph is in
seventeen components, so whole-network centrality and community detection are
not informative here. They are computed anyway and reported as a documented
non-result, because "we ran it and it says nothing, and here is why" is a
defensible answer and a fabricated ranking is not.

Inferred edges are excluded from every figure. Edges are reported by confidence
class throughout, so a reader can see how much rests on a named counterparty and
how much on one the Bank of Ghana described but did not name.

This module is imported, not run: scripts/phase2_report.py calls it and writes
the output. Kept separate so the numbers cannot be adjusted while prose is being
tuned around them.
"""

import json
import sqlite3
from collections import Counter, defaultdict
from pathlib import Path

import networkx as nx

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "db" / "graph.db"
OUT = ROOT / "docs" / "phase2"


def load_graph(con, layer="related_party"):
    """A MultiDiGraph of the documented evidence base. Inferred edges excluded.

    layer defaults to related_party, which is the graph every headline figure in
    this project describes. Passing layer=None returns both layers together, and
    that combined graph is a different object with a different meaning: it also
    contains fund managers placing client money in the 23 with no related-party
    claim in the source. It is reported separately and never mixed into the
    related-party figures.
    """
    g = nx.MultiDiGraph()
    for row in con.execute("""
            SELECT entity_id, canonical_name, entity_type, scope_class, regulator,
                   jurisdiction, member_count, is_named
            FROM entities"""):
        g.add_node(row[0], name=row[1], entity_type=row[2], scope_class=row[3],
                   regulator=row[4], jurisdiction=row[5], member_count=row[6],
                   is_named=row[7])
    for row in con.execute("""
            SELECT e.edge_id, e.source_entity_id, e.target_entity_id, e.relationship,
                   rt.category, rt.extracts_value, e.amount_value, e.amount_currency,
                   e.amount_unit, e.amount_basis, e.confidence, rt.layer
            FROM edges e
            JOIN relationship_types rt ON rt.relationship = e.relationship
            WHERE e.confidence <> 'inferred'
              AND (e.version_removed IS NULL OR e.version_removed = '')
              AND (? IS NULL OR rt.layer = ?)""", (layer, layer)):
        g.add_edge(row[1], row[2], key=row[0], relationship=row[3], category=row[4],
                   extracts_value=row[5], amount_value=row[6], amount_currency=row[7],
                   amount_unit=row[8], amount_basis=row[9], confidence=row[10],
                   layer=row[11])
    # Nodes no edge touches are not part of the graph's structure.
    g.remove_nodes_from([n for n in list(g.nodes) if g.degree(n) == 0])
    return g


def shape(g):
    """Question 0: what shape is this graph, and what can it therefore support?"""
    undirected = nx.Graph(g)
    components = sorted(nx.connected_components(undirected), key=len, reverse=True)
    return {
        "nodes": g.number_of_nodes(),
        "edges": g.number_of_edges(),
        "components": len(components),
        "component_sizes": [len(c) for c in components],
        "largest_components": [
            sorted(g.nodes[n]["name"] for n in c) for c in components[:2]
        ],
        "density": round(nx.density(nx.DiGraph(g)), 4),
    }


def hubs(g):
    """Question 1: does anyone connect more than one failed institution?

    Degree centrality counts a node's connections. Betweenness counts how often
    a node sits on the shortest path between two others - the broker measure,
    and the one that identifies a person or company bridging separate failures.
    Betweenness is only meaningful inside a connected structure: a node in a
    two-node component can lie on no path between anything.
    """
    simple = nx.Graph(g)
    degree = nx.degree_centrality(simple)
    between = nx.betweenness_centrality(simple)

    # The question the project was set to answer.
    institutions_touched = defaultdict(set)
    for node in g.nodes:
        if g.nodes[node]["scope_class"] == "core_23":
            continue
        for neighbour in set(simple.neighbors(node)):
            if g.nodes[neighbour]["scope_class"] == "core_23":
                institutions_touched[node].add(neighbour)

    multi = {g.nodes[n]["name"]: sorted(g.nodes[i]["name"] for i in insts)
             for n, insts in institutions_touched.items() if len(insts) > 1}

    ranked = sorted(g.nodes, key=lambda n: (-degree[n], g.nodes[n]["name"]))
    return {
        "nonzero_betweenness": sum(1 for v in between.values() if v > 0),
        "max_betweenness": round(max(between.values()), 4) if between else 0.0,
        "top_degree": [
            {"name": g.nodes[n]["name"], "type": g.nodes[n]["entity_type"],
             "degree": simple.degree(n), "degree_centrality": round(degree[n], 4),
             "betweenness": round(between[n], 4)}
            for n in ranked[:10]
        ],
        "connect_multiple_institutions": multi,
    }


def loops(g):
    """Question 2: does ownership or lending fold back on itself?

    A cycle is a path that returns to where it started. In a related-party
    structure a cycle is the signature worth looking for: value leaves an
    institution and control over it comes back, or two institutions lend to each
    other. Direction is what makes this meaningful, so it is run on the directed
    graph.
    """
    simple = nx.DiGraph()
    for u, v, data in sorted(g.edges(data=True), key=lambda e: (e[0], e[1])):
        simple.add_edge(u, v)
    found = []
    for cycle in nx.simple_cycles(simple):
        # A cycle has no start. simple_cycles returns it rotated to wherever its
        # search happened to begin, and that varies between processes, so two
        # runs described the same loop from different nodes and the committed
        # findings did not match a fresh build. Rotating to the lowest-sorting
        # member fixes the description without changing the loop.
        pivot = cycle.index(min(cycle))
        cycle = cycle[pivot:] + cycle[:pivot]
        members = [g.nodes[n]["name"] for n in cycle]
        legs = []
        for i, u in enumerate(cycle):
            v = cycle[(i + 1) % len(cycle)]
            # A leg extracts value only if some edge along it does. A cycle
            # whose return leg is, say, a merger application is not value
            # coming back, and the distinction decides what may be claimed.
            edges = list(g.get_edge_data(u, v).values())
            legs.append({
                "_from_id": u,
                "from": g.nodes[u]["name"],
                "to": g.nodes[v]["name"],
                "relationships": sorted({d["relationship"] for d in edges}),
                "extracts_value": any(d["extracts_value"] for d in edges),
            })
        found.append({
            "members": members,
            "legs": legs,
            "all_legs_extract_value": all(leg["extracts_value"] for leg in legs),
            # Whether any leg runs out of one of the 23. A loop where value only
            # ever moves toward an institution is circular funding, not value
            # leaving it, and the two should not carry the same name.
            "leaves_an_institution": any(
                g.nodes[leg["_from_id"]]["scope_class"] == "core_23"
                and leg["extracts_value"] for leg in legs),
        })
    # And the cycles themselves come back in search order, which varies too.
    found.sort(key=lambda c: (len(c["members"]), c["members"]))
    closed = [c for c in found if c["all_legs_extract_value"]]
    for c in found:
        for leg in c["legs"]:
            leg.pop("_from_id", None)
    return {
        "count": len(found),
        # Every leg moves value. Named for what it is rather than for what it
        # would be nice to have found: in the one case here, value leaves an
        # institution to a related party and that related party's client money
        # funds the same institution. That is circular funding between related
        # parties. Calling it an extraction loop claims a direction the
        # documents do not establish.
        "circular_funding_loops": len(closed),
        "of_which_leave_an_institution": sum(
            1 for c in closed if c["leaves_an_institution"]),
        "cycles": found,
    }


def communities(g):
    """Question 3: do clusters of institutions share owners or counterparties?

    Community detection looks for groups of nodes more densely connected to each
    other than to the rest of the graph. It can only find such a group inside a
    connected structure; across disconnected components it can do no better than
    return the components themselves, which is not a finding.
    """
    undirected = nx.Graph(g)
    comps = list(nx.connected_components(undirected))
    detected = list(nx.community.greedy_modularity_communities(undirected))
    same = sorted([sorted(c) for c in comps]) == sorted([sorted(c) for c in detected])
    return {
        "components": len(comps),
        "communities_detected": len(detected),
        "communities_equal_components": same,
        "modularity": round(nx.community.modularity(undirected, detected), 4),
    }


def typology(con, layer="related_party"):
    """The mechanisms the notices describe, counted.

    Split by which end of the edge one of the 23 sits at. extracts_value says
    value moved along the relationship; it does not say which way relative to a
    failed institution. Counting all of them together as "how value left the
    institutions" overstated it: of the related-party edges, well under half
    have one of the 23 as the source, and thirteen involve none of them at all -
    they are fund managers draining their own related parties, which is a real
    finding and a different one.
    """
    rows = con.execute("""
        SELECT rt.category, rt.relationship, rt.extracts_value, COUNT(*) AS n,
               SUM(CASE WHEN e.confidence = 'documented' THEN 1 ELSE 0 END),
               CASE WHEN se.scope_class = 'core_23' THEN 'from_institution'
                    WHEN te.scope_class = 'core_23' THEN 'into_institution'
                    ELSE 'between_third_parties' END
        FROM edges e
        JOIN relationship_types rt ON rt.relationship = e.relationship
        JOIN entities se ON se.entity_id = e.source_entity_id
        JOIN entities te ON te.entity_id = e.target_entity_id
        WHERE e.confidence <> 'inferred'
          AND (e.version_removed IS NULL OR e.version_removed = '')
          AND (? IS NULL OR rt.layer = ?)
        GROUP BY rt.category, rt.relationship, rt.extracts_value, 6
        ORDER BY rt.category, n DESC""", (layer, layer)).fetchall()
    return [{"category": r[0], "relationship": r[1], "extracts_value": bool(r[2]),
             "edges": r[3], "named_counterparty": r[4], "direction": r[5]}
            for r in rows]


def placement_layer(con):
    """The placement layer, reported on its own.

    A fund manager putting client money into one of the 23 is not an insider
    relationship and is not evidence of one. What makes it worth reporting is
    that the same institutions recur as destinations across fund managers with
    no stated connection to each other, which is a fact about where client money
    went and not about who owned whom. It is kept out of every related-party
    figure and out of the component count.
    """
    rows = con.execute("""
        SELECT fund_manager, institution, related_party_exposure,
               amount_value, amount_basis, amount_note, edge_id, verification
        FROM v_placement_into_23
        ORDER BY institution, fund_manager""").fetchall()
    by_institution = defaultdict(list)
    for r in rows:
        by_institution[r[1]].append({
            "fund_manager": r[0], "amount_value": r[3], "amount_basis": r[4],
            "amount_note": r[5], "edge_id": r[6], "verification": r[7],
        })
    managers = {r[0] for r in rows}
    multi = {name: [p["fund_manager"] for p in placements]
             for name, placements in by_institution.items() if len(placements) > 1}
    # A fund manager naming more than one of the 23 is the reason this layer
    # would collapse the component count if it were admitted as ordinary edges.
    reach = defaultdict(set)
    for r in rows:
        reach[r[0]].add(r[1])
    # What separating the layers is worth, stated as a number rather than as an
    # assurance. Five of the seven fund managers name more than one of the 23,
    # so admitting these as ordinary edges would merge components that share no
    # owner, no director and no stated relationship - only a fund manager who
    # placed client money in both.
    rp = shape(load_graph(con, "related_party"))
    combined = shape(load_graph(con, None))
    return {
        "edges": len(rows),
        "fund_managers": len(managers),
        "institutions_reached": len(by_institution),
        "if_admitted": {
            "components_related_party_only": rp["components"],
            "components_if_admitted": combined["components"],
            "largest_component_related_party_only": rp["component_sizes"][0],
            "largest_component_if_admitted": combined["component_sizes"][0],
        },
        "institutions_unflagged_by_bog": sorted(
            {r[1] for r in rows if r[2] == 0}),
        "institutions_with_more_than_one_manager": multi,
        "managers_reaching_more_than_one": {
            m: sorted(i) for m, i in sorted(reach.items()) if len(i) > 1},
        "by_institution": {k: v for k, v in sorted(by_institution.items())},
    }


def _median(values):
    if not values:
        return None
    values = sorted(values)
    mid = len(values) // 2
    if len(values) % 2:
        return values[mid]
    return (values[mid - 1] + values[mid]) / 2


def comparative(con):
    """Question 4: do the 17 differ structurally from the other 6?

    Answered on structural attributes rather than on centrality, because the
    graph's seventeen components make centrality uninformative.
    """
    rows = con.execute("""
        SELECT ia.entity_id, en.canonical_name, ia.related_party_exposure,
               ia.net_worth_ghs_m, ia.car_pct, ia.cause_count,
               COALESCE(p.edges_out, 0), COALESCE(p.value_extracting_edges, 0),
               COALESCE(p.distinct_counterparties, 0), COALESCE(p.named_edges, 0),
               COALESCE(p.unnamed_edges, 0), p.extracted_ghs_m
        FROM institution_attributes ia
        JOIN entities en ON en.entity_id = ia.entity_id
        LEFT JOIN v_institution_profile p ON p.entity_id = ia.entity_id
        ORDER BY ia.related_party_exposure DESC, p.value_extracting_edges DESC,
                 en.canonical_name""").fetchall()

    groups = {1: [], 0: []}
    for r in rows:
        groups[r[2]].append(r)

    def summarise(rs):
        if not rs:
            return {}
        amounts = [r[11] for r in rs if r[11] is not None]
        return {
            "institutions": len(rs),
            "with_any_edge": sum(1 for r in rs if r[6]),
            "with_value_extracting_edge": sum(1 for r in rs if r[7]),
            "total_value_extracting_edges": sum(r[7] for r in rs),
            "with_a_named_counterparty": sum(1 for r in rs if r[9]),
            # Indexing the filtered list by len(rs) would read past its end the
            # moment any cause_count were missing, and it takes the upper of the
            # two middle values on an even count rather than the median.
            "median_cause_count": _median([r[5] for r in rs if r[5] is not None]),
            "quantified_ghs_m": round(sum(amounts), 2) if amounts else None,
            "institutions_with_an_amount": len(amounts),
        }

    return {
        "flagged_related_party": summarise(groups[1]),
        "not_flagged": summarise(groups[0]),
        "rows": [{"name": r[1], "flagged": bool(r[2]), "net_worth_ghs_m": r[3],
                  "car_pct": r[4], "cause_count": r[5], "edges_out": r[6],
                  "value_extracting": r[7], "counterparties": r[8],
                  "named": r[9], "unnamed": r[10], "extracted_ghs_m": r[11]}
                 for r in rows],
    }


def verification_state(con):
    seen = dict(con.execute(
        "SELECT COALESCE(v.decision,'pending'), COUNT(*) FROM edges e "
        "LEFT JOIN verification v ON v.edge_id = e.edge_id "
        "WHERE e.version_removed IS NULL OR e.version_removed = '' GROUP BY 1"))
    version = con.execute(
        "SELECT version FROM changelog "
        "ORDER BY change_date DESC, CAST(SUBSTR(change_id, 2) AS INTEGER) DESC LIMIT 1"
    ).fetchone()
    return {"counts": seen, "version": version[0] if version else "unversioned"}
