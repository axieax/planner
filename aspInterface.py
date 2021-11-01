import clingo
import clingo.ast


# data: term(T). course(C). available(C,T). prereqs(C1,P,C2). uoc(C,U).
def course_to_asp(course):
    code_decl = 'course({}).'.format(course.code)
    available = ['available({},{}).'.format(course.code,t) for t in course.terms]
    uoc = 'uoc({},{}).'.format(course.code, course.uoc)
    if course.prereqs == [['none']]:
        prereqs = []
        prereqsstreams = ['prereqsOption({},0).'.format(course.code)]
    else:
        prereqs = ['prereqs({},{},{}).'.format(course.code, i, p) for i in range(len(course.prereqs)) for p in course.prereqs[i]]
        prereqsstreams = ['prereqsOption({},{}).'.format(course.code, i) for i in range(len(course.prereqs))]
    constraints = [code_decl] + available + [uoc] + prereqsstreams + prereqs
    return constraints

def plan_spec_to_asp(spec):
    maxuoc = 'maxAcceptableLoad({}).'.format(spec.max_uoc)
    term = 'earliestTerm({}).'.format(spec.starting_term)
    select = ['selected({}).'.format(course) for course in spec.selected]
    return [maxuoc,term] + select

def make_asp(all_courses, spec):
    courses = [constraint for course in all_courses for constraint in course_to_asp(course)]
    specs = plan_spec_to_asp(spec)
    return '\n'.join(specs + courses)


def storeModel(model,output):
    l = model.symbols(atoms=True)
    collect = []
    schedules = []
    loads = []
    for atom in l:
        if atom.name == "schedule":
            assert(len(atom.arguments) == 3)
            course = atom.arguments[0]
            term = atom.arguments[1]
            year = atom.arguments[2]
            schedules.append((str(course),int(str(term)),int(str(year))))
        if atom.name == "load":
            assert(len(atom.arguments) == 3)
            term = atom.arguments[0]
            year = atom.arguments[1]
            load = atom.arguments[2]
            loads.append((int(str(term)),int(str(year)),int(str(load))))
        elif atom.name == "attribute":
            collect += [(atom.arguments[0].name, atom.arguments[1].name)]
    output['schedules'] = schedules
    output['loads'] = loads

def collectDefaultConstraints():
    with open("asp/schedule.lp",'r') as f:
        total = f.read()
    return total

def computeSchedule(all_courses, spec):
    ctl = clingo.Control()
    with clingo.ast.ProgramBuilder(ctl) as bld:
        clingo.ast.parse_string(make_asp(all_courses, spec), bld.add)
        clingo.ast.parse_string(collectDefaultConstraints(), bld.add) # parse from string

    ctl.ground([('base', [])])
    #output = defaultdict(lambda: defaultdict(list))
    output = dict()
    #print(ctl.solve(on_model=print))
    result = ctl.solve(on_model=lambda m: storeModel(m, output))
    if result.satisfiable:
        return output
        print(output)
        pass
    elif result.satisfiable is False:
        return False
    else:
        print("???")
        assert False
