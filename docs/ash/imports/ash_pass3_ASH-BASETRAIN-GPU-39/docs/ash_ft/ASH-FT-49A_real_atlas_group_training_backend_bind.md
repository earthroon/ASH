# ASH-FT-49A

This patch binds the real native training backend for atlas-group sequential fine-tuning. It does not accept synthetic smoke, mock backend, or receipt-only forward/backward evidence. The backend manifest must expose an executable command; the runner invokes it with the selected group, microbatch, model manifest, safetensors manifest, and loss contract paths.

The command must return JSON proving `real_forward_executed`, `loss_finite`, `real_backward_executed`, `selected_group_gradient_present`, `gradient_finite`, and non-empty `gradient_tensor_sources`.
