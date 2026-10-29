Pillar: Build log

# Inference optimization: KV cache, PagedAttention, quantization

Inference optimization = making models faster and cheaper. Techniques include quantization, distillation, and parallelism.

Quantization reduces the precision of model weights — technically changes weights but is not considered training.

KV cache stores key and value vectors during inference so they don't need recomputation. PagedAttention manages KV cache memory more efficiently (like virtual memory for attention).

Two-step transformer inference:
1. Prefill — model processes input tokens in parallel, creates intermediate state for the first output token
2. Decode — model generates one output token at a time (sequential output bottleneck remains)

Latency metrics: TTFT (time to first token), TPOT (time per output token).