from z3 import *

def n_rooks(N):
    solver = Solver()
    rooks = [Int(f'Q_{i}') for i in range(N)]
    for i in range(N):
        solver.add(And(rooks[i] >= 0, rooks[i] < N))
    
    # solver.add(rooks)
    
    for i in range(N):
        for j in range(i + 1, N):
            solver.add(rooks[i] != rooks[j])
            #solver.add(rooks[i] != rooks[j])
    
    if solver.check() == sat:
        solution = solver.model()
        board = [['.' for _ in range(N)] for _ in range(N)]
        for i in range(N):
            col = solution[rooks[i]].as_long()
            board[i][col] = 'Q'
        for row in board:
            print(' '.join(row))
    else:
        print("No solution found")

n_rooks(8)
