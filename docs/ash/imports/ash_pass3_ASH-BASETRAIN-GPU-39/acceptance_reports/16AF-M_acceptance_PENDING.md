# 16AF-M Acceptance Status

## Verdict

```txt
16AF-M = PENDING_LOCAL_RUN
```

## Completed

```txt
source_bake = done
multi_layer_runner_added = true
generation_connected = false
json_report_writer = true
markdown_report_writer = true
acceptance_report_writer = true
forbidden_path_static_scan = clean
```

## Pending

```txt
cargo check --manifest-path crates/model_core/Cargo.toml --bin af16m_multi_layer_parity
runtime selected layer matrix: layers [0,1,last]
shape_match/max_abs_delta/mean_abs_delta/nan_count/inf_count/top_k_overlap report
```

## Local Command

```powershell
$ckpt = ".\tokenizer_v5\artifacts\full_model_vocab_v5_resized.safetensors"

cargo run --manifest-path crates/model_core/Cargo.toml --bin af16m_multi_layer_parity -- `
  --spec "specs/model_spec_300m_dialogue_continue_gqa8_headwise_atlas.toml" `
  --checkpoint $ckpt `
  --layers "0,1,last" `
  --threshold 0.001 `
  --top-k 8
```
