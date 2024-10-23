from z3 import *
square=Int('square')
triangle=Int('triangle')
circle=Int('circle')
solver = Solver()
solver.add(square+square==8)
solver.add(triangle*triangle==16)
solver.add(triangle*circle==35)

if solver.check() == sat:
    print(solver.model())
else:
    print("NOT POSSIBLE")
