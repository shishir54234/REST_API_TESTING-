import cvc5
from cvc5 import Kind

# Initialize the CVC5 solver

tm = cvc5.TermManager()
solver = cvc5.Solver(tm)
solver.setOption("produce-models", "true")
    # we need finite model finding to answer sat problems with universal
    # quantified formulas
solver.setOption("finite-model-find", "true")
    # we need sets extension to support set.universe operator
solver.setOption("sets-ext", "true")
#define sorts
integer = tm.getIntegerSort()
integer_sort = tm.getIntegerSort()
integer_set_sort = tm.mkSetSort(integer_sort)

tuple_sort = tm.mkTupleSort(integer,integer)  # Tuple sort for (username, password)
tuple_set_sort = tm.mkSetSort(tuple_sort)

users



