Pillar: Day N/100

# Sampling techniques: temperature, top-K, top-p

Sampling is how a model chooses an output from all possible options — an underrated concept that explains hallucinations and inconsistencies.

Greedy sampling = pick the token with the highest probability (can make outputs boring).

Temperature redistributes probabilities before softmax. Temp 0 = always pick the largest logit. Temp 0.7 = recommended for creative use cases (balances creativity and predictability). Higher temps reduce common-token probabilities, increase rarer-token probabilities.

Top-K = pick only the top-k logits, perform softmax over those. Smaller k = more predictable, less interesting.

Top-P = consider the smallest set of values whose cumulative probability exceeds p (e.g., 0.9 = 90%). Top-P doesn't necessarily reduce softmax computation load.

Test-time compute = generate multiple responses to increase chances of a good one. Works best for models that are already pretty good at the task and just need nudging.