import cvc5
from cvc5 import Kind

# Initialize the CVC5 solver
tm = cvc5.TermManager()
solver = cvc5.Solver(tm)
solver.setLogic("ALL")
solver.setOption("produce-models", "true")
    # we need finite model finding to answer sat problems with universal
    # quantified formulas
solver.setOption("finite-model-find", "true")
    # we need sets extension to support set.universe operator
solver.setOption("sets-ext", "true")
# variables- const, tuple, set
 
# options
# solver.setOption("produce-models", "true")
# # we need finite model finding to answer sat problems with universal
# # quantified formulas
# solver.setOption("finite-model-find", "true")
# # we need sets extension to support set.universe operator
# solver.setOption("sets-ext", "true")
# Define sorts
integer = tm.getIntegerSort()
integer_sort = tm.getIntegerSort()
integer_set_sort = tm.mkSetSort(integer_sort)

tuple_sort = tm.mkTupleSort(integer,integer)  # Tuple sort for (username, password)
tuple_set_sort = tm.mkSetSort(tuple_sort)
# Declare sets for usernames and credentials
users = tm.mkConst(integer_set_sort,"users")

credentials = tm.mkConst(tuple_set_sort,"creds")
# signup login signup 

user1=tm.mkConst(integer_sort,"user1")
pass1=tm.mkConst(integer_sort,"pass1")
# pre conditions
#shoudlnt exist in users
doesit=tm.mkTerm(Kind.SET_MEMBER,user1,users)

solver.assertFormula(tm.mkTerm(Kind.NOT,doesit))

res=solver.checkSat()
if res.isSat():
    print("user doesnt exist")
    user1=solver.getValue(user1)
    p1=solver.getValue(pass1)
    users=tm.mkTerm(Kind.SET_INSERT,user1,users)
    credentials=tm.mkTerm(Kind.SET_INSERT, tm.mkTuple([user1,pass1]), credentials)
    # credentials=tm.mkTerm(Kind.SET_INSERT, tm.mkTuple([user1,pass1]), credentials)
    print(user1)

user2=tm.mkConst(integer_sort,"user2")
pass2=tm.mkConst(integer_sort,"pass2")

doesit1=tm.mkTerm(Kind.SET_MEMBER,user2,users)
doesit2=tm.mkTerm(Kind.SET_MEMBER,tm.mkTuple([user2,pass2]),credentials)
solver.assertFormula(doesit1)
solver.assertFormula(doesit2)
res=solver.checkSat()
if res.isSat():
    print("Login succcesful")
    u2=solver.getValue(user2)
    p2=solver.getValue(pass2)
    print(u2)
    print(p2)

user4=tm.mkConst(integer_sort,"user4")
prog1=tm.mkConst(integer_sort,"prog1")

programs=tm.mkConst(tuple_set_sort,"programs")

does_it_exist = tm.mkTerm(Kind.SET_MEMBER,tm.mkTuple([user4,prog1]),programs)
user_exists=tm.mkTerm(Kind.SET_MEMBER,user4,users)
solver.assertFormula(user_exists)
solver.assertFormula(tm.mkTerm(Kind.NOT,does_it_exist))
res=solver.checkSat()
if res.isSat():
    print("we can create new program")
    u4=solver.getValue(user4)
    p4=solver.getValue(prog1)
    programs=tm.mkTerm(Kind.SET_INSERT,tm.mkTuple([u4,p4]),programs)
    print(programs)

user3=tm.mkConst(integer_sort,"user3")
pass3=tm.mkConst(integer_sort,"pass3")
# pre conditions
#shoudlnt exist in users
doesit=tm.mkTerm(Kind.SET_MEMBER,user3,users)
solver.assertFormula(tm.mkTerm(Kind.NOT,doesit))

res=solver.checkSat()
if res.isSat():
    print("user doesnt exist")
    u3=solver.getValue(user3)
    p3=solver.getValue(pass3)
    uset=solver.getValue(users)
    print(uset)
    users=tm.mkTerm(Kind.SET_INSERT,u3,users)
    # credentials=tm.mkTerm(Kind.SET_INSERT, tm.mkTuple([u3,p3]), credentials)
    # credentials=tm.mkTerm(Kind.SET_INSERT, tm.mkTuple([user1,pass1]), credentials)
    print(users)
    print(u3)
