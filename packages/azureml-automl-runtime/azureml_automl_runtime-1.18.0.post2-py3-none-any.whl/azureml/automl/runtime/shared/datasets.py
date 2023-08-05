# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Class for processing datasets for training/validation."""
from abc import ABC, abstractmethod, abstractproperty
import hashlib
import time
from contextlib import contextmanager
from typing import Any, cast, Dict, List, Optional, Tuple, Union, Iterable, Iterator

import gc
import logging
import math
import numpy as np
import pandas as pd
import scipy
import sklearn
from sklearn import model_selection
from sklearn.compose import ColumnTransformer

from azureml.automl.core.shared import constants
from azureml.automl.core.shared.exceptions import DataErrorException
from azureml.automl.runtime.shared import problem_info, utilities
from azureml.automl.runtime.shared._cv_splits import FeaturizedCVSplit, _CVSplits, _CVType
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.memory_cache_store import MemoryCacheStore
from azureml.automl.runtime.shared.types import CoreDataInputType, DataSingleColumnInputType


logger = logging.getLogger(__name__)
DEFAULT_DATASET_NAME = 'NoName'


class SubsampleCacheStrategy:
    """
    Different cache strategy for subsampling caching on training set.

    Classic: Sample for the specified sample size, cache the result.
    ClassicNoCache: Same as Classic, but the result is not cached.
    Preshuffle: Shuffle the train set indices on the first sampling call.
        Return the first specified percentage of data. The subsequent calls
        also return the first specified percentage. This strategy is only
        honored for non featurized train validation runs. Other run scenarios
        will fall back for the classic caching strategy.

    If we want to sample the dataset a few times with consistent
        result, use Classic.
    If we want to sample the dataset many times with consistent
        result, use Preshuffle.
    If we want to sample the dataset once, or resample everytime,
        use ClassicNoCache.
    """

    Classic = "Classic"
    ClassicNoCache = "ClassicNoCache"
    Preshuffle = "Preshuffle"


class DatasetBase(ABC):
    """Abstract base class for a dataset."""

    @abstractproperty
    def dataset_metadata(self):
        """Get the dataset metadata."""
        return NotImplementedError

    @abstractmethod
    def _get_raw_data_snapshot_str(self):
        """Set the data snapshot for the raw data."""
        raise NotImplementedError

    @abstractmethod
    def get_bin_info(self):
        """Get bin info."""
        raise NotImplementedError

    @abstractmethod
    def get_class_labels(self):
        """Get the class labels for a classification task."""
        raise NotImplementedError

    @abstractmethod
    def get_engineered_feature_names(self):
        """Get the engineered feature names available in different transformers."""
        raise NotImplementedError

    @abstractmethod
    def get_is_sparse(self):
        """Dataset that supports streaming data (data that may be too large to fit into memory)."""
        raise NotImplementedError

    @abstractmethod
    def get_num_classes(self):
        """
        Get the number of classes in the dataset.

        :return:  number of classes
        """
        raise NotImplementedError

    @abstractmethod
    def get_problem_info(self):
        """
        Get the ProblemInfo for the dataset.

        :return: _ProblemInfo
        """
        raise NotImplementedError

    @abstractmethod
    def get_subsampled_dataset(self, subsample_percent, random_state):
        """Get subsampled dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_train_class_labels(self):
        """Get the class labels from training data for a classification task."""
        raise NotImplementedError

    @abstractmethod
    def get_train_set(self):
        """Get the training part of the dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_training_type(self):
        """
        Get training type.

        :return: str: training type
        """
        return NotImplementedError

    @abstractmethod
    def get_transformers(self):
        """
        Get the transformers.

        :return: dict of transformers if success, else none
        """
        raise NotImplementedError

    @abstractmethod
    def get_raw_data_type(self):
        """Return the raw data type."""
        raise NotImplementedError

    @abstractmethod
    def get_X(self):
        """Return X of the training data."""
        raise NotImplementedError

    @abstractmethod
    def get_x_raw_column_names(self) -> Optional[List[str]]:
        """Return the raw column names of X."""
        raise NotImplementedError

    @abstractmethod
    def get_X_valid(self):
        """Return X of the validation data."""
        raise NotImplementedError

    @abstractmethod
    def get_valid_set(self):
        """Get the validation part of the dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_y(self):
        """Return y of the training data."""
        raise NotImplementedError

    @abstractmethod
    def get_y_valid(self):
        """Return y valid of the validation data."""
        raise NotImplementedError

    @abstractmethod
    def get_X_raw(self):
        """Return X of the unfeaturized training data."""
        raise NotImplementedError

    @abstractmethod
    def get_X_valid_raw(self):
        """Return X of the unfeaturized validation data."""
        raise NotImplementedError

    @abstractmethod
    def get_y_raw(self):
        """Return y of the unfeaturized training data."""
        raise NotImplementedError

    @abstractmethod
    def get_y_valid_raw(self):
        """Return y valid of the unfeaturized validation data."""
        raise NotImplementedError

    @abstractmethod
    def get_y_transformer(self):
        """Get the y_transformer."""
        raise NotImplementedError

    @abstractmethod
    def get_y_range(self):
        """
        Get the range of y values.

        :return: The y_min and y_max value.
        """
        raise NotImplementedError

    @abstractmethod
    def has_test_set(self):
        """Return true if the given dataset has test set available."""
        raise NotImplementedError

    @abstractmethod
    def get_num_auto_cv_splits(self) -> Optional[int]:
        """Return the number of auto CV splits that are to be used for this dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_preprocessor(self) -> Optional[Any]:
        """Return the preprocessor for this dataset, if any."""
        raise NotImplementedError

    @abstractmethod
    def get_preprocessor_pipeline_step(self) -> Optional[Tuple[str, Any]]:
        """
        Return the pre-processing pipeline for this Dataset, if any.

        :return: Pair consisting of the name of the pre-processor and the object
        """
        # The input dataset (X and y) are already transformed in this class
        raise NotImplementedError

    @abstractmethod
    def clear_cache(self) -> bool:
        """Clean up any temporary caches that this Dataset may have used."""
        raise NotImplementedError

    def is_timeseries(self) -> bool:
        """Check if this dataset is for forecasting."""
        raise NotImplementedError

    @classmethod
    def make_bin_info(cls, n_valid, y, percentile=1):
        """
        Compute bins based on the dataset targets.

        First and last bins hold all outliers of y. These outlier bins are used
            to make the histogram more readable for the user. The default edges
            of the outlier bins are the 1st and 99th percentiles of y
        The number of bins is selected to keep the amount of data in each bin
            at 10 samples on average. The number of bins is capped at 100, which
            becomes important for large validation sets. The size of metrics
            computed using bin info will not continue to grow with the size of
            the dataset indefinitely.
        :param n_valid: number of points in validation set which will be binned
        :param y: target values (needed for the range of the binning)
        :param percentile: Percentile.
        :return: A dictionary with keys: number_of_bins, bin_starts, bin_ends
            Information about how to bin regression data
            Used to avoid passing around the whole dataset in cases where
            cross validation only requires knowledge of the current split
        """
        if n_valid <= 0:
            raise DataErrorException(
                "Number of validation points must be greater than 0.", target="n_valid",
                reference_code="datasets.DatasetBase.make_bin_info.n_valid", has_pii=False)
        if y.shape[0] == 0:
            raise DataErrorException(
                "y must not be empty.", target="y",
                reference_code="datasets.DatasetBase.make_bin_info.y.shape", has_pii=False)

        if np.unique(y).shape[0] > 1:
            first_end, last_start = np.percentile(y, [percentile, 100 - percentile])
            if first_end == last_start:
                # The data is so skewed that the first percentile == 99th percentile, we need to fix this

                # max_precision sets how many times we want to halve the percentile
                max_precision = 32
                # weight sets how much of an effect the biased value will have on the middle bin's boundaries
                # given a, x, b and weight of 19, the boundaries are [0.05a + 0.95x, 0.95x + 0.05b] before rounding
                weight = 19

                # Halve the percentile every time until we find something different
                p = [1 / (2 ** i) for i in range(max_precision)] + [0]
                first_end_candidates = np.percentile(y, p, interpolation='lower')
                for candidate in first_end_candidates:
                    if candidate != first_end:
                        # Take a weighted average
                        first_end = (first_end * weight + candidate) / (weight + 1)
                        break

                p = [100 - 1 / (2 ** i) for i in range(max_precision)] + [100]
                last_start_candidates = np.percentile(y, p, interpolation='higher')
                for candidate in last_start_candidates:
                    if candidate != last_start:
                        last_start = (last_start * weight + candidate) / (weight + 1)
                        break

                # n_bins = 3 works in all cases here
                n_bins = 3
            else:
                min_bins = 1
                max_bins = 100

                n_bins = math.ceil(math.sqrt(n_valid))
                if n_bins < min_bins:
                    n_bins = min_bins
                elif n_bins > max_bins:
                    n_bins = max_bins

            inner_edges = np.linspace(first_end, last_start, n_bins - 1)
            bin_width = (last_start - first_end) / n_bins

            inner_edges = [cls._round_bin_edge(edge, bin_width) for edge in inner_edges]
            first_start = cls._round_bin_edge(y.min(), bin_width, direction='down')
            last_end = cls._round_bin_edge(y.max(), bin_width, direction='up')
            bin_edges = np.r_[first_start, inner_edges, last_end]

            # Remove bins with width zero
            bin_edges = np.unique(bin_edges)
            n_bins = bin_edges.shape[0] - 1
            if n_bins == 0:
                raise DataErrorException(
                    "Could not create bins based on y.",
                    reference_code="datasets.DatasetBase.make_bin_info.n_bins", has_pii=False)
        else:
            n_bins = 1
            bin_edges = np.array([y[0], y[0]])

        bin_info = {
            'number_of_bins': n_bins,
            'bin_starts': bin_edges[:-1],
            'bin_ends': bin_edges[1:]
        }

        return bin_info

    @abstractmethod
    @contextmanager
    def open_dataset(self) -> Iterator[None]:
        """
        Load the dataset from the cache and then clean it up automatically (if cached).

        Note that any changes made to the dataset won't be reflected back. This is only intended for
        reading the underlying dataset, and caching it back to reduce memory consumption.
        Usage:
            with client_datasets.open_dataset():
                do_something_with_dataset()
        """
        raise NotImplementedError

    @staticmethod
    def _round_bin_edge(edge, bin_width, decimals=2, direction='nearest'):
        """
        Round a bin edge so that it displays well in a UI.

        :param edge: The float value of one bin edge
        :param bin_width: The width of bins to give the magnitude of edges
        :param direction: The direction to round
            'nearest' rounds to the nearest value
            'up' rounds up
            'down' rounds down
        :return: The float value of the new rounded edge
        """
        if bin_width <= 0:
            raise DataErrorException(
                "bin_width must be greater than 0.",
                reference_code="datasets.DatasetBase._round_bin_edge.bin_width", has_pii=False)
        if direction not in ['nearest', 'up', 'down']:
            raise DataErrorException(
                "direction must be 'nearest', 'up', or 'down'.",
                reference_code="datasets.DatasetBase._round_bin_edge.direction", has_pii=False)

        log_magnitude = -1 * int(np.log10(bin_width)) + decimals
        if direction == 'nearest':
            if bin_width >= 1:
                return np.around(edge, decimals=decimals)
            else:
                return np.around(edge, decimals=log_magnitude)
        else:
            round_func = np.ceil if direction == 'up' else np.floor
            mult = 10 ** log_magnitude
            return np.around(round_func(edge * mult) / mult, decimals=log_magnitude)


class ClientDatasets(DatasetBase):
    """The object to state the experiment input data and training characteristics."""

    # TODO: it would be nice to codify all these.
    # Caution: These constants cannot be changed at the moment, Miro relies on these exact strings.
    TRAIN_CV_SPLITS = 'train CV splits'
    FEATURIZED_TRAIN_CV_SPLITS = 'featurized train CV splits'
    FEATURIZED_TRAIN = 'featurized train'
    FEATURIZED_TEST = 'featurized test'
    FEATURIZED_VALID = 'featurized valid'
    TRAIN = 'train indices'
    TEST = 'test indices'
    VALID = 'valid indices'

    DATASET_CACHED_KEYS = 'dataset_cached_keys'

    def __init__(self,
                 meta_data: Optional[Dict[str, Any]] = None,
                 subsample_cache_strategy: str = SubsampleCacheStrategy.Classic,
                 cache_store: Optional[CacheStore] = None):
        """
        Various methods for processing datasets for training/validation.

        :param meta_data: metadata to be directly set on the dataset.
        :param subsample_cache_strategy: SubsampleCacheStrategy value for
            subsample cache strategy.
        :param cache_store: Reference to the cache store.
        """
        self._dataset = meta_data or {}
        self.binary_fields = [
            'X', 'y', 'X_raw', 'y_raw',
            'class_labels',
            ClientDatasets.TRAIN, ClientDatasets.FEATURIZED_TRAIN,
            ClientDatasets.TEST, ClientDatasets.FEATURIZED_TEST,
            ClientDatasets.VALID, ClientDatasets.FEATURIZED_VALID,
            ClientDatasets.TRAIN_CV_SPLITS,
            ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS]
        self._data_fields = list(self.binary_fields + ['X_valid', 'y_valid'])
        self.meta_fields = [
            'dataset_id', 'num_samples', 'num_features', 'num_categorical',
            'num_classes', 'num_missing', 'y_mean', 'y_std', 'y_min', 'y_max',
            'X_mean', 'X_std', 'task', 'openml_id', 'name', 'is_sparse',
            'transformers', 'metadata_only', 'created_time', 'expiry_time',
            'categorical']
        self._subsample_cache_strategy = subsample_cache_strategy
        self._subsample_cache = {}  # type: Dict[float, ClientDatasets]
        self._shuffled_train_indices = None  # type: Optional[np.ndarray]
        self.cache_store = cache_store or MemoryCacheStore()
        self.training_type = None   # type: Optional[str]
        self.timeseries = None
        self.timeseries_param_dict = None
        self.x_raw_column_names = None
        self.raw_data_type = None   # type: Optional[str]
        self.raw_data_snapshot_str = None
        self.num_auto_cv_splits = None  # type: Optional[int]
        self._set_defaults()

    @property
    def dataset_metadata(self):
        """Get the dataset metadata."""
        return None

    def _set_defaults(self):
        # Default values for existing datasets.
        if "metadata_only" not in self._dataset:
            self._dataset['metadata_only'] = False
        if "created_time" not in self._dataset:
            self._dataset['created_time'] = time.mktime((2019, 1, 1, 0, 0, 0, 0, 0, 0))
        if "expiry_time" not in self._dataset:
            # Add 50 years to created date as expiry date for the dataset if no expiry provided.
            self._dataset['expiry_time'] = self._dataset['created_time'] + (50 * 365 * 24 * 60 * 60)

    def is_metadata_only(self):
        """
        Indicate if this dataset is full or metadata only.

        :return:  True if datasets does not contain training data or label.
        """
        if 'metadata_only' not in self._dataset:
            self._set_defaults()
        return self.get_meta('metadata_only')

    def get_y_range(self):
        """
        Get the range of y values.

        :return: The y_min and y_max value.
        """
        y_min, y_max = None, None
        if 'y_min' in self._dataset:
            y_min = self._dataset['y_min']
        if 'y_max' in self._dataset:
            y_max = self._dataset['y_max']
        return y_min, y_max

    def get_y_std(self):
        """Get y_std."""
        return self.get_meta('y_std')

    def get_engineered_feature_names(self):
        """Get the engineered feature names available in different transformers."""
        transformers = self.get_transformers()
        if transformers[constants.Transformers.TIMESERIES_TRANSFORMER] is not None:
            return transformers[constants.Transformers.TIMESERIES_TRANSFORMER].get_engineered_feature_names()
        if transformers[constants.Transformers.LAG_TRANSFORMER] is not None:
            return transformers[constants.Transformers.LAG_TRANSFORMER].get_engineered_feature_names()
        elif transformers[constants.Transformers.X_TRANSFORMER] is not None:
            return transformers[constants.Transformers.X_TRANSFORMER].get_engineered_feature_names()
        else:
            return self.x_raw_column_names

    def get_identifier(self):
        """
        Get a string that attempts to uniquely identify this dataset.

        Hashes all the data, and adds metadata.
        """
        if self.get_meta('is_sparse'):
            rows, cols = self._dataset['X'].nonzero()
            data_bytes = (
                self._dataset['X'].data.tostring() +
                rows.tostring() + cols.tostring())
        else:
            data_bytes = self._dataset['X'].tostring()
        sha = hashlib.sha512(data_bytes)
        sha.update(self._dataset['y'].tostring())
        for ind in [ClientDatasets.TRAIN, ClientDatasets.TEST,
                    ClientDatasets.VALID]:
            if ind in self._dataset:
                arr = self._dataset[ind]
                if isinstance(arr, list):
                    arr = np.array(arr)
                sha.update(arr.tostring())

        # TODO: handle CV indices.
        y_min, y_max = self.get_y_range()
        return '{0}-{1}-{2}-{3}-{4}-{5}-{6}'.format(
            sha.hexdigest(), self.get_task(), self.get_meta('num_samples'),
            self.get_meta('num_features'), y_min, y_max,
            self.get_meta('is_sparse'))

    def get_full_set(self):
        """
        Get the full dataset sample data and label.

        :return: return the full dataset
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        return X, y, sample_weight

    def get_train_set(self):
        """Get the training part of the dataset."""
        X_train = None
        y_train = None
        sample_weight_train = None
        if ClientDatasets.TRAIN in self._dataset:
            X, y = self._dataset['X'], self._dataset['y']
            sample_weight = self._dataset.get('sample_weight')
            if isinstance(X, pd.DataFrame):
                X_train, y_train = X.iloc[self._dataset[ClientDatasets.TRAIN]], y[
                    self._dataset[ClientDatasets.TRAIN]]
            else:
                X_train, y_train = X[self._dataset[ClientDatasets.TRAIN]], y[
                    self._dataset[ClientDatasets.TRAIN]]
            sample_weight_train = None \
                if sample_weight is None \
                else sample_weight[self._dataset[ClientDatasets.TRAIN]]
        elif ClientDatasets.FEATURIZED_TRAIN in self._dataset:
            X_train = self._dataset[ClientDatasets.FEATURIZED_TRAIN]['X']
            y_train = self._dataset[ClientDatasets.FEATURIZED_TRAIN]['y']
            sample_weight_train = \
                self._dataset[ClientDatasets.FEATURIZED_TRAIN]['sample_weight']

        return X_train, y_train, sample_weight_train

    def get_valid_set(self):
        """Get the validation part of the dataset."""
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        X_valid = None
        y_valid = None
        sample_weight_valid = None
        if 'X_valid' in self._dataset:
            assert 'y_valid' in self._dataset
            X_valid, y_valid, sample_weight_valid = (
                self._dataset['X_valid'],
                self._dataset['y_valid'],
                None)
            if sample_weight is not None:
                sample_weight_valid = self._dataset['sample_weight_valid']
        elif ClientDatasets.VALID in self._dataset:
            X_valid, y_valid = (
                X[self._dataset[ClientDatasets.VALID]],
                y[self._dataset[ClientDatasets.VALID]])
            sample_weight_valid = (None
                                   if sample_weight is None
                                   else sample_weight[
                                       self._dataset[ClientDatasets.VALID]])
        elif ClientDatasets.FEATURIZED_VALID in self._dataset:
            X_valid = self._dataset[ClientDatasets.FEATURIZED_VALID]['X']
            y_valid = self._dataset[ClientDatasets.FEATURIZED_VALID]['y']
            sample_weight_valid = \
                self._dataset[ClientDatasets.FEATURIZED_VALID]['sample_weight']

        return X_valid, y_valid, sample_weight_valid

    def get_y_transformer(self):
        """Get the y_transformer."""
        transformers = self.get_transformers()
        if transformers:
            return self.get_transformers().get(constants.Transformers.Y_TRANSFORMER)

    def get_transformers(self):
        """
        Get the transformers.

        :return: dict of transformers if success, else none
        """
        transformers = self._dataset.get('transformers')
        if transformers:
            return transformers

        dict_values = self.cache_store.get(['transformers'])

        if dict_values:
            self._dataset['transformers'] = dict_values.get('transformers')
            return self._dataset.get('transformers')

        return None

    def get_test_set(self):
        """
        Get the test set from the full dataset.

        :return: Test features, test labels, and weights of test samples
        :rtype: tuple(np.ndarray, np.ndarray, np.ndarray)
        """
        X, y = self._dataset['X'], self._dataset['y']
        sample_weight = self._dataset.get('sample_weight')
        X_test = None
        y_test = None
        sample_weight_test = None
        if 'X_test' in self._dataset:
            assert 'y_test' in self._dataset.keys()
            X_test, y_test = self._dataset['X_test'], self._dataset['y_test']
            sample_weight_test = self._dataset['sample_weight_test']
        elif ClientDatasets.TEST in self._dataset:
            X_test, y_test = X[self._dataset[ClientDatasets.TEST]
                               ], y[self._dataset[ClientDatasets.TEST]]
            sample_weight_test = (sample_weight and
                                  sample_weight[self._dataset[
                                      ClientDatasets.TEST]])
        elif ClientDatasets.FEATURIZED_TEST in self._dataset:
            X_test = self._dataset[ClientDatasets.FEATURIZED_TEST]['X']
            y_test = self._dataset[ClientDatasets.FEATURIZED_TEST]['y']
            sample_weight_test = \
                self._dataset[ClientDatasets.FEATURIZED_TEST]['sample_weight']

        return X_test, y_test, sample_weight_test

    def has_test_set(self):
        """Return true if the given dataset has test set available."""
        return 'X_test' in self._dataset and \
            self._dataset['X_test'].any() or \
            ClientDatasets.TEST in self._dataset or \
            ClientDatasets.FEATURIZED_TEST in self._dataset

    def has_training_set(self):
        """Return true if the given dataset has training set available."""
        return ClientDatasets.TRAIN in self._dataset or \
            ClientDatasets.FEATURIZED_TRAIN in self._dataset

    def get_CV_splits(self):
        """
        Get the CV splits of the dataset, if cross validation is specified.

        :return:
        """
        if (ClientDatasets.TRAIN_CV_SPLITS in self._dataset and
            self._dataset[
                ClientDatasets.TRAIN_CV_SPLITS] is not None):
            sample_wt = self._dataset.get('sample_weight')
            for train_ind, test_ind in self._dataset[
                    ClientDatasets.TRAIN_CV_SPLITS]:
                # the cached dataset key is expected to be a single numpy array of type .npy
                # if we see a file of type .npz, we need to log a warning because index access will fail
                if isinstance(self._dataset['X'], np.lib.npyio.NpzFile):
                    logger.warning("'X' was of type np.lib.npyio.NpzFile with contents: {}",
                                   sorted(self._dataset['X'].files))
                yield (self._dataset['X'][train_ind],
                       self._dataset['y'][train_ind],
                       None if sample_wt is None else sample_wt[train_ind],
                       self._dataset['X'][test_ind],
                       self._dataset['y'][test_ind],
                       None if sample_wt is None else sample_wt[test_ind])

        elif (ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS in self._dataset and
              self._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS]
              is not None):
            for featurized_cv_split in self._dataset[
                    ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS]:

                # Recover the cross validation data from the cache
                featurized_cv_split = featurized_cv_split._recover_from_cache_store()

                yield (
                    featurized_cv_split._X_train_transformed,
                    featurized_cv_split._y_train,
                    featurized_cv_split._sample_wt_train,
                    featurized_cv_split._X_test_transformed,
                    featurized_cv_split._y_test,
                    featurized_cv_split._sample_wt_test)
        else:
            raise DataErrorException(
                'CV splits not found in dataset.',
                reference_code="datasets.DatasetBase.ClientDatasets.get_CV_splits", has_pii=False)

    def get_num_classes(self):
        """
        Get the number of classes in the dataset.

        :return:  number of classes
        """
        return self.get_meta('num_classes')

    def get_class_labels(self):
        """Get the class labels for a classification task."""
        return self.get_meta('class_labels')

    def get_train_class_labels(self):
        """Get the class labels from training data for a classification task."""
        raise NotImplementedError

    def get_task(self):
        """
        Get the current task type.

        :return:  task type such as regression or classification.
        """
        return self.get_meta('task')

    def get_meta(self, attr):
        """
        Get the value of the dataset attribute such as task, y_max.

        :param attr:  the attribute to get
        :return: returns the value of the passed attribute
        """
        return self._dataset.get(attr, None)

    def get_is_sparse(self):
        """Get whether the dataset is sparse format."""
        is_sparse = self._dataset.get('is_sparse', None)
        if is_sparse is None:
            is_sparse = scipy.sparse.issparse(self._dataset['X'])
            self._dataset['is_sparse'] = is_sparse
        return is_sparse

    def get_training_type(self):
        """
        Get training type.

        :return: str: training type
        """
        if self.training_type:
            return self.training_type

        self.training_type = self.cache_store.get(['training_type']).get('training_type')
        return self.training_type

    def add_data(self, attr, val):
        """
        Set the value of a dataset attribute.

        :param attr: the attribute to set the value
        :param val: the value of the attribute
        :return: none
        """
        self._dataset[attr] = val

    def get_problem_info(self):
        """
        Get the ProblemInfo for the dataset.

        :return: _ProblemInfo
        """
        return problem_info.ProblemInfo(
            dataset_samples=self.get_meta('num_samples'),
            dataset_classes=self.get_num_classes(),
            dataset_features=self.get_meta('num_features'),
            dataset_num_categorical=self.get_meta('num_categorical'),
            dataset_y_std=self.get_meta('y_std'),
            is_sparse=self.get_meta('is_sparse'),
            task=self.get_meta('task'),
            metric=None)

    def _get_raw_data_snapshot_str(self) -> Any:
        """Set the data snapshot for the raw data."""
        return self.raw_data_snapshot_str

    def get_num_auto_cv_splits(self) -> Optional[int]:
        """Return the number of auto CV splits that are to be used for this dataset."""
        return self.num_auto_cv_splits

    def _init_dataset(self, name, task, X, y, sample_weight=None,
                      categorical=None, openml_id=None, num_classes=None,
                      class_labels=None,
                      y_min=None, y_max=None, transformers=None,
                      init_all_stats=True):
        """
        Initialize the data set with the input data, metadata and labels.

        :param name:
        :param X: train data
        :param y: label for train data
        :param task: the task type of training(regression/classification)
        :param sample_weight: size of the sample
        :param categorical: Boolean array to indicate which features are categorical
        :param openml_id:
        :param num_classes: number of classes in the experiment.
        :param y_min: min value of the label
        :param y_max: max value of the label
        :param init_all_stats:
        :param transformers: Transformers that are used in this input dataset.
        :return:
        """
        X_df = None
        if isinstance(X, pd.DataFrame):
            X_df = X
            X = X.values

        self._dataset = {}
        if openml_id is not None:
            self._dataset['openml_id'] = openml_id
        else:
            self._dataset['openml_id'] = 'NA'
        self._dataset['dataset_id'] = name
        self._dataset['name'] = name
        self._dataset['num_samples'] = int(X.shape[0])
        self._dataset['num_features'] = int(X.shape[1])
        self._dataset['num_missing'] = 0 if scipy.sparse.issparse(
            X) else int(np.sum(pd.isna(X)))
        self._dataset['is_sparse'] = scipy.sparse.issparse(X)
        if init_all_stats:
            self._dataset['y_mean'] = float(y.mean())
            self._dataset['X_mean'] = float(X.mean())
            self._dataset['X_std'] = float(
                X.std()) if not scipy.sparse.issparse(X) \
                else utilities.sparse_std(X)
        else:
            self._dataset['y_mean'] = None
            self._dataset['X_mean'] = None
            self._dataset['X_std'] = None

        try:
            self._dataset['y_min'] = y_min if y_min else float(y.min())
            self._dataset['y_max'] = y_max if y_max else float(y.max())
            self._dataset['y_std'] = float(y.std())
        except (TypeError, ValueError):
            # TypeError if y contains mixed type with unhashable type
            # ValueError if y contains mixed type with np.ndarray containing more than one element
            self._dataset['y_min'] = y_min if y_min else None
            self._dataset['y_max'] = y_max if y_max else None
            self._dataset['y_std'] = None

        if categorical is None:
            # assume 0, but we really don't know in this case.
            self._dataset['num_categorical'] = 0
        else:
            self._dataset['num_categorical'] = int(np.sum(categorical))

        self._dataset['categorical'] = categorical

        self._dataset['task'] = task
        if task == constants.Tasks.CLASSIFICATION:
            unique_y = utilities._get_unique(y[~pd.isna(y)])
            if num_classes is None:
                self._dataset['num_classes'] = len(unique_y)
            else:
                self._dataset['num_classes'] = num_classes

            if class_labels is None:
                self._dataset['class_labels'] = unique_y
            else:
                self._dataset['class_labels'] = class_labels

            if self._dataset['num_classes'] != len(self._dataset['class_labels']):
                raise DataErrorException(
                    "num_classes and class_labels not consistent",
                    reference_code="datasets.DatasetBase.make_bin_info.y.shape", has_pii=False)

        elif task == constants.Tasks.REGRESSION:
            self._dataset['num_classes'] = None

        for k in self._dataset.keys():
            # let 'class_labels' be special so we can write to DB still
            assert k in self.meta_fields or k == 'class_labels', \
                "%s is not in meta_fields" % k

        self._dataset['X'] = X if X_df is None else X_df
        self._dataset['y'] = y
        self._dataset['transformers'] = transformers
        self._dataset['sample_weight'] = sample_weight
        self._dataset['sample_weight_valid'] = None
        self._dataset['sample_weight_test'] = None
        self._set_defaults()

    def parse_simple_train_validate(
            self,
            name: str,
            task: str,
            X: CoreDataInputType,
            y: DataSingleColumnInputType,
            X_valid: CoreDataInputType,
            y_valid: DataSingleColumnInputType,
            sample_weight: Optional[DataSingleColumnInputType] = None,
            sample_weight_valid: Optional[DataSingleColumnInputType] = None,
            num_classes: Optional[int] = None,
            y_min: Optional[float] = None,
            y_max: Optional[float] = None,
            transformers: Optional[Any] = None,
            init_all_stats: bool = True,
            X_raw: Optional[CoreDataInputType] = None,
            y_raw: Optional[DataSingleColumnInputType] = None,
            X_valid_raw: Optional[CoreDataInputType] = None,
            y_valid_raw: Optional[DataSingleColumnInputType] = None) -> None:
        """
        Create a ClientDataset processing the input data.

        :param name:
        :param task: task type
        :param X: train data
        :param y: label
        :param sample_weight:
        :param X_valid: validation data
        :param y_valid: validation label
        :param sample_weight_valid:
        :param num_classes: number of classes in the experiment
        :param y_min: min value of the label
        :param y_max: max value of the label
        :param transformers: Transformers that are used in this input dataset.
        :param init_all_stats: Initialize all statistics.
        :return: a client dataset with all metadata set.
        """
        nan_y_index = utilities._get_indices_missing_labels_output_column(y)
        nan_y_valid_index = utilities._get_indices_missing_labels_output_column(y_valid)
        class_labels = np.union1d(np.delete(y, nan_y_index), np.delete(y_valid, nan_y_valid_index))
        if num_classes is None:
            num_classes = class_labels.shape[0]

        self._init_dataset(
            name, task, X, y,
            sample_weight=sample_weight,
            num_classes=num_classes, class_labels=class_labels,
            y_min=y_min, y_max=y_max,
            transformers=transformers, init_all_stats=init_all_stats)

        self._dataset['X_valid'] = X_valid
        self._dataset['y_valid'] = y_valid

        self._dataset['X_raw'] = X_raw
        self._dataset['y_raw'] = y_raw
        self._dataset['X_valid_raw'] = X_valid_raw
        self._dataset['y_valid_raw'] = y_valid_raw

        self._dataset["sample_weight"] = sample_weight
        self._dataset['sample_weight_valid'] = sample_weight_valid
        self._dataset[ClientDatasets.TRAIN] = np.arange(X.shape[0])

        if self._dataset['task'] == constants.Tasks.REGRESSION:
            self._dataset['bin_info'] = self.make_bin_info(X_valid.shape[0], y_valid)

    def parse_data(
            self,
            name: str,
            task: str,
            X: CoreDataInputType,
            y: DataSingleColumnInputType,
            sample_weight: Optional[DataSingleColumnInputType] = None,
            categorical: Optional[np.ndarray] = None,
            cv_splits: Optional[Any] = None,
            openml_id: Optional[Any] = None,
            num_classes: Optional[int] = None,
            y_min: Optional[float] = None,
            y_max: Optional[float] = None,
            transformers: Optional[Any] = None,
            init_all_stats: bool = True,
            X_raw: Optional[CoreDataInputType] = None,
            y_raw: Optional[DataSingleColumnInputType] = None,
            X_valid_raw: Optional[CoreDataInputType] = None,
            y_valid_raw: Optional[DataSingleColumnInputType] = None) -> None:
        """
        Parse data.

        :param name: Dataset name (legacy attribute from when ClientDatasets held many datasets).
        :param task: Task type.
        :param X: Input data training features.
        :param y: Input data target feature.
        :param sample_weight: Array of sample weights.
        :param cv_splits: CV splits information container.
        :type cv_splits: azureml.automl.core.shared._cv_splits
        :param categorical: Boolean array to indicate which features are categorical
        :param openml_id: OpenML dataset ID (legacy attribute).
        :param num_classes: Number of classes in the classification dataset.
        :param y_min: Minimum value of the target feature (regression).
        :param y_max: Maximum value of the target feature (regression).
        :param transformers: Transformers that are used in this input dataset.
        :param init_all_stats: Flag to compute stats_computation.
        :param X_raw: Input data training features.
        :param y_raw: Input data target feature.
        :param X_valid_raw: Input data validation features.
        :param y_valid_raw: Input data validation target feature.
        :return: a client dataset with all metadata set.
        """
        # Initialize all the stats_computation
        self._init_dataset(name, task, X, y,
                           sample_weight=sample_weight,
                           categorical=categorical, openml_id=openml_id,
                           num_classes=num_classes,
                           y_min=y_min, y_max=y_max,
                           transformers=transformers,
                           init_all_stats=init_all_stats)

        self._dataset['X_raw'] = X_raw
        self._dataset['y_raw'] = y_raw
        self._dataset['X_valid_raw'] = X_valid_raw
        self._dataset['y_valid_raw'] = y_valid_raw

        if cv_splits is not None:
            cv_split_type = cv_splits.get_cv_split_type()

            self._dataset[ClientDatasets.TRAIN_CV_SPLITS] = None
            self._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS] = None
            # Populate the CV splits indicies
            if cv_split_type != _CVType.TrainTestValidationPercSplit and \
               cv_split_type != _CVType.TrainValidationPercSplit:

                if cv_splits.get_featurized_cv_split_data() is None:
                    self._dataset[ClientDatasets.TRAIN_CV_SPLITS] = cv_splits.get_cv_split_indices()
                else:
                    self._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS] = \
                        cv_splits.get_featurized_cv_split_data()
            else:
                if cv_splits._featurized_train_test_valid_chunks is None:
                    train_indices, test_indices, valid_indices = cv_splits.get_train_test_valid_indices()
                    self._dataset[ClientDatasets.TRAIN] = train_indices
                    self._dataset[ClientDatasets.VALID] = valid_indices
                    if cv_splits._cv_split_type == _CVType.TrainTestValidationPercSplit:
                        self._dataset[ClientDatasets.TEST] = test_indices
                else:
                    featurized_train_data, featurized_test_data, featurized_valid_data = \
                        cv_splits.get_featurized_train_test_valid_data()
                    self._dataset[ClientDatasets.FEATURIZED_TRAIN] = featurized_train_data
                    self._dataset[ClientDatasets.FEATURIZED_VALID] = featurized_valid_data
                    if cv_splits._cv_split_type == _CVType.TrainTestValidationPercSplit:
                        self._dataset[ClientDatasets.FEATURIZED_TEST] = featurized_test_data

            # Based on the type of CV split populate all the bin info for
            # regression tasks
            if task == constants.Tasks.REGRESSION:
                self.set_bin_info(cv_splits)

    def set_bin_info(self, cv_splits):
        """Set the bin info for regression datasets."""
        cv_split_type = cv_splits.get_cv_split_type()
        if cv_split_type == _CVType.CustomCrossValidationSplit:
            # we know all split values with custom splits so we take
            # just values used in validation to create the range for
            # generated bins
            tot_indices = [ind for split in cv_splits.get_cv_split_indices() for ind in split[1]]
            tot_y = self._dataset['y'][np.unique(tot_indices)]
            self._dataset['bin_info'] = self.make_bin_info(
                len(tot_indices),
                tot_y)
        elif cv_split_type == _CVType.KFoldCrossValidationSplit:
            self._dataset['bin_info'] = self.make_bin_info(
                int(self._dataset['num_samples'] /
                    cv_splits.get_num_k_folds()),
                self._dataset['y'])
        elif cv_split_type == _CVType.MonteCarloCrossValidationSplit:
            # Monte-Carlo may take any value from the dataset so in this case
            # we send of all of y to ensure the entire range is represented in
            # generated bins
            self._dataset['bin_info'] = self.make_bin_info(
                int(self._dataset['num_samples'] *
                    cv_splits.get_fraction_validation_size()),
                self._dataset['y'])
        elif cv_split_type == _CVType.TestCutoffCVSplit:
            self._dataset['bin_info'] = self.make_bin_info(
                int(self._dataset['num_samples'] *
                    cv_splits.get_fraction_validation_size() /
                    cv_splits.get_num_k_folds()),
                self._dataset['y'])
        elif cv_split_type == _CVType.TimeSeriesSplit:
            tot_indices = [ind for split in cv_splits.get_cv_split_indices() for ind in split[1]]
            # ideally we would use
            # tot_y = self._dataset['y'][np.unique(tot_indices)]
            # however splits are based on the raw data while _dataset['y'] contains transformed data
            # which may have been expended based on timeseries featurizers. Instead we take the values
            # from the generated splits
            y_tot = []
            for _, _, _, _, y_test, _ \
                    in self.get_CV_splits():
                y_tot.append(y_test)
            y_tot = np.concatenate(y_tot)

            self._dataset['bin_info'] = self.make_bin_info(
                len(tot_indices),
                y_tot)
        else:
            if 'bin_info' not in self._dataset:
                self._dataset['bin_info'] = self.make_bin_info(
                    int(self._dataset['num_samples'] * cv_splits.get_fraction_validation_size()),
                    self._dataset['y'])

    def get_bin_info(self):
        """Get bin info."""
        return self.get_meta('bin_info')

    def get_subsampled_dataset(self, subsample_percent,
                               random_state=None, force_resample=False):
        """
        Get subsampled dataset.

        For train validation non featurized scenario, a new dataset is created with a mapping
        to the original dataset. For cv and featurized scenarios, the original dataset is
        deepcopied and subsampled.

        :param subsample_percent:
        :param random_state: int, RandomState instance or None, optional
            (default=None) If int, random_state is the seed used by the
            random number generator; If RandomState instance, random_state
            is the random number generator; If None, the random number
            generator is the RandomState instance used by `np.random`.
        :param force_resample: Should force resample or not.
        :return: Another ClientDatasets object that is a subsample.
        """
        assert subsample_percent > 0 and subsample_percent < 100

        if not force_resample and subsample_percent in self._subsample_cache:
            return self._subsample_cache[subsample_percent]

        subsample_frac = float(subsample_percent) / 100.0

        if ClientDatasets.TRAIN in self._dataset or ClientDatasets.FEATURIZED_TRAIN in self._dataset:
            # for Train validation
            set_key = ClientDatasets.FEATURIZED_TRAIN if ClientDatasets.FEATURIZED_TRAIN in self._dataset \
                else ClientDatasets.TRAIN

            ret = self._clone(exclude_fields=[set_key])

            if set_key == ClientDatasets.FEATURIZED_TRAIN:
                orig_data = self._dataset[set_key]
                n = orig_data['X'].shape[0]
                train_y = None if self.get_meta('task') != constants.Tasks.CLASSIFICATION else \
                    orig_data['y']

                new_train_indices, _ = ClientDatasets._train_test_split(
                    data=np.arange(n),
                    train_size=subsample_frac,
                    stratify=train_y,
                    random_state=random_state)

                ret._dataset[set_key] = {
                    'X': orig_data['X'][new_train_indices],
                    'y': orig_data['y'][new_train_indices],
                    'sample_weight': orig_data['sample_weight'][new_train_indices] if
                    orig_data['sample_weight'] is not None else None
                }
            else:
                train_y = None if self.get_meta('task') != constants.Tasks.CLASSIFICATION else \
                    self._dataset['y'][self._dataset[set_key]]

                if self._subsample_cache_strategy == SubsampleCacheStrategy.Preshuffle:
                    if not self._shuffled_train_indices:
                        self._shuffled_train_indices = utilities.stratified_shuffle(
                            self._dataset[set_key], train_y, random_state)
                    subsample_count = math.ceil(len(cast(np.ndarray, self._shuffled_train_indices)) * subsample_frac)
                    ret._dataset[set_key] = cast(np.ndarray, self._shuffled_train_indices)[:subsample_count]
                else:
                    new_train_indices, _ = ClientDatasets._train_test_split(
                        data=self._dataset[set_key],
                        train_size=subsample_frac,
                        stratify=train_y,
                        random_state=random_state
                    )

                    ret._dataset[set_key] = new_train_indices
        else:
            # for CV
            if self._dataset.get(ClientDatasets.TRAIN_CV_SPLITS, None):
                ret = self._clone(exclude_fields=[ClientDatasets.TRAIN_CV_SPLITS])
                ret._dataset[ClientDatasets.TRAIN_CV_SPLITS] = []
                # not featurized
                for cv_split in self._dataset[ClientDatasets.TRAIN_CV_SPLITS]:
                    train, test = cv_split
                    original_n = train.shape[0]
                    subsample_n = int(original_n * subsample_frac)
                    sub_train = train[:subsample_n]
                    ret._dataset[ClientDatasets.TRAIN_CV_SPLITS].append((sub_train, test))
            else:
                # featurized
                subsampled_featurized_splits = []
                ret = self._clone(exclude_fields=[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS])
                ret._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS] = []
                for featurized_cv_split in self._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS]:
                    featurized_cv_split = featurized_cv_split._recover_from_cache_store()

                    original_n = featurized_cv_split._y_train.shape[0]
                    subsample_n = int(original_n * subsample_frac)
                    x_train = featurized_cv_split._X_train_transformed[:subsample_n]
                    y_train = featurized_cv_split._y_train[:subsample_n]
                    if featurized_cv_split._sample_wt_train is not None:
                        sample_wt_train = featurized_cv_split._sample_wt_train[:subsample_n]
                    else:
                        sample_wt_train = None

                    subsampled_split = FeaturizedCVSplit(x_train, y_train, sample_wt_train,
                                                         featurized_cv_split._X_test_transformed,
                                                         featurized_cv_split._y_test,
                                                         featurized_cv_split._sample_wt_test,
                                                         data_transformer=featurized_cv_split._data_transformer,
                                                         lag_transformer=featurized_cv_split._lag_transformer)

                    subsampled_featurized_splits.append(subsampled_split)
                ret._dataset[ClientDatasets.FEATURIZED_TRAIN_CV_SPLITS] = subsampled_featurized_splits

        if self._subsample_cache_strategy != SubsampleCacheStrategy.ClassicNoCache:
            self._subsample_cache[subsample_percent] = ret

        return ret

    def _clone(self, exclude_fields=[]):
        clone = ClientDatasets(subsample_cache_strategy=self._subsample_cache_strategy)
        clone._dataset = {}
        for field in self._dataset:
            if field not in exclude_fields:
                clone._dataset[field] = self._dataset[field]
        return clone

    def get_transformer(self, transformer: str) -> Optional[Any]:
        """
        Get the transformer from the cache.

        :param transformer: The transformer name to retrieve.
        :return: The transformer.
        """
        cache_key = "transformers"
        if self.cache_store:
            self.cache_store.load()
            data = self.cache_store.get([cache_key])
            try:
                cached_transformers = cast(Dict[str, Any], data.get(cache_key, dict()))
                return cached_transformers.get(transformer, None)
            except Exception:
                pass
        return None

    def is_timeseries(self) -> bool:
        """Check if this dataset is for timeseries."""
        ts_str = "timeseries"
        is_ts = cast(bool, self.get_meta(ts_str))
        if is_ts is not None:
            return is_ts
        else:
            self.cache_store.load()
            is_ts_d = self.cache_store.get([ts_str], dict())
            is_ts = is_ts_d.get(ts_str, False)
            self.add_data(ts_str, is_ts)
            return is_ts

    def _load_dataset_from_dict(self, dataset: Dict[str, Any]) -> None:
        for k, v in dataset.items():
            if k not in self._dataset:
                self._dataset[k] = v

    def load_dataset_from_cache(self) -> None:
        """Populate the underlying dataset that may have been cached."""
        self.cache_store.load()

        keys = self.cache_store.get([ClientDatasets.DATASET_CACHED_KEYS])
        if keys is None or keys.get(ClientDatasets.DATASET_CACHED_KEYS) is None:
            return

        dataset_keys = cast(Iterable[Any], keys[ClientDatasets.DATASET_CACHED_KEYS])
        retrieved_dataset = self.cache_store.get(dataset_keys)
        self._load_dataset_from_dict(retrieved_dataset)

    def cache_dataset(self, keep_in_memory: bool = True) -> None:
        """
        Cache and garbage collect the attributes in this class.

        This method caches the memory intensive resources from the `self._dataset` dict. These are represented by the
        keys present in `self._data_fields`, which can contain input or featurized data along with validation sets.
        Note that this function does not update the objects if it's already present in the cache store.

        :param keep_in_memory: If False, the dataset objects are flushed to cache and garbage collected.
        :return: None
        """
        # Only cache those keys from `self._dataset` which:
        # 1. Could be memory heavy (represented by the keys in self._data_fields),
        # 2. Are not already cached in the cache store
        for key, value in self._dataset.items():
            if (key in self._data_fields and
                    key not in self.cache_store.cache_items):
                self.cache_store.add([key], [value])
        cached_keys = set(self._dataset.keys()).intersection(set(self._data_fields))
        self.cache_store.add([self.DATASET_CACHED_KEYS], [list(cached_keys)])

        if not keep_in_memory:
            self._gc_dataset()

    def _gc_dataset(self) -> None:
        keys = set(self._dataset.keys()).intersection(set(self._data_fields))   # list(self._dataset.keys())
        for key in keys:
            del self._dataset[key]
        gc.collect()

    def clear_cache(self) -> bool:
        """
        Garbage collect the attributes in `self._dataset` and delete the underlying files from the cache store.

        :return: True if unloading the data from the cache_store succeeded, FaLse otherwise
        """
        try:
            self._gc_dataset()
            self.cache_store.unload()
            return True
        except IOError:
            return False

    def get_preprocessor(self) -> Optional[Any]:
        """Return the preprocessor for this dataset, if any."""
        return None

    def get_preprocessor_pipeline_step(self) -> Optional[Tuple[str, Any]]:
        """
        Return the pre-processing pipeline for this Dataset, if any.

        :return: Pair consisting of the name of the pre-processor and the object
        """
        # The input dataset (X and y) are already transformed in this class
        return None

    @contextmanager
    def open_dataset(self) -> Iterator[None]:
        """
        Load the dataset from the cache and then clean it up automatically (if cached).

        Note that any changes made to the dataset won't be reflected back. This is only intended for
        reading the underlying dataset, and caching it back to reduce memory consumption.
        Usage:
            with client_datasets.open_dataset():
                do_something_with_dataset()
        """
        self.load_dataset_from_cache()
        yield
        # Don't GC the dataset if it wasn't already cached
        keys = self.cache_store.get([ClientDatasets.DATASET_CACHED_KEYS])
        if keys.get(ClientDatasets.DATASET_CACHED_KEYS) is not None:
            self._gc_dataset()

    @staticmethod
    def _train_test_split(data: CoreDataInputType,
                          train_size: float,
                          stratify: Optional[Iterable[Any]],
                          random_state: Optional[Union[int, np.random.RandomState]]) -> Tuple[CoreDataInputType,
                                                                                              CoreDataInputType]:
        """
        Wrapper on `sklearn.model_selection.train_test_split` to gracefully fallback to random sampling in case
        stratified sampling fails.

        :param dataset: See ``arrays`` parameter of ``sklearn.model_selection.train_test_split`` method.
        :param train_size: See ``train_size`` parameter of ``sklearn.model_selection.train_test_split`` method.
        :param stratify: See ``stratify`` parameter of ``sklearn.model_selection.train_test_split`` method.
        :param random_state: See ``random_state`` parameter of ``sklearn.model_selection.train_test_split`` method.
        :return: Tuple of train indices and test indices.
        """
        try:
            train_size = float(train_size)
            train_indices, test_indices = model_selection.train_test_split(
                data,
                train_size=train_size,
                stratify=stratify,
                random_state=random_state)
        except ValueError:
            # Fall back to non-stratified sampling when stratification fails.
            train_indices, test_indices = model_selection.train_test_split(
                data,
                train_size=train_size,
                stratify=None,
                random_state=random_state)

        return train_indices, test_indices

    @staticmethod
    def _check_data(X, y, categorical=None, missing_data=False):
        """
        Check data for issues.

        :param X: Dataset features to encode
        :param y: Dataset target values
        :param categorical: Boolean array to indicate which features are categorical
        :param missing_data:
        :return: Encoded X, y
        """
        if not missing_data:
            assert (isinstance(X, np.ndarray) and not np.any(
                pd.isna(X))) or scipy.sparse.issparse(X)

        if categorical is not None:
            if type(categorical) == np.ndarray:
                assert X.shape[1] == len(
                    categorical), ("there should be one categorical indicator "
                                   "for each feature")

        assert not np.any(pd.isna(y)), "can't have any missing values in y"
        assert X.shape[0] == y.shape[0], "X and y should have the same shape"
        assert len(y.shape) == 2, "y should be a vector Nx1"
        assert y.shape[1] == 1, "y should be a vector Nx1"

    @staticmethod
    def _encode_data(X: np.ndarray,
                     y: np.ndarray,
                     categorical: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Encode data.

        :param X: Dataset features to encode
        :param y: Dataset target values
        :param categorical: Boolean array to indicate which features are categorical
        :return: Encoded X, y
        """
        if np.any(categorical):
            ohe = sklearn.preprocessing.OneHotEncoder()
            # We need to maintain prior functionality where encoded columns were returned first.
            # This column transformer will apply the encoding to categoricals and then pass
            # other non-categoricals after
            enc = ColumnTransformer(
                [('encoder', ohe, categorical), ('others', 'passthrough', ~categorical)],
                sparse_threshold=0
            )
            X = enc.fit_transform(X)
        return X, y

    @staticmethod
    def decode_data(X: np.ndarray) -> Tuple[np.ndarray, np.ndarray]:
        """
        Decode all columns of X that are one-hot encodings.

        Scan through the columns of X looking for chunks where the following hold:
        - All values are 0 or 1
        - Each row of the chunk has exactly one 1

        :param X: The features from a dataset that has been one-hot encoded
        :return: A tuple with the decoded X array and a 1 dimensional ndarray containing
            the cardinalities for all categorical features that were found
        """
        n_binary = 0
        for column_index in range(X.shape[1]):
            column = X[:, column_index]
            # Column of all zeros implies a one-hot encoder was not used
            # Probably a dataset of images where the pixels are not categorical
            if not np.any(column):
                break
            # Check that all values are 0s and 1s
            if np.array_equal(column, column.astype(bool)):
                n_binary += 1
            else:
                break

        if n_binary == 0:
            return (X, np.array([]))

        # The last column of a one-hot chunk appears when
        # the cumulative row sums are all equal for that column
        binary_columns = X[:, :n_binary]
        cum_row_sums = np.cumsum(binary_columns, axis=1)
        all_same = np.all(cum_row_sums == cum_row_sums[0, :], axis=0).reshape((n_binary, 1))
        categorical_ends = np.where(all_same)[0]

        # Decode each chunk
        categorical_columns = []
        cardinalities = []  # type: List[int]
        for i, end in enumerate(categorical_ends):
            start = 0 if i == 0 else categorical_ends[i - 1] + 1
            chunk = binary_columns[:, start:end + 1]
            _, column = np.where(chunk == 1)
            categorical_columns.append(column)
            cardinalities.append(end - start + 1)

        if len(categorical_columns) == 0:
            return (X, np.array([]))

        # Combine categorical and non-categorical columns
        categorical_X = np.array(categorical_columns).T
        cardinalities_array = np.array(cardinalities)
        non_categorical_X = X[:, cardinalities_array.sum():]
        decoded_X = np.concatenate((categorical_X, non_categorical_X), axis=1)
        return (decoded_X, cardinalities_array)

    @staticmethod
    def get_dataset(
            name, X, y, task, sample_weight=None, missing_data=False,
            categorical=None, seed=123, perc_test=0.1, perc_valid=0.1, CV=10,
            cv_splits_indices=None, openml_id=None, y_min=None, y_max=None,
            subsample_cache_strategy=SubsampleCacheStrategy.Classic,
            transformers=None, is_time_series=False, test_cutoff=None):
        """
        Get dataset for sub sampling strategy and other parameters.

        This is the method for initializing a dataset if it doesn't already exist.
        It will create all necessary objects.

        :param name:
        :param X: input data
        :param y: label data
        :param sample_weight:
        :param missing_data:
        :param categorical: Boolean array to indicate which features are categorical
        :param task:
        :param seed:
        :param perc_test:
        :param perc_valid:
        :param CV:
        :param cv_splits_indices:
        :param openml_id:
        :param y_min:
        :param y_max:
        :param subsample_cache_strategy:
        :param transformers:
        :param is_time_series:
        :param test_cutoff:
        :return:
        """
        ClientDatasets._check_data(X, y, categorical, missing_data)
        if categorical is not None:
            # allow adding meta_data to prefeaturized datasets
            if type(categorical) == np.ndarray:
                X, y = ClientDatasets._encode_data(X, y, categorical)

        ret = ClientDatasets(subsample_cache_strategy=subsample_cache_strategy)

        cv_splits = _CVSplits(X, y, seed=seed, frac_test=perc_test,
                              frac_valid=perc_valid,
                              CV=CV,
                              is_time_series=is_time_series,
                              test_cutoff=test_cutoff,
                              cv_splits_indices=cv_splits_indices)
        ret.parse_data(
            name=name, task=task, X=X, y=y, sample_weight=sample_weight,
            categorical=categorical, openml_id=openml_id,
            y_min=y_min, y_max=y_max, transformers=transformers,
            cv_splits=cv_splits)
        return ret

    def get_raw_data_type(self):
        """Return the raw data type."""
        return self.raw_data_type

    def get_x_raw_column_names(self) -> Optional[List[str]]:
        """Return the raw column names of X."""
        return self.x_raw_column_names

    def get_X(self):
        """Return X of the training data."""
        return self.get_meta('X')

    def get_X_valid(self):
        """Return X of the validation data."""
        return self.get_meta('X_valid')

    def get_y(self):
        """Return y of the training data."""
        return self.get_meta('y')

    def get_y_valid(self):
        """Return y of the validation data."""
        return self.get_meta('y_valid')

    def get_X_raw(self):
        """Return X of the unfeaturized training data."""
        return self.get_meta('X_raw')

    def get_X_valid_raw(self):
        """Return X of the unfeaturized validation data."""
        return self.get_meta('X_valid_raw')

    def get_y_raw(self):
        """Return y of the unfeaturized training data."""
        return self.get_meta('y_raw')

    def get_y_valid_raw(self):
        """Return y of the unfeaturized validation data."""
        return self.get_meta('y_valid_raw')


if __name__ == '__main__':
    pass
