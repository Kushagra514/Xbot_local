Pillar: Build log

# Quantizing qwen3.5:4b to Q4_K_M

Ran `ollama pull qwen3.5:4b-q4_K_M` — 3.3 GB, fits the 6 GB RTX 3050 with room for the context window.

The trade-off: Q4 quantizes each 4-bit block with a shared scale. Slight perplexity bump, big memory saving. On this laptop it runs at a usable tokens/sec for drafting tweets.

NUM_CTX=8192 keeps the full draft+critique prompt in context without truncation.
