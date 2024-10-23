from z3 import *

def main():
    # Create a solver
    s = Solver()

    # Define sorts
    Node = DeclareSort('Node')
    Var = DeclareSort('Var')

    # Define relations
    succ = Function('succ', Node, Node, BoolSort())
    use = Function('use', Node, Var, BoolSort())
    defn = Function('def', Node, Var, BoolSort())
    live_in = Function('live_in', Node, Var, BoolSort())
    live_out = Function('live_out', Node, Var, BoolSort())
    
    # Define variables
    n, m = Consts('n m', Node)
    v = Const('v', Var)
    a, b, c, d, e = Consts('a b c d e', Var)

    # Define rules
    s.add(ForAll([n, v], Implies(And(live_out(n, v), Not(defn(n, v))), live_in(n, v))))
    s.add(ForAll([n, v], Implies(use(n, v), live_in(n, v))))
    s.add(ForAll([n, m, v], Implies(And(succ(n, m), live_in(m, v)), live_out(n, v))))

    # Define program structure
    n1, n2, n3, n4, n5, n6, n7, n8 = Consts('n1 n2 n3 n4 n5 n6 n7 n8', Node)

    # Define CFG (more complex with a loop and a conditional branch)
    s.add(succ(n1, n2))  # n1 -> n2
    s.add(succ(n2, n3))  # n2 -> n3
    s.add(succ(n3, n4))  # n3 -> n4
    s.add(succ(n3, n5))  # n3 -> n5 (conditional branch)
    s.add(succ(n4, n6))  # n4 -> n6
    s.add(succ(n5, n6))  # n5 -> n6
    s.add(succ(n6, n7))  # n6 -> n7
    s.add(succ(n7, n3))  # n7 -> n3 (loop back)
    s.add(succ(n7, n8))  # n7 -> n8 (exit loop)

    # Define variable usage and definitions
    # n1: a = input()
    s.add(defn(n1, a))

    # n2: b = a + 1
    s.add(use(n2, a))
    s.add(defn(n2, b))

    # n3: if b > 10 (uses b)
    s.add(use(n3, b))

    # n4: c = b * 2 (if branch)
    s.add(use(n4, b))
    s.add(defn(n4, c))

    # n5: d = b + 5 (else branch)
    s.add(use(n5, b))
    s.add(defn(n5, d))

    # n6: e = c if b > 10 else d
    s.add(use(n6, b))
    s.add(use(n6, c))
    s.add(use(n6, d))
    s.add(defn(n6, e))

    # n7: b = b - 1
    s.add(use(n7, b))
    s.add(defn(n7, b))

    # n8: print(a, e)
    s.add(use(n8, a))
    s.add(use(n8, e))

    # Add constraints to ensure variables are not live before they are used or defined
    s.add(Not(live_in(n1, a)))
    s.add(Not(live_in(n1, b)))
    s.add(Not(live_in(n1, c)))
    s.add(Not(live_in(n1, d)))
    s.add(Not(live_in(n1, e)))
    s.add(Not(live_out(n8, b)))
    s.add(Not(live_out(n8, c)))
    s.add(Not(live_out(n8, d)))

    # Query live variables
    def check_live(node, var, live_func):
        s.push()
        s.add(live_func(node, var))
        result = s.check()
        s.pop()
        return result == sat

    print("Live variables at entry of each node:")
    for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
        print(f"Node {node}:")
        for var in [a, b, c, d, e]:
            if check_live(node, var, live_in):
                print(f"  Variable {var} is live at entry")

    print("\nLive variables at exit of each node:")
    for node in [n1, n2, n3, n4, n5, n6, n7, n8]:
        print(f"Node {node}:")
        for var in [a, b, c, d, e]:
            if check_live(node, var, live_out):
                print(f"  Variable {var} is live at exit")

if __name__ == "__main__":
    main()