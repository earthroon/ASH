#!/usr/bin/env python3
from __future__ import annotations
import json, pathlib, shutil, subprocess, datetime, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
WORKSPACE = ROOT / 'workspace'
WORKSPACE.mkdir(exist_ok=True)
PATCH_ID = '16AI-QW-38G-R6A-BUILD-00-RERUN'
COMMANDS = {
    'cargo_metadata': ['cargo','metadata','--format-version','1'],
    'cargo_check_workspace_all_targets': ['cargo','check','--workspace','--all-targets'],
    'cargo_test_workspace_no_run': ['cargo','test','--workspace','--no-run'],
    'cargo_fmt_all_check': ['cargo','fmt','--all','--','--check'],
}
def run(name, cmd):
    out = WORKSPACE / f'build_00_rerun_{name}_stdout.log'
    err = WORKSPACE / f'build_00_rerun_{name}_stderr.log'
    if shutil.which(cmd[0]) is None:
        out.write_text('', encoding='utf-8')
        err.write_text(f'{cmd[0]}: command not found\n', encoding='utf-8')
        return {'executed': False, 'exit_code': None, 'reason': f'{cmd[0]}_not_found', 'stdout_log': str(out), 'stderr_log': str(err), 'cmd': cmd}
    p = subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out.write_text(p.stdout, encoding='utf-8')
    err.write_text(p.stderr, encoding='utf-8')
    return {'executed': True, 'exit_code': p.returncode, 'reason': None if p.returncode == 0 else 'nonzero_exit', 'stdout_log': str(out), 'stderr_log': str(err), 'cmd': cmd}
results = {name: run(name, cmd) for name, cmd in COMMANDS.items()}
status = 'PASS' if all(r['executed'] and r['exit_code'] == 0 for r in results.values()) else 'FAIL_OR_BLOCKED'
receipt = {
  'patch_id': PATCH_ID,
  'domain_ssot': 'en_to_ko_translation_subtitle_machine',
  'generated_at_utc': datetime.datetime.utcnow().replace(microsecond=0).isoformat() + 'Z',
  'cargo_available': shutil.which('cargo') is not None,
  'rustc_available': shutil.which('rustc') is not None,
  'commands': results,
  'build_readiness_status': status,
  'runtime_decode_executed': False,
  'model_forward_executed': False,
  'sampling_executed': False,
  'subtitle_export_executed': False
}
(WORKSPACE / 'build_00_rerun_static_build_receipt.json').write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(receipt, ensure_ascii=False, indent=2))
sys.exit(0 if status == 'PASS' else 1)
