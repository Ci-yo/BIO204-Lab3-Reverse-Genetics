"""Summarize GenBank designs and the predicted protein model."""

from __future__ import annotations

import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def genbank_summary(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="ignore")
    locus_match = re.search(r"^LOCUS\s+(\S+)\s+(\d+) bp", text, re.MULTILINE)
    labels = sorted(set(re.findall(r'/label="([^"]+)"', text)))
    return {
        "file": path.name,
        "locus": locus_match.group(1) if locus_match else "unknown",
        "sequence_length_bp": int(locus_match.group(2)) if locus_match else 0,
        "feature_labels": ";".join(labels),
    }


def pdb_summary(path: Path) -> dict[str, object]:
    atoms = 0
    residues: set[tuple[str, str]] = set()
    with path.open(encoding="utf-8", errors="ignore") as handle:
        for line in handle:
            if line.startswith(("ATOM  ", "HETATM")):
                atoms += 1
                residues.add((line[21:22], line[22:26].strip()))
    return {"file": path.name, "atom_records": atoms, "modelled_residues": len(residues)}


def main() -> None:
    results = ROOT / "results"
    results.mkdir(exist_ok=True)

    records = [
        genbank_summary(ROOT / "sequences/ANID_08533-wild-type.gbk"),
        genbank_summary(ROOT / "sequences/ANID_08533-predicted-deletion.gbk"),
    ]
    with (results / "sequence_inventory.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=records[0].keys())
        writer.writeheader()
        writer.writerows(records)

    protein = pdb_summary(ROOT / "structures/ANID_08533-model.pdb")
    with (results / "structure_inventory.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=protein.keys())
        writer.writeheader()
        writer.writerow(protein)

    print(f"Design inventory written for {len(records)} loci and {protein['modelled_residues']} modelled residues.")


if __name__ == "__main__":
    main()
