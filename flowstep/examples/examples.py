from flow import Flow

from logging_ import logger
from .utils import random_bool


class ExampleBatch:
    def __init__(self):
        self.logger = logger

    @staticmethod
    def _test_wrapper(func):
        def wrapper(*args, **kwargs):
            # Print test name and description before running the test
            print(f"\n** Test: {func.__name__} **")
            print(f"{func.__doc__}")
            func(*args, **kwargs)

        return wrapper

    @_test_wrapper
    def example_next(self):
        """
        This test demonstrates basic Flow usage with pause, resume, and skip operations.
        """
        lst = [1, 2, 3, 4, 5]
        flow = Flow(lst)
        print(next(flow))  # Move to the first item

        flow.pause()
        flow.resume()
        print(next(flow))

        flow.skip()
        print(next(flow))

    @_test_wrapper
    def example_list_flow(self, length: int = 10, lower: int = 4, upper: int = 8):
        """
        This test showcases Flow iteration with a custom skip condition on a list.
        """
        iter_list = range(length)

        def skip_condition(x: int):
            return x > lower and x < upper

        flow = Flow(iter_list, skip_condition, verbose=True)
        has_pause = True

        for i in flow:
            print(i)

            if has_pause:
                flow.pause()

    @_test_wrapper
    def example_file_flow(self):
        """
        This test simulates Flow usage with file processing and error handling.
        """
        filenames = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]

        flow = Flow(filenames, verbose=True)

        for index, filename in flow:
            try:
                print(f"Processing file: {filename}")

                if random_bool():
                    raise Exception(f"File processing of {filename} failed.")

            except Exception as e:
                self.logger.error(f"Filename {filename} is paused. Error: {e}")
                flow.pause(f"Filename {filename} is paused. Error: {e}")

    def run(self):
        # Call test methods directly from within run()
        self.example_next()
        self.example_list_flow()
        self.example_file_flow()


if __name__ == "__main__":
    ExampleBatch().run()
