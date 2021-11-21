there are a few main modules of this project

# Data / scrape
interacts with the handbook API to generate course objects in JSON form, which can be used by the rest of the project.
Exposes get_course, to fetch from this file/database

# Models
## course
the course object maintains data in an accessible form for the algorithm to use. This is mostly a dataclass, and should stay that way. Put logic in other areas.

## degree
dataclass about the degree being undertaken. Also a dataclass

## Graph
the graph is a dependancy graph. This connects what courses in some way "are beneficial" for anther course. 

## Priority queue
depends upon the graph - will make a priority queue that arranges courses based on their dependancy score, rarity, and difficulty / level. 

# Utils
## constants
used for constant values
## requirements
use a composite  pattern to generate an object that can be given a plan and asked "are the requirements met yet?"
