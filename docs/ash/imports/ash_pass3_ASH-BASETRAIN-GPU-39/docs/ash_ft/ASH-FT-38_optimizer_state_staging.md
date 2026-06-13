# ASH-FT-38 Optimizer State Staging

FT-38 is not a training patch. It is the optimizer staging boundary for the selected atlas group from FT-37.

It writes planning artifacts only:

- optimizer staging plan
- FT-37 train run binding receipt
- AdamW group-local optimizer profile
- group-local state layout
- optimizer state size estimate
- staging path manifest
- full-model optimizer allocation guard
- optimizer staging manifest
- no materialized optimizer state guard
- no model training guard
- next route to FT-39

The patch keeps full-model optimizer state allocation impossible by default. It also prevents materialized optimizer state payload files from being written in FT-38.
