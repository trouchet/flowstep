import pytest
from unittest.mock import patch  # For mocking user input

from flowstep.flow import Flow
from flowstep.defaults import (
    default_skip_message_callback,
    PROMPT_MESSAGE,
    action_default_message,
    PAST_ACTIONS,
)


class TestFlow:

    def test_init(self, iterable):
        skip_condition = lambda x: x % 2 == 0  # Skip even numbers

        flow = Flow(iterable, skip_condition=skip_condition)

        assert flow.iterator is not iter(iterable)
        assert flow.paused is False
        assert flow.skipped is False
        assert flow._skip_condition == skip_condition

    def test_iter(self, iterable):
        flow = Flow(iterable)
        assert iter(flow) is flow

    def test_counter(self, iterable):
        flow = Flow(iterable)
        assert flow._counter == 0

    def test_current_item(self, iterable):
        flow = Flow(iterable)
        assert flow.current_item is None

    def test_verbose(self, iterable):
        flow = Flow(iterable, verbose=True)
        assert flow.verbose is True

    def test_default_skip_condition(self):
        flow = Flow([])
        assert flow._skip_condition(1) is False
        assert flow._skip_condition(2) is False
        assert flow._skip_condition(42) is False

    def test_default_skip_message_callback(self):
        assert default_skip_message_callback() == ''

    def test_stop_on_pause(self, iterable):
        flow = Flow(iterable)
        flow.stop()
        assert flow.stopped is True

    def test_iter_exhausted(self, empty_iterable):
        flow = Flow(empty_iterable)
        with pytest.raises(StopIteration):
            next(flow)
    
    @patch('flowstep.flow.Flow._get_user_input')
    def test_flow_pause_and_stop(self, mocker, iterable):
        flow = Flow(iterable)
        
        mocker.return_value = 'c'  # Stop the flow

        # Simulate first iteration
        item = next(flow)
        assert item == (0, 1)  # First item

        # Pause the flow
        flow.pause()

        # Verify stopped flag is not set yet
        assert not flow.stopped

        # Mock wouldn't trigger loop exit, process pause manually
        flow._process_pause()

        # Verify flow is resumed after user input ("resume")
        assert not flow.paused

        # Iterate again and check next item
        item = next(flow)
        assert item == (1, 2)  # Second item

        # Stop the flow explicitly
        flow.stop()

        # Verify stopped flag is set
        assert flow.stopped

        # Raise StopIteration on further iteration
        with pytest.raises(StopIteration):
            next(flow)

    def test_stop_exhaust_iteration(self, empty_iterable):
        flow = Flow([1, 2])  # Create a Flow object with a custom iterable
        next(flow)  # Move to the first item
        next(flow)  # Move to the second item

        # This will raise StopIteration when iterating over the empty iterable
        with pytest.raises(StopIteration):
            next(flow)

    def test_enter(self):
        flow = Flow([])
        with flow:
            pass
        assert True  # No exception raised

    def test_exit(self):
        flow = Flow([])
        with flow:
            pass
        # No specific cleanup needed, so nothing to assert in exit

    @patch('builtins.input')  # Mock user input for pause testing
    def test_pause_no_message(self, mock_input, iterable):
        # Simulate user continuing
        mock_input.return_value = "c"

        flow = Flow(iterable)
        next(flow)  # Move to the first item

        flow.pause()
        assert flow.paused
        assert flow._messages['pause'] == 'Paused at item count 2'

        flow.resume()

        assert next(flow) == (1, 2)  # Move to the second item

    @patch('builtins.input')  # Mock user input for pause testing
    def test_pause_no_message(self, mock_input, iterable):
        # Simulate user stop
        mock_input.return_value = "x"

        flow = Flow(iterable)
        next(flow)  # Move to the first item

        flow.pause()
        assert flow.paused
        assert flow._messages['pause'] == 'Paused at item count 2'

        # Call _process_pause directly to trigger user input handling
        flow._process_pause()

        assert flow.stopped

        with pytest.raises(StopIteration):
            next(flow)

    @patch('builtins.input')
    def test_pause_with_message_and_skip(self, mock_input, iterable):
        flow = Flow(iterable)

        # Move to the first item
        next(flow)

        flow.pause("Paused for user input")
        assert flow.paused
        assert flow._messages['pause'] == "Paused for user input"

        # Simulate user skipping
        flow.skip()

        # Skipping happens within pause loop
        flow.resume()

        # Move to the third item (assuming skip in pause loop)
        assert next(flow) == (2, 3)

    def test_resume_not_paused(self, iterable):
        flow = Flow(iterable)

        # Move to the first item
        next(flow)

        # Should have no effect
        flow.resume()

        # Move to the second item
        assert next(flow) == (1, 2)

    def test_stop(self, iterable):
        flow = Flow(iterable)

        # Move to the first item
        next(flow)
        flow.stop()
        with pytest.raises(StopIteration):
            next(flow)

    @patch('builtins.input')
    def test_resume_with_message(self, mock_input, iterable):
        # Simulate user continuing
        mock_input.return_value = "c"

        flow = Flow(iterable)

        # Move to the first item
        next(flow)
        flow.pause()

        # Simulate user continuing
        flow.resume()

        # Move to the second item
        assert next(flow) == (1, 2)

    @patch('builtins.input')
    def test_process_pause_resume(self, mocker, iterable):
        """Tests flow pause and resume functionality with user input 'c' (continue)."""
        # Simulate user continuing
        mocker.return_value = "c"

        # Create a Flow object with a sample iterable
        flow = Flow(iterable)

        # Call next to initiate flow and enter pause state (assuming some logic pauses it)
        next(flow)
        flow.pause()

        # Assert that flow is paused before processing pause
        assert flow.paused is True

        # Call process_pause to handle pause logic
        flow._process_pause()

        # Assert that flow is resumed after processing pause with 'c' input
        assert flow.paused is False

    @patch('builtins.input')
    def test_process_pause_skip(self, mocker, iterable):
        """Tests flow pause and skip functionality with user input 's' (skip)."""
        # Mock user input to return 's' (skip)
        mocker.return_value = 's'

        # Create a Flow object with a sample iterable
        flow = Flow(iterable)

        # Call next to initiate flow and enter pause state
        next(flow)
        flow.pause()

        # Assert that flow is paused before processing pause
        assert flow.paused is True

        # Call process_pause to handle pause logic
        flow._process_pause()

        # Assert that flow is not paused (resumed)
        # and skipped is True after processing pause with 's' input
        assert flow.paused is True
        assert flow.skipped is True

    def test_next_stopped(self, iterable):
        flow = Flow(iterable)
        flow.stop()

        with pytest.raises(StopIteration):
            next(flow)

    def test_skip_condition(self, iterable):
        is_even = lambda x: x % 2 == 0
        flow = Flow(iterable, skip_condition=is_even)
        item = next(flow)

        # First item (odd) is processed
        assert item == (0, 1)

        with pytest.raises(StopIteration):
            flow.stopped = True

            # Stop after first item
            next(flow)

    @patch('builtins.input')  # Patch the input function
    @patch('builtins.print')  # Patch the print function
    def test_print_messages(self, mock_input, mock_print, iterable):
        flow = Flow(iterable, verbose=True)

        # Simulate setting messages
        flow._messages['pause'] = (
            "Paused for user input (c: continue, s: skip, other: stop)"
        )
        flow._messages['skip'] = "Item skipped"
        flow._messages['resume'] = "Resuming iteration"

        # Simulate pause scenario
        flow.pause()

        # Mock user input to skip (modify as needed for other actions)
        mock_input.return_value = "s"
        flow._process_pause()

        # Assert print calls
        mock_print.assert_called_with(PROMPT_MESSAGE)

    # test_messages.py
    def test_action_default_message_valid(self):
        """Tests the action_default_message function with valid inputs."""
        for action in PAST_ACTIONS:
            message = action_default_message(action, 10)
            assert message == f"{action.capitalize()} at item count 11"

    def test_action_default_message_invalid(self):
        """Tests the action_default_message function with an invalid action."""
        with pytest.raises(ValueError) as excinfo:
            action_default_message("Foo", 5)  # Invalid action

        assert excinfo.value.args[0] == "Action Foo not supported"

    def test_get_item_at_step_success(self, iterable):
        flow = Flow(iterable)
        
        # Test getting item at specific step
        assert flow._get_item_at_step(1) == (1, 2)
        assert flow.restart_on_get_item == True

    def test_get_item_at_step_out_of_bounds_low(self):
        iterable = ["apple", "banana", "cherry"]
        flow = Flow(iterable)

        with pytest.raises(ValueError):
            flow._get_item_at_step(-1)

    def test_get_item_at_step_out_of_bounds_high(self):
        iterable = ["apple", "banana", "cherry"]
        flow = Flow(iterable)

        with pytest.raises(ValueError):
            flow._get_item_at_step(4)