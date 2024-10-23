# this code is for undirected graphs 
#similar modifications can be used for directed graphs as well 

from z3 import *

nodes = ['A', 'B', 'C', 'D']

edges = [
    ('A', 'B'),
    ('B', 'C'),
    ('A', 'C'),
    ('C', 'D')
]

start_node = 'A'
end_node = 'D'

s = Solver()

reachable = {node: Bool(f'reachable_{node}') for node in nodes}

s.add(reachable[start_node] == True)

for (u, v) in edges:
    s.add(Implies(reachable[u], reachable[v]))
    s.add(Implies(reachable[v], reachable[u]))

s.add(reachable[end_node] == True)

if s.check() == sat:
    print(f"path exists from {start_node} to {end_node}.")
else:
    print(f"No path exists from {start_node} to {end_node}.")
