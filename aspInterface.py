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
    maxuoc = 'maxUocLoad({}).'.format(spec.maxUocLoad)
    sdate = 'startdate(time({},{})).'.format(spec.startdate[0],spec.startdate[1])
    fdate = 'finaldate(time({},{})).'.format(spec.finaldate[0],spec.finaldate[1])
    select = ['selected({}).'.format(course) for course in spec.selected]
    return [maxuoc,sdate,fdate] + select

def make_asp(inst, spec):
    courses = [constraint for course in inst.courses for constraint in course_to_asp(course)]
    terms = ['term({}).'.format(t) for t in inst.terms]
    specs = plan_spec_to_asp(spec)
    return '\n'.join(terms + specs + courses)


def storeModel(model,output):
    l = model.symbols(atoms=True)
    schedules = []
    loads = []
    for atom in l:
        if atom.name == "schedule":
            assert(len(atom.arguments) == 2)
            (date, course) = atom.arguments
            assert date.match('time', 2)
            (year,term) = date.arguments
            schedules.append((int(str(year)),int(str(term)),str(course)))
        elif atom.name == "uocLoad":
            assert(len(atom.arguments) == 2)
            (date, load) = atom.arguments
            assert date.match('time', 2)
            (year,term) = date.arguments
            loads.append((int(str(year)),int(str(term)),int(str(load))))
    output['schedules'] = schedules
    output['loads'] = loads

def collectDefaultConstraints():
    with open("asp/schedule.lp",'r') as f:
        total = f.read()
    return total

def computeSchedule(institution, spec):
    ctl = clingo.Control()
    with clingo.ast.ProgramBuilder(ctl) as bld:
        clingo.ast.parse_string(make_asp(institution, spec), bld.add)
        clingo.ast.parse_string(collectDefaultConstraints(), bld.add) # parse from string

    ctl.ground([('base', [])])
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
