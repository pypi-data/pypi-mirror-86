import numpy as np
from sklearn.datasets import make_regression
from sklearn.model_selection import KFold


def make_regression_federated(n_clients, iid=True, random_state=None, *args, **kwargs):
    """
    Generate a federated dataset for regression
    :param int n_clients: Number of clients.
    :param iid: follow and iid distribution across clients (default: True).
    :param random_state: Seed for generating the data
    :return tuple: Tuple of lists [X1,...,XN], [Y1,...,YN]
    """
    # Generate a global dataset
    X, y = make_regression(random_state=random_state, *args, **kwargs)
    X_c = []
    y_c = []

    if iid:
        splitter = KFold(n_splits=n_clients, random_state=random_state, shuffle=True)
        for center_index, _ in splitter.split(X, y):
            X_c.append(X[center_index])
            y_c.append(y[center_index])
    else:
        raise NotImplementedError('Non-IID federated dataset implementation is not ready yet')

    return X_c, y_c

