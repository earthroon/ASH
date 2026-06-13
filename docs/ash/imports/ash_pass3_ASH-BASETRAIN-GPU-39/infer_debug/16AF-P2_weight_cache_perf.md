# 16AF-P2 FFN Weight Preupload Cache Seal

## Status

```txt
runtime_gate = ffn_weight_preupload_perf_only
generation_connected = false
threshold = 0.0010000000474974513
top_k = 8
parity_pass = true
```

## Cache

```txt
preupload = true
cached_layers = 14
mode = ffn_weights_only
total_bytes = 1937768448
preupload_ms = 361.6366
weight_upload_sum_before_ms = 213.099
weight_upload_sum_after_ms = 0
weight_upload_reduction_ratio = 1
```

## Summary

```txt
total = 14
completed = 14
passed = 14
failed = 0
max_abs_delta_global = 0.0000000260770320892334
mean_abs_delta_avg = 0.0000000024972721668348186
elapsed_ms_total = 50050.742300000005
telemetry_total_gpu_ms = 291.70550000000003
telemetry_weight_upload_ms = 0
telemetry_submit_readback_ms = 273.6732
telemetry_readback_buffers = 14
telemetry_readback_elements = 28672
```

## Layer Matrix

| layer | shape_match | max_abs_delta | mean_abs_delta | nan | inf | top_k_ratio | parity_pass | elapsed_ms | weight_upload_ms |
|---:|---|---:|---:|---:|---:|---|---|---:|---:|
| 0 | true | 0.0000000260770320892334 | 0.0000000020633399433478417 | 0 | 0 | 8/8 | true | 459.787 | 0.000 |
| 1 | true | 0.000000015832483768463135 | 0.0000000021861623622498882 | 0 | 0 | 8/8 | true | 317.721 | 0.000 |
| 2 | true | 0.000000016298145055770874 | 0.0000000023017856509710555 | 0 | 0 | 8/8 | true | 331.787 | 0.000 |
| 3 | true | 0.000000014435499906539917 | 0.0000000024335966575250723 | 0 | 0 | 8/8 | true | 297.306 | 0.000 |
| 4 | true | 0.000000016763806343078613 | 0.0000000024028665723818676 | 0 | 0 | 8/8 | true | 292.500 | 0.000 |
| 5 | true | 0.00000001955777406692505 | 0.000000002555091471734272 | 0 | 0 | 8/8 | true | 291.872 | 0.000 |
| 6 | true | 0.000000013504177331924438 | 0.000000002562797973837405 | 0 | 0 | 8/8 | true | 352.213 | 0.000 |
| 7 | true | 0.000000013969838619232178 | 0.0000000024793176400805805 | 0 | 0 | 8/8 | true | 278.072 | 0.000 |
| 8 | true | 0.000000016763806343078613 | 0.0000000025876705223026875 | 0 | 0 | 8/8 | true | 279.204 | 0.000 |
| 9 | true | 0.0000000130385160446167 | 0.0000000025239761392015225 | 0 | 0 | 8/8 | true | 269.721 | 0.000 |
| 10 | true | 0.000000021420419216156006 | 0.000000002676262766954096 | 0 | 0 | 8/8 | true | 351.060 | 0.000 |
| 11 | true | 0.000000015832483768463135 | 0.0000000027698761062566746 | 0 | 0 | 8/8 | true | 330.076 | 0.000 |
| 12 | true | 0.000000014901161193847656 | 0.000000002691240785779314 | 0 | 0 | 8/8 | true | 278.558 | 0.000 |
| 13 | true | 0.000000014901161193847656 | 0.000000002727825965109787 | 0 | 0 | 8/8 | true | 311.969 | 0.000 |

## Seal

```txt
if parity_pass == true:
    16AF-P2 FFN weight preupload cache perf closed
else:
    keep generation integration locked
```
