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
total = 14
completed = 14
passed = 14
failed = 0
max_abs_delta_global = 0.0000000260770320892334
mean_abs_delta_avg = 0.0000000024972721668348186
elapsed_ms_total = 55588.9549
```

## Layer Matrix

| layer | shape_match | max_abs_delta | mean_abs_delta | nan | inf | top_index_match | top_k_overlap | top_k_ratio | parity_pass | elapsed_ms |
|---:|---|---:|---:|---:|---:|---|---:|---|---|---:|
| 0 | true | 0.0000000260770320892334 | 0.0000000020633399433478417 | 0 | 0 | true | 8 | 8/8 | true | 993.127 |
| 1 | true | 0.000000015832483768463135 | 0.0000000021861623622498882 | 0 | 0 | true | 8 | 8/8 | true | 651.833 |
| 2 | true | 0.000000016298145055770874 | 0.0000000023017856509710555 | 0 | 0 | true | 8 | 8/8 | true | 652.650 |
| 3 | true | 0.000000014435499906539917 | 0.0000000024335966575250723 | 0 | 0 | true | 8 | 8/8 | true | 661.123 |
| 4 | true | 0.000000016763806343078613 | 0.0000000024028665723818676 | 0 | 0 | true | 8 | 8/8 | true | 650.989 |
| 5 | true | 0.00000001955777406692505 | 0.000000002555091471734272 | 0 | 0 | true | 8 | 8/8 | true | 674.406 |
| 6 | true | 0.000000013504177331924438 | 0.000000002562797973837405 | 0 | 0 | true | 8 | 8/8 | true | 647.092 |
| 7 | true | 0.000000013969838619232178 | 0.0000000024793176400805805 | 0 | 0 | true | 8 | 8/8 | true | 635.212 |
| 8 | true | 0.000000016763806343078613 | 0.0000000025876705223026875 | 0 | 0 | true | 8 | 8/8 | true | 623.961 |
| 9 | true | 0.0000000130385160446167 | 0.0000000025239761392015225 | 0 | 0 | true | 8 | 8/8 | true | 637.720 |
| 10 | true | 0.000000021420419216156006 | 0.000000002676262766954096 | 0 | 0 | true | 8 | 8/8 | true | 643.453 |
| 11 | true | 0.000000015832483768463135 | 0.0000000027698761062566746 | 0 | 0 | true | 8 | 8/8 | true | 639.622 |
| 12 | true | 0.000000014901161193847656 | 0.000000002691240785779314 | 0 | 0 | true | 8 | 8/8 | true | 656.237 |
| 13 | true | 0.000000014901161193847656 | 0.000000002727825965109787 | 0 | 0 | true | 8 | 8/8 | true | 650.747 |

## Seal

```txt
if parity_pass == true:
    16AF-M selected layer parity matrix closed
else:
    keep generation integration locked
```
