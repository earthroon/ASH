# 16AF-R Runtime Parity Probe Seal

## Status

```txt
build_gate = pass_by_user_reported_local_cargo_check
runtime_gate = layer0_native_atlas_ffn_parity_probe
generation_connected = false
parity_pass = true
```

## Metrics

```txt
layer = 0
hidden = 2048
intermediate = 5632
threshold = 0.0010000000474974513
shape_match = true
max_abs_delta = 0.0000000260770320892334
mean_abs_delta = 0.0000000020633399433478417
top_index_match = true
top_k_overlap = 8/8
nan_count = 0
inf_count = 0
resolved_backend = native_atlas_ffn_16AF_R1+storage3_split_passes+owned_wgpu_buffers
elapsed_ms = 40604.0776
```

## Weight Layout

```txt
gate_shape = Array [Number(5632), Number(2048)]
up_shape = Array [Number(5632), Number(2048)]
down_shape = Array [Number(2048), Number(5632)]
row_major_weight_layout = true
gate_bias_present = false
up_bias_present = false
down_bias_present = false
```

## Dispatch Log

- `[16AF][ffn] enable_native_atlas_ffn=true enable_silu_swiglu=true`
- `[16AF][ffn] burn_cubecl_ffn_matmul_disabled=true`
- `[16AF][ffn] native-owned WGPU buffers used; raw lease path not used`
- `[16AF-R1][ffn] storage buffer layout split into gate/up/swiglu/down passes; max storage buffers per pipeline = 3`

## Seal

```txt
if parity_pass == true:
    16AF-R runtime parity closed
else:
    keep generation integration locked
```
