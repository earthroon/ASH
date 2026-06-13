# 16AF-P Native Atlas FFN Performance Probe Seal

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
elapsed_ms_total = 50325.8817
telemetry_total_gpu_ms = 622.6086999999999
telemetry_weight_upload_ms = 213.10080000000002
telemetry_submit_readback_ms = 393.1204
telemetry_readback_buffers = 14
telemetry_readback_elements = 28672
```

## Layer Matrix

| layer | shape_match | max_abs_delta | mean_abs_delta | nan | inf | top_index_match | top_k_overlap | top_k_ratio | parity_pass | elapsed_ms |
|---:|---|---:|---:|---:|---:|---|---:|---|---|---:|
| 0 | true | 0.0000000260770320892334 | 0.0000000020633399433478417 | 0 | 0 | true | 8 | 8/8 | true | 325.092 |
| 1 | true | 0.000000015832483768463135 | 0.0000000021861623622498882 | 0 | 0 | true | 8 | 8/8 | true | 369.476 |
| 2 | true | 0.000000016298145055770874 | 0.0000000023017856509710555 | 0 | 0 | true | 8 | 8/8 | true | 284.467 |
| 3 | true | 0.000000014435499906539917 | 0.0000000024335966575250723 | 0 | 0 | true | 8 | 8/8 | true | 270.397 |
| 4 | true | 0.000000016763806343078613 | 0.0000000024028665723818676 | 0 | 0 | true | 8 | 8/8 | true | 272.073 |
| 5 | true | 0.00000001955777406692505 | 0.000000002555091471734272 | 0 | 0 | true | 8 | 8/8 | true | 319.993 |
| 6 | true | 0.000000013504177331924438 | 0.000000002562797973837405 | 0 | 0 | true | 8 | 8/8 | true | 308.622 |
| 7 | true | 0.000000013969838619232178 | 0.0000000024793176400805805 | 0 | 0 | true | 8 | 8/8 | true | 293.997 |
| 8 | true | 0.000000016763806343078613 | 0.0000000025876705223026875 | 0 | 0 | true | 8 | 8/8 | true | 313.581 |
| 9 | true | 0.0000000130385160446167 | 0.0000000025239761392015225 | 0 | 0 | true | 8 | 8/8 | true | 344.654 |
| 10 | true | 0.000000021420419216156006 | 0.000000002676262766954096 | 0 | 0 | true | 8 | 8/8 | true | 404.227 |
| 11 | true | 0.000000015832483768463135 | 0.0000000027698761062566746 | 0 | 0 | true | 8 | 8/8 | true | 353.010 |
| 12 | true | 0.000000014901161193847656 | 0.000000002691240785779314 | 0 | 0 | true | 8 | 8/8 | true | 335.181 |
| 13 | true | 0.000000014901161193847656 | 0.000000002727825965109787 | 0 | 0 | true | 8 | 8/8 | true | 380.433 |

## Seal

```txt
if parity_pass == true:
    16AF-P FFN performance probe closed
else:
    keep generation integration locked
```
