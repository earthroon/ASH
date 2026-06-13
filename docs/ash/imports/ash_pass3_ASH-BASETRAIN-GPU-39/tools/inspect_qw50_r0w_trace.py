#!/usr/bin/env python3
from __future__ import annotations
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: inspect_qw50_r0w_trace.py <trace.json>", file=sys.stderr)
        return 2
    path = Path(sys.argv[1])
    trace = json.loads(path.read_text(encoding="utf-8"))
    generation = trace.get("generation", {})
    pieces = generation.get("generatedPieces", []) or []
    ids = generation.get("generatedTokenIds", []) or []
    piece_counts = Counter(pieces)
    id_counts = Counter(ids)
    print("[repeat]")
    for piece, count in piece_counts.most_common(12):
        if count > 1:
            steps = [i for i, p in enumerate(pieces) if p == piece]
            print(f"piece={piece!r} count={count} steps={steps}")
    for token_id, count in id_counts.most_common(12):
        if count > 1:
            steps = [i for i, v in enumerate(ids) if v == token_id]
            print(f"token_id={token_id} count={count} steps={steps}")
    print("[topk reentry]")
    by_piece = defaultdict(list)
    for step in trace.get("topKCandidatesByStep", []) or []:
        step_idx = step.get("step")
        for cand in step.get("candidates", []) or []:
            by_piece[cand.get("piece", "")].append(step_idx)
    for piece, steps in sorted(by_piece.items(), key=lambda kv: len(kv[1]), reverse=True)[:20]:
        if piece and len(steps) > 1:
            print(f"piece={piece!r} topk_steps={steps}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
