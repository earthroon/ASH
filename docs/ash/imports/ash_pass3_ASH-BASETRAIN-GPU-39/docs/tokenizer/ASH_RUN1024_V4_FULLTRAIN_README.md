# Ash Run1024 V4 full-train pack

들어간 파일:
- model_spec_run1024_v4.toml
- backend_spec_full_train.toml
- v4_guarded_dataset_manifest.json
- inspect_run1024_checkpoint.py
- run_base_train_v4_guarded.ps1

## 중요한 점
이 묶음에서 **확정으로 잡힌 값**은 아래뿐입니다.
- vocab_size = 56832
- hidden_size = 1024
- source checkpoint family = run1024
- target task family = guarded_freeform / V4 tokenizer

그 외 `num_layers`, `num_attention_heads`, `num_key_value_heads`, `head_dim`, `intermediate_size`는
현재 대화에서 확보한 증거만으로는 100% 확정할 수 없어서,
**기존 1024-class GQA 계열 + 파일 크기 근사**를 바탕으로 best-effort로 넣었습니다.

## 그래서 권장 순서
1. 먼저 inspect_run1024_checkpoint.py 로 실제 checkpoint 구조를 찍어보기
2. 그 결과와 model_spec_run1024_v4.toml 비교
3. mismatch 없으면 run_base_train_v4_guarded.ps1 실행
4. mismatch가 있으면 model_spec 차원만 수정 후 실행

## inspect 예시
python .\inspect_run1024_checkpoint.py --checkpoint .\workspace\base_train_runs\run1024\full_model.safetensors
