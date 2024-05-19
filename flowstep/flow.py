from typing import Iterable, Dict

from .defaults import (
    Condition,
    default_skip_condition,
    action_default_message,
    PROMPT_MESSAGE,
    IMPERATIVE_ACTIONS,
)


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
        skip_condition: Condition = default_skip_condition,
        verbose: bool = False,
    ):
        self.iterator = iter(iterable)

        self.paused: bool = False
        self.skipped: bool = False
        self.stopped = False

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

    def resume(self, message=None):
        self.paused = False
        self._messages["resume"] = (
            message if message else action_default_message('Resumed', self._counter)
        )

        resume_message = self._messages['resume']
        if resume_message and self.verbose:
            print(resume_message)

    def skip(self, message=None):
        self.skipped = True
        self._messages["skip"] = (
            message if message else action_default_message('Skipped', self._counter)
        )

    def stop(self, message=None):
        self.stopped = True
        self.paused = False
        self._messages["stop"] = (
            message if message else action_default_message('Stopped', self._counter)
        )

    def __print_message(self, action: str, message: str = ''):
        message = self._messages[action]
        if message and self.verbose:
            print(message)

    def __check_skip_condition(self, item: object):
        if self._skip_condition(item) or self.skipped:
            self.skipped = False
            self._counter += 1
            return self.__next__()
        else:
            counter = self._counter
            self._counter += 1
            return (counter, item)

    def _process_pause(self):
        '''
        Process the pause state and handle user input

        The user input is used to determine the next action to take.
        It is case-insensitive and can be one of the following:
        - c: Continue (resume)
        - s: Skip
        - Any other key: Stop
        '''

        self.__print_message('pause')

        # Implement logic for handling pause state
        user_input = input(PROMPT_MESSAGE).lower()

        resume_condition = user_input == "c" or user_input == ""
        skip_condition = user_input == "s"

        if resume_condition:
            self.resume()
            self.__print_message('resume')

        elif skip_condition:
            self.skip()
            self.__print_message('skip')

        else:
            self.stop()
            self.__print_message('stop')

        # Clear the messages after handling pause
        for action in IMPERATIVE_ACTIONS:
            self._messages[action] = None

    def __next__(self):
        """
        Iterates over the underlying iterable with flow control (pause, skip, stop).

        Raises StopIteration when exhausted or explicitly stopped.
        Yields elements, skipping based on conditions and user input during pause.
        """
        if self.stopped:
            raise StopIteration

        while self.paused:
            self._process_pause()

        # Verify if provided
        if self.stopped:
            raise StopIteration

        try:
            item = next(self.iterator)
            return self.__check_skip_condition(item)

        except StopIteration:
            raise

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass
