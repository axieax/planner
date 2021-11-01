#! /usr/bin/env python3

import aspInterface
import dummyData

if __name__ == "__main__":
    #print(dummy.comp3411.prereqs)
    ac = dummyData.all_courses
    sp = dummyData.spec
    sched = aspInterface.computeSchedule(ac,sp)
    if sched:
        print(sched)
    else:
        print("unsat")
