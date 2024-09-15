import cvc5
from cvc5 import Kind
tm = cvc5.TermManager()
ds=cvc5.DatatypeSelector()
solver = cvc5.Solver(tm)
solver.setLogic("ALL")
solver.setOption("produce-models", "true")
    # we need finite model finding to answer sat problems with universal
    # quantified formulas
solver.setOption("finite-model-find", "true")
    # we need sets extension to support set.universe operator
solver.setOption("sets-ext", "true")
# variables- const, tuple, set
integer = tm.getIntegerSort()
integer_sort = tm.getIntegerSort()
integer_set_sort = tm.mkSetSort(integer_sort)

tuple_sort = tm.mkTupleSort(integer,integer)  # Tuple sort for (username, password)
tuple_set_sort = tm.mkSetSort(tuple_sort)

def success_signup(users,credentials):
    user1=tm.mkConst(integer_sort,"user1")
    pass1=tm.mkConst(integer_sort,"pass1")
    doesit=tm.mkTerm(Kind.SET_MEMBER,user1,users)
    solver.assertFormula(tm.mkTerm(Kind.NOT,doesit))
    res=solver.checkSat()
    if res.isSat():
        user1=solver.getValue(user1)
        p1=solver.getValue(pass1)
        users=tm.mkTerm(Kind.SET_INSERT,user1,users)
        credentials=tm.mkTerm(Kind.SET_INSERT, tm.mkTuple([user1,p1]), credentials)
        print("Test Case generated for signup is ",user1,p1)
def success_login(users,credentials,active_users):
    user1=tm.mkConst(integer_sort,"user1")
    pass1=tm.mkConst(integer_sort,"pass1")
    doesit=tm.mkTerm(Kind.SET_MEMBER,user1,users)
    doesit1=tm.mkTerm(Kind.SET_MEMBER,tm.mkTuple([user1,pass1]),credentials)

    solver.assertFormula(doesit)
    solver.assertFormula(doesit1)
    res=solver.checkSat()
    if res.isSat():
        user1=solver.getValue(user1)
        p1=solver.getValue(pass1)
        active_users=tm.mkTerm(Kind.SET_INSERT,user1,active_users)
        print("Test Case generated for login is ",user1,p1)
def success_logout(users,active_users):
    u1=tm.mkConst(integer_sort,"u1")
    user1=tm.mkConst(integer_set_sort,"user1")

    cond1=tm.mkTerm(Kind.SET_MEMBER,u1,users)
    cond2=tm.mkTerm(Kind.SET_MEMBER,u1,active_users)
    cond3=tm.mkTerm(Kind.SET_IS_SINGLETON,user1)
    cond4=tm.mkTerm(Kind.SET_MEMBER,u1,user1)
    solver.assertFormula(cond1)
    solver.assertFormula(cond2)
    solver.assertFormula(cond3)
    solver.assertFormula(cond4)
    res=solver.checkSat()
    if res.isSat():
        user1=solver.getValue(user1)
        active_users=tm.mkTerm(Kind.SET_MINUS,user1,active_users)
        print("Test Case generated for logout is ",user1)

def success_programcreation(users,active_users,programs):
    user4=tm.mkConst(integer_sort,"user4")
    progamid=tm.mkConst(integer_sort,"progamid")
    cond1=tm.mkTerm(Kind.SET_MEMBER,user4,users)
    cond2=tm.mkTerm(Kind.SET_MEMBER,user4,active_users)
    cond3=tm.mkTerm(Kind.SET_MEMBER,tm.mkTuple([user4,progamid]),programs)
    solver.assertFormula(cond1)
    solver.assertFormula(cond2)
    solver.assertFormula(tm.mkTerm(Kind.NOT,cond3))
    res=solver.checkSat()
    if res.isSat():
        user4=solver.getValue(user4)
        progamid=solver.getValue(progamid)

        programs=tm.mkTerm(Kind.SET_INSERT,tm.mkTuple([user4,progamid]),programs)
        # programs1=solver.getValue(programs)
        print("Test Case generated for program creation is ",user4,progamid)
        return programs
    else:
        return None
        

def success_getprogram(users,active_users,programs):
    user1=tm.mkConst(integer_sort,"user1")
    progamids=tm.mkConst(integer_set_sort,"progamid")
    # equal=tm.mkOp(Kind.EQUAL,tm.mkTuple([user1,progamids]))
    cond1=tm.mkTerm(Kind.SET_MEMBER,user1,users)
    cond2=tm.mkTerm(Kind.SET_MEMBER,user1,active_users)
    solver.assertFormula(cond1)
    solver.assertFormula(cond2)
    res=solver.checkSat()
    if res.isSat():
        user1=solver.getValue(user1)
        programs1=solver.getValue(programs)
        print("User id:",user1)
        print("program ids for this user are: ")
        for t in programs1:
            if t[0]==user1:
                print(t[1])
        # print("Test Case generated for get program is ",user1,progamids)
users = tm.mkConst(integer_set_sort,"users")
credentials = tm.mkConst(tuple_set_sort,"creds")
programs = tm.mkConst(tuple_set_sort,"programs")
active_users = tm.mkConst(integer_set_sort,"active_users")

success_signup(users,credentials)
success_login(users,credentials,active_users)
programs=success_programcreation(users,active_users,programs)
print("check " ,solver.getValue(programs))
success_getprogram(users,active_users,programs)


success_logout(users,active_users)
