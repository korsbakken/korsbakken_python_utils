"""Module for the DataObject class

Classes
-------
DataObject
    A basic object class that can be initialized with any set of attributes as
    keyword arguments, provides a readable string representation, and allows
    setting and getting attributes using dictionary-like syntax.
"""
from collections.abc import (
    Iterator,
    MutableMapping,
)
import typing as tp


class DataObject(MutableMapping):
    """A basic object class that can be initialized with any set of attributes
    as keyword arguments, provides a readable string representation, and allows
    setting and getting attributes using dictionary-like syntax.

    Examples
    --------
    >>> obj = DataObject(name="Kari", age=30)
    >>> print(obj)
    DataObject(name='Kari', age=30)
    >>> obj['city'] = 'Drammen'
    >>> print(obj.city)
    Drammen
    >>> print(obj['age'])
    30
    >>> obj.country = 'Noreg'
    >>> print(obj)
    DataObject(name='Kari', age=30, city='Drammen', country='Noreg')
    """

    def __init__(self, **kwargs: tp.Any) -> None:
        """
        Parameters
        ----------
        **kwargs : Any
            Arbitrary keyword arguments to set as attributes of the object.
        """
        for key, value in kwargs.items():
            setattr(self, key, value)
    ###END DataObject.__init__

    def __getitem__(self, key: str) -> tp.Any:
        # If __getitem__ is called, it means that the key is being accessed like
        # a dictionary key rather than an attribute. We should therefore use
        # self.__dict__.__getitem__ rather than getattr(self, ...), so that a
        # KeyError is raised rather than an AttributeError if they key does not
        # exist.
        return self.__dict__[key]
    ###END DataObject.__getitem__

    def __setitem__(self, key: str, value: tp.Any) -> None:
        setattr(self, key, value)
    ###END DataObject.__setitem__

    def __delitem__(self, key: str) -> None:
        delattr(self, key)
    ###END DataObject.__delitem__

    def __iter__(self) -> Iterator[str]:
        return iter(self.__dict__)
    ###END DataObject.__iter__

    def __len__(self) -> int:
        return len(self.__dict__)
    ###END DataObject.__len__

    def __repr__(self) -> str:
        attrs: str = ',\n    '.join(
            f"{key}={repr(value)}" for key, value in self.__dict__.items()
        )
        return f'{self.__class__.__name__}(\n    {attrs}\n)'
    ###END DataObject.__repr__

    def __str__(self) -> str:
        attrs: str = ', '.join(
            f"{key}={repr(value)}" for key, value in self.__dict__.items()
        )
        return f'{self.__class__.__name__}({attrs})'
    ###END DataObject.__str__

    def to_dict(
            self,
            copy: bool = True,
    ) -> dict[str, tp.Any]:
        """Convert the DataObject to a dictionary.

        Parameters
        ----------
        copy : bool, optional
            If True, returns a shallow copy of the attributes dictionary.
            If False, returns the actual attributes dictionary, in which case
            modifications to the returned dictionary will affect the DataObject.
            There is no option to return a deep copy. If you need a deep copy,
            instead set `copy=False` and then use `copy.deepcopy()` on the
            result. Default is True.

        Returns
        -------
        dict[str, Any]
            A dictionary representation of the DataObject's attributes.
        """
        if copy:
            return self.__dict__.copy()
        else:
            return self.__dict__
    ###END DataObject.to_dict

    def to_tuples(self) -> list[tuple[str, tp.Any]]:
        """Convert the DataObject's attributes to a list of key-value tuples.

        Returns
        -------
        list[tuple[str, Any]]
            A list of tuples where each tuple contains an attribute name and its
            corresponding value.
        """
        return list(self.__dict__.items())
    ###END DataObject.to_tuples

###END class DataObject
