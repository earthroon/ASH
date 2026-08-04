--vocab-size
--tie-word-embeddings
--rope-theta
--tensor-count
```

Those values must come from config and parent authorities.

---

# 21. Negative controls

The gate must execute real negative mutations against cloned metadata or temporary fixture copies. It must not mutate the production candidate.

## 21.1 Root and CAS controls

```text
NEG-R5R6-ROOT-001 both root modes supplied
NEG-R5R6-ROOT-002 no root mode supplied
NEG-R5R6-CAS-001 config digest mismatch
NEG-R5R6-CAS-002 index digest mismatch
NEG-R5R6-CAS-003 shard digest mismatch
NEG-R5R6-CAS-004 shard byte-count mismatch
NEG-R5R6-CAS-005 duplicate normalized shard path
NEG-R5R6-CAS-006 parent-directory shard traversal
```

## 21.2 Index and header controls

```text
NEG-R5R6-IDX-001 weight_map references missing shard
NEG-R5R6-IDX-002 weight_map references missing tensor key
NEG-R5R6-IDX-003 header tensor absent from weight_map
NEG-R5R6-IDX-004 same key appears in two shard headers
NEG-R5R6-HDR-001 invalid header length
NEG-R5R6-HDR-002 unsupported dtype
NEG-R5R6-HDR-003 zero shape dimension
NEG-R5R6-HDR-004 shape-product overflow
NEG-R5R6-HDR-005 range overlap
NEG-R5R6-HDR-006 range beyond file
NEG-R5R6-HDR-007 byte-length mismatch
NEG-R5R6-HDR-008 unmapped payload bytes nonzero
```

## 21.3 Canonical schema controls

```text
NEG-R5R6-NAME-001 unknown tensor key
NEG-R5R6-NAME-002 ambiguous alias rule
NEG-R5R6-NAME-003 duplicate canonical role
NEG-R5R6-NAME-004 missing global embedding
NEG-R5R6-NAME-005 missing final norm
NEG-R5R6-NAME-006 missing required LM-head representation
NEG-R5R6-NAME-007 missing layer index
NEG-R5R6-NAME-008 out-of-range layer index
NEG-R5R6-NAME-009 missing per-layer attention tensor
NEG-R5R6-NAME-010 missing per-layer MLP tensor
NEG-R5R6-NAME-011 unexpected bias tensor
```

## 21.4 Shape and identity controls

```text
NEG-R5R6-SHAPE-001 embedding shape mismatch
NEG-R5R6-SHAPE-002 Q shape mismatch
NEG-R5R6-SHAPE-003 K shape mismatch
NEG-R5R6-SHAPE-004 V shape mismatch
NEG-R5R6-SHAPE-005 O shape mismatch
NEG-R5R6-SHAPE-006 norm shape mismatch
NEG-R5R6-SHAPE-007 gate/up shape mismatch
NEG-R5R6-SHAPE-008 down shape mismatch
NEG-R5R6-CONV-001 config geometry differs from R5-R3
NEG-R5R6-CONV-002 config RoPE differs from R5-R5
NEG-R5R6-CONV-003 inventory role count mismatch
NEG-R5R6-CONV-004 parameter-count mismatch
```

## 21.5 Synthetic and authority controls

```text
NEG-R5R6-SYN-001 synthetic fixture profile
NEG-R5R6-SYN-002 production_checkpoint_payload=false
NEG-R5R6-SYN-003 missing role filled by fixture bytes
NEG-R5R6-SYN-004 padded mismatch admitted
NEG-R5R6-AUTH-001 forward authority true
NEG-R5R6-AUTH-002 GPU upload authority true
NEG-R5R6-AUTH-003 production admitted true
NEG-R5R6-AUTH-004 proof ledger admitted true
NEG-R5R6-AUTH-005 R6 admitted true
```

Every negative control must fail for the intended reason and produce a stable error code.

---

# 22. Admission matrix

Required final checks include:

```text
parent R5-R5 exact PASS                              1
parent authority digests complete                    1
production config byte digest exact                  1
production config semantic completeness              1
config-to-R5 geometry convergence                     1
config-to-R5 RoPE convergence                         1
checkpoint root mode exclusive                        1
index digest exact or explicit absence                1
weight_map ownership exact                            1
all referenced shards present                         1
all shard CAS digests exact                           1
all shard byte counts exact                           1
all shard headers valid                               1
cross-shard duplicate key count zero                  1
range overlap count zero                              1
range out-of-bounds count zero                        1
unmapped payload bytes zero                           1
canonical resolver version sealed                     1
unresolved tensor count zero                          1
duplicate canonical role count zero                   1
missing global role count zero                        1
missing layer role count zero                         1
out-of-range layer count zero                         1
dtype-policy mismatch count zero                      1
shape mismatch count zero                             1
byte-length mismatch count zero                       1
tied-role representation valid                        1
physical/logical tensor counts valid                  1
parameter count derived without overflow              1
total payload bytes derived without overflow          1
synthetic tensor count zero                           1
payload mutation count zero                           1
GPU upload count zero                                 1
forward dispatch count zero                           1
negative-control suite complete                       1
production admission false                            1
proof-ledger admission false                          1
R6 admission false                                    1
```

The gate must record the exact denominator. It must not print `PASS` from a partial subset.

---

# 23. Error taxonomy

Required stable error families:

```text
AW02R5R6ParentManifestReadFailed
AW02R5R6ParentPassTokenMismatch
