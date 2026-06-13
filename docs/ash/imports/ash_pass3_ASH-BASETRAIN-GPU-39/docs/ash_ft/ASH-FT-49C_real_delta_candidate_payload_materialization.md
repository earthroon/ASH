# ASH-FT-49C Implementation Notes

This patch starts the real post-optimizer payload line. It deliberately does not reuse the earlier FT-44 payload staging line, because FT-44 may have descriptor-era payload semantics. FT-49C accepts only ASH-FT-49B real optimizer candidate tensor sources.

Runtime hard stops:

- no synthetic candidate source
- no stale FT-44 payload source
- no official delta packet creation
- no delta stack append
- no checkpoint apply
- no safetensors rewrite
- no shadow/runtime/promotion route
