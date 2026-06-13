import json
from pathlib import Path

manifest = Path(r".\artifacts\tokenizer_manifest_v5_final.json")
ids = [30645]

d = json.loads(manifest.read_text(encoding="utf-8-sig"))

vocab = d.get("vocab") or d.get("tokens") or d.get("id_to_token")
if isinstance(vocab, dict):
    for i in ids:
        print(i, "=", vocab.get(str(i)) or vocab.get(i))
elif isinstance(vocab, list):
    for i in ids:
        print(i, "=", vocab[i] if 0 <= i < len(vocab) else None)
else:
    print("Unknown manifest vocab shape:", type(vocab))
