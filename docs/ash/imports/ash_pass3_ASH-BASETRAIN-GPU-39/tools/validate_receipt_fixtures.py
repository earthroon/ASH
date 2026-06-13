#!/usr/bin/env python3
"""CLOSURE-04 static JSON/receipt validation runner.
Performs no cargo build, model forward, sampling, or subtitle export.
"""
from __future__ import annotations
import argparse, json, hashlib
from pathlib import Path

DOMAIN_DEFAULT = "en_to_ko_translation_subtitle_machine"


def sha256_text(text: str) -> str:
    return "sha256:" + hashlib.sha256(text.encode("utf-8")).hexdigest()


def iter_all_json(root: Path):
    for p in sorted(root.rglob("*.json")):
        rel = p.relative_to(root).as_posix()
        if rel.startswith("workspace/closure_04_repair_backup/"):
            continue
        yield p


def iter_receipt_json(root: Path):
    for p in sorted(root.rglob("*_receipt.json")):
        rel = p.relative_to(root).as_posix()
        if rel.startswith("workspace/closure_04_repair_backup/"):
            continue
        yield p


def walk_receipts(obj, path):
    if isinstance(obj, dict):
        if isinstance(obj.get("deterministic_receipt_key"), str) and obj.get("patch_id") and obj.get("domain_ssot"):
            yield path, obj
            return
        for k, v in obj.items():
            yield from walk_receipts(v, f"{path}/{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            yield from walk_receipts(v, f"{path}[{i}]")


def valid_key(key):
    return isinstance(key, str) and ((key.startswith("q4sha256:") and len(key) == 73) or key.startswith("sha256:") or key.startswith("wctx"))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--require-domain-ssot", default=DOMAIN_DEFAULT)
    ap.add_argument("--out", default="workspace/closure_04_ad_hoc_static_validation.json")
    args = ap.parse_args()
    root = Path(args.root).resolve()
    parse_failures = []
    seen = {}
    receipt_entries = []
    duplicates = []
    domain_mismatches = []

    for p in iter_all_json(root):
        rel = p.relative_to(root).as_posix()
        try:
            json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            parse_failures.append({"fixture_path": rel, "error": str(e)})

    for p in iter_receipt_json(root):
        rel = p.relative_to(root).as_posix()
        try:
            obj = json.loads(p.read_text(encoding="utf-8"))
        except Exception:
            continue
        for receipt_path, receipt in walk_receipts(obj, rel):
            key = receipt.get("deterministic_receipt_key")
            duplicate_of = seen.get(key) if key else None
            if key and duplicate_of:
                duplicates.append({"receipt_path": receipt_path, "duplicate_of_receipt_path": duplicate_of, "deterministic_receipt_key": key})
            elif key:
                seen[key] = receipt_path
            if receipt.get("domain_ssot") != args.require_domain_ssot:
                domain_mismatches.append({"receipt_path": receipt_path, "domain_ssot": receipt.get("domain_ssot")})
            receipt_entries.append({
                "receipt_path": receipt_path,
                "patch_id": receipt.get("patch_id"),
                "domain_ssot": receipt.get("domain_ssot"),
                "deterministic_receipt_key": key,
                "key_present": bool(key),
                "key_format_valid": valid_key(key),
                "duplicate_key_detected": bool(duplicate_of),
                "duplicate_of_receipt_path": duplicate_of,
            })

    report = {
        "json_parse_failure_count": len(parse_failures),
        "json_parse_failures": parse_failures,
        "receipt_scan_scope": "*_receipt.json only; reports/key_material/validation indices are evidence copies, not canonical active registry",
        "receipt_key_checked_count": len(receipt_entries),
        "duplicate_receipt_key_count": len(duplicates),
        "duplicates": duplicates,
        "domain_ssot_mismatch_count": len(domain_mismatches),
        "domain_mismatches": domain_mismatches,
        "static_integrity_status": "PASS" if not parse_failures and not duplicates and not domain_mismatches else "FAIL",
        "runtime_decode_executed": False,
        "model_forward_executed": False,
        "sampling_executed": False,
        "subtitle_export_executed": False,
    }
    report["report_sha256"] = sha256_text(json.dumps(report, ensure_ascii=False, sort_keys=True))
    out = root / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["static_integrity_status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
