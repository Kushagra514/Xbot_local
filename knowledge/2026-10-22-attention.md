Pillar: Concept via analogy

# Attention as a lookup table

Think of self-attention as a differentiable lookup table.

Query = what you're looking for. Key = how each item is indexed. Value = the content you retrieve.

Attention weights = softmax(query · keys) tell you how much to pull from each value. The output is a weighted sum of values.

Where the analogy breaks: a real lookup table returns one exact match; attention returns a blend of everything, weighted by relevance. That blend is both the feature and the bug.
