Pillar: Book I hit and fixed

# AI Engineering (Chip Huyen) — key takeaways

AI engineering = building applications on top of foundation models. ML engineering develops models; AI engineering adapts and evaluates them.

Two adaptation techniques:
1) Prompt-based — adapt without updating weights (instructions + context only)
2) Fine-tuning — update model weights; more complex, needs more data, but improves quality/latency/cost

Prompt engineering, RAG, and fine-tuning are the three common techniques to adapt foundation models. RAG connects the model to a database (e.g., customer reviews) to supplement instructions.

Evaluation is the biggest problem in AI engineering — open-ended outputs have no ground truth, unlike closed-ended ML tasks. Benchmarks saturate fast (HumanEval, MBPP).

Three layers of the AI stack:
- Application development: AI interface, prompt engineering, context construction, evaluation
- Model development: inference optimization, dataset engineering, modeling and training, evaluation
- Infrastructure: compute management, data management, serving, monitoring

With foundation models, you experiment with different models, prompts, retrieval algorithms, and sampling variables.