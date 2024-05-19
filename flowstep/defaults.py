from typing import Callable

# Type aliases for readability
Condition = Callable[[object], bool]


# Default skip condition and message callback
def default_skip_condition(item: object):
    return False


def default_skip_message_callback():
    return ''


# Default message for pause, resume, and skip actions
PROMPT_MESSAGE = "Paused for user input (c: continue, s: skip, other: stop): "

# Actions that can be performed on the flow
IMPERATIVE_ACTIONS = ['pause', 'resume', 'skip', 'stop']
PAST_ACTIONS = ['Paused', 'Resumed', 'Skipped', 'Stopped']


# Default message for pause, resume, skip, and stop actions
def action_default_message(action: str, counter: int):
    if action not in PAST_ACTIONS:
        raise ValueError(f"Action {action} not supported")
    else:
        return f"{action.capitalize()} at item count {counter + 1}"
