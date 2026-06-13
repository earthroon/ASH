# ASH-FT-06 Single Group Gradient Receipt

FT-06 is the last receipt-only stage before optimizer dry-run. It turns the FT-05 backward smoke result into an optimizer input candidate contract while keeping all mutation gates closed.

The implementation intentionally imports FT-05 receipt types through the FT-05 module path to avoid root export coupling.

```rust
crate::ash_ft05_single_group_forward_backward_smoke::{ ... }
```

The generated optimizer input candidate is marked `RECEIPT_ONLY` and points to the next allowed stage: `ASH-FT-07_OPTIMIZER_DRYRUN_NO_CANDIDATE_WRITE`.
