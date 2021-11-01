%% Input
%% data: term(T). course(C). available(C,T). prereqs(C1,P,C2). uoc(C,U).
%% user: startdate(Y). finaldate(Y). maxUocLoad(L). selected(C).

date(D) :- year(Y), term(T), D=time(Y,T), startdate(D1), finaldate(D2), D1 <= D, D <= D2.
year(Y1..Y2):- startdate(time(Y1,T1)), finaldate(time(Y2,T2)).

{ schedule(D,C) : date(D) } 1 :- course(C).
:- schedule(time(Y,T),C), not available(C,T).
scheduleC(C) :- schedule(D,C).
:- selected(C), not scheduleC(C).


1 { prereqsStream(C,P) : prereqsOption(C,P) } :- scheduleC(C).
%error(b(C1,P,C2,T1,Y1))
:- prereqsStream(C1,P), prereqs(C1,P,C2), schedule(D1,C1), not scheduleC(C2).
%error(a(C1,P,C2,T1,Y1,T2,Y2))
:- prereqsStream(C1,P), prereqs(C1,P,C2), schedule(D1,C1), schedule(D2,C2), D2 >=  D1.

uocLoad(D,L) :- date(D), L = #sum { U, C: schedule(D,C), uoc(C, U) }.
:- maxUocLoad(L), uocLoad(D,L2), L < L2.

#show.
#show schedule/2.
%#show error/1.
