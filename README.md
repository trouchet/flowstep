# Flowstep

[![Version](https://img.shields.io/pypi/v/flowstep.svg)](https://pypi.python.org/pypi/flowstep)
[![downloads](https://img.shields.io/pypi/dm/flowstep)](https://pypi.org/project/flowstep/)

[![codecov](https://codecov.io/gh/trouchet/flowstep/branch/main/graph/badge.svg?token=PJMBaLIqar)](https://codecov.io/gh/trouchet/flowstep)
[![Lint workflow](https://github.com/trouchet/flowstep/actions/workflows/check-lint.yaml/badge.svg)](https://github.com/trouchet/flowstep/actions/workflows/check-lint.yaml)

Flowstep is a Python library that provides enhanced control flow functionalities for iterating over iterables. It allows you to pause, resume, skip, or stop the iteration process based on conditions and user interaction.

## Key Features:

- Pause and Resume Iteration: Temporarily halt the iteration and resume at your convenience.
- Conditional Skipping: Define custom logic to skip specific elements based on your criteria.
- User Interaction: Interact with the flow during pauses to choose the next action (resume, skip, or stop).
- Clear Messaging: Receive informative messages during pauses and actions (optional).
- Context Manager Integration: Use Flowstep within a with statement for easy flow management.

## Benefits:

- Streamline complex iteration logic: Easily manage complex workflows with conditional processing and user interaction.
- Improve code readability: Separate iteration logic from your core functionality for better maintainability.
- Enhance user experience: Provide users with control over the processing flow, especially for large datasets.

## Installation:

```bash
pip install flowstep
```

Use o código com cuidado.

## Usage:

Here's a basic example demonstrating how to use Flowstep to iterate over a list with conditional skipping and informative messages:

```Python
from flowstep import Flow

data = [1, 2, 3, 4, 5]
skip_condition = lambda x: x % 2 == 0  # Skip even numbers

with Flow(data, skip_condition=skip_condition, verbose=True) as flow:
  for index, item in flow:
    print(f"Processing item: {item} (Index: {index})")
```

This code iterates over the data list, skipping even numbers based on the provided skip_condition function. During pauses (triggered by user input), the library will display informative messages to guide the user's choice (resume, skip, or stop).


# Contributing:

We welcome contributions to Flowstep! Feel free to submit pull requests for bug fixes, new features, or improvements. Make sure to add appropriate tests and update the documentation request as needed.

# License:

Flowstep is distributed under the [License Name] License. See the LICENSE file for details.

Take control of your iterations with Flowstep!
