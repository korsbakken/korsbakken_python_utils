"""Utility functions for working with Dask.

Functions
---------
get_registered_progress_bars:
    Retrieve a set of registered Dask progress bar objects
"""
from collections.abc import Callable
import typing as tp

from dask.diagnostics.progress import ProgressBar



@tp.runtime_checkable
class BoundMethod(tp.Protocol):
    """Protocol for bound methods."""
    __self__: tp.Any
###END class BoundMethod

def get_registered_progress_bars() -> set[ProgressBar]:
    """Retrieve all ProgressBar objects registered globally in Dask.

    Returns
    -------
    set[ProgressBar]
        The set of registered Dask progress bar objects.
    """
    pb_set: set[ProgressBar] = set()
    for _callback_tuple in ProgressBar.active:
        _callback_func: Callable|None = _callback_tuple[0]
        if (
                isinstance(_callback_func, BoundMethod)
                and isinstance(_callback_func.__self__, ProgressBar)
        ):
            pb_set.add(_callback_func.__self__)
    return pb_set
###END def get_registered_progress_bars
