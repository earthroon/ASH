# QW-54H Roadmap

1. Add QW-54H escape selector module.
2. Run after QW-54G demotion and before final argmax.
3. Treat greedy top1 as provisional when it belongs to a detected attractor set.
4. Prefer highest non-attractor candidate from expanded finite CPU row.
5. Apply finite final-authority demotion to attractor members only; no bans or masks.
6. Emit `qw54h_escape_selector_trace.jsonl` and `qw54h_no_greedy_fallback_receipt.json`.
