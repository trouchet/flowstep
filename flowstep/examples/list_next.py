from flow import Flow

lst=[1,2,3,4,5]
flow = Flow(lst)
print(next(flow))  # Move to the first item

flow.pause()
flow.resume()
print(next(flow))

flow.skip()
print(next(flow))