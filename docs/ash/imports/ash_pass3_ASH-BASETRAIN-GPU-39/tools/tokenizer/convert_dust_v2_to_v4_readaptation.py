#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Convert DUST v2 chat/dialogue JSONL into the V4 re-adaptation JSONL shape.

Input record (observed):
{
  "schema_version": "dust.v2",
  "kind": "chat",
  "task": "dialogue.continue",
  "task_family": "dialogue",
  "source": "...",
  "id": "...",
  "group_id": "...",
  "weight": 0.2,
  "messages": [...],
  "input_text": "...",
  "target_text": "...",
  "meta": {...},
  "split": "train|valid"
}

Output record:
{
  "id": "...",
  "bucket": "...",
  "input": "...",
  "target": "...",
  "glossary": [],
  "tm": [],
  "control": [...],
  "trace": {...}
}
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, Iterator, List, Optional

# ---------------------------------------------------------------------
# Matching rules (edit here first if you want different defaults)
# ---------------------------------------------------------------------

DEFAULT_RULES = {
    # exact task mapping
    "dialogue.continue": {
        "bucket": "dialogue_continue",
        "task_token": "<task:guarded_freeform>",   # change to <task:freeform> if you want it looser
        "style_token": "<style:compact>",
        "bridge_token": "<bridge:stable>",
        "extra_control": [
            "<id:dust>",
            "<id:neutral>",
            "<id:nonhuman>",
            "<guard:no_kinship>",
            "<guard:no_relationship_override>",
            "<guard:no_subculture_roleplay>",
            "<guard:no_meta_prompt_leak>",
            "<qwave:on>",
            "<delta_k:on>",
            "<morph:strict>",
        ],
    },
}

DEFAULT_FAMILY_RULES = {
    "dialogue": {
        "bucket": "dialogue_continue",
        "task_token": "<task:guarded_freeform>",
        "style_token": "<style:compact>",
        "bridge_token": "<bridge:stable>",
        "extra_control": [
            "<id:dust>",
            "<id:neutral>",
            "<id:nonhuman>",
            "<guard:no_kinship>",
            "<guard:no_relationship_override>",
            "<guard:no_subculture_roleplay>",
            "<guard:no_meta_prompt_leak>",
            "<qwave:on>",
            "<delta_k:on>",
        ],
    }
}

BASE_CONTROL = [
    "<bos>",
    "<lang:ko>",
    "<glossary:off>",
    "<tm:off>",
    "<cue>",
    "<line>",
    "</line>",
    "</cue>",
]

# ---------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------

def load_jsonl(path: Path) -> Iterator[Dict[str, Any]]:
    with path.open("r", encoding="utf-8-sig") as f:
        for line_no, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                yield json.loads(line)
            except Exception as e:
                print(
                    f"[warn] failed to parse line {line_no} in {path}: {e}",
                    file=sys.stderr,
                )

def normalize_space(s: str) -> str:
    if s is None:
        return ""
    s = s.replace("\r\n", "\n").replace("\r", "\n")
    return s.strip()

def infer_input_from_messages(messages: List[Dict[str, Any]]) -> str:
    if not messages:
        return ""
    # Prefer everything except final assistant if possible.
    if len(messages) >= 2 and messages[-1].get("role") == "assistant":
        chunks = []
        for msg in messages[:-1]:
            role = msg.get("role", "unknown")
            content = normalize_space(str(msg.get("content", "")))
            if content:
                chunks.append(content)
        return "\n".join(chunks).strip()

    # fallback: join all
    chunks = []
    for msg in messages:
        content = normalize_space(str(msg.get("content", "")))
        if content:
            chunks.append(content)
    return "\n".join(chunks).strip()

def infer_target_from_messages(messages: List[Dict[str, Any]]) -> str:
    if not messages:
        return ""
    if messages[-1].get("role") == "assistant":
        return normalize_space(str(messages[-1].get("content", "")))
    return ""

def pick_rules(task: str, task_family: str) -> Dict[str, Any]:
    if task in DEFAULT_RULES:
        return DEFAULT_RULES[task]
    if task_family in DEFAULT_FAMILY_RULES:
        return DEFAULT_FAMILY_RULES[task_family]
    return {
        "bucket": "freeform",
        "task_token": "<task:freeform>",
        "style_token": "<style:compact>",
        "bridge_token": "<bridge:stable>",
        "extra_control": [
            "<id:dust>",
            "<id:neutral>",
            "<qwave:on>",
            "<delta_k:on>",
        ],
    }

def build_control(rec: Dict[str, Any], rules: Dict[str, Any], opts: argparse.Namespace) -> List[str]:
    control = list(BASE_CONTROL)

    # task token should come early, right after bos if possible
    control.insert(1, rules["task_token"])

    extra = [
        rules["bridge_token"],
        rules["style_token"],
        *rules.get("extra_control", []),
    ]

    # Optional additions
    if opts.add_cheonjiiin:
        extra.extend(["<cheon:on>", "<ji:on>", "<in:on>"])
    if opts.add_trace:
        extra.append("<trace:on>")
    if opts.add_probe:
        extra.append("<probe:on>")

    # keep unique, preserve order
    seen = set()
    out = []
    for token in control + extra:
        if token not in seen:
            out.append(token)
            seen.add(token)
    return out

def make_trace(rec: Dict[str, Any], bucket: str, control: List[str]) -> Dict[str, Any]:
    messages = rec.get("messages", []) or []
    roles = [m.get("role", "unknown") for m in messages if isinstance(m, dict)]
    return {
        "source_schema_version": rec.get("schema_version"),
        "source_kind": rec.get("kind"),
        "source_task": rec.get("task"),
        "source_task_family": rec.get("task_family"),
        "source_dataset": rec.get("source"),
        "source_id": rec.get("id"),
        "source_group_id": rec.get("group_id"),
        "source_split": rec.get("split"),
        "source_weight": rec.get("weight"),
        "bucket": bucket,
        "message_count": len(messages),
        "message_roles": roles,
        "has_input_text": bool(rec.get("input_text")),
        "has_target_text": bool(rec.get("target_text")),
        "meta": rec.get("meta", {}),
        "control_len": len(control),
    }

def convert_record(rec: Dict[str, Any], opts: argparse.Namespace) -> Optional[Dict[str, Any]]:
    task = str(rec.get("task", "") or "")
    task_family = str(rec.get("task_family", "") or "")
    rules = pick_rules(task, task_family)

    messages = rec.get("messages", []) or []

    input_text = normalize_space(rec.get("input_text") or "")
    target_text = normalize_space(rec.get("target_text") or "")

    if not input_text:
        input_text = infer_input_from_messages(messages)
    if not target_text:
        target_text = infer_target_from_messages(messages)

    if not input_text or not target_text:
        return None

    bucket = rules["bucket"]
    control = build_control(rec, rules, opts)
    trace = make_trace(rec, bucket, control)

    out = {
        "id": rec.get("id") or rec.get("group_id") or "unknown",
        "bucket": bucket,
        "input": input_text,
        "target": target_text,
        "glossary": [],
        "tm": [],
        "control": control,
        "trace": trace,
    }

    if opts.keep_messages:
        out["source_messages"] = messages

    return out

def write_jsonl(path: Path, rows: Iterable[Dict[str, Any]]) -> int:
    count = 0
    with path.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count

def main() -> int:
    parser = argparse.ArgumentParser(description="Convert DUST v2 JSONL to V4 re-adaptation JSONL.")
    parser.add_argument("--inputs", nargs="+", required=True, help="Input JSONL files.")
    parser.add_argument("--output-dir", required=True, help="Output directory.")
    parser.add_argument("--add-cheonjiiin", action="store_true", help="Append <cheon:on> <ji:on> <in:on>.")
    parser.add_argument("--add-trace", action="store_true", help="Append <trace:on>.")
    parser.add_argument("--add-probe", action="store_true", help="Append <probe:on>.")
    parser.add_argument("--keep-messages", action="store_true", help="Keep original messages array in output.")
    parser.add_argument("--prefix", default="v4_readapt_", help="Output file prefix.")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    summary = []

    for input_str in args.inputs:
        input_path = Path(input_str)
        if not input_path.exists():
            print(f"[error] input not found: {input_path}", file=sys.stderr)
            return 1

        rows: List[Dict[str, Any]] = []
        skipped = 0
        for rec in load_jsonl(input_path):
            out = convert_record(rec, args)
            if out is None:
                skipped += 1
                continue
            rows.append(out)

        out_name = f"{args.prefix}{input_path.stem}.jsonl"
        out_path = out_dir / out_name
        written = write_jsonl(out_path, rows)

        summary.append({
            "input": str(input_path),
            "output": str(out_path),
            "written": written,
            "skipped": skipped,
        })

        print(f"[done] {input_path.name} -> {out_path.name}  written={written} skipped={skipped}")

    summary_path = out_dir / f"{args.prefix}summary.json"
    with summary_path.open("w", encoding="utf-8") as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)

    print(f"[done] summary -> {summary_path}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
