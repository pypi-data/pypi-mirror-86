"""Mathematical operations usable with graph and backpropagation.

Each function (lowercase) has it's corresponding class which can handle
backpropagation. This approach allows us to simply use ops like this:

    from coreai.supervised import graph as g

    g.mean(np.array([1, 2, 3, 4, 5]))
    g.get().backward()


"""

import abc

import numpy as np

from ._graph import get, has_grad
from ._parameter import Parameter


class Operation(abc.ABC):
    """Base class of mathematical operation to be run on Parameter/np.array

    Attributes:
        cache (Optional[np.array])
            Cache attribute one can use to save anything during forward pass
            to reuse in backward
        index_in_graph (int):
            Index of operation in graph's operation dictionary
        is_leaf (bool):
            Always `False`, used by graph to easily discern between parameters
            and operations.
    """

    def __init__(self):
        self.cache = None
        self.index_in_graph = None
        self.is_leaf = False

    def __call__(self, *arguments):
        """Run forward and register operation in graph.

        Additionally operation's inputs will be registered using mapping and
        whether those are leafs (parameters) or operations to be further
        backpropagated.

        """
        if has_grad():
            mapping = {}
            add_to_graph = False
            for input_index, argument in enumerate(arguments):
                if isinstance(argument, Parameter):
                    add_to_graph = True
                    is_first_operation = argument.last_operation_index is None
                    if is_first_operation:
                        mapping[input_index] = (argument.index_in_graph, True)
                    else:
                        mapping[input_index] = (argument.last_operation_index, False)

            if add_to_graph:
                self.index_in_graph = get()._register_operation(self, mapping)
                for argument in arguments:
                    if isinstance(argument, Parameter):
                        argument.last_operation_index = self.index_in_graph

        # Pack return value in tuple always
        return self.forward(*arguments)

    @abc.abstractmethod
    def forward(self, *_):
        """Define your forward pass here.

        Use self.cache to cache anything needed during backpropagation.

        """
        pass

    @abc.abstractmethod
    def backward(self, upstream_gradient):
        """Define your backward pass here.

        Use self.cache in order to calculate gradient. There has to be as
        many outputs as there was inputs to forward.

        """
        pass


###############################################################################
#
#                           BASIC MATH OPERATIONS
#
###############################################################################


class _Add(Operation):
    def forward(self, a, b):
        return a + b

    def backward(self, upstream_gradient):
        return upstream_gradient, upstream_gradient


def add(a, b):
    return _Add()(a, b)


class _Mean(Operation):
    def __init__(self, axis: int = None):
        super().__init__()
        self.axis = axis

    def forward(self, inputs):
        mean = np.mean(inputs, axis=self.axis)
        self.cache = np.ones_like(inputs) / inputs.size
        return mean

    def backward(self, upstream_gradient):
        grad = upstream_gradient * self.cache
        return grad


def mean(inputs, axis: int = None):
    return _Mean(axis)(inputs)


class _Dot(Operation):
    def forward(self, a, b):
        self.cache = (a, b)
        return a @ b

    # Needs automatic reshape in order to work
    def backward(self, upstream_gradient):
        a = np.dot(upstream_gradient.reshape(-1, 1), self.cache[1].reshape(1, -1))
        b = np.dot(self.cache[0].T, upstream_gradient)
        return a, b


def dot(a, b):
    return _Dot()(a, b)


###############################################################################
#
#                       ACTIVATIONS & ADVANCED MATH
#
###############################################################################


def _negative_sigmoid(inputs):
    # Second formula for negative values
    # Cache exp so you won't have to calculate it twice
    exp = np.exp(inputs)
    return exp / (exp + 1)


def _positive_sigmoid(inputs):
    # First formula for positive values
    return 1 / (1 + np.exp(-inputs))


def sigmoid(inputs):
    positive = inputs >= 0
    # Boolean array inversion is faster than another comparison
    negative = ~positive

    # empty contains junk hence will be faster to allocate than zeros
    result = np.empty_like(inputs)
    result[positive] = _positive_sigmoid(inputs[positive])
    result[negative] = _negative_sigmoid(inputs[negative])
    return result


# That's how derivative of sigmoid goes
# class Sigmoid(Operation):
#     @classmethod
#     def forward(self, inputs):
#         result = _sigmoid(inputs)
#         self.cache = result
#         return self.cache

#     def backward(self, derivatives, inputs):
#         return derivatives * self.cache * (1 - self.cache)


def softmax(logits):
    exps = np.exp(logits - np.max(logits, axis=1).reshape(-1, 1))
    return exps / np.sum(exps, axis=1).reshape(-1, 1)


###############################################################################
#
#                               LOSS FUNCTIONS
#
###############################################################################


class _SquaredError(Operation):
    def forward(self, logits, targets):
        self.cache = logits - targets
        return self.cache ** 2

    def backward(self, upstream_gradient):
        gradient = 2 * self.cache * upstream_gradient
        return gradient, -gradient


def squared_error(a, b):
    return _SquaredError()(a, b)


###############################################################################
#
#                           BINARY CROSS ENTROPY
#
###############################################################################


class _BCEWithLogits(Operation):
    def forward(self, logits, targets):
        self.cache = (logits, targets)
        return (
            np.maximum(np.zeros_like(logits), logits)
            - logits * targets
            + np.log(1 + np.exp(-np.abs(logits)))
        )

    def backward(self, upstream_gradient):
        return sigmoid(self.cache[0]) - self.cache[1], -self.cache[0]


def bce_with_logits(logits, targets):
    return _BCEWithLogits()(logits, targets)


###############################################################################
#
#                           MULTICLASS CROSS ENTROPY
#
###############################################################################


def to_one_hot(labels, max_labels: int = None):
    if max_labels is None:
        max_labels = np.max(labels) + 1
    return np.eye(max_labels)[labels]


def to_labels(one_hot):
    return np.argmax(one_hot, axis=-1)


class _CrossEntropyWithLogits(Operation):
    def forward(self, logits, targets):
        softmaxed = softmax(logits) + 1e-100
        one_hot = to_one_hot(targets)
        self.cache = (softmaxed, one_hot)
        return -np.sum(one_hot * np.log(softmaxed), axis=1)

    def backward(self, upstream_gradient):
        expanded_output = upstream_gradient.reshape(-1, 1)
        return (
            -expanded_output * np.log(self.cache[0]),
            expanded_output
            * (
                self.cache[0] * np.expand_dims(np.sum(self.cache[1], axis=1), axis=1)
                - self.cache[1]
            ),
        )


def ce_with_logits(logits, targets):
    return _CrossEntropyWithLogits()(logits, targets)
