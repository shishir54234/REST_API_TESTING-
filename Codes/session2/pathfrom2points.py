from z3 import *


#Implementation of if they are in the same component basically
# if it was a directed graph then we can use the same code
# while changing some relations 
#  cf. https://ericpony.github.io/z3py-tutorial/fixpoint-examples.htm

fp = Fixedpoint()
fp.set(engine='datalog')

#  3 bits are sufficient to model our 6 nodes
s = BitVecSort(3)
edge = Function('edge', s, s, BoolSort())
path = Function('path', s, s, BoolSort())
a = Const('a', s)
b = Const('b', s)
c = Const('c', s)

#  the rules:
#  a path can be a single edge or
#  a combination of a path and an edge
fp.register_relation(path,edge)
fp.declare_var(a, b, c)
# if edge from a to b then there is also a path a to b
fp.rule(path(a, b), edge(a, b))
# if path from a to b exists then there is also a path a to c if path from b to c also exists 
fp.rule(path(a, c), [path(a, b), path(b, c)])

n1 = BitVecVal(1, s) # 001
n2 = BitVecVal(2, s) # 010
n3 = BitVecVal(3, s) # 011
n4 = BitVecVal(4, s)  #100
n5 = BitVecVal(5, s) #101
n6 = BitVecVal(6, s)
n7 = BitVecVal(7, s)

graph = {n1: [n2, n6, n7],
         n2: [n3, n5],
         n3: [n4, n5, n6],
         n4: [n3],
         n5: [n2, n3],
         n6: [n3, n1]}

#  establish facts by enumerating the graph dictionary
for i, (source, nodes) in enumerate(graph.items()):
    for destination in nodes:
        fp.fact(edge(source, destination))

print("current set of rules:\n", fp)

print(fp.query(path(n1, n4)), "yes, we can reach n4 from n1\n")

print(fp.query(path(n7, n1)), "no, we cannot reach n1 from n7\n")