from typing import Iterable, Dict

from .defaults import (
    Condition,
    default_skip_condition,
    action_default_message,
    PROMPT_MESSAGE,
    IMPERATIVE_ACTIONS,
)
from .logging_ import logger


class Flow:
    """
    Provides flow control functionalities for iterables.

    Args:
        iterable: The iterable to iterate over.
        messages: Optional dictionary with messages for pause, resume, and skip actions.
        conditions: Optional function that takes the current item and returns True to skip.
    """

    def __init__(
        self,
        iterable: Iterable,
        total: int = None,
        skip_condition: Condition = default_skip_condition,
        verbose: bool = False,
        restart_on_get_item: bool = True,
    ):
        self.total = len(list(iterable)) if total is None else total
        self.iterator = iter(iterable)

        self.paused: bool = False
        self.skipped: bool = False
        self.stopped = False
        self.restart_on_get_item = restart_on_get_item

        self._messages: Dict = {
            "pause": None,
            "resume": None,
            "skip": None,
            "stop": None,
        }

        self._counter: int = 0
        self.current_item: object = None

        self._skip_condition = skip_condition

        self.verbose = verbose

    def __iter__(self):
        return self

    def pause(self, message=None):
        self.paused = True
        self._messages["pause"] = (
            message if message else action_default_message('Paused', self._counter)
        )

        self.__print_message('pause')

    def resume(self, message=None):
        self.paused = False
        self._messages["resume"] = (
            message if message else action_default_message('Resumed', self._counter)
        )

        self.__print_message('resume')

    def skip(self, message=None):
        self.skipped = True
        self._messages["skip"] = (
            message if message else action_default_message('Skipped', self._counter)
        )

        self.__print_message('skip')

    def stop(self, message=None):
        self.stopped = True
        self.paused = False
        self._messages["stop"] = (
            message if message else action_default_message('Stopped', self._counter)
        )

        self.__print_message('stop')

    def __print_message(self, action: str, message: str = ''):
        message = self._messages[action]
        if message and self.verbose:
            logger.info(message)

    def __check_skip_condition(self, item: object):
        if self._skip_condition(item) or self.skipped:
            self.skipped = False
            self._counter += 1
            return self.__next__()
        else:
            counter = self._counter
            self._counter += 1
            return (counter, item)

    def _get_user_input(self):
        """
        Retrieves user input during pause state.

        This method can be implemented to prompt the user for input (e.g., resume, skip, stop)
        and return the user's choice. You can use libraries like `input` or more advanced UI toolkits.

        By default, this method simply returns an empty string.

        Override this method for custom user input handling during pauses.
        """
        return input(PROMPT_MESSAGE).lower()

    def _process_pause(self):
        '''
        Process the pause state and handle user input

        The user input is used to determine the next action to take.
        It is case-insensitive and can be one of the following:
        - c: Continue (resume)
        - s: Skip
        - Any other key: Stop
        '''

        # Implement logic for handling pause state
        user_input = self._get_user_input()

        # Handle user input
        resume_condition = user_input == "c" or user_input == ""
        skip_condition = user_input == "s"

        # Process the user input
        if resume_condition:
            self.resume()
        elif skip_condition:
            self.skip()
        else:
            self.stop()

        # Clear the messages after handling pause
        for action in IMPERATIVE_ACTIONS:
            self._messages[action] = None

    def __next__(self):
        """
        Iterates over the underlying iterable with flow control (pause, skip, stop).

        Raises StopIteration when exhausted or explicitly stopped.
        Yields elements, skipping based on conditions and user input during pause.
        """
        # Verify if stopped
        if self.stopped:
            raise StopIteration

        # Process pause state
        while self.paused:
            self._process_pause()

        # Verify if stopped after processing pause
        if self.stopped:
            raise StopIteration

        # Get the next item
        try:
            item = next(self.iterator)
            return self.__check_skip_condition(item)

        # Raise StopIteration when exhausted
        except StopIteration:
            raise

    def fast_forward(self, steps: int):
        for i in range(steps):
            try:
                self.__next__()

            except StopIteration:
                # We don't need to raise it here, as the loop will terminate
                pass

            except Exception as e:
                error_message = f"Error fast-forwarding the iterator at index {i}: {e}"
                logger.error(error_message)

    def _get_item_at_step(self, step: int):
        """
        Retrieves the item at a specific step within the iterator by advancing it.

        This approach works for any iterable, but might be less efficient for large datasets.

        Args:
            step: The step position of the desired item.

        Returns:
            The item at the specified step.

        Raises:
            ValueError: If the requested step is outside the valid range.
        """
        # Check bounds using temporary list
        if step < self._counter or step >= self.total:
            raise ValueError("Requested step is outside the valid range.")

        # Reset the iterator to the target step
        counter_value = self._counter
        self.fast_forward(step)

        # Get the item at the target step
        item = self.__next__()

        # Optionally reset the iterator and counter for restart after processing
        if self.restart_on_get_item:
            self.iterator = iter(self.iterator)
            self.fast_forward(counter_value)

        return item

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
