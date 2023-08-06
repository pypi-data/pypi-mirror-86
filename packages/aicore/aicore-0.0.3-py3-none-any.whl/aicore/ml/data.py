import matplotlib.pyplot as plt
import numpy as np
from sklearn import datasets, model_selection, preprocessing

###############################################################################
#
#                        SKLEARN STANDARDIZATION
#
###############################################################################


def standard_scaler(*datasets):
    scaler = preprocessing.StandardScaler().fit(datasets[0])
    return [scaler.transform(dataset) for dataset in datasets]


def polynomial_datasets(degree: int, *datasets):
    polynomial = preprocessing.PolynomialFeatures(degree=degree)
    return [polynomial.fit_transform(dataset) for dataset in datasets]


###############################################################################
#
#                           STANDARDIZE DATA
#
###############################################################################


def standardize(dataset, mean=None, std=None):
    if mean is None and std is None:
        mean, std = np.mean(dataset, axis=0), np.std(
            dataset, axis=0
        )  # get mean and standard deviation of dataset
    standardized_dataset = (dataset - mean) / std
    return standardized_dataset, (mean, std)


def standardize_multiple(*datasets):
    mean, std = None, None
    for dataset in datasets:
        dataset, (mean, std) = standardize(dataset, mean, std)
        yield dataset


###############################################################################
#
#                               BATCHING
#
###############################################################################


class DataLoader:
    def __init__(self, *datasets, batch_size: int):
        self.datasets = datasets
        self.batch_size = batch_size

    def __iter__(self):
        permutation = np.random.permutation(self.datasets[0].shape[0])
        # Use permutation to shuffle every dataset
        self.datasets = [dataset[permutation] for dataset in self.datasets]
        # Yield batches
        for i in range(len(self.datasets[0]) // self.batch_size):
            yield [
                dataset[i * self.batch_size : (i + 1) * self.batch_size]
                for dataset in self.datasets
            ]


###############################################################################
#
#                           LOAD DATA SPLITTED
#
###############################################################################


def split(dataset, non_train: float = 0.4):
    X, y = dataset
    X_train, X_test, y_train, y_test = model_selection.train_test_split(
        X, y, test_size=non_train
    )

    X_validation, X_test, y_validation, y_test = model_selection.train_test_split(
        X_test, y_test, test_size=0.5
    )
    return (X_train, y_train), (X_validation, y_validation), (X_test, y_test)


###############################################################################
#
#                       PREVIOUS COURSE ITERATION
#
###############################################################################


def classification(
    sd=3, m=10, n_features=2, n_clusters=2, variant="blobs", noise=0.4, factor=0.1
):
    if variant == "circles":
        return datasets.make_circles(n_samples=m, factor=factor, noise=noise)
    if variant == "blobs":
        return datasets.make_blobs(
            n_samples=m, n_features=n_features, centers=n_clusters, cluster_std=sd
        )


def regression(m=20):
    ground_truth_w = 2.3  # slope
    ground_truth_b = -8  # intercept
    X = np.random.uniform(0, 1, size=(m, 1)) * 2
    idxs = np.argsort(X, axis=0)
    idxs = np.squeeze(idxs)
    X = X[idxs]
    Y = ground_truth_w * X + ground_truth_b + 0.2 * np.random.randn(m, 1)
    return X, Y
