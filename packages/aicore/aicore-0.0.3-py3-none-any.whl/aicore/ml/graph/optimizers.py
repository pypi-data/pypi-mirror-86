"""Module with optimizers written from scratch working on `np.array`-like Parameters.

Each new optimizer should inherit from Optimizer base class.

"""

import abc
import collections

import numpy as np


class Optimizer(abc.ABC):
    """Base optimizer class.

    Defines `__call__` which iterates over provided parameters and clears
    their gradients afterwards.

    """

    def __call__(self, parameters):
        if isinstance(parameters, collections.abc.Iterable):
            parameters = parameters
        else:
            parameters = (parameters,)
        for parameter in parameters:
            self.forward(parameter)
            parameter.gradient = None

    @abc.abstractmethod
    def forward(self, parameter):
        pass


class SGD(Optimizer):
    """Stochastic Gradient Descent"""

    # lr is common abbreviation for learning rate
    def __init__(self, lr: float = 3e-4):
        self.lr = lr

    def forward(self, parameter):
        parameter -= self.lr * parameter.gradient


class SGDL2(Optimizer):
    """Stochastic Gradient Descent"""

    # lr is common abbreviation for learning rate
    def __init__(self, lr: float = 3e-4, decay: float = 1e-5):
        self.lr = lr
        self.decay = decay

    def forward(self, parameter):
        parameter.gradient += self.decay * parameter
        parameter -= self.lr * parameter.gradient


class SGDL1(Optimizer):
    """Stochastic Gradient Descent"""

    # lr is common abbreviation for learning rate
    def __init__(self, lr: float = 3e-4, decay: float = 1e-5):
        self.lr = lr
        self.decay = decay

    def forward(self, parameter):
        parameter.gradient += self.decay * np.sign(parameter)
        parameter -= self.lr * parameter.gradient
