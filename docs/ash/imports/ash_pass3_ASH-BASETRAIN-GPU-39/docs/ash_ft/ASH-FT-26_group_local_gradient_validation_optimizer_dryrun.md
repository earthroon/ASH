# ASH-FT-26 Operator Notes

FT-26 is the optimizer boundary dry-run after FT-25 group-local forward/backward smoke. It revalidates the selected group gradient and computes update-candidate metadata only.

It intentionally does not persist a delta packet. Delta packet writing belongs to ASH-FT-27.

## Command

```powershell
cargo run --bin ash_ft26_group_local_gradient_validation_optimizer_dryrun -- `
  --ft25-receipt "artifacts\ash_ft\ASH-FT-25_receipt.json" `
  --ft25-selected-group "artifacts\ash_ft\ash_ft25_selected_group_receipt.json" `
  --ft25-backward-receipt "artifacts\ash_ft\ash_ft25_group_local_backward_receipt.json" `
  --ft25-gradient-health "artifacts\ash_ft\ash_ft25_gradient_health_receipt.json" `
  --ft25-no-optimizer-step-guard "artifacts\ash_ft\ash_ft25_no_optimizer_step_guard.json" `
  --ft25-no-weight-update-guard "artifacts\ash_ft\ash_ft25_no_weight_update_guard.json" `
  --allow-gradient-revalidation true `
  --allow-optimizer-dryrun true `
  --allow-real-optimizer-step false `
  --allow-optimizer-state-mutation false `
  --allow-weight-update false `
  --allow-delta-packet-creation false `
  --allow-delta-stack-append false `
  --allow-base-checkpoint-mutation false `
  --allow-runtime-default-apply false `
  --allow-checkpoint-alias-rebind false `
  --allow-promotion false `
  --optimizer-profile "adamw_dryrun" `
  --learning-rate "0.00001" `
  --clip-norm-threshold "1.0" `
  --next-patch "ASH-FT-27" `
  --out-dryrun-plan "artifacts\ash_ft\ash_ft26_optimizer_dryrun_plan.json" `
  --out-gradient-revalidation "artifacts\ash_ft\ash_ft26_gradient_revalidation_receipt.json" `
  --out-gradient-norm-policy "artifacts\ash_ft\ash_ft26_gradient_norm_policy_receipt.json" `
  --out-optimizer-profile "artifacts\ash_ft\ash_ft26_optimizer_profile_receipt.json" `
  --out-update-candidate-dryrun "artifacts\ash_ft\ash_ft26_update_candidate_dryrun_receipt.json" `
  --out-no-optimizer-state-mutation "artifacts\ash_ft\ash_ft26_no_optimizer_state_mutation_guard.json" `
  --out-no-weight-update "artifacts\ash_ft\ash_ft26_no_weight_update_guard.json" `
  --out-no-delta-packet "artifacts\ash_ft\ash_ft26_no_delta_packet_guard.json" `
  --out-next-route "artifacts\ash_ft\ash_ft26_next_patch_route.json" `
  --out-receipt "artifacts\ash_ft\ASH-FT-26_receipt.json"
```
