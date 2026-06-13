# ASH-FT-12-R2 Stack-safe Worker

FT-12 performs metadata-only runtime candidate binding. A Windows main-thread stack overflow was observed even though the CLI included `--worker-stack-mb 128`.

R2 makes that flag effective by executing the run/write sequence inside a worker thread with explicit stack sizing. This is a runner-surface fix, not a semantic expansion.
