# ASH-FT-08 Acceptance

PASS when:

1. FT-00 manifest is read.
2. FT-07 optimizer plan, delta preview, and weight-after-preview receipts are read.
3. Candidate sha256 matches the expected value.
4. Selected group is single-group only and matches FT-07.
5. Tensor keys exist in the FT-00 manifest.
6. Delta packet entries are created.
7. Packet sha256 is created.
8. Rollback metadata is created.
9. `safetensors_write_executed = false`.
10. `candidate_weight_write_executed = false`.
11. `runtime_default_apply_executed = false`.

Expected PASS string:

```txt
PASS_ASH_FT08_SINGLE_GROUP_CANDIDATE_DELTA_PACKET_NO_SAFETENSORS_WRITE
```
