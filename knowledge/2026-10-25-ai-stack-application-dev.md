Pillar: Build log

# AI stack and application development layers

Three layers of the AI stack:

Application development: AI interface, prompt engineering, context construction, evaluation
Model development: inference optimization, dataset engineering, modeling and training, evaluation  
Infrastructure: compute management, data management, serving, monitoring

Structured output approaches (for tasks used by downstream apps — text-to-SQL, semantic parsing, API querying):
- Prompting — ask for format, depends on instruction-following; can use AI to validate (extra tokens)
- Post-processing — simple and cheap; models repeat the same mistakes, find common ones
- Constrained sampling — guide generation toward constraints (JSON, YAML, regex); each format needs its own grammar
- Finetuning — most effective and general approach for structured outputs

LLMs as parameterized functions trained on Common Crawl / Colossal Clean Crawled Corpus. Quantity, quality, and diversity are the three golden goals for training data. Smaller high-quality data can outperform larger low-quality data.