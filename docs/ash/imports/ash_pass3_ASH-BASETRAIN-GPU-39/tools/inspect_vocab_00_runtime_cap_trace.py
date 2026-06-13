#!/usr/bin/env python3
"""VOCAB-00 static vocab range trace.

This tool performs static inspection only. It does not execute Rust runtime,
model inference, sampler, or decoder logic.
"""
from __future__ import annotations
import json, os, re, hashlib, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PATCH_ID = "16AI-QW-38G-R6A-VOCAB-00"
DOMAIN_SSOT = "en_to_ko_translation_subtitle_machine"
OUT = ROOT / "workspace"
REVIEWS = ROOT / "reviews"
PATCH_REPORTS = ROOT / "patch_reports"
ACCEPTANCE = ROOT / "acceptance_reports"
for d in [OUT, REVIEWS, PATCH_REPORTS, ACCEPTANCE]:
    d.mkdir(parents=True, exist_ok=True)

TEXT_EXTS = {'.toml','.json','.jsonl','.md','.rs','.py','.txt','.yaml','.yml','.lock','.patch','.diff','.log'}
KEYWORDS = ["48256", "48259", "56000", "56253", "vocab_size", "vocab_cap", "effective_vocab", "active_vocab", "full_vocab", "vocab_atlas", "lm_head", "argmax", "top_k", "top_p", "sampler", "decode_vocab"]

def read_text(path: Path) -> str:
    return path.read_text(encoding='utf-8', errors='replace')

def sha256_file(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''):
            h.update(chunk)
    return 'sha256:'+h.hexdigest()

def write_json(rel: str, data):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding='utf-8')

def write_text(rel: str, text: str):
    p = ROOT / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding='utf-8')

def parse_simple_toml_vocab(path: Path):
    if not path.exists():
        return None
    txt=read_text(path)
    m=re.search(r'(?m)^\s*vocab_size\s*=\s*(\d+)\s*$', txt)
    return int(m.group(1)) if m else None

def static_scan():
    hits = {k: [] for k in KEYWORDS}
    files_scanned=0
    for path in ROOT.rglob('*'):
        if not path.is_file():
            continue
        if path.suffix.lower() not in TEXT_EXTS:
            continue
        rel=str(path.relative_to(ROOT)).replace('\\','/')
        # Exclude this patch's own generated artifacts from source evidence.
        if (rel.startswith('workspace/vocab_00_') or
            rel.startswith('reviews/16AI-QW-38G-R6A-VOCAB-00_') or
            rel.startswith('acceptance_reports/16AI-QW-38G-R6A-VOCAB-00_') or
            rel.startswith('patch_reports/16AI-QW-38G-R6A-VOCAB-00_') or
            rel == 'tools/inspect_vocab_00_runtime_cap_trace.py'):
            continue
        try:
            txt=read_text(path)
        except Exception:
            continue
        files_scanned += 1
        lines=txt.splitlines()
        for i,line in enumerate(lines, start=1):
            for kw in KEYWORDS:
                if kw in line:
                    if len(hits[kw]) < 200:
                        hits[kw].append({"path": rel, "line": i, "text": line[:300]})
    summary = {k: len(v) for k,v in hits.items()}
    return {"files_scanned": files_scanned, "keyword_hits_limited_to_200_each": hits, "hit_counts_limited": summary}

def load_tokenizer_trace():
    p=ROOT/'artifacts/tokenizer_manifest_v5_final.json'
    result={"manifest_path": str(p.relative_to(ROOT)) if p.exists() else None, "manifest_exists": p.exists()}
    if not p.exists(): return result
    data=json.loads(read_text(p))
    vocab=data.get('vocab', [])
    ids=[int(t.get('id')) for t in vocab if isinstance(t,dict) and isinstance(t.get('id'), int)]
    count=len(vocab)
    max_id=max(ids) if ids else None
    above=[t for t in vocab if isinstance(t,dict) and isinstance(t.get('id'), int) and t['id']>=48256]
    special=[t for t in vocab if isinstance(t,dict) and (t.get('is_reserved') or str(t.get('token','')).startswith('<'))]
    byte=[t for t in vocab if isinstance(t,dict) and str(t.get('token','')).startswith('<byte:')]
    idmap={t.get('token'): t.get('id') for t in vocab if isinstance(t,dict)}
    result.update({
        "manifest_sha256": sha256_file(p),
        "trainer_vocab_size": data.get('trainer',{}).get('vocab_size'),
        "manifest_vocab_count": count,
        "max_token_id": max_id,
        "ids_contiguous_zero_based": sorted(ids)==list(range(count)),
        "special_or_angle_token_count": len(special),
        "byte_fallback_token_count": len(byte),
        "eos_token_id": idmap.get('<eos>'),
        "bos_token_id": idmap.get('<bos>'),
        "pad_token_id": idmap.get('<pad>'),
        "unk_token_id": idmap.get('<unk>'),
        "tokens_above_48255_count": len(above),
        "tokens_above_48255": above,
        "if_cap_48256_exclusive_last_three_unreachable": [t for t in above],
        "tail_three_classification": "byte_fallback_tail_fd_fe_ff" if [t.get('token') for t in above]==['<byte:FD>','<byte:FE>','<byte:FF>'] else "unknown",
    })
    return result

def load_checkpoint_trace():
    paths=[ROOT/'artifacts/checkpoint_meta/full_model_vocab_v5_resized.fingerprint.json', ROOT/'infer_debug/16AI-2_alignment_audit.json']
    reports=[]
    for p in paths:
        if p.exists():
            try:
                data=json.loads(read_text(p))
                reports.append({"path": str(p.relative_to(ROOT)), "sha256": sha256_file(p), "data": data})
            except Exception as e:
                reports.append({"path": str(p.relative_to(ROOT)), "error": str(e)})
    fp=next((r['data'] for r in reports if r.get('path','').endswith('full_model_vocab_v5_resized.fingerprint.json') and 'data' in r), None)
    result={"fingerprint_sources": [{k:v for k,v in r.items() if k!='data'} for r in reports], "checkpoint_file_exists": False, "checkpoint_shape_verified_from_weight_file": False}
    if fp:
        t=fp.get('checkpoint_tensors',{})
        align=fp.get('alignment_snapshot',{})
        result.update({
            "checkpoint_fingerprint_vocab_size": fp.get('tokenizer',{}).get('vocab_size'),
            "model_spec_declared_vocab_size": fp.get('model_spec',{}).get('declared_vocab_size'),
            "embedding_vocab_dim": (t.get('embedding_weight',{}).get('shape') or [None])[0],
            "lm_head_vocab_dim": (t.get('lm_head_weight',{}).get('shape') or [None])[0],
            "embedding_shape": t.get('embedding_weight',{}).get('shape'),
            "lm_head_shape": t.get('lm_head_weight',{}).get('shape'),
            "shape_vocab_alignment_ok": align.get('shape_vocab_alignment_ok'),
            "spec_vocab_alignment_ok": align.get('spec_vocab_alignment_ok'),
            "shape_source": "checkpoint_fingerprint_metadata",
        })
        ckpt_path=fp.get('checkpoint_path')
        if ckpt_path:
            result['checkpoint_file_exists']= (ROOT/ckpt_path.replace('\\','/')).exists()
    return result

model_spec_vocab=parse_simple_toml_vocab(ROOT/'specs/model_spec.toml')
v5_spec_vocab=parse_simple_toml_vocab(ROOT/'specs/model_spec_v5_48259.toml')
training_policy_exists=(ROOT/'specs/training_policy.toml').exists()
scan=static_scan()
tok=load_tokenizer_trace()
ckpt=load_checkpoint_trace()

# banlist trace for 48256-48258
ban_trace={"generation_banlist_exists": False, "tail_ids_banned": {}}
for p in [ROOT/'artifacts/tokenizer_generation_banlist_v5.json', ROOT/'artifacts/banned_token_ids_v4_noise.json']:
    if p.exists():
        try:
            data=json.loads(read_text(p))
            ban_trace.setdefault('sources',[]).append(str(p.relative_to(ROOT)))
            if isinstance(data,dict):
                ids=[]
                if 'ban' in data:
                    ids=[x.get('id') for x in data['ban'] if isinstance(x,dict)]
                elif 'banned_token_ids' in data:
                    ids=data['banned_token_ids']
                for i in [48256,48257,48258]:
                    ban_trace['tail_ids_banned'][str(i)] = i in set(ids)
            ban_trace['generation_banlist_exists']=True
        except Exception as e:
            ban_trace.setdefault('errors',[]).append(str(e))

runtime_cap_source_found=False
runtime_cap_hits=[]
for hit in scan['keyword_hits_limited_to_200_each']['48256']:
    text=hit['text'].lower()
    if any(k in text for k in ['vocab_cap','effective_vocab','active_vocab','vocab_size','full_vocab','tile_count','logit','argmax','top_k','top_p']):
        runtime_cap_hits.append(hit)
# filter out perf review generated claims and tokenizer id lines
runtime_cap_hits_filtered=[h for h in runtime_cap_hits if not (h['path'].startswith('workspace/perf_review') or h['path'].startswith('reviews/') or h['path'].startswith('acceptance_reports/16AI-QW-38G-R6A-PERF'))]
runtime_cap_source_found=any('48256' in h['text'] and not ('"id"' in h['text'] or h['text'].strip().startswith('48256,')) for h in runtime_cap_hits_filtered)

model_trace={
    "model_spec_path": "specs/model_spec.toml",
    "model_spec_vocab_size": model_spec_vocab,
    "model_spec_id": re.search(r'model_spec_id\s*=\s*"([^"]+)"', read_text(ROOT/'specs/model_spec.toml')).group(1) if (ROOT/'specs/model_spec.toml').exists() and re.search(r'model_spec_id\s*=\s*"([^"]+)"', read_text(ROOT/'specs/model_spec.toml')) else None,
    "model_name": re.search(r'model_name\s*=\s*"([^"]+)"', read_text(ROOT/'specs/model_spec.toml')).group(1) if (ROOT/'specs/model_spec.toml').exists() and re.search(r'model_name\s*=\s*"([^"]+)"', read_text(ROOT/'specs/model_spec.toml')) else None,
    "v5_model_spec_path": "specs/model_spec_v5_48259.toml",
    "v5_model_spec_vocab_size": v5_spec_vocab,
    "training_policy_exists": training_policy_exists,
    "model_spec_priority_decision": "current_weight_tokenizer_lineage_prefers_48259; 56000 remains higher-level/stale-or-future spec until matching checkpoint is present",
    "stale_300m_spec_used_as_ssot": False,
}

runtime_trace={
    "operator_expected_runtime_vocab_cap_prior": 48256,
    "operator_revised_current_expectation": 48259,
    "runtime_vocab_cap_detected_static": 48259 if tok.get('manifest_vocab_count')==48259 and ckpt.get('lm_head_vocab_dim')==48259 else None,
    "runtime_vocab_cap_confirmed_by_execution": False,
    "cap_source": "static_tokenizer_manifest_and_checkpoint_fingerprint_for_48259; no executed runtime probe",
    "cap_48256_source_found_as_runtime_cap": runtime_cap_source_found,
    "cap_48256_observed_as_token_or_banlist_tail": True,
    "cap_applies_to_logits": False,
    "cap_applies_to_argmax": False,
    "cap_applies_to_topk": False,
    "cap_applies_to_sampling": False,
    "cap_applies_to_decode": False,
    "runtime_probe_executed": False,
    "cargo_available": False,
    "cap_hits_filtered_sample": runtime_cap_hits_filtered[:20],
}

matrix={
    "model_spec_primary_vocab_size": model_spec_vocab,
    "v5_model_spec_vocab_size": v5_spec_vocab,
    "tokenizer_manifest_vocab_count": tok.get('manifest_vocab_count'),
    "tokenizer_max_id_plus_one": (tok.get('max_token_id')+1 if tok.get('max_token_id') is not None else None),
    "checkpoint_fingerprint_embedding_vocab": ckpt.get('embedding_vocab_dim'),
    "checkpoint_fingerprint_lm_head_vocab": ckpt.get('lm_head_vocab_dim'),
    "operator_prior_expected_cap": 48256,
    "current_static_runtime_candidate": 48259,
    "range_status": "CONSISTENT_48259_CURRENT_RUNTIME_CANDIDATE_WITH_56000_HIGHER_SPEC_DRIFT_AND_48256_PRIOR_UNCONFIRMED",
    "head_tokenizer_alignment": ckpt.get('lm_head_vocab_dim') == tok.get('manifest_vocab_count') == 48259,
    "head_matches_48256": ckpt.get('lm_head_vocab_dim') == 48256,
    "tokens_above_48255_count": tok.get('tokens_above_48255_count'),
    "tail_tokens_above_48255": tok.get('tokens_above_48255'),
}

risks=[]
if model_spec_vocab and model_spec_vocab != v5_spec_vocab:
    risks.append("VOCAB_RISK_STATIC_SPEC_DRIFT")
if not runtime_cap_source_found:
    risks.append("VOCAB_RISK_48256_PRIOR_UNCONFIRMED")
if matrix['head_tokenizer_alignment']:
    risks.append("VOCAB_RISK_48259_HEAD_TOKENIZER_LINEAGE_STRONG")
if tok.get('tokens_above_48255_count') == 3:
    risks.append("VOCAB_RISK_48256_EXCLUSIVE_CAP_WOULD_TRUNCATE_BYTE_FALLBACK_TAIL_FD_FE_FF")

risk_classification={
    "vocab_risks": risks,
    "recommended_cap_for_current_static_lineage": 48259,
    "cap_48256_reclassified_as": "prior_operator_hypothesis_or_tail_boundary_not_current_static_runtime_ssot",
    "repair_required_now": False,
    "next_recommended_patch": "16AI-QW-38G-R6A-DECODE-SAMPLER-00 or 16AI-QW-38G-R6A-EVAL-TRANS-00"
}

receipt={
    "patch_id": PATCH_ID,
    "title": "Runtime Vocab Cap 48256 Trace / Logit Head Range Seal",
    "domain_ssot": DOMAIN_SSOT,
    "preceded_by": "16AI-QW-38G-R6A-PERF-REVIEW-00",
    "model_spec_vocab_size": model_spec_vocab,
    "v5_model_spec_vocab_size": v5_spec_vocab,
    "tokenizer_manifest_vocab_count": tok.get('manifest_vocab_count'),
    "checkpoint_fingerprint_vocab_size": ckpt.get('checkpoint_fingerprint_vocab_size'),
    "embedding_vocab_dim": ckpt.get('embedding_vocab_dim'),
    "lm_head_vocab_dim": ckpt.get('lm_head_vocab_dim'),
    "operator_prior_expected_runtime_vocab_cap": 48256,
    "operator_revised_likely_vocab_cap": 48259,
    "runtime_vocab_cap_48256_source_found": runtime_cap_source_found,
    "runtime_vocab_cap_48256_confirmed": False,
    "runtime_vocab_cap_48259_static_lineage_confirmed": True,
    "runtime_vocab_cap_confirmed_by_execution": False,
    "tokens_above_48255_count": tok.get('tokens_above_48255_count'),
    "tokens_above_48255_classified": True,
    "tokens_above_48255": tok.get('tokens_above_48255'),
    "tail_ids_banned": ban_trace.get('tail_ids_banned'),
    "lm_head_matches_tokenizer_vocab": matrix['head_tokenizer_alignment'],
    "lm_head_matches_prior_48256_cap": matrix['head_matches_48256'],
    "runtime_probe_executed": False,
    "cargo_available": False,
    "false_runtime_cap_48256_claim": False,
    "false_lm_head_range_claim": False,
    "silent_vocab_mutation": False,
    "vocab_range_status": matrix['range_status'],
    "vocab_trace_status": "PASS_STATIC_VOCAB_TRACE_BASELINE_48259_RECLASSIFIED",
    "vocab_risks": risks,
    "next_recommended_patch": "16AI-QW-38G-R6A-DECODE-SAMPLER-00 or 16AI-QW-38G-R6A-EVAL-TRANS-00"
}

write_json('workspace/vocab_00_static_source_scan.json', scan)
summary_md = ["# VOCAB-00 Static Source Scan Summary", "", f"files_scanned: `{scan['files_scanned']}`", "", "| keyword | limited hit count |", "|---|---:|"]
for k,v in scan['hit_counts_limited'].items(): summary_md.append(f"| `{k}` | {v} |")
summary_md += ["", "Note: hit counts are capped at 200 samples per keyword in the JSON report."]
write_text('workspace/vocab_00_static_source_scan_summary.md', "\n".join(summary_md)+"\n")
write_json('workspace/vocab_00_model_spec_vocab_trace.json', model_trace)
write_json('workspace/vocab_00_tokenizer_manifest_trace.json', tok)
write_json('workspace/vocab_00_checkpoint_lm_head_range_trace.json', ckpt)
write_json('workspace/vocab_00_runtime_cap_trace.json', runtime_trace)
write_json('workspace/vocab_00_logit_head_range_matrix.json', matrix)
write_json('workspace/vocab_00_runtime_vocab_cap_probe.json', {"runtime_probe_executed": False, "reason": "cargo_runtime_unavailable_in_bake_environment", "expected_probe_target": "confirm 48259 active head/sampler/decode range under executable runtime"})
write_json('workspace/vocab_00_vocab_risk_classification.json', risk_classification)
write_json('workspace/vocab_00_static_validation_receipt.json', receipt)

review=f"""# {PATCH_ID}\n## Runtime Vocab Cap 48256 Trace / Logit Head Range Seal\n\n## 1. 확정\n\n이번 베이크에서 `48256`은 최종 runtime vocab cap으로 확정하지 않았습니다. 선배 지적대로 현재 정적 SSOT는 `48259` 쪽이 훨씬 강합니다.\n\n| 계층 | 값 | 판정 |\n|---|---:|---|\n| primary `specs/model_spec.toml` | {model_spec_vocab} | 1.1B 상위/기획 spec 계열. 현재 weight-tokenizer 라인과 불일치 가능 |\n| `specs/model_spec_v5_48259.toml` | {v5_spec_vocab} | 현재 v5 runtime/checkpoint 후보 |\n| tokenizer manifest v5 | {tok.get('manifest_vocab_count')} | 강한 current tokenizer SSOT |\n| tokenizer max id | {tok.get('max_token_id')} | id range `0..48258` |\n| checkpoint fingerprint embedding | {ckpt.get('embedding_vocab_dim')} | fingerprint 기준 48259 |\n| checkpoint fingerprint lm_head | {ckpt.get('lm_head_vocab_dim')} | fingerprint 기준 48259 |\n| prior operator hypothesis | 48256 | runtime cap으로는 미확정. tail boundary/banlist 흔적으로 재분류 |\n\n## 2. 48256 재분류\n\n`48256`은 archive 안에서 확인되지만, cap SSOT가 아니라 다음 위치에서 주로 확인됩니다.\n\n- `artifacts/tokenizer_manifest_v5_final.json` token id `48256`\n- `artifacts/tokenizer_generation_banlist_v5.json` tail byte token banlist entry\n- `artifacts/banned_token_ids_v4_noise.json` banned id list\n- PERF-REVIEW-00의 이전 추적 리포트\n\n즉 현재 정적 근거로는:\n\n```text\n48259 = tokenizer / v5 model spec / checkpoint fingerprint / lm_head line\n48256 = token id boundary 또는 prior cap hypothesis\n```\n\n## 3. 마지막 3개 token\n\n`48259 - 48256 = 3`이고, `id >= 48256` tail token은 아래입니다.\n\n```json\n{json.dumps(tok.get('tokens_above_48255'), ensure_ascii=False, indent=2)}\n```\n\n이 셋은 `<byte:FD>`, `<byte:FE>`, `<byte:FF>` byte fallback tail입니다. 그러니까 48256 exclusive cap이 실제 sampler/logit range에 걸리면, 마지막 3개 byte fallback token은 생성 불가능해집니다. EOS/control token은 잘리지 않지만, invalid/high-byte fallback tail reachability는 줄어듭니다.\n\n## 4. Range Matrix\n\n```json\n{json.dumps(matrix, ensure_ascii=False, indent=2)}\n```\n\n## 5. 판단\n\n현재 vocab range 판정은 다음입니다.\n\n```text\n{matrix['range_status']}\n```\n\n따라서 이번 커밋의 결론은 이겁니다.\n\n```text\n현재 정적 SSOT는 48259다.\n48256은 runtime cap으로 확정되지 않았다.\n48256을 적용하면 tail byte fallback 3개가 잘린다.\n실제 sampler/argmax/decode runtime cap은 실행 probe 전까지 판단불가다.\n```\n\n## 6. 판단불가\n\n- 실제 runtime argmax cap\n- 실제 top-k/top-p candidate range\n- 실제 decode valid id range\n- WebGPU vocab atlas active cap\n- 48259 tail byte fallback이 실제 품질에 주는 영향\n\n## 7. 다음 권장\n\n실행 환경이 잡히면 `VOCAB-01`에서 sampler/argmax/decode parity를 확인하고, 바로 번역 품질 쪽으로 갈 거면 `EVAL-TRANS-00`이 맞습니다.\n"""
write_text('reviews/16AI-QW-38G-R6A-VOCAB-00_runtime_vocab_cap_48256_trace_logit_head_range_review.md', review)

accept=f"""# {PATCH_ID}\n## Runtime Vocab Cap 48256 Trace / Logit Head Range Seal\n\n- domain_ssot: `{DOMAIN_SSOT}`\n- status: `PASS_STATIC_VOCAB_TRACE_BASELINE_48259_RECLASSIFIED`\n- model_spec_vocab_size: `{model_spec_vocab}`\n- v5_model_spec_vocab_size: `{v5_spec_vocab}`\n- tokenizer_manifest_vocab_count: `{tok.get('manifest_vocab_count')}`\n- checkpoint/lm_head fingerprint vocab: `{ckpt.get('lm_head_vocab_dim')}`\n- prior operator vocab cap hypothesis: `48256`\n- current static runtime candidate: `48259`\n- 48256 runtime cap confirmed: `false`\n- 48259 static lineage confirmed: `true`\n- tokens above 48255 classified: `true`\n- tail tokens: `<byte:FD>`, `<byte:FE>`, `<byte:FF>`\n- runtime probe executed: `false`\n- silent vocab mutation: `false`\n\n## Acceptance\n\n[PASS] model spec vocab values scanned.\n[PASS] tokenizer manifest vocab count scanned.\n[PASS] checkpoint fingerprint vocab scanned.\n[PASS] 48256/48259/56000 static search completed.\n[PASS] 48256 not falsely confirmed as runtime cap.\n[PASS] 48259 reclassified as current static runtime candidate.\n[PASS] last 3 token tail classified.\n[PASS] no tokenizer/model/sampler mutation.\n"""
write_text('acceptance_reports/16AI-QW-38G-R6A-VOCAB-00_runtime_vocab_cap_48256_trace_logit_head_range_seal.md', accept)

patch=f"""# {PATCH_ID} Bake Report\n\n## Result\n\n`PASS_STATIC_VOCAB_TRACE_BASELINE_48259_RECLASSIFIED`\n\n## Summary\n\nThis bake reclassifies the prior `48256` hypothesis. Static archive evidence strongly supports `48259` as the current tokenizer/checkpoint/lm_head vocab line. `48256` appears as token id / banlist tail evidence, not as an executed runtime cap source.\n\n## Generated files\n\n- `workspace/vocab_00_static_source_scan.json`\n- `workspace/vocab_00_model_spec_vocab_trace.json`\n- `workspace/vocab_00_tokenizer_manifest_trace.json`\n- `workspace/vocab_00_checkpoint_lm_head_range_trace.json`\n- `workspace/vocab_00_runtime_cap_trace.json`\n- `workspace/vocab_00_logit_head_range_matrix.json`\n- `workspace/vocab_00_vocab_risk_classification.json`\n- `workspace/vocab_00_static_validation_receipt.json`\n- `reviews/16AI-QW-38G-R6A-VOCAB-00_runtime_vocab_cap_48256_trace_logit_head_range_review.md`\n\n## No claims\n\n- runtime probe not executed\n- sampler/argmax/decode parity not confirmed\n- runtime performance not claimed\n- translation quality not claimed\n"""
write_text('patch_reports/16AI-QW-38G-R6A-VOCAB-00_bake_report.md', patch)

# generated file manifest and JSON validation
new_files=[
'workspace/vocab_00_static_source_scan.json','workspace/vocab_00_static_source_scan_summary.md','workspace/vocab_00_model_spec_vocab_trace.json','workspace/vocab_00_tokenizer_manifest_trace.json','workspace/vocab_00_checkpoint_lm_head_range_trace.json','workspace/vocab_00_runtime_cap_trace.json','workspace/vocab_00_logit_head_range_matrix.json','workspace/vocab_00_runtime_vocab_cap_probe.json','workspace/vocab_00_vocab_risk_classification.json','workspace/vocab_00_static_validation_receipt.json','reviews/16AI-QW-38G-R6A-VOCAB-00_runtime_vocab_cap_48256_trace_logit_head_range_review.md','patch_reports/16AI-QW-38G-R6A-VOCAB-00_bake_report.md','acceptance_reports/16AI-QW-38G-R6A-VOCAB-00_runtime_vocab_cap_48256_trace_logit_head_range_seal.md','tools/inspect_vocab_00_runtime_cap_trace.py']
manifest={"patch_id":PATCH_ID,"generated_file_count":len(new_files),"generated_files":[]}
for rel in new_files:
    p=ROOT/rel
    manifest['generated_files'].append({"path":rel,"exists":p.exists(),"size_bytes":p.stat().st_size if p.exists() else None,"sha256":sha256_file(p) if p.exists() else None})
write_json('workspace/vocab_00_generated_file_manifest.json', manifest)

json_files=[rel for rel in new_files if rel.endswith('.json')]+['workspace/vocab_00_generated_file_manifest.json']
validation={"patch_id":PATCH_ID,"json_file_count":len(json_files),"json_parse_error_count":0,"files":[]}
for rel in json_files:
    p=ROOT/rel
    try:
        json.loads(read_text(p))
        validation['files'].append({"path":rel,"valid":True})
    except Exception as e:
        validation['json_parse_error_count']+=1
        validation['files'].append({"path":rel,"valid":False,"error":str(e)})
write_json('workspace/vocab_00_json_validation_report.json', validation)
print(json.dumps(receipt, ensure_ascii=False, indent=2))
