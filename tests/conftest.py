import pytest

@pytest.fixture
def iterable():
    return [1, 2, 3, 4]


class EmptyIterable:
    def __iter__(self):
        return iter([])

@pytest.fixture
def empty_iterable():     
    return EmptyIterable()