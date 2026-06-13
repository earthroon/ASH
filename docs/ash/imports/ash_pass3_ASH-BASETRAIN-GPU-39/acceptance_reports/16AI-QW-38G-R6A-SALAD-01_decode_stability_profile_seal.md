# 16AI-QW-38G-R6A-SALAD-01 — Decode Stability Profile Seal

## SSOT

Word-salad suppression belongs to the inference decode loop, not the snapshot runner.

## Baked Status

- Code integrated: yes
- Model mutation: no
- Runtime inference executed in bake container: no
- Local replay required: yes

## Required Local Command Shape

Run the existing generation entrypoint with the same prompt/seed/model and compare:

1. `DEBUG_GREEDY_BASELINE`
2. previous/current default
3. `SAFE_KOREAN_STABLE_V1`

## Pass Gate

`SAFE_KOREAN_STABLE_V1` must reduce word-salad risk without collapsing all answers into empty or over-short output.
