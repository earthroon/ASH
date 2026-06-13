import json, struct, sys

p = sys.argv[1]
with open(p, "rb") as f:
    n = struct.unpack("<Q", f.read(8))[0]
    header = json.loads(f.read(n))

keys = [k for k in header.keys() if k != "__metadata__"]
print("tensor_count:", len(keys))
for k in keys[:300]:
    shape = header[k].get("shape")
    dtype = header[k].get("dtype")
    print(k, dtype, shape)
