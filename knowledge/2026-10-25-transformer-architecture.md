Pillar: Concept via analogy

# Transformer architecture under the hood

At the heart of the transformer is the attention mechanism, leveraging query (Q), key (K), and value (V) vectors. Attention computes how much to attend to each input token via dot product between Q and K. Each previous token has corresponding K and V vectors — longer sequences mean more K/V vectors to compute and store.

Attention is almost always multi-headed — multiple heads attend to different groups of tokens simultaneously. Each transformer block contains an attention module and an MLP module. The attention module has four weight matrices: Q, K, V, and output projection. The MLP has linear layers separated by nonlinear activations.

Number of transformer blocks = number of layers. Two modules sit before/after: the embedding module (embedding matrix + positional embedding matrix) and the output module (unembedding layer / model head) converting output vectors to token probabilities.

Increased context length impacts memory footprint but not total parameter count.

Alternatives to transformers: RWKV (RNN-based, parallelized for training), SSMs (promising for long-range memory).