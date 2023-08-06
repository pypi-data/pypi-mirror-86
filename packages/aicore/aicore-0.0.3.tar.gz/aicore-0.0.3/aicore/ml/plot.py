import matplotlib.pyplot as plt
import numpy as np

_COLORS = [
    "#e6194b",
    "#3cb44b",
    "#ffe119",
    "#4363d8",
    "#f58231",
    "#911eb4",
    "#46f0f0",
    "#f032e6",
    "#bcf60c",
    "#fabebe",
    "#008080",
    "#e6beff",
    "#9a6324",
    "#fffac8",
    "#800000",
    "#aaffc3",
    "#808000",
    "#ffd8b1",
    "#000075",
    "#808080",
    "#ffffff",
    "#000000",
]


def feature_label(X_train, y_true, feature, n_samples: int = 20):
    features = X_train[:n_samples, feature]
    labels = y_true[:n_samples]
    plt.figure()
    plt.scatter(features, labels, c="r", label="targets")
    plt.legend()
    plt.xlabel("Feature values")
    plt.ylabel("Target values")
    plt.show()


def show(X, Y, predictions=None):
    for i in range(min(Y), max(Y) + 1):
        y = Y == i
        x = X[y]
        plt.scatter(x[:, 0], x[:, 1], c=_COLORS[i])
        if predictions is not None:
            y = predictions == i
            x = X[y]
            plt.scatter(x[:, 0], x[:, 1], c=_COLORS[i], marker="x", s=100)
    plt.show()


def visualise_predictions(H, X, Y=None, n=50):
    xmin, xmax, ymin, ymax = min(X[:, 0]), max(X[:, 0]), min(X[:, 1]), max(X[:, 1])
    meshgrid = np.zeros((n, n))
    for x1_idx, x1 in enumerate(np.linspace(xmin, xmax, n)):  # for each column
        for x2_idx, x2 in enumerate(np.linspace(ymin, ymax, n)):  # for each row
            h = H(np.array([[x1, x2]]))[0]
            meshgrid[
                n - 1 - x2_idx, x1_idx
            ] = h  # axis 0 is the vertical direction starting from the top and increasing downward
    if Y is not None:
        for idx in list(set(Y)):
            plt.scatter(X[Y == idx][:, 0], X[Y == idx][:, 1], c=_COLORS[idx])
    else:
        plt.scatter(X[:, 0], X[:, 1])
    plt.imshow(meshgrid, extent=(xmin, xmax, ymin, ymax), cmap="winter")
    plt.show()


def visualise_regression_data(X, Y, H=None):
    ordered_idxs = np.argsort(X, axis=0)
    X = X[ordered_idxs]
    Y = Y[ordered_idxs]
    plt.figure()
    plt.scatter(X, Y, c="r", label="Label")
    if H is not None:
        domain = np.linspace(np.min(X.squeeze()), np.max(X.squeeze()))
        domain = np.expand_dims(domain, axis=1)
        y_hat = H(domain)
        plt.plot(domain, y_hat, label="Hypothesis")
    plt.legend()
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()


def regression(X, Y):
    plt.figure()
    plt.scatter(X, Y, c="r")
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.show()
