#! /usr/bin/env python3

import aspInterface
import dummyData

def simpleTest():
    ac = dummyData.unsw
    sp = dummyData.spec
    sched = aspInterface.computeSchedule(ac,sp)
    if sched:
        print("schedule and loads: ", sched)
    else:
        print("unfeasible")

def iterateTest():
    ac = dummyData.unsw
    selected_courses = ["comp1511", "math1081","math1141","data1001","comp2521","math1241","comp1521","comp1531","math2621","comp3411","comp6841","math2111","comp3121","math2601","math2901","comp2511","math2931","math3411","comp3891","comp9417","math3901","comp3141","comp6447","math3821","comp9447","math3171","math3871","psyc1001","math3521","math3911","comp6843","comp3900","comp9444"]
    startDate = (2022,2)
    finalDate = [(y, t) for y in range(2025,2027) for t in range(0,4) if (y,t) >= startDate]
    configuration = [(d, maxload) for d in finalDate for maxload in range(15,21)]
    for (date, load) in configuration:
        sp = dummyData.PlanSpec(startDate, date, selected_courses, load)
        print('final date: {}, max load {}uoc '.format(date, load), end='')
        sched = aspInterface.computeSchedule(ac,sp)
        if sched:
            print("feasible")
        else:
            print("unfeasible")

if __name__ == "__main__":
    #print(dummyData.comp9243.prereqs)
    #iterateTest()
    simpleTest()
