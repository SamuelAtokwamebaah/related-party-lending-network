"""
Rebuild everything from the source documents in one command.

    python run_all.py

Each step is reproducible from what is committed: the extract from the notice,
the CSV seed from the extract, and the database from the CSVs. The database is a
build artefact and is not committed - if a figure is wrong, a CSV row is wrong.

Stops at the first failing step. The loader failing is not a crash; it means a
validation rule caught something, and it will name the row and the reason.
"""

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent

STEPS = [
    ("Extract related-party evidence from the notice",
     [sys.executable, "scripts/phase0_extract_evidence.py"]),
    ("Seed the CSV evidence base from the Phase 0 candidates",
     [sys.executable, "scripts/phase1_seed_from_phase0.py"]),
    ("Validate and build the graph database",
     [sys.executable, "scripts/load.py"]),
    ("Rebuild the verification pack",
     [sys.executable, "scripts/build_review_pack.py"]),
    ("Rebuild the SEC verification pack",
     [sys.executable, "scripts/build_sec_review.py"]),
    ("Build the graph and run the Phase 2 analyses",
     [sys.executable, "scripts/phase2_report.py"]),
    ("Render the network map",
     [sys.executable, "scripts/build_site.py"]),
]


def main():
    for number, (title, command) in enumerate(STEPS, start=1):
        print(f"\n{'=' * 72}\n[{number}/{len(STEPS)}] {title}\n{'=' * 72}", flush=True)
        result = subprocess.run(command, cwd=ROOT)
        if result.returncode != 0:
            print(f"\nStopped at step {number}: {title}")
            sys.exit(result.returncode)
    print(f"\n{'=' * 72}\nDone. Database at db/graph.db\n{'=' * 72}")


if __name__ == "__main__":
    main()
