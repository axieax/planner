"""
Courses
"""
from adt import Course
courses = []

### Course Options ###
# Y1T1
comp1511 = Course("COMP1511", [1, 2, 3], [], 6)
math1081 = Course("MATH1081", [1, 2, 3], [], 6) # Co-requisite with 1141
math1141 = Course("MATH1141", [1, 3], [], 6)
# Y1T2
comp2521 = Course("COMP2521", [1, 2, 3], ["COMP1511"], 6)
data1001 = Course("DATA1001", [2], [], 6)
math1241 = Course("MATH1241", [1, 2], ["MATH1141"], 6)
# Y1T3
comp1521 = Course("COMP1521", [2, 3], ["COMP1511"], 6)
comp1531 = Course("COMP1531", [1, 3], ["COMP1511"], 6)
math2621 = Course("MATH2621", [3], ["MATH1241"], 6)
# Y2T1
comp3411 = Course("COMP3411", [4, 1], ["COMP2521"], 6)
comp3821 = Course("COMP3821", [1], ["COMP2521"], 6)
math2111 = Course("MATH2111", [1], ["MATH1241"], 6)
# Y2T2
comp2511 = Course("COMP2511", [2, 3], ["COMP1531", "COMP2521"], 6)
math2601 = Course("MATH2601", [2], ["MATH1241"], 6)
math2901 = Course("MATH2901", [2], ["MATH1241"], 6)
# Y2T3
math2931 = Course("MATH2931", [3], ["MATH2901"], 6)
scif1131 = Course("SCIF1131", [1, 3], [], 6)
comp3311 = Course("COMP3311", [1, 3], ["COMP2521"], 6)
# Y3T1
math3901 = Course("MATH3901", [1], ["MATH2901", "MATH2601", "MATH2111"], 6)
math3911 = Course("MATH3911", [1], ["MATH2931"], 6)

# Y3T2
math3821 = Course("MATH3821", [2], ["MATH2931"], 6)


# Possible
comp9318 = Course("COMP9318", [1], ["COMP2521", "COMP3311", "MATH1081"], 6)
comp9417 = Course("COMP9417", [1, 2], ["COMP2521"], 6)
# comp9417 = Course("COMP9417", [1, 2], ["MATH1081", "COMP1531"], 6) # Determine which comes first
comp9444 = Course("COMP9444", [2, 3], ["COMP2521"], 6)


### Selected Options ###
courses.append(comp9318)
courses.append(comp9417)
courses.append(comp9444)

courses.append(comp1511)
courses.append(math1081)
courses.append(math1141)
courses.append(comp2521)
courses.append(data1001)
courses.append(math1241)
courses.append(comp1521)
courses.append(comp1531)
courses.append(math2621)
courses.append(comp3411)
courses.append(comp3821)
courses.append(math2111)
courses.append(comp2511)
courses.append(math2601)
courses.append(math2901)
courses.append(math2931)
courses.append(scif1131)
courses.append(comp3311)
courses.append(math3901)
courses.append(math3911)
courses.append(math3821)


"""
Plan
"""
# Plan - can have courses already in certain terms
plan = [[] for i in range(len(courses))]

# Max num of courses per term
planSize = [3 for i in range(len(courses))]


"""
Front end design:
    Bundle courses by category
    Ensure all prerequisites are selected - select prerequisites as well automatically
    Drag and drop interface for pre-planned
    Summer option
"""