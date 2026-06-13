# ASH-FT-09 Acceptance

PASS requires:
1. FT-08 delta packet, manifest, integrity receipt, and rollback metadata are readable.
2. Source candidate sha256 matches expected.
3. Source candidate is copied to staging temp path.
4. Temp sha256 matches source before patch.
5. All packet tensor keys exist in FT-00 manifest.
6. All byte ranges are inside tensor offsets.
7. Before checksums match staged copy.
8. Staged shadow candidate is created.
9. Source candidate sha256 is unchanged after staging.
10. Runtime default apply and checkpoint alias rebind remain false.

FAIL if source candidate is overwritten, runtime default is touched, alias is rebound, promotion runs, or checksum/range validation fails.
