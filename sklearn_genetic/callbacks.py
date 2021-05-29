from collections.abc import Callable
from .parameters import Metrics


def check_stats(metric):
    if metric not in Metrics.list():
        raise ValueError(f'metric must be one of {Metrics.list()}, but got {metric} instead')


def check_callback(callback):
    """
    Check if callback is a callable or a list of callables.
    """
    if callback is not None:
        if isinstance(callback, Callable):
            return [callback]

        elif (isinstance(callback, list) and
              all([isinstance(c, Callable) for c in callback])):
            return callback

        else:
            raise ValueError("callback should be either a callable or a list of callables.")
    else:
        return []


def eval_callbacks(callbacks, record):
    """Evaluate list of callbacks on result.
    Parameters
    ----------
    callbacks : list of callables
        Callbacks to evaluate.
    record : logbook record
    Returns
    -------
    decision : bool
        Decision of the callbacks whether or not to keep optimizing
    """
    stop = False
    if callbacks:
        for c in callbacks:
            decision = c(record)
            if decision is not None:
                stop = stop or decision

    return stop


class ThresholdStopping:
    """
    Stop the optimization if the cross validation score is greater or equals than the define threshold
    """

    def __init__(self, threshold: float = None, metric: str = 'fitness'):
        """
        Parameters
        ----------
        threshold: float, default=None
            Threshold to compare against the current cross validation average score and determine if
            the optimization process must stop
        metric: str, default ='fitness'
            Name of the metric inside 'record' logged in each iteration
        """

        check_stats(metric)

        self.threshold = threshold
        self.metric = metric

    def _check(self, record: dict = None):
        """
        Parameters
        ----------
        record: dict: default=None
            A logbook record

        Returns
        -------
        decision: bool
            True if the optimization algorithm must stop, false otherwise
        """

        return record[self.metric] >= self.threshold

    def __call__(self, record):
        return self._check(record)