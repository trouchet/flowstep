
from typing import Iterable
from flowstep.utils import is_sliceable


class TestUtils:
    def test_is_sliceable_list(self):
        """
        Test if a list is sliceable.
        """
        assert is_sliceable([1, 2, 3]) is True

    def test_is_sliceable_string(self):
        """
        Test if a string is sliceable.
        """
        assert is_sliceable("hello") is True

    def test_is_sliceable_tuple(self):
        """
        Test if a tuple is sliceable.
        """
        assert is_sliceable((1, 2, 3)) is True

    def test_is_sliceable_non_iterable(self):
        """
        Test if a non-iterable object is not sliceable.
        """
        assert is_sliceable(10) is False

    def test_is_sliceable_custom_class_no_getitem(self):
        """
        Test if a custom class without __getitem__ is not sliceable.
        """

        class NoGetItem:
            pass

        assert is_sliceable(NoGetItem()) is False

    def test_is_sliceable_custom_class_with_getitem(self):
        """
        Test if a custom class with __getitem__ is sliceable.
        """

        class WithGetItem(Iterable):
            def __iter__(self):
                return iter([1, 2, 3])

            def __getitem__(self, key):
                return key

        assert is_sliceable(WithGetItem()) == True
