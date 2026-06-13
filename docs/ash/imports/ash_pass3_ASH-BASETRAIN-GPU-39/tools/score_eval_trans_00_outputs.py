#!/usr/bin/env python3
"""EVAL-TRANS-00 scoring scaffold.

Scores automatic surface flags only when model outputs exist. It does not assign
manual adequacy/fluency/tone scores without human review.
"""
from __future__ import annotations
import argparse, json, re
from pathlib import Path

PATCH_ID = "16AI-QW-38G-R6A-EVAL-TRANS-00"

def read_jsonl(path: Path):
    if not path.exists(): return []
    rows=[]
    for line in path.open('r', encoding='utf-8'):
        if line.strip(): rows.append(json.loads(line))
    return rows

def has_repetition(text: str) -> bool:
    toks = re.findall(r'[A-Za-z가-힣]+|[!?.,]+', text)
    for a,b,c in zip(toks, toks[1:], toks[2:]):
        if a == b == c: return True
    return bool(re.search(r'([가-힣A-Za-z!?.,])\1{5,}', text))

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--eval', default='eval/eval_trans_00/en_ko_subtitle_actual_eval_138.jsonl')
    ap.add_argument('--outputs', default='workspace/eval_trans_00_model_outputs.jsonl')
    ap.add_argument('--scan', default='workspace/eval_trans_00_auto_quality_scan.json')
    ap.add_argument('--scores', default='workspace/eval_trans_00_quality_scores.json')
    args=ap.parse_args()
    eval_rows=read_jsonl(Path(args.eval))
    output_rows=read_jsonl(Path(args.outputs))
    out_by_id={r.get('case_id'): r for r in output_rows}
    scan_cases=[]
    flags={
        'empty_output_count':0,
        'untranslated_source_count':0,
        'word_salad_count':0,
        'control_token_leak_count':0,
        'number_mismatch_count':0,
        'proper_noun_mismatch_count':0,
        'needs_manual_review_count': len(eval_rows),
    }
    for c in eval_rows:
        out=out_by_id.get(c['case_id'], {})
        text=out.get('model_output','') or ''
        row={'case_id':c['case_id'],'category':c['category'],'has_output':bool(text)}
        if not text: flags['empty_output_count'] += 1
        if text and c['source_text'].lower() in text.lower(): flags['untranslated_source_count'] += 1; row['untranslated_source']=True
        if has_repetition(text): flags['word_salad_count'] += 1; row['word_salad_or_repetition']=True
        if any(tok in text for tok in ['<eos>','<bos>','<pad>','<|endoftext|>','[INST]']): flags['control_token_leak_count'] += 1; row['control_token_leak']=True
        scan_cases.append(row)
    scan={'patch_id':PATCH_ID,'eval_case_count':len(eval_rows),'model_output_case_count':len(output_rows),'auto_flags':flags,'cases':scan_cases}
    Path(args.scan).write_text(json.dumps(scan, ensure_ascii=False, indent=2), encoding='utf-8')
    quality={
        'patch_id':PATCH_ID,
        'case_count':len(eval_rows),
        'model_outputs_generated': len(output_rows)==len(eval_rows) and len(eval_rows)>0,
        'scored_case_count':0,
        'manual_scores_completed':False,
        'average_scores':{
            'adequacy': None,
            'fluency': None,
            'subtitle_fit': None,
            'tone_register': None,
            'compression': None,
            'terminology': None,
            'context_use': None,
            'linebreak_handling': None
        },
        'flags': flags,
        'quality_tier':'UNSCORED_OR_UNKNOWN',
        'false_translation_quality_claim': False
    }
    Path(args.scores).write_text(json.dumps(quality, ensure_ascii=False, indent=2), encoding='utf-8')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
