from z3 import *
solver = Optimize()
x = Int('x')
y = Int('y')

solver.add(x >= 0, y >= 0, x + y <= 10)
solver.maximize(x + 2*y)
if solver.check() == sat:
    solution = solver.model()
    print(f"Solution: x = {solution[x]}, y = {solution[y]}")
else:
    print("No solution found")
