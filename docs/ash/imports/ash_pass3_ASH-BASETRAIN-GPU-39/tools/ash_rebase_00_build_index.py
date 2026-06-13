#!/usr/bin/env python3
"""Build ASH-REBASE-00 manifest, legacy index, policy candidates, receipt, and report."""
from __future__ import annotations

import json
import time
from pathlib import Path
from typing import Any, Dict, List

PATCH_ID = "ASH-REBASE-00"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "workspace" / "rebase"
SCAN_PATH = OUT_DIR / "ash_rebase_00_scan_result.json"

LEGACY_FAMILY_META = {
    "decode": {
        "legacy_patch_prefix": "16AI-QW-38G-R6A-DECODE",
        "status": "candidate_only",
        "rebind_policy": "receipt_index_only",
        "notes": ["transition guard / min-p / dynamic overlay remain disabled until R0W token/top-k trace exists"],
    },
    "eval": {
        "legacy_patch_prefix": "16AI-QW-38G-R6A-EVAL",
        "status": "calibration_reference",
        "rebind_policy": "fixture_reference_only",
        "notes": ["candidate calibration and long horizon eval are replay inputs only"],
    },
    "wctx_mock": {
        "legacy_patch_prefix": "16AI-QW-38G-R6A-WCTX-MOCK",
        "status": "audit_reference",
        "rebind_policy": "archive_and_fixture_reference_only",
        "notes": ["mock audit packets are reference artifacts, not active inference context sources"],
    },
    "lora_rt": {
        "legacy_patch_prefix": "16AI-QW-38G-R6A-LORA-RT",
        "status": "runtime_support_reference",
        "rebind_policy": "attach_ledger_reference_only",
        "notes": ["runtime attach lessons are ledger candidates only; do not alter current LoRA scale or attachment"],
    },
    "r12": {
        "legacy_patch_prefix": "16AI-QW-38G-R6A-R12",
        "status": "quarantined_low_confidence",
        "rebind_policy": "quarantine_candidate_only",
        "notes": ["R12 head-direction candidates remain reversible runtime-only / no-model-write / default-off"],
    },
    "tcu": {
        "legacy_patch_prefix": "TCU",
        "status": "health_ledger_reference",
        "rebind_policy": "operator_review_candidate",
        "notes": ["TCU health recommendations require operator approval before policy update"],
    },
}


def load_scan() -> Dict[str, Any]:
    if not SCAN_PATH.exists():
        raise SystemExit(f"missing scan result: {SCAN_PATH}. Run tools/ash_rebase_00_scan.py first.")
    return json.loads(SCAN_PATH.read_text(encoding="utf-8"))


def write_json(name: str, data: Dict[str, Any]) -> None:
    (OUT_DIR / name).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def build_manifest() -> Dict[str, Any]:
    return {
        "patch_id": PATCH_ID,
        "title": "Legacy Decode / WCTX / LoRA / TCU Receipt Rebind Seal",
        "base_patch": "QW-50-R0V",
        "next_patch": "QW-50-R0W",
        "mutation_policy": {
            "model_weights": "no_write",
            "runtime_mutation": False,
            "lora_scale": "no_change",
            "decode_policy": "no_change",
            "guard_policy": "no_change",
            "runtime_default_apply": False,
        },
        "legacy_families": [
            "QW-38G-R6A-DECODE",
            "QW-38G-R6A-EVAL",
            "QW-38G-R6A-WCTX-MOCK",
            "QW-38G-R6A-LORA-RT",
            "QW-38G-R6A-R12",
            "TCU",
        ],
        "outputs": {
            "scan_result": "workspace/rebase/ash_rebase_00_scan_result.json",
            "legacy_index": "workspace/rebase/ash_rebase_00_legacy_index.json",
            "policy_candidates": "workspace/rebase/ash_rebase_00_policy_candidates.json",
            "missing_artifacts": "workspace/rebase/ash_rebase_00_missing_artifacts.json",
            "receipt": "workspace/rebase/ash_rebase_00_receipt.json",
            "report": "workspace/rebase/ash_rebase_00_rebind_report.md",
        },
        "blocked_actions": [
            "enable_legacy_decode_guard_by_default",
            "apply_r12_head_direction",
            "change_lora_scale",
            "change_guard_threshold",
            "ban_attractor_tokens",
            "enable_qwave_cheonjiin_detector",
            "enable_webgpu_inference_policy",
        ],
    }


def build_legacy_index(scan: Dict[str, Any]) -> Dict[str, Any]:
    entries = []
    for fam in scan["families"]:
        meta = LEGACY_FAMILY_META.get(fam["family"], {})
        status = meta.get("status", fam["status"])
        if not fam["found"]:
            status = fam["status"]
        entry = {
            "family": fam["family"],
            "source_family": fam["source_family"],
            "legacy_patch_prefix": meta.get("legacy_patch_prefix", fam["source_family"]),
            "found": fam["found"],
            "hit_count": fam["hit_count"],
            "status": status,
            "current_binding": "QW-50",
            "default_apply": False,
            "runtime_default_apply": False,
            "rebind_policy": meta.get("rebind_policy", fam["rebind_policy"]),
            "sample_hits": fam["sample_hits"],
            "notes": meta.get("notes", []),
        }
        if fam["family"] == "r12":
            entry["safety"] = {
                "runtime_only": True,
                "reversible": True,
                "no_model_write": True,
                "production_safe_confirmed": False,
                "root_cause_confirmed": False,
            }
        entries.append(entry)
    return {
        "patch_id": PATCH_ID,
        "base_patch": "QW-50-R0V",
        "legacy_entries": entries,
    }


def build_policy_candidates() -> Dict[str, Any]:
    return {
        "patch_id": PATCH_ID,
        "candidates": [
            {
                "candidate_id": "LEGACY_DECODE_TRANSITION_GUARD",
                "source_family": "QW-38G-R6A-DECODE",
                "target_future_patch": "QW-50-R0X",
                "status": "candidate",
                "default_apply": False,
                "requires": [
                    "QW-50-R0W generatedTokenIds",
                    "QW-50-R0W topKCandidatesByStep",
                    "QW-50-R0W repeatLoopReason",
                ],
                "forbidden_before_requirements": [
                    "runtime_default_enable",
                    "hard_token_ban",
                    "lora_scale_change",
                    "guard_threshold_change",
                ],
            },
            {
                "candidate_id": "LEGACY_CANDIDATE_CALIBRATION_REPLAY",
                "source_family": "QW-38G-R6A-EVAL",
                "target_future_patch": "QW-53B",
                "status": "candidate",
                "default_apply": False,
                "requires": [
                    "R0W trace fixture",
                    "controlled rerank candidate output",
                ],
            },
            {
                "candidate_id": "LEGACY_WCTX_AUDIT_PACKET_REFERENCE",
                "source_family": "QW-38G-R6A-WCTX-MOCK",
                "target_future_patch": "ASH-PRO-20",
                "status": "reference_only",
                "default_apply": False,
            },
            {
                "candidate_id": "LEGACY_LORA_RT_ATTACH_LEDGER",
                "source_family": "QW-38G-R6A-LORA-RT",
                "target_future_patch": "QW-50-R0Y",
                "status": "candidate",
                "default_apply": False,
                "runtime_mutation": False,
            },
            {
                "candidate_id": "LEGACY_R12_HEAD_DIRECTION_ORTHOGONAL",
                "source_family": "QW-38G-R6A-R12",
                "target_future_patch": "none",
                "status": "quarantined_low_confidence",
                "default_apply": False,
                "runtime_default_apply": False,
                "production_safe_confirmed": False,
                "root_cause_confirmed": False,
                "no_model_write": True,
            },
            {
                "candidate_id": "TCU_HEALTH_RECOMMENDATION_GATE",
                "source_family": "TCU",
                "target_future_patch": "TCU-21",
                "status": "candidate",
                "default_apply": False,
                "requires_operator_approval": True,
            },
        ],
    }


def build_missing(scan: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "patch_id": PATCH_ID,
        "missing_artifacts": scan["missing_artifacts"],
        "strict_policy": {
            "missing_legacy_artifact_blocks_default_apply": True,
            "missing_legacy_artifact_does_not_block_R0W": True,
            "missing_legacy_artifact_must_not_be_silently_recreated": True,
        },
    }


def build_receipt(scan: Dict[str, Any], legacy_index: Dict[str, Any]) -> Dict[str, Any]:
    legacy_rebind = {}
    for entry in legacy_index["legacy_entries"]:
        legacy_rebind[entry["family"]] = {
            "found": entry["found"],
            "hit_count": entry["hit_count"],
            "status": entry["status"],
            "default_apply": False,
            "runtime_default_apply": False,
        }
    return {
        "patch_id": PATCH_ID,
        "base_patch": "QW-50-R0V",
        "status": "PASS",
        "created_unix_ms": int(time.time() * 1000),
        "runtime_mutation": False,
        "model_weight_mutation": False,
        "decode_policy_mutation": False,
        "guard_policy_mutation": False,
        "lora_scale_mutation": False,
        "runtime_default_apply": False,
        "legacy_rebind": legacy_rebind,
        "missing_legacy_artifacts": scan["missing_artifacts"],
        "next_allowed_patch": "QW-50-R0W",
        "blocked_actions": [
            "enable_legacy_decode_guard_by_default",
            "apply_r12_head_direction",
            "change_lora_scale",
            "change_guard_threshold",
            "ban_attractor_tokens",
            "enable_webgpu_inference_policy",
            "enable_qwave_cheonjiin_detector",
        ],
    }


def build_report(scan: Dict[str, Any], legacy_index: Dict[str, Any], receipt: Dict[str, Any]) -> str:
    rows = []
    for entry in legacy_index["legacy_entries"]:
        rows.append(
            f"| {entry['family']} | {entry['source_family']} | {entry['found']} | {entry['hit_count']} | {entry['status']} | false | {entry['rebind_policy']} |"
        )
    return "\n".join([
        "# ASH-REBASE-00 Rebind Report",
        "",
        "## Base",
        "- Current base: QW-50-R0V",
        "- Next patch: QW-50-R0W",
        "",
        "## Purpose",
        "Legacy Decode / EVAL / WCTX-MOCK / LoRA-RT / R12 / TCU chains were rebound as references, candidates, or quarantined records only.",
        "No runtime inference path, model weights, decode policy, guard policy, or LoRA scale was changed.",
        "",
        "## Mutation Policy",
        "- Model weights: no write",
        "- Runtime mutation: false",
        "- Decode policy: no change",
        "- Guard policy: no change",
        "- LoRA scale: no change",
        "- Runtime default apply: false",
        "",
        "## Rebound Families",
        "| Family | Source | Found | Hits | Status | Default Apply | Rebind Policy |",
        "|---|---|---:|---:|---|---:|---|",
        *rows,
        "",
        "## Blocked Actions",
        *[f"- {x}" for x in receipt["blocked_actions"]],
        "",
        "## Next",
        "Proceed to QW-50-R0W.",
        "Do not enable legacy policies before generated token/top-k trace exists.",
        "",
    ])


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    scan = load_scan()
    manifest = build_manifest()
    legacy_index = build_legacy_index(scan)
    policy_candidates = build_policy_candidates()
    missing = build_missing(scan)
    receipt = build_receipt(scan, legacy_index)
    report = build_report(scan, legacy_index, receipt)

    write_json("ash_rebase_00_manifest.json", manifest)
    write_json("ash_rebase_00_legacy_index.json", legacy_index)
    write_json("ash_rebase_00_policy_candidates.json", policy_candidates)
    write_json("ash_rebase_00_missing_artifacts.json", missing)
    write_json("ash_rebase_00_receipt.json", receipt)
    (OUT_DIR / "ash_rebase_00_rebind_report.md").write_text(report, encoding="utf-8")
    print((OUT_DIR / "ash_rebase_00_receipt.json").as_posix())


if __name__ == "__main__":
    main()
