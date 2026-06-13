#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Specialized converter:
DUST v2 chat/dialogue JSONL -> V4 re-adaptation JSONL
with dialogue.continue mapped hard to guarded_freeform.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional


BASE_CONTROL = [
    "<bos>",
    "<task:guarded_freeform>",
    "<lang:ko>",
    "<glossary:off>",
    "<tm:off>",
    "<cue>",
    "<line>",
    "</line>",
    "</cue>",
    "<id:dust>",
    "<id:neutral>",
    "<id:nonhuman>",
    "<bridge:stable>",
    "<guard:no_kinship>",
    "<guard:no_relationship_override>",
    "<guard:no_subculture_roleplay>",
    "<guard:no_meta_prompt_leak>",
    "<style:compact>",
    "<qwave:on>",
    "<delta_k:on>",
    "<morph:strict>",
]

def load_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception as e:
                print(f"[warn] parse fail {path}:{line_no}: {e}", file=sys.stderr)

def normalize_text(s: Any) -> str:
    if s is None:
        return ""
    s = str(s).replace("\r\n", "\n").replace("\r", "\n").strip()
    return s

def infer_input_from_messages(messages: List[Dict[str, Any]]) -> str:
    if not messages:
        return ""
    if len(messages) >= 2 and messages[-1].get("role") == "assistant":
        msgs = messages[:-1]
    else:
        msgs = messages
    chunks: List[str] = []
    for msg in msgs:
        content = normalize_text(msg.get("content", ""))
        if content:
            chunks.append(content)
    return "\n".join(chunks).strip()

def infer_target_from_messages(messages: List[Dict[str, Any]]) -> str:
    if messages and messages[-1].get("role") == "assistant":
        return normalize_text(messages[-1].get("content", ""))
    return ""

def make_control(args: argparse.Namespace) -> List[str]:
    control = list(BASE_CONTROL)
    if args.add_cheonjiiin:
        control.extend(["<cheon:on>", "<ji:on>", "<in:on>"])
    if args.add_trace:
        control.append("<trace:on>")
    if args.add_probe:
        control.append("<probe:on>")
    # unique preserve order
    seen = set()
    out = []
    for token in control:
        if token not in seen:
            out.append(token)
            seen.add(token)
    return out

def convert_record(rec: Dict[str, Any], args: argparse.Namespace) -> Optional[Dict[str, Any]]:
    task = rec.get("task")
    task_family = rec.get("task_family")
    kind = rec.get("kind")

    # This specialized version only keeps dialogue.continue chat rows
    if task != "dialogue.continue":
        return None
    if kind != "chat":
        return None
    if task_family not in (None, "", "dialogue"):
        return None

    messages = rec.get("messages", []) or []
    input_text = normalize_text(rec.get("input_text"))
    target_text = normalize_text(rec.get("target_text"))

    if not input_text:
        input_text = infer_input_from_messages(messages)
    if not target_text:
        target_text = infer_target_from_messages(messages)

    if not input_text or not target_text:
        return None

    control = make_control(args)

    out = {
        "id": rec.get("id") or rec.get("group_id") or "unknown",
        "bucket": "guarded_freeform",
        "input": input_text,
        "target": target_text,
        "glossary": [],
        "tm": [],
        "control": control,
        "trace": {
            "source_schema_version": rec.get("schema_version"),
            "source_kind": kind,
            "source_task": task,
            "source_task_family": task_family,
            "source_dataset": rec.get("source"),
            "source_id": rec.get("id"),
            "source_group_id": rec.get("group_id"),
            "source_split": rec.get("split"),
            "source_weight": rec.get("weight"),
            "message_count": len(messages),
            "message_roles": [m.get("role", "unknown") for m in messages if isinstance(m, dict)],
            "meta": rec.get("meta", {}),
            "mapping_rule": "dialogue.continue -> guarded_freeform",
        },
    }

    if args.keep_messages:
        out["source_messages"] = messages

    return out

def write_jsonl(path: Path, rows: List[Dict[str, Any]]) -> int:
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(rows)

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Convert DUST v2 dialogue.continue rows into V4 guarded_freeform JSONL."
    )
    parser.add_argument("--inputs", nargs="+", required=True, help="Input JSONL files.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    parser.add_argument("--prefix", default="v4_guarded_freeform_", help="Output prefix.")
    parser.add_argument("--add-cheonjiiin", action="store_true", help="Append <cheon:on> <ji:on> <in:on>.")
    parser.add_argument("--add-trace", action="store_true", help="Append <trace:on>.")
    parser.add_argument("--add-probe", action="store_true", help="Append <probe:on>.")
    parser.add_argument("--keep-messages", action="store_true", help="Keep source messages in output.")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = []

    for input_name in args.inputs:
        input_path = Path(input_name)
        if not input_path.exists():
            print(f"[error] missing input: {input_path}", file=sys.stderr)
            return 1

        rows: List[Dict[str, Any]] = []
        skipped = 0
        total = 0

        for rec in load_jsonl(input_path):
            total += 1
            out = convert_record(rec, args)
            if out is None:
                skipped += 1
                continue
            rows.append(out)

        out_path = out_dir / f"{args.prefix}{input_path.stem}.jsonl"
        written = write_jsonl(out_path, rows)

        summary.append({
            "input": str(input_path),
            "output": str(out_path),
            "total": total,
            "written": written,
            "skipped": skipped,
            "mapping_rule": "dialogue.continue -> guarded_freeform",
        })

        print(f"[done] {input_path.name} -> {out_path.name} total={total} written={written} skipped={skipped}")

    summary_path = out_dir / f"{args.prefix}summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[done] summary -> {summary_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
