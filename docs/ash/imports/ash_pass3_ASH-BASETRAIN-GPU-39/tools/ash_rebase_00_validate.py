#!/usr/bin/env python3
"""Validate ASH-REBASE-00 bake outputs and safety invariants."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List

PATCH_ID = "ASH-REBASE-00"
ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "workspace" / "rebase"

REQUIRED = [
    "ash_rebase_00_scan_result.json",
    "ash_rebase_00_manifest.json",
    "ash_rebase_00_legacy_index.json",
    "ash_rebase_00_policy_candidates.json",
    "ash_rebase_00_missing_artifacts.json",
    "ash_rebase_00_receipt.json",
    "ash_rebase_00_rebind_report.md",
]


def read_json(name: str) -> Dict[str, Any]:
    return json.loads((OUT_DIR / name).read_text(encoding="utf-8"))


def fail(errors: List[str]) -> None:
    result = {
        "patch_id": PATCH_ID,
        "status": "FAIL",
        "errors": errors,
    }
    (OUT_DIR / "ash_rebase_00_validation_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    raise SystemExit("\n".join(errors))


def main() -> None:
    errors: List[str] = []
    for name in REQUIRED:
        if not (OUT_DIR / name).exists():
            errors.append(f"missing required output: {name}")
    if errors:
        fail(errors)

    manifest = read_json("ash_rebase_00_manifest.json")
    legacy_index = read_json("ash_rebase_00_legacy_index.json")
    candidates = read_json("ash_rebase_00_policy_candidates.json")
    receipt = read_json("ash_rebase_00_receipt.json")
    missing = read_json("ash_rebase_00_missing_artifacts.json")

    if manifest.get("base_patch") != "QW-50-R0V":
        errors.append("manifest base_patch must be QW-50-R0V")
    if manifest.get("next_patch") != "QW-50-R0W":
        errors.append("manifest next_patch must be QW-50-R0W")

    mutation_policy = manifest.get("mutation_policy", {})
    if mutation_policy.get("runtime_default_apply") is not False:
        errors.append("manifest runtime_default_apply must be false")
    if mutation_policy.get("model_weights") != "no_write":
        errors.append("manifest model_weights must be no_write")
    if mutation_policy.get("lora_scale") != "no_change":
        errors.append("manifest lora_scale must be no_change")
    if mutation_policy.get("decode_policy") != "no_change":
        errors.append("manifest decode_policy must be no_change")
    if mutation_policy.get("guard_policy") != "no_change":
        errors.append("manifest guard_policy must be no_change")

    for key in [
        "runtime_mutation",
        "model_weight_mutation",
        "decode_policy_mutation",
        "guard_policy_mutation",
        "lora_scale_mutation",
        "runtime_default_apply",
    ]:
        if receipt.get(key) is not False:
            errors.append(f"receipt {key} must be false")

    if receipt.get("next_allowed_patch") != "QW-50-R0W":
        errors.append("receipt next_allowed_patch must be QW-50-R0W")

    for entry in legacy_index.get("legacy_entries", []):
        if entry.get("default_apply") is not False:
            errors.append(f"legacy entry {entry.get('family')} default_apply must be false")
        if entry.get("runtime_default_apply") is not False:
            errors.append(f"legacy entry {entry.get('family')} runtime_default_apply must be false")
        if entry.get("family") == "r12":
            safety = entry.get("safety", {})
            if entry.get("status") != "quarantined_low_confidence":
                errors.append("r12 must remain quarantined_low_confidence")
            if safety.get("no_model_write") is not True:
                errors.append("r12 safety.no_model_write must be true")
            if safety.get("runtime_only") is not True:
                errors.append("r12 safety.runtime_only must be true")
            if safety.get("production_safe_confirmed") is not False:
                errors.append("r12 production_safe_confirmed must be false")

    for cand in candidates.get("candidates", []):
        if cand.get("default_apply") is not False:
            errors.append(f"candidate {cand.get('candidate_id')} default_apply must be false")
        if cand.get("candidate_id") == "LEGACY_R12_HEAD_DIRECTION_ORTHOGONAL":
            if cand.get("status") != "quarantined_low_confidence":
                errors.append("legacy R12 candidate must remain quarantined_low_confidence")
            if cand.get("no_model_write") is not True:
                errors.append("legacy R12 candidate no_model_write must be true")

    strict = missing.get("strict_policy", {})
    if strict.get("missing_legacy_artifact_blocks_default_apply") is not True:
        errors.append("missing artifacts must block default apply")
    if strict.get("missing_legacy_artifact_does_not_block_R0W") is not True:
        errors.append("missing artifacts must not block R0W")

    blocked = set(receipt.get("blocked_actions", []))
    for required_block in [
        "enable_legacy_decode_guard_by_default",
        "apply_r12_head_direction",
        "change_lora_scale",
        "change_guard_threshold",
        "ban_attractor_tokens",
    ]:
        if required_block not in blocked:
            errors.append(f"missing blocked action: {required_block}")

    result = {
        "patch_id": PATCH_ID,
        "status": "PASS" if not errors else "FAIL",
        "checked_outputs": REQUIRED,
        "safety_invariants": {
            "runtime_mutation": False,
            "model_weight_mutation": False,
            "decode_policy_mutation": False,
            "guard_policy_mutation": False,
            "lora_scale_mutation": False,
            "runtime_default_apply": False,
            "r12_quarantined_low_confidence": True,
            "next_allowed_patch": "QW-50-R0W",
        },
        "errors": errors,
    }
    (OUT_DIR / "ash_rebase_00_validation_result.json").write_text(
        json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if errors:
        fail(errors)
    print((OUT_DIR / "ash_rebase_00_validation_result.json").as_posix())


if __name__ == "__main__":
    main()
