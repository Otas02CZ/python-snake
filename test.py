from DisplayServer import DisplayServer, OBSTACLE
from time import time
from os import system

ds = DisplayServer(50, 50, True, OBSTACLE)
results = [0, 0]
for i in range(10000):
    timestamp = time() * 1000
    ds.draw_normal()
    results[0] += time() * 1000 - timestamp
for i in range(10000):
    timestamp = time() * 1000
    ds.draw_optimised()
    results[1] += time() * 1000 - timestamp

print()
print("unoptimised took " + str(results[0]) + "ms")
print("optimised took " + str(results[1]) + "ms")
