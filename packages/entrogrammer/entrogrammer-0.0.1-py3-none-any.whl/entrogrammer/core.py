"""Core functions to call to calculate the entrogram."""

import numpy as np
from scipy.stats import entropy
from . import classifier


def global_entropy(Classifier, base=np.e):
    """Calculate global entropy of some data.

    From an :obj:`entrogrammer.classifier.BaseClassifier`, calculate the
    global entropy of the classified data.

    Parameters
    ----------
    Classifier: :obj:`entrogrammer.classifier.BaseClassifier`
        Any initialized class from `classifier.py` that has had the
        `classify()` method run.

    base: float, optional
        Logarithmic base for the entropy calculation. Same as the
        `scipy.stats.entropy()` base parameter meaning it takes a default
        value of `e` (natural logarithm) if not specified.

    Returns
    -------
    HG: float
        The global entropy of the classified data array

    """
    if isinstance(Classifier, classifier.BaseClassifier) is False:
        raise TypeError('Input must be a BaseClassifier, '
                         'was: %s', str(type(Classifier)))
    elif Classifier.classified is None:
        raise ValueError('`Classifier.classify()` method must be run first.')
    # get probabilities
    n_vals = len(Classifier.classified.flat)  # total number of values
    # get number of each unique (classified) value in the array
    _, unique_counts = np.unique(Classifier.classified, return_counts=True)
    probs = unique_counts / n_vals  # get probabilities
    HG = entropy(probs, base=base)  # get global entropy, this is returned
    return HG
