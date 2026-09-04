"""
Phase 0 - source inventory.

Reads the Bank of Ghana notice of 16 August 2019 revoking the licences of the
23 savings & loans companies and finance houses, splits it into its 23
institution sections, and extracts every bullet that carries related-party
language. Each extracted bullet keeps the line number it came from, so any
node or edge built later can be traced back to a specific passage.

This script makes no judgement about what the passages mean. It only counts
what is there, so the project mode (real-entity / stylized / hybrid) can be
decided from the evidence rather than from an assumption.

Outputs
  docs/phase0/evidence-extract.md   every matched bullet, quoted, per institution
  docs/phase0/source-inventory.csv  one row per institution, counts and candidates
"""

import csv
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "data" / "raw" / "bog-2019-08-16-savings-loans-revocation.txt"
OUT_MD = ROOT / "docs" / "phase0" / "evidence-extract.md"
OUT_CSV = ROOT / "docs" / "phase0" / "source-inventory.csv"

SOURCE_ID = "bog-2019-08-16-savings-loans-revocation"

# A section header is a numbered, ALL-CAPS institution name on its own line.
HEADER = re.compile(r"^\s*(\d{1,2})\.\s+([A-Z][A-Z0-9'&().,\- ]{8,})\s*$")

# A bullet starts with a letter or number enumerator: "a. ", "3. ", "c) ".
BULLET = re.compile(r"^\s*(?:[a-z]|\d{1,2})[.)]\s+\S")

# A line holding nothing but a printed page number. There are 27 of them, one
# per page break, and they are furniture rather than text.
PAGE_NUMBER = re.compile(r"^\s*\d{1,3}\s*$")

# Signal vocabulary, grouped so the inventory can report which kind of
# relationship each passage evidences.
SIGNALS = {
    "related_party": r"related[- ]part(?:y|ies)",
    "affiliate_group": r"\baffiliate[sd]?\b|\bsister compan|\bparent compan|\bgroup compan|related compan",
    "ownership": r"\bshareholder(?:s|s')?\b|\bown(?:s|ed|er|ers|ership)\b|\bsubsidiar",
    # Ownership history: acquisitions, takeovers and renamings are how one
    # entity comes to sit behind two separately licensed institutions.
    "ownership_history": (
        r"\bacquisition\b|\bacquired\b|\btak(?:ing|en|e)s?\s+over\b|\btook over\b"
        r"|\bHoldings?\b|\bformerly\b|\bname was changed\b|\bpreviously known as\b"
        r"|\bwas known as\b|\bmerge[rd]?\b|\bconvert(?:ed|sion)\b"
    ),
    "officer_role": r"\bdirector(?:s)?\b|\bboard\b|\bchief executive\b|\bCEO\b|\bkey management\b",
    "placement_exposure": r"\bplacement|\bexposure[sd]?\b|\boverdrawn\b|\bmanagement fees\b",
}
SIGNAL_RE = {k: re.compile(v, re.I) for k, v in SIGNALS.items()}
ANY_SIGNAL = re.compile("|".join(SIGNALS.values()), re.I)

# A named counterparty candidate: a run of capitalised tokens ending in a
# corporate suffix. Deliberately loose - the output is reviewed by hand, and a
# false positive costs a moment's reading while a miss costs an edge.
CORP_SUFFIX = (
    r"(?:Limited|Ltd\.?|Company|Companies|Plc|PLC|Bank|Remittances"
    r"|Securities|Capital|Holdings|Investments|Management|Microfinance"
    r"|Services|Advisors|Partners|Fund|Trust|Enterprises?)"
)
NAMED = re.compile(
    r"\b((?:[A-Z][A-Za-z&'’.\-]*|uni[A-Z][A-Za-z]*|[a-z]+[A-Z][A-Za-z]*)"
    r"(?:\s+(?:of|and|for|the)?\s*[A-Za-z][A-Za-z&'’.\-]*){0,4}\s+"
    + CORP_SUFFIX
    + r")\b"
)

# Amounts, so the inventory can show which passages carry a quantum.
AMOUNT = re.compile(
    r"GHS\s?[\d,]+(?:\.\d+)?\s*(?:million|billion)?"
    r"|[\d,]+(?:\.\d+)?\s*(?:million|billion)",
    re.I,
)

# Governance boilerplate the loose regex picks up ("the Board and Senior
# Management", "the Bank of Ghana"). None of it is a counterparty.
REJECT = re.compile(
    r"\bBoard\b|\bBank of Ghana\b|\bthe Bank\b|\breview\b|\bDirectives\b"
    r"|\bengaged\b|\breported\b|\bfunds\b|\bSenior Management\b"
    r"|\bdirected\b|\bManagement of\b",
    re.I,
)

NOT_A_COUNTERPARTY = {
    "bank of ghana", "the bank", "the company", "the institution",
    "consolidated bank ghana limited", "consolidated bank", "the receiver",
    "this bank", "the said company",
}


def read_lines():
    text = SRC.read_text(encoding="utf-8")
    # The cedi sign survives the PDF text extraction as a replacement character.
    text = text.replace("�", "GHS ")
    text = text.replace("GHGHS ", "GHS ").replace("GHS  ", "GHS ")
    # Split on real newlines only. str.splitlines() also breaks on form feeds,
    # and this document carries 27 of them as page breaks - which would put
    # every line number up to 26 ahead of what grep, sed or a text editor
    # shows, and an anchor nobody can follow is not a citation.
    return text.replace("\r\n", "\n").replace("\r", "\n").split("\n")


def split_sections(lines):
    """Return [(number, name, start_line, end_line)] for the 23 institutions."""
    marks = []
    expected = 1
    for i, line in enumerate(lines, start=1):
        m = HEADER.match(line)
        if m and int(m.group(1)) == expected:
            marks.append((expected, m.group(2).strip().rstrip("."), i))
            expected += 1
    out = []
    for idx, (num, name, start) in enumerate(marks):
        end = marks[idx + 1][2] - 1 if idx + 1 < len(marks) else len(lines)
        out.append((num, name, start, end))
    return out


def spans_page_break(lines, i, current, end):
    """True if the blank at line i is a page break interrupting a sentence.

    The notice wraps paragraphs across pages, leaving blank / page-number /
    blank between the halves. Flushing the block there would truncate a quote
    mid-sentence, so a block continues across the break - but only when the
    text so far does not end on sentence-final punctuation, which keeps this
    from gluing genuinely separate bullets together.
    """
    if not current or current[-1].rstrip().endswith((".", ":", ";")):
        return False
    saw_page_number = False
    for j in range(i + 1, min(end, len(lines)) + 1):
        stripped = lines[j - 1].strip()
        if not stripped:
            continue
        if PAGE_NUMBER.match(stripped):
            saw_page_number = True
            continue
        if not saw_page_number:
            return False
        return not (BULLET.match(lines[j - 1]) or HEADER.match(lines[j - 1]))
    return False


def blocks(lines, start, end):
    """Group a section's wrapped lines into bullets. Yields (line_no, text)."""
    current, first_line = [], None
    for i in range(start + 1, end + 1):
        raw = lines[i - 1]
        stripped = raw.strip()
        if PAGE_NUMBER.match(stripped):
            continue  # furniture, never part of a quote
        if not stripped:
            if current and spans_page_break(lines, i, current, end):
                continue
            if current:
                yield first_line, " ".join(current)
                current, first_line = [], None
            continue
        if BULLET.match(raw) and current:
            yield first_line, " ".join(current)
            current, first_line = [], None
        if not current:
            first_line = i
        current.append(stripped)
    if current:
        yield first_line, " ".join(current)


def tidy(text):
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"^(?:[a-z]|\d{1,2})[.)]\s+", "", text)


def counterparties(text, institution):
    inst_words = {w.lower() for w in re.findall(r"[A-Za-z]+", institution)}
    generic = {"limited", "ltd", "company", "savings", "and", "loans",
               "the", "house", "finance"}
    found = []
    for cand in NAMED.findall(text):
        c = re.sub(r"\s+", " ", cand).strip(" .,")
        if c.lower() in NOT_A_COUNTERPARTY or REJECT.search(c):
            continue
        cand_words = {w.lower() for w in re.findall(r"[A-Za-z]+", c)}
        distinctive = cand_words - generic
        if not distinctive:
            continue
        # Skip anything that is only the institution's own name restated.
        if distinctive <= inst_words:
            continue
        if c not in found:
            found.append(c)
    # Drop any candidate wholly contained in a longer one.
    return [c for c in found if not any(c != o and c in o for o in found)]


def main():
    lines = read_lines()
    sections = split_sections(lines)
    assert len(sections) == 23, f"expected 23 institution sections, found {len(sections)}"

    md = [
        "# Phase 0 - related-party evidence extract",
        "",
        f"Source: `{SOURCE_ID}` (Bank of Ghana, 16 August 2019). "
        f"Working text: `data/raw/{SRC.name}`; PDF as published: `sources/{SRC.stem}.pdf`.",
        "",
        "Every bullet below is quoted verbatim from the notice and anchored to the line "
        "it begins on in the working text, in the form `L<line>`. A bullet appears here "
        "only because it matched the related-party vocabulary in "
        "`scripts/phase0_extract_evidence.py`. Inclusion is a search result, not a finding.",
        "",
        "Regenerate with `python scripts/phase0_extract_evidence.py`.",
        "",
    ]
    rows = []

    for num, name, start, end in sections:
        matched = []
        for line_no, block in blocks(lines, start, end):
            text = tidy(block)
            if len(text) < 25 or not ANY_SIGNAL.search(text):
                continue
            kinds = [k for k, rx in SIGNAL_RE.items() if rx.search(text)]
            matched.append((line_no, text, kinds))

        all_cp, all_kinds, amounts = [], set(), 0
        md.append(f"## {num}. {name}")
        md.append("")
        md.append(f"Section: L{start}-L{end}. Matched bullets: {len(matched)}.")
        md.append("")
        if not matched:
            md.append("_No bullet in this section matched the related-party vocabulary._")
            md.append("")
        for line_no, text, kinds in matched:
            cps = counterparties(text, name)
            for c in cps:
                if c not in all_cp:
                    all_cp.append(c)
            all_kinds.update(kinds)
            amounts += len(AMOUNT.findall(text))
            md.append(f"- **L{line_no}** [{', '.join(kinds)}] {text}")
            if cps:
                md.append(f"    - named entity candidates: {'; '.join(cps)}")
        md.append("")

        rows.append({
            "institution_name": name,
            "section_start_line": start,
            "section_end_line": end,
            "matched_bullets": len(matched),
            "signal_related_party": int("related_party" in all_kinds),
            "signal_affiliate_group": int("affiliate_group" in all_kinds),
            "signal_ownership": int("ownership" in all_kinds),
            "signal_ownership_history": int("ownership_history" in all_kinds),
            "signal_officer_role": int("officer_role" in all_kinds),
            "signal_placement_exposure": int("placement_exposure" in all_kinds),
            "named_counterparty_candidates": "; ".join(all_cp),
            "n_named_candidates": len(all_cp),
            "n_amounts_quoted": amounts,
            "source_id": SOURCE_ID,
        })

    OUT_MD.parent.mkdir(parents=True, exist_ok=True)
    OUT_MD.write_text("\n".join(md) + "\n", encoding="utf-8")
    with OUT_CSV.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print(f"sections parsed                    : {len(rows)}")
    print(f"with any matched bullet            : {sum(1 for r in rows if r['matched_bullets'])}")
    print(f"with related-party wording         : {sum(r['signal_related_party'] for r in rows)}")
    print(f"with a named counterparty candidate: {sum(1 for r in rows if r['n_named_candidates'])}")
    print(f"total matched bullets              : {sum(r['matched_bullets'] for r in rows)}")
    print(f"wrote {OUT_MD.relative_to(ROOT)} and {OUT_CSV.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
