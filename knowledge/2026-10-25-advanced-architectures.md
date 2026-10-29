Pillar: Paper in 5 tweets

# Advanced model architectures: MoE, RoPE, ALiBi, GQA, MLA

MoE (Mixture of Experts) is a sparse model — only 2 experts active at a time. A 56B-param MoE model takes the compute of a 14B-parameter model. Sparsity enables efficient storage and computation.

RoPE (Rotary Positional Embeddings) and ALiBi are positional encoding approaches for transformers. GQA (Grouped Query Attention) and MLA (Multi-head Latent Attention) are attention optimizations that reduce KV cache memory during inference.

Inference optimization techniques: KV cache, PagedAttention, quantization, distillation, parallelism.

FLOP = floating point operation, a standardized unit for compute requirement. Three numbers signal model scale: parameters (learning capacity), tokens trained on, FLOPs (proxy for training cost).

Chinchilla scaling law: for compute-optimal training, training tokens should be approximately 20x the model size.