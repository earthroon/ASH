# 16AF-M Multi-Layer Native Atlas FFN Parity Matrix Seal

## Status

```txt
runtime_gate = multi_layer_ffn_parity_only
generation_connected = false
threshold = 0.0010000000474974513
top_k = 8
parity_pass = true
```

## Summary

```txt
total = 5
completed = 5
passed = 5
failed = 0
max_abs_delta_global = 0.0000000260770320892334
mean_abs_delta_avg = 0.0000000023516864011696725
elapsed_ms_total = 42343.07780000001
```

## Layer Matrix

| layer | shape_match | max_abs_delta | mean_abs_delta | nan | inf | top_index_match | top_k_overlap | top_k_ratio | parity_pass | elapsed_ms |
|---:|---|---:|---:|---:|---:|---|---:|---|---|---:|
| 0 | true | 0.0000000260770320892334 | 0.0000000020633399433478417 | 0 | 0 | true | 8 | 8/8 | true | 1024.720 |
| 1 | true | 0.000000015832483768463135 | 0.0000000021861623622498882 | 0 | 0 | true | 8 | 8/8 | true | 758.603 |
| 2 | true | 0.000000016298145055770874 | 0.0000000023017856509710555 | 0 | 0 | true | 8 | 8/8 | true | 720.362 |
| 7 | true | 0.000000013969838619232178 | 0.0000000024793176400805805 | 0 | 0 | true | 8 | 8/8 | true | 781.192 |
| 13 | true | 0.000000014901161193847656 | 0.000000002727825965109787 | 0 | 0 | true | 8 | 8/8 | true | 688.577 |

## Seal

```txt
if parity_pass == true:
    16AF-M selected layer parity matrix closed
else:
    keep generation integration locked
```
