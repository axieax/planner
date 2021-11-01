term(0..3). year(2022..2027).

%% Input
%% data: term(T). course(C). available(C,T). prereqs(C1,P,C2). uoc(C,U).
%% user: year(Y). maxAcceptableLoad(L). selected(C).

{ schedule(C,T,Y) : term(T), year(Y) } 1 :- course(C).
:- schedule(C,T,Y), not available(C,T).
scheduleC(C) :- schedule(C,T,Y).
:- selected(C), not scheduleC(C).


1 { prereqsStream(C,P) : prereqsOption(C,P) } :- scheduleC(C).
%error(b(C1,P,C2,T1,Y1))
:- prereqsStream(C1,P), prereqs(C1,P,C2), schedule(C1,T1,Y1), not scheduleC(C2).
%error(a(C1,P,C2,T1,Y1,T2,Y2))
:- prereqsStream(C1,P), prereqs(C1,P,C2), schedule(C1,T1,Y1), schedule(C2,T2,Y2), Y2 >  Y1.
:- prereqsStream(C1,P), prereqs(C1,P,C2), schedule(C1,T1,Y1), schedule(C2,T2,Y1), T2 >= T1.

load(T,Y,L) :- term(T), year(Y), L = #sum { U, C: schedule(C, T, Y), uoc(C, U) }.
:- maxAcceptableLoad(L), load(T,Y,L2), L < L2.

%prereqsStream(comp3411,0).
%schedule(comp1927,1,2024).
%schedule(comp2521,3,2025).
%schedule(comp3411,1,2026).
%:- error(b(C1,_,_,_,_)), C1 != comp3411.
#show.
#show schedule/3.
%#show error/1.
%#show prereqsStream(P) : prereqsStream(comp3411,P).
