#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def read_json(path: Path):
    with path.open('r', encoding='utf-8') as f:
        return json.load(f)


def write_json(path: Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--input', required=True)
    ap.add_argument('--output-dir', required=True)
    ap.add_argument('--wrong-out-dim', type=int, default=48259)
    args = ap.parse_args()

    src = Path(args.input)
    out_dir = Path(args.output_dir)
    base = read_json(src)
    stem = src.stem

    cases = []

    classifier = dict(base)
    classifier['artifact_family'] = 'shared_hidden_token_adapter'
    classifier['target_key'] = 'classifier.shared_hidden_token_head'
    classifier_path = out_dir / f'{stem}.classifier_family.adapter.json'
    write_json(classifier_path, classifier)
    cases.append({'case_name': 'classifier_family', 'path': str(classifier_path)})

    legacy = dict(base)
    legacy.pop('artifact_family', None)
    legacy_path = out_dir / f'{stem}.legacy_unknown.adapter.json'
    write_json(legacy_path, legacy)
    cases.append({'case_name': 'legacy_unknown', 'path': str(legacy_path)})

    wrong_dim = dict(base)
    wrong_dim['artifact_family'] = 'module_lora'
    wrong_dim['out_dim'] = int(args.wrong_out_dim)
    wrong_dim_path = out_dir / f'{stem}.wrong_dim.adapter.json'
    write_json(wrong_dim_path, wrong_dim)
    cases.append({'case_name': 'wrong_dim', 'path': str(wrong_dim_path)})

    wrong_target = dict(base)
    wrong_target['artifact_family'] = 'module_lora'
    wrong_target['target_key'] = 'classifier.shared_hidden_token_head'
    wrong_target_path = out_dir / f'{stem}.wrong_target_family.adapter.json'
    write_json(wrong_target_path, wrong_target)
    cases.append({'case_name': 'wrong_target_family', 'path': str(wrong_target_path)})

    manifest = {
        'input': str(src),
        'generated_cases': cases,
        'generated_case_paths': [case['path'] for case in cases],
    }
    manifest_path = out_dir / f'{stem}.negative_suite_manifest.json'
    write_json(manifest_path, manifest)
    print(manifest_path)


if __name__ == '__main__':
    main()
