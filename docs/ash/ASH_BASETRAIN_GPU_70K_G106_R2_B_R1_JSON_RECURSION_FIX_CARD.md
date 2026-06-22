# ASH G106 R2 B R1 JSON Recursion Fix

Source: G106 R2 B TRAIN
FixId: G106-R2-B-R1-JSON-RECURSION-FIX

Scope: fixes compile failure caused by serde_json json macro recursion in ClosedState to_json.

Change:
- Replaced the large json object macro with explicit serde_json Map insertion.
- Did not use recursion_limit as the fix.
- Preserved patch id, runtime pass target, and semantic boundaries.

Boundaries unchanged:
- No optimizer
- No weight delta materialization
- No weight commit
- No checkpoint finalize
- No production or runtime route mutation
- No quality claim
