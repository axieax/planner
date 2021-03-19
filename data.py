# scrape data - courses and degrees
all_degrees = {} # indexed by degree_code
all_courses = {} # indexed by course_code

# load pickled data
NUM_TERMS = 4




def scrape_data():
    bad_courses = []
    # prereq - UOC, WAM, COURSES, YEAR
    pass


def check_plan():
    # prereqs
    # equivalent courses
    pass



"""
Courses
"""
from util import Course
courses = []

# ALL COURSES AS A DICT? with code as key

### Course Options ###
# currently have to manually remove mark requirements
# UNDERGRAD COURSES
# re to extract from after 'Prerequisite: ' to newline or fullstop
''' DATA '''
data1001 = Course('DATA1001', [2], '', 6)

''' SCIF '''
scif1131 = Course('SCIF1131', [1, 3], '', 6)
# scif3199 = Course('SCIF3199', [0, 1, 2, 3], '48 units of credit', 6) # found under 'conditions for enrolment'
scif3199 = Course('SCIF3199', [0, 1, 2, 3], '', 6) # found under 'conditions for enrolment'

''' ENGG '''
engg2600 = Course('ENGG2600', [1, 2, 3], '??', 2) # !!!

''' PSYC '''
psyc1001 = Course('PSYC1001', [1, 2], '', 6)

''' COMP '''
comp1511 = Course('COMP1511', [1, 2, 3], '', 6)
comp2521 = Course('COMP2521', [1, 2, 3], 'COMP1511 or DPST1091 or COMP1917 or COMP1921', 6)
comp1521 = Course('COMP1521', [2, 3], 'COMP1511 or DPST1091 or COMP1911 or COMP1917', 6)
comp1531 = Course('COMP1531', [1, 3], 'COMP1511 or DPST1091 or COMP1917 or COMP1921', 6)
comp2511 = Course('COMP2511', [2, 3], 'COMP1531 AND (COMP2521 OR COMP1927)', 6)
comp3121 = Course('COMP3121', [2, 3], 'COMP1927 or COMP2521', 6)
comp3231 = Course('COMP3231', [1], '(COMP1521 or DPST1092 or COMP2121 or ELEC2142) and (COMP2521 or COMP1927)', 6)
comp3311 = Course('COMP3311', [1, 3], 'COMP2521 or COMP1927', 6)
comp3411 = Course('COMP3411', [0, 1], 'COMP2521 or COMP1927', 6)
# comp3900 = Course('COMP3900', [1, 2, 3], 'COMP1531, and COMP2521 or COMP1927, and enrolled in a BSc Computer Science major with completion of 102 uoc', 6)
comp3900 = Course('COMP3900', [1, 2, 3], 'COMP1531 and (COMP2521 or COMP1927)', 6)
comp4418 = Course('COMP4418', [3], 'COMP3411', 6)
# comp4920 = Course('COMP4920', [3], '(COMP2511 or COMP2911) and completion of 96 UOC in Computer Science.', 6)
comp4920 = Course('COMP4920', [3], '(COMP2511 or COMP2911)', 6)
# comp6841 = Course('COMP6841', [1], 'Completion of 48 UOC, and COMP1927 or COMP2521') # !!!
comp6841 = Course('COMP6841', [1], 'COMP1927 or COMP2521', 6) # !!!
comp9318 = Course('COMP9318', [1], '(COMP2521 or COMP1927) and COMP3311 and MATH1081', 6)
comp9417 = Course('COMP9417', [1, 2], '(MATH1081 and (COMP1531 or COMP2041)) or (COMP1927 or COMP2521)', 6) # determine which comes first
comp9418 = Course('COMP9418', [3], 'COMP9417', 6)
comp9444 = Course('COMP9444', [2, 3], 'COMP1927 or COMP2521 or MTRN3500', 6)

''' MATH '''
math1081 = Course('MATH1081', [1, 2, 3], '', 6) # Co-requisite with 1141
math1141 = Course('MATH1141', [1, 3], '', 6)
math1241 = Course('MATH1241', [1, 2], 'MATH1131 or MATH1141 or DPST1013', 6)
math2111 = Course('MATH2111', [1], 'MATH1231 or DPST1014 or MATH1241 or MATH1251', 6)
math2601 = Course('MATH2601', [2], 'MATH1231 or DPST1014 or MATH1241 or MATH1251', 6)
math2621 = Course('MATH2621', [3], 'MATH1231 or DPST1014 or MATH1241 or MATH1251', 6)
math2901 = Course('MATH2901', [2], 'MATH1231 or MATH1241 or MATH1251 or DPST1014', 6)
math2931 = Course('MATH2931', [3], 'MATH2901 or MATH2801', 6)
# math3171 = Course('MATH3171', [3], '(1) [MATH2011 or MATH2111] and [MATH2501 or MATH2601]; or (2) both MATH2069 (CR) and MATH2099 ; or (3) both [MATH2018 or MATH2019] (DN) and MATH2089 .', 6)
math3171 = Course('MATH3171', [3], '([MATH2011 or MATH2111] and [MATH2501 or MATH2601]) or (MATH2069 (CR) and MATH2099) or ([MATH2018 or MATH2019] (DN) and MATH2089)', 6)
math3411 = Course('MATH3411', [3], 'MATH1081 or MATH1231(CR) or DPST1014 (CR) or MATH1241(CR) or MATH1251(CR) or MATH2099', 6)
# math3521 = Course('MATH3521', [1], '12 units of credit in Level 2 Math courses', 6) # under conditions for enrolment
math3521 = Course('MATH3521', [1], 'MATH2111 and MATH2621', 6) # under conditions for enrolment
math3821 = Course('MATH3821', [2], 'MATH2831 or MATH2931', 6)
math3871 = Course('MATH3871', [3], 'MATH2801 or MATH2901', 6)
# math3901 = Course('MATH3901', [1], 'MATH2901 or MATH2801(DN) and MATH2501 or MATH2601 and MATH2011 or MATH2111 or MATH2510 or MATH2610', 6) # BAD LOGIC
math3901 = Course('MATH3901', [1], '((MATH2901 or MATH2801) and (MATH2501 or MATH2601) and (MATH2011 or MATH2111)) or (MATH2510 or MATH2610)', 6) # BAD LOGIC
math3911 = Course('MATH3911', [1], 'MATH2931 or MATH2831', 6)

# 3789 2021 Version

### Selected Options ###
# # OLD PLAN
# courses.append(comp1511)
# courses.append(math1081)
# courses.append(math1141)
# courses.append(data1001)
# courses.append(comp2521)
# courses.append(math1241)
# courses.append(comp1521)
# courses.append(comp1531)
# courses.append(math2621)
# courses.append(comp3411)
# courses.append(comp6841)
# courses.append(math2111)
# # courses.append(engg2600) # * 3 - placing it once automatically places it for the next 2 terms??
# courses.append(comp3121)
# courses.append(math2601)
# courses.append(math2901)
# courses.append(comp4418)
# courses.append(math2931)
# courses.append(math3411)
# courses.append(psyc1001)
# courses.append(comp9417)
# courses.append(math3911)
# courses.append(comp2511)
# courses.append(comp9444)
# courses.append(math3821)
# courses.append(comp3900)
# courses.append(comp4920)
# courses.append(math3871)
# courses.append(scif3199)
# courses.append(comp3231)
# courses.append(math3521)
# courses.append(math3901)

# NEW PLAN
courses.append(math1081)
courses.append(comp1511)
courses.append(comp1521)
courses.append(comp1531)
courses.append(comp2511)
courses.append(comp2521)
courses.append(comp3121)
courses.append(comp3900)
courses.append(comp4920)

courses.append(engg2600) # * 3 - placing it once automatically places it for the next 2 terms?? or manual placement
courses.append(comp3231)
courses.append(comp3311)
courses.append(comp3411)
courses.append(comp6841)
courses.append(comp9417)
courses.append(comp9444)


courses.append(math1141)
courses.append(math1241)
courses.append(math2111)
courses.append(math2601)
courses.append(math2901)
courses.append(math2931)
courses.append(math3821)
courses.append(math3901)
courses.append(math3911)
courses.append(math3871)


courses.append(data1001)
courses.append(math2621)
courses.append(math3411)
courses.append(math3521)
courses.append(math3171)
courses.append(psyc1001)

all_courses = {course.code: course for course in courses}


"""
Plan
"""
# Plan - can have courses already in certain terms
plan = [[] for i in range(len(courses))]
plan[1] = ['comp1511', 'math1141', 'math1081']
plan[2] = ['comp2521', 'math1241', 'data1001']
plan[3] = ['comp1521', 'comp1531', 'math2621']
# plan[2].append('data1001')
plan[5] = ['comp3411', 'comp6841', 'engg2600', 'math2111']
# plan[5].append('engg2600')
plan[6].append('engg2600')
plan[6].append('comp3121')
plan[7].append('engg2600')
# plan[7].append('comp3311')
plan[9].append('psyc1001')
plan[9].append('comp9417')
# plan[9].append('math3911')

# Max num of courses per term
plan_specs = {
    'starting_term': 1,
    'max_uoc': [12 if i % NUM_TERMS == 0 else 20 for i in range(len(courses))],
}
plan_specs['max_uoc'][4] = 0

"""
Front end design:
    Course selection --> Degree plan
    Bundle courses by category
    Ensure all prerequisites are selected - select prerequisites as well automatically
    Drag and drop interface for pre-planned
    Summer option
Back end design:
    Separate function in main.py for calculating last placed term index for (within place function):
        Year placement
        UOC placement
    Choose prereq option
"""
