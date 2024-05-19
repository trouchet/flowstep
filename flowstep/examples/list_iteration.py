from flow import Flow

iter_list = range(10)
skip_condition = lambda x: x > 4 and x < 8
flow = Flow(iter_list, skip_condition, verbose=True)
has_pause = True

for i in flow:
    print(i)

    if has_pause:
        flow.pause()
