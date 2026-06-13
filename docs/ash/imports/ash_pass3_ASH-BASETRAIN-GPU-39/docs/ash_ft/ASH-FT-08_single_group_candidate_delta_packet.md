# ASH-FT-08 Single Group Candidate Delta Packet

FT-08 packages the FT-07 optimizer dry-run delta preview into a candidate delta packet.

This is a packetization step only. It does not write into the safetensors file. FT-09 or later must own any staged/shadow write gate.

Outputs:

- `ash_ft08_candidate_delta_packet.json`
- `ash_ft08_delta_packet_manifest.json`
- `ash_ft08_delta_packet_integrity_receipt.json`
- `ash_ft08_rollback_metadata.json`
- `ASH-FT-08_receipt.json`
