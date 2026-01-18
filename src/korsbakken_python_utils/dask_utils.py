"""Utility functions for working with Dask.

Functions
---------
get_registered_progress_bars:
    Retrieve a set of registered Dask progress bar objects
set_global_progress_bar:
    Sets or replaces a global Dask progress bar.
"""
from collections.abc import Callable
import dataclasses
from io import TextIOBase
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


class _UniqueProgressBar(ProgressBar):
    """A subclass of ProgressBar, which instantiates a single instance,
    returns that instance if instantiated again with the same parameters, and
    removes the previous instance if called with different parameters.

    Class Methods
    -------------
    clear_instances:
        Unregister and clear all stored _UniqueProgressBar instances.
    get_current_instance:
        Retrieve the current _UniqueProgressBar instance, if any. Will also
        check that not more than one instance exists, and raise a RuntimeError
        if that is the case.
    """

    @dataclasses.dataclass(frozen=True, kw_only=True)
    class InitParams:
        """Dataclass for storing the initialization parameters of a
        _UniqueProgressBar instance.

        Defaults are set using the documented default values of
        `dask.diagnostics.progress.ProgressBar` as of version 2026.1.1.
        """
        minimum: int = 0
        width: int = 40
        dt: float = 0.1
        out: TextIOBase | None = None
    ###END class _UniqueProgressBar.InitParams

    _instances: dict[_UniqueProgressBar.InitParams, _UniqueProgressBar] = {}

    @classmethod
    def clear_instances(cls):
        """Clear all stored _UniqueProgressBar instances."""
        for _params, _instance in cls._instances.items():
            _instance.unregister()
            del cls._instances[_params]
    ###END def clear_instances

    @classmethod
    def get_current_instance(cls) -> ProgressBar | None:
        """Retrieve the current _UniqueProgressBar instance, if any.

        Raises
        ------
        RuntimeError
            If more than one _UniqueProgressBar instance exists.

        Returns
        -------
        ProgressBar | None
            The current ProgressBar instance, or None if no instances exist.
        """
        if len(cls._instances) > 1:
            raise RuntimeError("More than one _UniqueProgressBar instance exists.")
        if len(cls._instances) == 1:
            return next(iter(cls._instances.values()))
        return None
    ###END def get_current_instance

    def __new__(
            cls,
            minimum: int = 0,
            width: int = 40,
            dt: float = 0.1,
            out: TextIOBase | None = None,
    ) -> ProgressBar:
        init_params = _UniqueProgressBar.InitParams(
            minimum=minimum,
            width=width,
            dt=dt,
            out=out,
        )
        if init_params in cls._instances:
            return cls._instances[init_params]
        # Remove all existing instances
        cls.clear_instances()
        instance = super().__new__(cls)
        cls._instances[init_params] = instance
        return instance
    ###END def __new__

    def __init__(
            self,
            minimum: int = 0,
            width: int = 40,
            dt: float = 0.1,
            out: TextIOBase | None = None,
    ):
        super().__init__(
            minimum=minimum,
            width=width,
            dt=dt,
            out=out,
        )
        self.register()
    ###END def __init__

###END class _UniqueProgressBar

def set_global_progress_bar(
        minimum: int = 0,
        width: int = 40,
        dt: float = 0.1,
        out: TextIOBase | None = None,
) -> ProgressBar:
    """Sets or replaces a global Dask progress bar.

    If a progress bar with the same parameters already exists, it is reused.
    Otherwise, any existing progress bars are unregistered and removed, and a
    new progress bar is created and registered.

    The parameters are the same as those of
    `dask.diagnostics.progress.ProgressBar`. They are listed below for
    convenience and to confirm compatibility with new dask versions, but please
    refer to the Dask documentation for a description of each parameter.

    Parameters
    ----------
    minimum : int, optional
    width : int, optional
    dt : float, optional
    out : TextIOBase | None, optional

    Returns
    -------
    ProgressBar
        The existing or new global Dask progress bar.
    """
    return _UniqueProgressBar(
        minimum=minimum,
        width=width,
        dt=dt,
        out=out,
    )
###END def set_global_progress_bar
