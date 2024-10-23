import cvc5
from cvc5 import Kind

# Create a solver
solver = cvc5.Solver()
solver.setLogic("QF_UFLIAFS")
solver.setOption("sets-ext", "true")
solver.setOption("produce-models", "true")

# Define sorts
int_sort = solver.getIntegerSort()
set_sort = solver.mkSetSort(int_sort)

# Define sets of students
A = solver.mkConst(set_sort, "A")  # Academic Clubs
S = solver.mkConst(set_sort, "S")  # Sports Clubs
C = solver.mkConst(set_sort, "C")  # Cultural Clubs

# Define a list of student variables
students = [solver.mkConst(int_sort, f"x{student}") for student in range(1, 11)]

def set_union(set1, set2):
    return solver.mkTerm(Kind.SET_UNION, set1, set2)

def set_member(set_expr, element_expr):
    # Ensure that set_expr is of set sort and element_expr is of the correct element sort
    if set_expr.getSort() == set_sort and element_expr.getSort() == int_sort:
        return solver.mkTerm(Kind.SET_MEMBER, element_expr, set_expr)
    else:
        raise TypeError("set_expr must be a set of integers and element_expr must be an integer.")

def set_difference(set1, set2):
    return solver.mkTerm(Kind.SET_MINUS, set1, set2)

def set_intersection(set1, set2):
    return solver.mkTerm(Kind.SET_INTER, set1, set2)

def logical_or(term1, term2):
    return solver.mkTerm(Kind.OR, term1, term2)

def logical_and(term1, term2):
    return solver.mkTerm(Kind.AND, term1, term2)

def logical_not(term):
    return solver.mkTerm(Kind.NOT, term)

def equal(term1, term2):
    return solver.mkTerm(Kind.EQUAL, term1, term2)

def logical_or_multiple(terms):
    if not terms:
        return solver.mkFalse()
    result = terms[0]
    for term in terms[1:]:
        result = logical_or(result, term)
    return result

# Define a set of all students using the same variables
student_set = solver.mkEmptySet(set_sort)
for student in students:
    student_set = set_union(student_set, solver.mkTerm(Kind.SET_SINGLETON, student))

# Add constraints

# Requirement 1: Every student must be in at least one club
for student in students:
    or_club_membership = logical_or(
        set_member(A, student),
        logical_or(
            set_member(S, student),
            set_member(C, student)
        )
    )
    solver.assertFormula(or_club_membership)

# Requirement 2: Exclusive memberships between academic and sports clubs
empty_set = solver.mkEmptySet(set_sort)
solver.assertFormula(equal(set_intersection(A, S), empty_set))

# Requirement 3: No student can be part of all three clubs at the same time
solver.assertFormula(equal(set_intersection(A, set_intersection(S, C)), empty_set))

# Requirement 4: At least 50% of the students should be in cultural clubs
num_students = len(students)
approx_50_percent = num_students // 2
# This is a heuristic; you might need to adjust based on actual requirements
for student in students[:approx_50_percent]:
    solver.assertFormula(set_member(C, student))

# Requirement 5: Every academic club should have at least one student not in sports clubs
academic_not_sports = set_difference(A, S)
exists_one = logical_or_multiple([set_member(academic_not_sports, student) for student in students])
solver.assertFormula(exists_one)

# Ensure combined set is a subset of student_set and vice versa
combined = set_union(A, set_union(S, C))

# Ensure combined is a subset of student_set
subset_constraint1 = equal(set_difference(student_set, combined), empty_set)
# Ensure student_set is a subset of combined
subset_constraint2 = equal(set_difference(combined, student_set), empty_set)

solver.assertFormula(subset_constraint1)
solver.assertFormula(subset_constraint2)

# Check the constraints
result = solver.checkSat()
if result:
    # solver = solver.getsolver()
    
    # Print sets
    print("Academic Clubs (A):", solver.getValue(A))
    print("Sports Clubs (S):", solver.getValue(S))
    print("Cultural Clubs (C):", solver.getValue(C))
    
    # Print intersections and differences to verify conditions
    print("\nIntersection of Academic and Sports (should be empty):", solver.getValue(set_intersection(A, S)))
    print("Intersection of all three (should be empty):", solver.getValue(set_intersection(A, set_intersection(S, C))))
    print("Students in academic but not in sports (should not be empty):", solver.getValue(academic_not_sports))
    
    # Print total number of unique students across all clubs
    print("Total number of unique students across all clubs:", solver.getValue(combined))
else:
    print("Constraints are unsatisfiable.")
