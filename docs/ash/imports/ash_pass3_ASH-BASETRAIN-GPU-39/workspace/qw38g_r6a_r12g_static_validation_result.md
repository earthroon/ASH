# R12G Static Validation

- patch_id: 16AI-QW-38G-R6A-R12A-R12G
- status: PASS_STATIC_VALIDATION
- script_sha256: 137a30141e7827741bd3987209572c319295642b52aa10fda7c92f022366a5fb

## Scope

R12G adds the threshold edge sweep script and static validation receipts. Runtime validation must still be executed locally with PowerShell against the user's R12F artifacts.

## Locked Semantics

- baseline_margin_min = 0.05
- 0.049 blocks
- 0.050 allows
- negative control actual apply is blocked regardless of margin
- mutation flags remain false
- production_safe_confirmed/root_cause_confirmed remain false
