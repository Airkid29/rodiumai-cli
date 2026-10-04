import inspect
from rodiumai import RodiumAI
print(RodiumAI)
print('INIT', inspect.signature(RodiumAI))
print('METHODS', [m for m in dir(RodiumAI) if not m.startswith('_')][:100])
print('MODULE', RodiumAI.__module__)