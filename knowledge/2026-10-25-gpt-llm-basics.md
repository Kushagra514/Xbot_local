Pillar: Day N/100

# GPT and LLMs: next-token prediction explained

GPT (Generative Pretrained Transformer) and other LLMs do one thing while conversing: predict the next most probable word, then feed the sentence back in to predict the next word, and so on.

Tokens are small chunks of text (or pixels, or voice snippets), stored as vectors placed closer together if semantically similar (leap, jump, hop).

After tokenization and embedding, the attention layer modifies word meaning based on context. Example: "a fashion model" vs "a machine learning model" — attention lets tokens interact to get high-level contextual meaning.

After attention comes the MLP (multi-layer perceptron / feedforward network) — essentially a long list of questions and matrix multiplications. Attention + MLP repeat over multiple layers to produce a final probability for the next word.

Context window = how much data you can input so the model sets up congruency with previous responses. Softmax normalizes logits into probabilities. Temperature controls randomness: temp 0 = always pick the most predictable word; higher temps give lesser-probability tokens a chance.

Decoder-only transformers use causal (left-to-right) attention — best for text generation and chat (GPT, BERT, RoBERTa). Encoder-only uses bidirectional attention — excels at classification, NER, embeddings.