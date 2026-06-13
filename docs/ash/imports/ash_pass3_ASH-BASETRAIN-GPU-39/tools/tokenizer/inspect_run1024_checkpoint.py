#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Inspect a safetensors checkpoint and infer architecture hints that matter for model_spec alignment.
This is the "don't guess twice" script for run1024.
"""

from __future__ import annotations
import argparse
import json
from collections import defaultdict

from safetensors import safe_open

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--checkpoint", required=True)
    args = ap.parse_args()

    with safe_open(args.checkpoint, framework="np") as f:
        keys = list(f.keys())
        shapes = {k: f.get_tensor(k).shape for k in keys}

    result = {
        "checkpoint": args.checkpoint,
        "embedding_key": None,
        "lm_head_key": None,
        "hidden_size": None,
        "vocab_size": None,
        "num_layers_inferred": None,
        "q_proj_shapes": [],
        "k_proj_shapes": [],
        "v_proj_shapes": [],
        "o_proj_shapes": [],
        "gate_proj_shapes": [],
        "up_proj_shapes": [],
        "down_proj_shapes": [],
    }

    for key in ("model.embed_tokens.weight", "embed_tokens.weight", "tok_embeddings.weight"):
        if key in shapes:
            result["embedding_key"] = key
            result["vocab_size"] = shapes[key][0]
            result["hidden_size"] = shapes[key][1]
            break

    for key in ("lm_head.weight", "output.weight"):
        if key in shapes:
            result["lm_head_key"] = key
            break

    layer_ids = set()
    for key in keys:
        if ".layers." in key:
            parts = key.split(".layers.", 1)[1].split(".", 1)
            if parts and parts[0].isdigit():
                layer_ids.add(int(parts[0]))
        elif key.startswith("layers."):
            parts = key.split(".", 2)
            if len(parts) > 1 and parts[1].isdigit():
                layer_ids.add(int(parts[1]))

        for tag, bucket in [
            ("q_proj.weight", "q_proj_shapes"),
            ("k_proj.weight", "k_proj_shapes"),
            ("v_proj.weight", "v_proj_shapes"),
            ("o_proj.weight", "o_proj_shapes"),
            ("gate_proj.weight", "gate_proj_shapes"),
            ("up_proj.weight", "up_proj_shapes"),
            ("down_proj.weight", "down_proj_shapes"),
        ]:
            if key.endswith(tag):
                result[bucket].append({"key": key, "shape": list(shapes[key])})

    if layer_ids:
        result["num_layers_inferred"] = max(layer_ids) + 1

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
