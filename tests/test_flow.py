import pytest

from flowstep.flow import Flow
from itertools import islice

class TestFlow:
  
  def test_init(self):
    iterable = [1, 2, 3]
    flow = Flow(iterable)

    # Compare the first N elements using islice
    assert list(islice(flow.iterable, 2)) == list(islice(iter(iterable), 2))
    assert flow.iterable is not iter(iterable)  # Assert they are different objects

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

  def test_pause_no_message(self):
    flow = Flow([1, 2, 3])
    next(flow)  # Move to the first item
    flow.pause()
    assert flow.paused
    assert flow.pause_message is None

  def test_pause_with_message(self):
    flow = Flow([1, 2, 3])
    next(flow)  # Move to the first item
    flow.pause("Paused for user input")
    assert flow.paused
    assert flow.pause_message == "Paused for user input"

  def test_resume_not_paused(self):
    flow = Flow([1, 2, 3])
    next(flow)  # Move to the first item
    flow.resume()  # Should have no effect
    assert next(flow) == 2  # Move to the second item

  def test_resume_with_message(self, capsys):
    flow = Flow([1, 2, 3])
    next(flow)  # Move to the first item
    flow.pause()
    flow.set_continue_message("Resuming iteration")
    flow.resume()
    captured = capsys.readouterr()
    assert captured.out == "Resuming iteration\n"
    assert next(flow) == 2  # Move to the second item

  def test_stop(self):
    flow = Flow([1, 2, 3])
    
    # Move to the first item
    next(flow)
    flow.stop()
    with pytest.raises(StopIteration):
      next(flow)

  def test_next_stopped(self):
    flow = Flow([1, 2, 3])
    flow.stop()
    with pytest.raises(StopIteration):
      next(flow)

  def test_next_paused_user_continues(self, monkeypatch):
    flow = Flow([1, 2, 3])
    next(flow)  # Move to the first item
    flow.pause()
    monkeypatch.setattr(input, 'return_value', 'c')  # Simulate user input "c" (continue)
    assert next(flow) == 2  # Move to the second item
    assert not flow.paused

  def test_next_paused_user_continues(self, monkeypatch):
    flow = Flow([1, 2, 3])
    next(flow)  # Move to the first item
    flow.pause()

    # Simulate user input "c" (continue) using monkeypatch
    monkeypatch.setattr(input, 'return_value', 'c')

    assert next(flow) == 2  # Move to the second item
    assert not flow.paused


  