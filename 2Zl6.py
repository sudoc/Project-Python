import numpy as np
import matplotlib.pyplot as plt


def Kwadratowa():
    max_iteration = 10000
    iter = 0
    eta = 0.001

    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    class Neural_Network:
        def __init__(self):
            self.input = 1
            self.output = 1
            self.layers = 5
            self.create_weights_and_biases()

        def create_weights_and_biases(self):
            self.w1 = np.random.randn(self.input, self.layers)
            self.b1 = np.zeros(self.layers) + 0.25
            self.w2 = np.random.randn(self.layers, self.layers)
            self.b2 = np.zeros(self.output) + 0.01

        def feedforward(self, X):
            self.z2 = np.dot(X, self.w1) + self.b1
            self.a2 = sigmoid(self.z2)
            self.z3 = np.dot(self.a2, self.w2) + self.b2
            sig = sigmoid(self.z3)
            return sig

        def costfuction(self, X, y):
            self.sig = self.feedforward(X)
            C = 0.5 * sum((y - self.sig) ** 2)
            return C

        def sigmoidPrime(self, z):
            return np.exp(-z) / ((1 + np.exp(-z)) ** 2)

        def backpropagation(self, X, y):
            self.sig = self.feedforward(X)
            delta3 = np.multiply(-(y - self.sig), self.sigmoidPrime(self.z3))
            dCdw2 = np.dot(self.a2.T, delta3)
            dCdb2 = np.sum(delta3)
            delta2 = np.dot(delta3, self.w2.T) * self.sigmoidPrime(self.z2)
            dCdw1 = np.dot(X.T, delta2)
            dCdb1 = np.sum(delta2)
            return dCdw1, dCdw2, dCdb1, dCdb2

    np.random.seed()
    X = np.linspace(0, 3, 101).reshape(101, 1)

    # Kwadratowa
    x = np.linspace(-50, 50, 101)
    y = x ** 2

    plt.plot(y)
    plt.show()
    print(X.shape)
    print(y.shape)

    NN = Neural_Network()
    while iter < max_iteration:

        dCdw1, dCdw2, dCdb1, dCdb2 = NN.backpropagation(X, y)

        NN.w1 = NN.w1 - eta * dCdw1
        NN.w2 = NN.w2 - eta * dCdw2
        NN.b1 = NN.b1 - eta * dCdb1
        NN.b2 = NN.b2 - eta * dCdb2
        iter = iter + 1

    NN = Neural_Network()
    plt.plot(NN.feedforward(X))
    plt.show()


def Sinus():
    Fs = 301
    f = 5
    sample = 161
    max_iteration = 10000
    iter = 0
    eta = 0.001
    def sigmoid(z):
        return 1 / (1 + np.exp(-z))

    class Neural_Network:
        def __init__(self):
            self.input = 1
            self.output = 1
            self.layers = 5
            self.create_weights_and_biases()

        def create_weights_and_biases(self):
            self.w1 = np.random.randn(self.input, self.layers)
            self.b1 = np.zeros(self.layers) + 0.25
            self.w2 = np.random.randn(self.layers, self.layers)
            self.b2 = np.zeros(self.output) + 0.01

        def feedforward(self, X):
            self.z2 = np.dot(X, self.w1) + self.b1
            self.a2 = sigmoid(self.z2)
            self.z3 = np.dot(self.a2, self.w2) + self.b2
            sig = sigmoid(self.z3)
            return sig

        def costfuction(self, X, y):
            self.sig = self.feedforward(X)
            C = 0.5 * sum((y - self.sig) ** 2)
            return C

        def sigmoidPrime(self, z):
            return np.exp(-z) / ((1 + np.exp(-z)) ** 2)

        def backpropagation(self, X, y):
            self.sig = self.feedforward(X)
            delta3 = np.multiply(-(y - self.sig), self.sigmoidPrime(self.z3))
            dCdw2 = np.dot(self.a2.T, delta3)
            dCdb2 = np.sum(delta3)
            delta2 = np.dot(delta3, self.w2.T) * self.sigmoidPrime(self.z2)
            dCdw1 = np.dot(X.T, delta2)
            dCdb1 = np.sum(delta2)
            return dCdw1, dCdw2, dCdb1, dCdb2

    np.random.seed()
    X = np.linspace(0, 3, 161).reshape(161, 1)

    # Sinus
    x = np.arange(sample)
    y = np.sin(2 * np.pi * f * x / Fs).reshape(161, 1)
    plt.plot(y)
    plt.show()
    print(X.shape)
    print(y.shape)

    NN = Neural_Network()

    while iter < max_iteration:

        dCdw1, dCdw2, dCdb1, dCdb2 = NN.backpropagation(X, y)

        NN.w1 = NN.w1 - eta * dCdw1
        NN.w2 = NN.w2 - eta * dCdw2
        NN.b1 = NN.b1 - eta * dCdb1
        NN.b2 = NN.b2 - eta * dCdb2

        if iter % 1 == 0:
            print(NN.costfuction(X, y))

        iter = iter + 1

    NN = Neural_Network()
    plt.plot(NN.feedforward(X))
    plt.show()


x = input("K - Kwadratowa, S - Sinus")
if x == 'K':
    Kwadratowa()
elif x == 'S':
    Sinus()
else:
    print("Nie ma takiej opcji")
