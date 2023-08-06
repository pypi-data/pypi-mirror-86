#!/usr/bin/env python3
#
# Copyright 2020 Graviti. All Rights Reserved.
#

"""This file defines class UserSequence, UserMutableSequence"""

from typing import (
    Iterable,
    Iterator,
    List,
    MutableSequence,
    Sequence,
    Tuple,
    TypeVar,
    Union,
    overload,
)

_T = TypeVar("_T")


class UserSequence(Sequence[_T]):
    """This class defines the concept of UserSequence,
    which contains a sequence of object.

    """

    _data: Tuple[_T, ...]

    @overload
    def __getitem__(self, index: int) -> _T:
        ...

    @overload
    def __getitem__(self, index: slice) -> Tuple[_T, ...]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[Tuple[_T, ...], _T]:
        return self._data.__getitem__(index)

    def __len__(self) -> int:
        return self._data.__len__()

    def index(self, value: _T, start: int = 0, end: int = -1) -> int:
        """
        Return first index of value.

        Raises ValueError if the value is not present.
        """

        return self._data.index(value, start, end)

    def count(self, value: _T) -> int:
        """ Return number of occurrences of value. """

        return self._data.count(value)

    def __contains__(self, value: object) -> bool:
        return self._data.__contains__(value)

    def __iter__(self) -> Iterator[_T]:
        return self._data.__iter__()


class UserMutableSequence(MutableSequence[_T]):
    """This class defines the concept of UserMutableSequence,
    which contains a mutable sequence of object.

    """

    _data: List[_T]

    @overload
    def __getitem__(self, index: int) -> _T:
        ...

    @overload
    def __getitem__(self, index: slice) -> List[_T]:
        ...

    def __getitem__(self, index: Union[int, slice]) -> Union[List[_T], _T]:
        return self._data.__getitem__(index)

    @overload
    def __setitem__(self, index: int, value: _T) -> None:
        ...

    @overload
    def __setitem__(self, index: slice, value: Iterable[_T]) -> None:
        ...

    def __setitem__(self, index: Union[int, slice], value: Union[_T, Iterable[_T]]) -> None:
        # https://github.com/python/mypy/issues/7858
        self._data.__setitem__(index, value)  # type: ignore[index, assignment]

    def __len__(self) -> int:
        return self._data.__len__()

    def __delitem__(self, index: Union[int, slice]) -> None:
        self._data.__delitem__(index)

    def insert(self, index: int, value: _T) -> None:
        """ Insert object before index. """

        self._data.insert(index, value)

    def append(self, value: _T) -> None:
        """ Append object to the end of the list. """

        self._data.append(value)

    def clear(self) -> None:
        """ Remove all items from list. """

        self._data.clear()

    def extend(self, value: Iterable[_T]) -> None:
        """ Extend list by appending elements from the iterable. """

        self._data.extend(value)

    def reverse(self) -> None:
        """ Reverse *IN PLACE*. """

        self._data.reverse()

    def pop(self, index: int = -1) -> _T:
        """
        Remove and return item at index (default last).

        Raises IndexError if list is empty or index is out of range.
        """

        return self._data.pop(index)

    def remove(self, value: _T) -> None:
        """
        Remove first occurrence of value.

        Raises ValueError if the value is not present.
        """

        self._data.remove(value)

    def __iadd__(self, value: Iterable[_T]) -> List[_T]:
        return self._data.__iadd__(value)
