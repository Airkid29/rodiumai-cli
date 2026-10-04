import inspect, rodiumai
from rodiumai import RodiumAI
print('RodiumAI attrs:')
for name in ['chat','images','videos','wallet','usage','model']:
    print(name, hasattr(RodiumAI, name), getattr(RodiumAI, name, None))
print('module attrs', [a for a in dir(rodiumai) if not a.startswith('_')])
print('client module file', inspect.getsourcefile(RodiumAI))