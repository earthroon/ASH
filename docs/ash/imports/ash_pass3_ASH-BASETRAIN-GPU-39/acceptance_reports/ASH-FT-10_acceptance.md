# ASH-FT-10 Acceptance

PASS requires:

1. FT-09 write/staging/apply/integrity/rollback receipts are readable.
2. Source candidate sha256 matches expected and remains unchanged.
3. Shadow candidate exists and can be opened read-only.
4. Shadow safetensors header parses.
5. Shadow tensor key set, dtype, shape, and offsets match FT-00 manifest.
6. Metadata-only dry-run is accepted only when explicitly allowed.
7. Unpatched deterministic spot-checks match source candidate.
8. Runtime default apply, checkpoint alias rebind, promotion, model load, inference, decode, generation, and train remain false.
