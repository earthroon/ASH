# ASH-FT-10-R1 Compile Surface Fix

This repair closes two compile errors observed after ASH-FT-10 bake:

1. FT-10 referenced a non-existent FT-09 staging receipt type.
2. FT-10 used a shorthand JSON struct field for a variable that did not exist in scope.

The patch is intentionally narrow and does not alter the validation seal behavior.
