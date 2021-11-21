# Algorithms

## greedy
you greedily use the priority queue and assume that the order is somewhat reasonable. 
This is at worst a T * Nlog(N) solution, where T is the number of terms and N is the number of courses. This is generally a blazing fast algo, but makes no guarantees on optimaility.
This is heavily based on the way the priority queue places courses: 
first in order of dependancy (how many other courses depend on this course to be done?)
then on rarity (how many times is it offered?)
then on difficulty (what is the level of the course?)

simply put:
1. Place unplaced courses in a priority queue
2. Go through the plan term by term. For each term, attempt to place a course in the prder provided by the priority queue. Keep attempting to do this until you have filled up the term

## ASP
A solution provided by Abdallah Saffidine (abdallah.saffidine@gmail.com)
This is an ASP solver that uses clingo to produce a solution. This is an AI-type solution.
It takes in its constraints and tries to come up with both solutions and contradictions. This allows it to quickly find solutions for easy problems and find contradictions for impossible ones (this is pretty useful for us), but can take a while for hard problems. Overall, it is pretty fast, and can guarantee optimality through an iterative process in a much better way than the other two algos here.


## anytime end
This is basically the same as the greedy solution, but uses an iterative deepening on the length of the degree. This has a horrible worst case complexity time, so the idea is to use the priority queue to push the best solutions to the left of the tree. There are ways to optomise this by using forward checking.
This is not currently implemented in the new form of the solver, but is implemented (without the anytime end) in the old master branch (look at one of the commits from before ~september 2021)
