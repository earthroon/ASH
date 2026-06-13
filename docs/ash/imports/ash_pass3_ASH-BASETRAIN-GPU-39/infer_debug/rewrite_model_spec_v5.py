from pathlib import Path
import re

src = Path(r".\specs\model_spec_tinyllama_1p1b_v4.toml")
dst = Path(r".\specs\model_spec_v5_48259.toml")

text = src.read_text(encoding="utf-8-sig")
text = re.sub(r"(?m)^\s*vocab_size\s*=\s*\d+", "vocab_size = 48259", text)

dst.write_text(text, encoding="utf-8")
print("[OK] wrote", dst)
