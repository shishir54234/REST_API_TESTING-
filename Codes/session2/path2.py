# this path exists in the graph lets say, can we find the path from A to D with the lowest weight in a graph using smt solvers

from z3 import *

nodes = ['A', 'B', 'C', 'D']

edges = {
    ('A', 'B'): 1,
    ('B', 'C'): 2,
    ('A', 'C'): 2,
    ('C', 'D'): 1
}

start_node = 'A'
end_node = 'D'

s = Optimize()

edge_used = {edge: Bool(f'used_{edge[0]}_{edge[1]}') for edge in edges}

distances = {node: Int(f'distance_{node}') for node in nodes}

s.add(distances[start_node] == 0)

for node in nodes:
    if node != start_node:
        s.add(distances[node] > 0)

for (u, v), weight in edges.items():
    # s.add(Implies(edge_used[(u, v)], distances[v] == distances[u] + weight))
    # s.add(Implies(edge_used[(u, v)], distances[u] == distances[v] + weight))
    s.add(Implies(edge_used[(u, v)], Or(distances[v] == distances[u] + weight, distances[u] == distances[v] + weight)))

s.add(distances[end_node] > 0)

s.minimize(distances[end_node])

if s.check() == sat:
    model = s.model()
    print(f"A path exists from {start_node} to {end_node} with the lowest weight.")
    # path = []
    # current_node = start_node
    # for (u, v) in edges:
    #     if model.eval(edge_used[(u, v)], model_completion=True):
    #         if model.eval(distances[v] == distances[u] + edges[(u, v)]):
    #             path.append((u, v))
    #             current_node = v
    #             break
    #         elif model.eval(distances[u] == distances[v] + edges[(u, v)]):
    #             path.append((v, u))
    #             current_node = u
    #             break
        
    # print("Path:", ' -> '.join([start_node] + [v for _, v in path]))
    print("Total Weight:", model.eval(distances[end_node]))
else:
    print(f"No path exists from {start_node} to {end_node}.")
