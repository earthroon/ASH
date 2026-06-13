#!/usr/bin/env python3
"""ASH-REBASE-00 legacy artifact scanner.

This tool performs read-only discovery for legacy Decode/WCTX/LoRA-RT/R12/TCU
artifacts and writes a scan result under workspace/rebase. It does not mutate
runtime profiles, model weights, LoRA scale, guard policy, or decode policy.
"""
from __future__ import annotations

import hashlib
import json
import time
from pathlib import Path
from typing import Dict, List

PATCH_ID = "ASH-REBASE-00"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "workspace" / "rebase"

FAMILIES = [
    {
        "family": "decode",
        "source_family": "QW-38G-R6A-DECODE",
        "patterns": ["16AI-QW-38G-R6A-DECODE"],
        "status_when_found": "candidate_only",
        "status_when_missing": "missing_candidate_blocked",
        "rebind_policy": "receipt_index_only",
    },
    {
        "family": "eval",
        "source_family": "QW-38G-R6A-EVAL",
        "patterns": ["16AI-QW-38G-R6A-EVAL"],
        "status_when_found": "calibration_reference",
        "status_when_missing": "missing_reference_unresolved",
        "rebind_policy": "fixture_reference_only",
    },
    {
        "family": "wctx_mock",
        "source_family": "QW-38G-R6A-WCTX-MOCK",
        "patterns": ["16AI-QW-38G-R6A-WCTX-MOCK"],
        "status_when_found": "audit_reference",
        "status_when_missing": "missing_reference_unresolved",
        "rebind_policy": "archive_and_fixture_reference_only",
    },
    {
        "family": "lora_rt",
        "source_family": "QW-38G-R6A-LORA-RT",
        "patterns": ["lora_rt", "LORA-RT", "LORA_RT"],
        "status_when_found": "runtime_support_reference",
        "status_when_missing": "missing_do_not_patch_runtime",
        "rebind_policy": "attach_ledger_reference_only",
    },
    {
        "family": "r12",
        "source_family": "QW-38G-R6A-R12",
        "patterns": ["16AI-QW-38G-R6A-R12"],
        "status_when_found": "quarantined_low_confidence",
        "status_when_missing": "missing_quarantine_unresolved",
        "rebind_policy": "quarantine_candidate_only",
    },
    {
        "family": "tcu",
        "source_family": "TCU",
        "patterns": ["TCU-"],
        "status_when_found": "health_ledger_reference",
        "status_when_missing": "missing_defer_TCU21",
        "rebind_policy": "operator_review_candidate",
    },
]

SCAN_ROOTS = [
    "acceptance_reports",
    "patch_reports",
    "bake_artifacts",
    "workspace",
    "artifacts",
    "logs",
]


def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def iter_files() -> List[Path]:
    paths: List[Path] = []
    for root_name in SCAN_ROOTS:
        root = ROOT / root_name
        if root.exists():
            paths.extend(p for p in root.rglob("*") if p.is_file())
    return sorted(set(paths))


def match_family(paths: List[Path], patterns: List[str]) -> List[Dict[str, str]]:
    hits: List[Dict[str, str]] = []
    for p in paths:
        rel = p.relative_to(ROOT).as_posix()
        rel_lower = rel.lower()
        if any(pat.lower() in rel_lower for pat in patterns):
            hits.append({
                "path": rel,
                "sha256": sha256_file(p),
                "size_bytes": str(p.stat().st_size),
            })
    return hits


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    all_files = iter_files()
    families = []
    missing = []
    for spec in FAMILIES:
        hits = match_family(all_files, spec["patterns"])
        found = bool(hits)
        entry = {
            "family": spec["family"],
            "source_family": spec["source_family"],
            "found": found,
            "hit_count": len(hits),
            "status": spec["status_when_found"] if found else spec["status_when_missing"],
            "rebind_policy": spec["rebind_policy"],
            "default_apply": False,
            "sample_hits": hits[:25],
        }
        families.append(entry)
        if not found:
            missing.append({
                "family": spec["source_family"],
                "expected": spec["patterns"],
                "found": False,
                "action": spec["status_when_missing"],
            })

    result = {
        "patch_id": PATCH_ID,
        "base_patch": "QW-50-R0V",
        "next_patch": "QW-50-R0W",
        "scan_unix_ms": int(time.time() * 1000),
        "mutation_policy": {
            "runtime_mutation": False,
            "model_weight_mutation": False,
            "decode_policy_mutation": False,
            "guard_policy_mutation": False,
            "lora_scale_mutation": False,
            "runtime_default_apply": False,
        },
        "scan_roots": SCAN_ROOTS,
        "families": families,
        "missing_artifacts": missing,
        "strict_policy": {
            "missing_legacy_artifact_blocks_default_apply": True,
            "missing_legacy_artifact_does_not_block_R0W": True,
        },
    }
    out = OUT_DIR / "ash_rebase_00_scan_result.json"
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(out.as_posix())


if __name__ == "__main__":
    main()
