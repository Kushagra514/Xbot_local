Pillar: Bug I hit and fixed

# Evaluation and benchmarks for LLMs

Perplexity = exponential of cross-entropy, measures uncertainty when predicting the next token. Perplexity of 3 = 1 in 3 chance of predicting the next token correctly. Good proxy for capabilities, but not great for post-trained models (SFT/RLHF can improve task performance while hurting next-token prediction).

Cross-entropy, perplexity, BPC (bits per character), BPB (bits per byte) are variations of predictive accuracy measurement.

Structured data → lower expected perplexity. Bigger vocabulary → higher perplexity. Longer context → lower perplexity.

Pass@k = fraction of problems solved when any of k code samples passes all test cases. Used in HumanEval (OpenAI) and MBPP (Google) for code generation evaluation.

Open-ended outputs are harder to evaluate than closed-ended tasks — no ground truth to compare against. "AI as a judge" (using AI to evaluate AI responses) is a rising but subjective approach.