from util import Course

class PlanSpec:
    def __init__(self, startterm, select, maxuoc):
        self.starting_term = startterm
        self.max_uoc = maxuoc
        self.selected = select

### 
# dropped engg2600 has the prereqs didn't make sense
# comp6447 edited the prereqs to remove a comma

### Course Options ###
''' DATA '''
data1001 = Course('DATA1001', [2], 'none', 6)

''' SCIF '''
scif1131 = Course('SCIF1131', [1, 3], 'none', 6)
# scif3199 = Course('SCIF3199', [0, 1, 2, 3], '48 units of credit', 6) # found under 'conditions for enrolment'
scif3199 = Course('SCIF3199', [0, 1, 2, 3], 'none', 6) # found under 'conditions for enrolment'

''' ENGG '''
###engg2600 = Course('ENGG2600', [1, 2, 3], '??', 2) # !!!

''' PSYC '''
psyc1001 = Course('PSYC1001', [1, 2], 'none', 6)

''' COMP '''
comp1511 = Course('COMP1511', [1, 2, 3], 'none', 6)
comp2521 = Course('COMP2521', [1, 2, 3], 'COMP1511 or DPST1091 or COMP1917 or COMP1921', 6)
comp1521 = Course('COMP1521', [2, 3], 'COMP1511 or DPST1091 or COMP1911 or COMP1917', 6)
comp1531 = Course('COMP1531', [1, 3], 'COMP1511 or DPST1091 or COMP1917 or COMP1921', 6)
comp2511 = Course('COMP2511', [2, 3], 'COMP1531 AND (COMP2521 OR COMP1927)', 6)
comp3121 = Course('COMP3121', [2, 3], 'COMP1927 or COMP2521', 6)
comp3141 = Course('COMP3141', [2], 'COMP1927 or COMP2521', 6)
comp3231 = Course('COMP3231', [1], '(COMP1521 or DPST1092 or COMP2121 or ELEC2142) and (COMP2521 or COMP1927)', 6)
comp3311 = Course('COMP3311', [1, 3], 'COMP2521 or COMP1927', 6)
comp3411 = Course('COMP3411', [0, 1], 'COMP2521 or COMP1927', 6)
# (COMP1521 or DPST1092 or COMP2121) and (COMP2521 or COMP1927) and a WAM of at least 75
comp3891 = Course('COMP3891', [1], '(COMP1521 or DPST1092 or COMP2121) and (COMP2521 or COMP1927)', 6)
# comp3900 = Course('COMP3900', [1, 2, 3], 'COMP1531, and COMP2521 or COMP1927, and enrolled in a BSc Computer Science major with completion of 102 uoc', 6)
comp3900 = Course('COMP3900', [1, 2, 3], 'COMP1531 and (COMP2521 or COMP1927)', 6)
comp4121 = Course('COMP4121', [3], 'COMP3121 or COMP3821', 6)
comp4418 = Course('COMP4418', [3], 'COMP3411', 6)
# comp4920 = Course('COMP4920', [3], '(COMP2511 or COMP2911) and completion of 96 UOC in Computer Science.', 6)
comp4920 = Course('COMP4920', [3], '(COMP2511 or COMP2911)', 6)
# A mark of at least 65 in COMP6841, or a mark of at least 75 in COMP6441 or COMP3441.
comp6447 = Course('COMP6447', [2], 'COMP6841 or COMP6441 or COMP3441')
# comp6841 = Course('COMP6841', [1], 'Completion of 48 UOC, and COMP1927 or COMP2521') # !!!
comp6841 = Course('COMP6841', [1], 'COMP1927 or COMP2521', 6) # !!!
comp6843 = Course('COMP6843', [2], 'COMP6441 or COMP6841 or COMP3441', 6)
comp9243 = Course('COMP9243', [3], '[COMP3231 or COMP3891] and [COMP3331 or TELE3018]', 6)
comp9318 = Course('COMP9318', [1], '(COMP2521 or COMP1927) and COMP3311 and MATH1081', 6)
comp9417 = Course('COMP9417', [1, 2], '(MATH1081 and (COMP1531 or COMP2041)) or (COMP1927 or COMP2521)', 6) # determine which comes first
comp9418 = Course('COMP9418', [3], 'COMP9417', 6)
comp9444 = Course('COMP9444', [2, 3], 'COMP1927 or COMP2521 or MTRN3500', 6)
comp9447 = Course('COMP9447', [1, 2, 3], 'COMP6441 or COMP6841 or COMP3441', 6)

''' MATH '''
math1081 = Course('MATH1081', [1, 2, 3], 'none', 6) # Co-requisite with 1141
math1141 = Course('MATH1141', [1, 3], 'none', 6)
math1241 = Course('MATH1241', [1, 2], 'MATH1131 or MATH1141 or DPST1013', 6)
math2111 = Course('MATH2111', [1], 'MATH1231 or DPST1014 or MATH1241 or MATH1251', 6)
math2601 = Course('MATH2601', [2], 'MATH1231 or DPST1014 or MATH1241 or MATH1251', 6)
math2621 = Course('MATH2621', [3], 'MATH1231 or DPST1014 or MATH1241 or MATH1251', 6)
math2901 = Course('MATH2901', [2], 'MATH1231 or MATH1241 or MATH1251 or DPST1014', 6)
math2931 = Course('MATH2931', [3], 'MATH2901 or MATH2801', 6)
math3171 = Course('MATH3171', [3], '([MATH2011 or MATH2111] and [MATH2501 or MATH2601]) or (MATH2069 (CR) and MATH2099) or ([MATH2018 or MATH2019] (DN) and MATH2089)')
math3411 = Course('MATH3411', [3], 'MATH1081 or MATH1231(CR) or DPST1014 (CR) or MATH1241(CR) or MATH1251(CR) or MATH2099', 6)
math3521 = Course('MATH3521', [1], 'MATH2111 and MATH2621', 6) # under conditions for enrolment
math3821 = Course('MATH3821', [2], 'MATH2831 or MATH2931', 6)
math3871 = Course('MATH3871', [3], 'MATH2801 or MATH2901', 6)
math3901 = Course('MATH3901', [1], '((MATH2901 or MATH2801) and (MATH2501 or MATH2601) and (MATH2011 or MATH2111)) or (MATH2510 or MATH2610)', 6) # BAD LOGIC
math3911 = Course('MATH3911', [1], 'MATH2931 or MATH2831', 6)

all_courses = [data1001,scif1131,scif3199,#engg2600,
               psyc1001,comp1511,comp2521,comp1521,comp1531,comp2511,comp3121,comp3141,comp3231,comp3311,comp3411,comp3891,comp3900,comp4121,comp4418,comp4920,comp6447,comp6841,comp6843,comp9243,comp9318,comp9417,comp9418,comp9444,comp9447,math1081,math1141,math1241,math2111,math2601,math2621,math2901,math2931,math3171,math3411,math3521,math3821,math3871,math3901,math3911]

### Selected Options ###
courses = ["comp1511", "math1081","math1141","data1001","comp2521","math1241","comp1521","comp1531","math2621","comp3411","comp6841","math2111","comp3121","math2601","math2901","comp2511","math2931"]#,"math3411","comp3891","comp9417","math3901","comp3141","comp6447","math3821","comp9447","math3171","math3871","psyc1001","math3521","math3911","comp6843","comp3900","comp9243","comp9444"]

#courses = ["comp1511", "math1081","math1141","data1001","comp2521","math1241","comp1521","comp1531","math2621"]#,"comp3411"]#,"comp6841","math2111","comp3121","math2601","math2901","comp2511","math2931","math3411","comp3891","comp9417","math3901","comp3141","comp6447","math3821","comp9447","math3171","math3871","psyc1001","math3521","math3911","comp6843","comp3900","comp9243","comp9444"]


spec = PlanSpec(1, courses, 20)

