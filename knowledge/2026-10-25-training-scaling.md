Pillar: Build log

# Training, fine-tuning, and scaling laws

Pre-training = training from scratch with randomly initialized weights. Most resource-intensive; small mistakes incur large costs. Fine-tuning = continuing to train a previously trained model — fewer resources, done by application developers. Post-training = fine-tuning done by model developers; goal is to align with human preferences.

SFT (supervised fine-tuning) = fine-tune on high-quality instruction data to optimize for conversations. Preference fine-tuning = align with human preferences via RLHF (train reward model on good/bad response pairs, then optimize the model to maximize reward scores).

Self-supervision = model generates its own labels from input data. Language modeling is self-supervised because each input sequence provides both label and context ("I love street food" = 6 training examples).

Model size = number of parameters. Generally, more parameters = greater capacity, but need more training data to maximize performance. Given a compute budget, Chinchilla law says tokens ≈ 20x model size.

Inverse scaling checks if bigger models can actually perform worse. Hyperparameter transferring predicts best hyperparameters for large models by studying smaller ones.