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
# Define sorts
integer_sort = tm.getIntegerSort()
integer_set_sort = tm.mkSetSort(integer_sort)
tuple_sort = tm.mkTupleSort(integer_sort, integer_sort)  # Tuple sort for (username, password)
tuple_set_sort = tm.mkSetSort(tuple_sort)  # Set sort for tuples


# Declare sets for usernames and credentials
users = tm.mkEmptySet(tm.mkSetSort(integer_sort))  # Set for usernames
credentials = tm.mkEmptySet(tuple_set_sort)  # Set for credentials
tm.mkTerm(Kind.SET_INSERT, tm.mkInteger(321), users)
tm.mkTerm(Kind.SET_INSERT, tm.mkTuple([tm.mkInteger(321), tm.mkInteger(321)]), credentials)
# Define functions for signup and login conditions
def exists_in_users(u):
    isposs=tm.mkTerm(Kind.SET_MEMBER,u,users)
    return isposs
    

def can_login(u):
    
    existing_user = tm.mkTerm(Kind.SET_MEMBER, u,credentials)
    return existing_user
# print(can_login(solver.mkInteger(321),solver.mkInteger(321)))
# Generate test cases
def generate_signup_test_case():
    new_user = tm.mkInteger(321)
    
    solver.assertFormula(tm.mkTerm(Kind.NOT, exists_in_users(new_user)))
    # tm.push()
    result = solver.checkSat()
    if result.isSat():
        model = solver.getModel(users,credentials)
        new_user_value = solver.getValue(users).getId()
        # solver.pop()
        return new_user_value
    else:
        # tm.pop()
        return None
def generate_login_test_case():
    existing_user=tuple_sort
    solver.assertFormula(can_login(existing_user))
    # solver.assertFormula(exists_in_users(existing_user))
    result = solver.checkSat()
    if result.isSat():
        model = solver.getModel(users,credentials)
        existing_user_value = model.getValue(existing_user).getId()
        return existing_user_value
    else:
        print("1")
        return None

# Generate and print test cases
# signup_test_case = generate_signup_test_case()
# if signup_test_case is not None:
#     print(f"Signup Test Case: new_user = {signup_test_case}")
login_test_case=generate_login_test_case()

if login_test_case is not None:
    print(f"Login Test Case: existing_user = {login_test_case}")