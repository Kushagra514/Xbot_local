Pillar: Concept via analogy

# Hallucinations, robustness, and mitigation

Hallucination = model gives a response not grounded in facts. Two hypotheses:

1) Model can't differentiate between given data and generated data — conditions later responses on factually wrong info ("snowballing hallucinations"). Mitigate via RL (differentiate user prompts from generated tokens) or supervised learning (include factual and counterfactual signals in training data).

2) Mismatch between model's internal knowledge and labeler's internal knowledge. Mitigate by asking the model to use its own knowledge, verify sources, or use a better reward function that punishes hallucination more.

Hallucination is worse for models using both RLHF and SFT vs. SFT alone.

Robustness = model doesn't dramatically change outputs with small input variations. Less robust models benefit more from sampling multiple outputs.

Without quality control of AI outputs, the risk of AI might outweigh its benefits.