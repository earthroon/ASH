#!/usr/bin/env python3
import argparse
import json
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover
    import tomli as tomllib


def resolve_module_dims(spec: dict, target_key: str):
    dims = spec["dimensions"]
    hidden = max(int(dims["hidden_size"]), 1)
    inter = max(int(dims["intermediate_size"]), 1)
    kv_hidden = max(int(dims["num_key_value_heads"]), 1) * max(int(dims["head_dim"]), 1)
    suffix = target_key
    if "layers." in target_key:
        rest = target_key.split("layers.", 1)[1]
        parts = rest.split(".", 1)
        if len(parts) == 2:
            suffix = parts[1]
    mapping = {
        "attn.q_proj": (hidden, hidden),
        "attn.k_proj": (hidden, kv_hidden),
        "attn.v_proj": (hidden, kv_hidden),
        "attn.o_proj": (hidden, hidden),
        "ffn.gate_proj": (hidden, inter),
        "ffn.up_proj": (hidden, inter),
        "ffn.down_proj": (inter, hidden),
    }
    if suffix not in mapping:
        raise SystemExit(f"unsupported module target for migration: {target_key}")
    return mapping[suffix]


def iter_attachments(payload):
    if isinstance(payload, list):
        return payload
    if isinstance(payload, dict):
        return [payload]
    raise SystemExit("unsupported sidecar payload")


def main():
    ap = argparse.ArgumentParser(description="Explicitly migrate runtime LoRA sidecars to a declared artifact_family.")
    ap.add_argument("--input", required=True)
    ap.add_argument("--output", required=True)
    ap.add_argument("--family", required=True, choices=["module_lora", "shared_hidden_token_adapter"])
    ap.add_argument("--model-spec", help="required when migrating to module_lora")
    ap.add_argument("--force", action="store_true", help="allow overwriting the output file")
    args = ap.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output)
    if output_path.exists() and not args.force:
        raise SystemExit(f"output already exists: {output_path}")

    payload = json.loads(input_path.read_text(encoding="utf-8"))
    attachments = iter_attachments(payload)

    spec = None
    if args.family == "module_lora":
        if not args.model_spec:
            raise SystemExit("--model-spec is required for module_lora migration")
        spec = tomllib.loads(Path(args.model_spec).read_text(encoding="utf-8"))

    migrated = []
    for item in attachments:
        item = dict(item)
        item["artifact_family"] = args.family
        item.setdefault("source_path", str(input_path))
        target_key = item.get("target_key", "")
        in_dim = int(item.get("in_dim", 0))
        out_dim = int(item.get("out_dim", 0))
        if args.family == "module_lora":
            expected_in, expected_out = resolve_module_dims(spec, target_key)
            if (in_dim, out_dim) != (expected_in, expected_out):
                raise SystemExit(
                    f"module_lora migration refused: target_key={target_key} expected={expected_in}->{expected_out} actual={in_dim}->{out_dim} source={input_path}"
                )
        migrated.append(item)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(payload, list):
        output_path.write_text(json.dumps(migrated, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    else:
        output_path.write_text(json.dumps(migrated[0], indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print(f"[migrate] input={input_path}")
    print(f"[migrate] output={output_path}")
    print(f"[migrate] family={args.family}")
    print(f"[migrate] attachments={len(migrated)}")


if __name__ == "__main__":
    main()
