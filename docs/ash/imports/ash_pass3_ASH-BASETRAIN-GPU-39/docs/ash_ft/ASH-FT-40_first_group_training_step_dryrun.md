# ASH-FT-40 First Group Training Step Dry-run

This patch is the first compute-open stage in the ASH-FT training-preparation mainline.
It opens forward, real loss, backward, selected-group gradient inspection, and optimizer candidate update calculation. It does not commit anything.

The runner blocks rather than fabricating PASS when backend/model forward evidence is unavailable.

Next: ASH-FT-41 Gradient Receipt / Selected Group Finite Delta Candidate Seal.
