import pytest
from flowstep.flowstep import ControlledIteration

class TestControlledIteration:

    @pytest.fixture
    def iterable(self):
        return ["Item 1", "Item 2", "Item 3"]

    def test_init(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        assert controlled_iter.iterable is iter(iterable)
        assert not controlled_iter.paused
        assert not controlled_iter.stopped
        assert controlled_iter.pause_message is None
        assert controlled_iter.continue_message is None
        assert controlled_iter.skip is False

    def test_enter(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        with controlled_iter:
            pass
        # No specific assertions needed as __enter__ doesn't perform actions

    def test_exit(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        with controlled_iter:
            pass
        # No specific assertions needed as __exit__ doesn't perform actions

    def test_pause_no_message(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        controlled_iter.pause()
        assert controlled_iter.paused
        assert controlled_iter.pause_message is None

    def test_pause_with_message(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        controlled_iter.pause("Paused for maintenance.")
        assert controlled_iter.paused
        assert controlled_iter.pause_message == "Paused for maintenance."

    def test_resume_not_paused(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        controlled_iter.resume()
        assert not controlled_iter.paused
        assert controlled_iter.continue_message is None

    def test_resume_with_message(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        controlled_iter.pause("Paused for maintenance.")
        controlled_iter.set_continue_message("Resuming iteration.")
        controlled_iter.resume()
        assert not controlled_iter.paused
        assert controlled_iter.continue_message is None

        # Check message was printed
        captured = pytest.capture.allcalls
        assert any(call.args[0] == "Resuming iteration." for call in captured)

    def test_stop(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        controlled_iter.stop()
        assert controlled_iter.stopped

    def test_iteration_normal(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        for item in controlled_iter:
            assert item in iterable

    def test_iteration_pause(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        with pytest.raises(StopIteration):
            for item in controlled_iter:
                assert item in iterable
                if item == "Item 1":
                    controlled_iter.pause("Taking a break.")
                    user_input = "q"  # Simulate stopping during pause
                    controlled_iter.__next__()  # Trigger pause handling
                    assert controlled_iter.stopped

    def test_iteration_skip(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        for item in controlled_iter:
            assert item in iterable
            if item == "Item 1":
                controlled_iter.pause("Skip this item?")
                user_input = "s"  # Simulate skipping
                controlled_iter.__next__()  # Trigger pause handling
                assert item != next(controlled_iter)  # Verify skip

    def test_iteration_skip_multiple(self, iterable):
        controlled_iter = ControlledIteration(iterable)
        for item in controlled_iter:
            assert item in iterable
            if item == "Item 1":
                controlled_iter.pause("Skip this item?")
                user_input = "s"  # Simulate skipping
                controlled_iter.__next__()  # Trigger pause handling
            if item == "Item 2":
                controlled_iter.pause("Skip this too?")
                user_input = "s"  # Simulate skipping
                controlled_iter.__next__()  # Trigger pause handling
                assert item != next(controlled_iter)  # Verify skip

    def test_set_continue_message(self):
        controlled_iter = ControlledIteration(iterable)
        controlled_iter.set_continue_message("Continuing...")
        assert controlled_iter.continue_message ==
