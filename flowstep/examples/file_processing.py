from flow import Flow

from random import choice


def to_be_or_not_to_be():
    return choice([True, False])


filenames = ["file1.txt", "file2.txt", "file3.txt", "file4.txt", "file5.txt"]

flow = Flow(filenames, verbose=True)

for index, filename in flow:
    try:
        print(f"Processing file: {filename}")

        if to_be_or_not_to_be():
            raise Exception(f"File processing of {filename} failed.")

    except Exception as e:
        flow.pause(f"Filename {filename} is paused. Error: {e}")
