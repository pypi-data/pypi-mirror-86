"""Classes and methods for binning and classifying data."""

import abc
import xarray as xr
import numpy as np


class BaseClassifier(abc.ABC):
    """Base classifier class.

    Abstract class that exists as a blueprint for classifier classes.
    This class defines the expected methods for each classifier class that is
    implemented.
    """

    def __init__(self, data):
        """Read data.

        This method should handle pre-processing of data for all classifiers.
        Sub-classed classifiers should be able to pre-process and standardize
        data using methods defined here via `super().__init__(data)`

        """
        self.data = data
        self.classified = None  # init classified array as Nonetype

    @property
    def data(self):
        """Return private data array."""
        return self._data

    @data.setter
    def data(self, data):
        """Type-check the input data array and create private variable."""
        # standardize data to a numpy.ndarray or raise an error
        if type(data) is xr.core.dataarray.DataArray:
            self._data = data.data  # convert to ndarray
        elif type(data) is np.ndarray:
            self._data = data
        else:
            raise TypeError('Invalid type for "data", expected a '
                            'numpy.ndarray but got: %s', type(data))

    @property
    def classified(self):
        """Return private classified array."""
        return self._classified

    @classified.setter
    def classified(self, classified):
        """Create private variable."""
        self._classified = classified

    @abc.abstractmethod
    def classify(self):
        """Classify the data.

        All classifier classes should have this method.
        The object of this method is to perform the classification of the
        data into different bins or categories.

        """


class BinaryClassifier(BaseClassifier):
    """Simple binary classifier.

    This class classifies data into a binary scheme. Pretty simple.

    """

    def __init__(self, data, threshold):
        """Initialize the BinaryClassifier.

        Parameters
        ----------
        data : numpy.ndarray
            Input data array.

        thereshold : int, float
            Value below which data will be put into the "0" class.
            Data values at and above this threshold will go into the "1" class.

        """
        super().__init__(data)
        self.threshold = threshold

    @property
    def threshold(self):
        """Return private threshold variable."""
        return self._threshold

    @threshold.setter
    def threshold(self, threshold):
        """Type-check the threshold value and set it as a private variable."""
        if type(threshold) is int:
            self._threshold = threshold
        elif type(threshold) is float:
            self._threshold = threshold
        else:
            raise TypeError('Invalid type for "threshold", expected an '
                            'int or float but got: %s' + type(threshold))

    def classify(self, threshold=None):
        """Do the binary classification."""
        # initialize the classified array
        self.classified = np.zeros_like(self._data)
        # can overwrite threshold with a new one if supplied
        if threshold is not None:
            self.threshold = threshold
        # need if tree to avoid making all values 0 or 1 depending on threshold
        if self._threshold > 0:
            self._classified[self._data < self._threshold] = 0
            self._classified[self._data >= self._threshold] = 1
        else:
            self._classified[self._data >= self._threshold] = 1
            self._classified[self._data < self._threshold] = 0
