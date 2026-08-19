"""Dependency-free repository and privacy checks."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = [
    "README.md",
    "data/gene_summary.csv",
    "data/primers.csv",
    "data/diagnostic_expectations.csv",
    "data/diagnostic_pcr_lanes.csv",
    "sequences/ANID_08533-wild-type.gbk",
    "sequences/ANID_08533-predicted-deletion.gbk",
    "structures/ANID_08533-model.pdb",
    "results/sequence_inventory.csv",
    "results/structure_inventory.csv",
    "figures/diagnostic-pcr-design.png",
    "figures/predicted-structure.jpg",
    "showcase/BIO204-Lab3-Poster.pdf",
    "showcase/BIO204-Lab3-Poster-preview.png",
]


def main() -> None:
    missing = [item for item in REQUIRED if not (ROOT / item).is_file()]
    assert not missing, f"Missing required files: {missing}"

    with (ROOT / "results/sequence_inventory.csv").open(encoding="utf-8", newline="") as handle:
        sequences = list(csv.DictReader(handle))
    assert [int(row["sequence_length_bp"]) for row in sequences] == [3610, 4202]
    assert "Af-pyrG_insertion" in sequences[1]["feature_labels"]

    with (ROOT / "results/structure_inventory.csv").open(encoding="utf-8", newline="") as handle:
        structure = next(csv.DictReader(handle))
    assert int(structure["atom_records"]) > 1000
    assert 340 <= int(structure["modelled_residues"]) <= 355

    private_extensions = {".doc", ".docx", ".xls", ".xlsx", ".pdf", ".pptx"}
    allowed_submission_artifacts = {"showcase/BIO204-Lab3-Poster.pdf"}
    forbidden = [
        path.relative_to(ROOT).as_posix()
        for path in ROOT.rglob("*")
        if path.is_file()
        and ".git" not in path.parts
        and path.relative_to(ROOT).as_posix() not in allowed_submission_artifacts
        and (path.suffix.lower() in private_extensions or "2255737" in path.name or "Xiyao Chen" in path.name)
    ]
    assert not forbidden, f"Private or submission files found: {forbidden}"

    print("Repository checks passed: design, sequences, model and privacy guard are valid.")


if __name__ == "__main__":
    main()
