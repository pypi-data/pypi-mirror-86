import numpy as np

from ._graph import get, no_grad
from ._operations import (add, bce_with_logits, ce_with_logits, dot, mean,
                          sigmoid, softmax, squared_error)
from ._parameter import Parameter


class LinearRegression:
    def __init__(self, n_features, optimizer):
        self.W = Parameter(np.random.randn(n_features))
        self.b = Parameter(np.random.randn(1))
        self.optimizer = optimizer

    def parameters(self):
        return self.W, self.b

    def predict(self, X):
        return add(dot(X, self.W), self.b)

    def fit(self, X, y_true, epochs: int = 10):
        for _ in range(epochs):
            y_pred = self.predict(X)
            # loss is our final node
            mean(squared_error(y_pred, y_true))
            get().backward()
            self.optimizer(self.parameters())


class BinaryLogisticRegression:
    def __init__(self, n_features, optimizer):
        self.W = Parameter(np.random.randn(n_features))
        self.b = Parameter(np.random.randn(1))
        self.optimizer = optimizer

    def parameters(self):
        return self.W, self.b

    def predict_logits(self, X):
        return add(dot(X, self.W), self.b)

    def predict_proba(self, X):
        with no_grad():
            return sigmoid(self.predict_logits(X))

    def predict(self, X):
        with no_grad():
            return self.predict_logits(X) > 0

    def fit(self, X, y_true, epochs: int = 10):
        for _ in range(epochs):
            y_pred = self.predict_logits(X)
            # loss is our final node
            mean(bce_with_logits(y_pred, y_true))
            get().backward()
            self.optimizer(self.parameters())


class MulticlassLogisticRegression:
    def __init__(self, n_classes, n_features, optimizer):
        self.W = Parameter(np.random.randn(n_features, n_classes))
        self.b = Parameter(np.random.randn(n_classes))
        self.optimizer = optimizer

    def parameters(self):
        return self.W, self.b

    def predict_logits(self, X):
        return add(dot(X, self.W), self.b)

    def predict_proba(self, X):
        with no_grad():
            return softmax(self.predict_logits(X))

    def predict(self, X):
        with no_grad():
            return self.predict_logits(X) > 0

    def fit(self, X, y_true, epochs: int = 10):
        for _ in range(epochs):
            y_pred = self.predict_logits(X)
            # loss is our final node
            mean(ce_with_logits(y_pred, y_true))
            get().backward()
            self.optimizer(self.parameters())
