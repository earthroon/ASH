# ASH-FT-39 Dataloader Microbatch Preflight

FT-39 is not a training patch. It is the dataloader and microbatch shape preflight boundary before the first selected-group training dry-run.

It writes planning and validation artifacts only:

- dataloader preflight plan
- training inputs binding receipt
- microbatch policy receipt
- microbatch sample receipt
- shape/dtype validation
- label mask alignment receipt
- split batch boundary receipt
- dataloader preflight manifest
- no model mutation guard
- no training execution guard
- next route to FT-40

The patch intentionally blocks model forward, real loss computation, backward, optimizer step, weight update, optimizer state materialization, delta packet creation, and shadow route.
