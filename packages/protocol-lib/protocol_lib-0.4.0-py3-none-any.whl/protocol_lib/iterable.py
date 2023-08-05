from typing import TypeVar

from typing_extensions import Protocol, runtime_checkable

__all__ = [
    "Iterable",
    "Iterator",
]


T = TypeVar("T", covariant=True)


@runtime_checkable
class Iterable(Protocol[T]):
    def __iter__(self) -> "Iterator[T]":
        ...


@runtime_checkable
class Iterator(Protocol[T]):
    def __iter__(self) -> "Iterator[T]":
        ...

    def __next__(self) -> T:
        ...
