Pillar: Concept via analogy

# How neural networks learn (MNIST, gradient descent, backprop)

A neural network is a parameterized function. Training repeatedly evaluates that function on examples, measures the error using a loss function, computes how each parameter contributed to that error using backpropagation, and updates the parameters using gradient descent.

Concrete example: MNIST digit classification. Each 28x28 image becomes pixels, flows through layers sequentially, maps to 10 outputs (digits 0-9). Starts with random weights = trash output. The cost function (sum of squared differences averaged) gives a single number — the gradient — that nudges weights and biases toward the ideal output. Repeat across many images, average gradients, and the weights learn patterns that generalize to the test set.

Key insight: A neural network learns by repeatedly making predictions and adjusting itself based on how wrong it was. The weights that contribute most to the error get adjusted most — "most buck for the job."

Reference: 3Blue1Brown Deep Learning Lecture 4 for an intuitive guide.