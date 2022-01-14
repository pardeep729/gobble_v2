import random
import math

arrangements = ['a', 'b', 'c']
results = [random.randint(0,len(arrangements)-1) for _ in range(10000)]

print(max(results), min(results), sum(results)/len(results))