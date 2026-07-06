# ASH-TCU-K6B

K6B grid parity specification.

Required: L16D PASS and K6B-R0 PASS.

Shape: M64, N64, K32.

Grid: 4 by 4, 16 macro controls, 16 descriptors.

Output: 4096 f32, 16384 bytes.

Layout: macro contiguous, then logical16 subtile contiguous.

Guards: runtime splice closed, performance claim closed.

PASS marker: PASS_ASH_TCU_K6B_NATIVE_4X4_SQUARE_GRID_READBACK_PARITY_SEAL.
