# ASH-FT-11 Shadow Candidate Header Load Dry-run

ASH-FT-11 checks whether the staged shadow candidate can pass the loader entry gate at metadata level. It does not construct a runnable model and does not execute inference.

Boundary:

```txt
metadata-only header/load preflight: allowed
actual runtime object construction: forbidden
inference/decode/generation: forbidden
runtime default apply/promotion: forbidden
```
