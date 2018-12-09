# boolean_satisfiability

Our programs are implemented in python 3 and we used all standard python libraries. We used the textbook (Artificial Intelligence: A Modern Approach)'s online code base as a launchpad for the basic implementations of DPLL and walkSAT. We added a lot of our code for running experiments, modifying the algorithms, adding timeouts, etc. The source code for our experiments which we used to generate the graphs in final report are in the "experiments" directory.

The "assets" directory has graphs and images that we used in our final report.

## our final algorithm: walkSAT modified
To run:
```python WalkSAT_SATSolver.py sample_50var_testcase.txt```

The program will read in an input file containing a set of clauses in CNF. Multiple input files can also be specified when delimited by spaces. For example: ```python WalkSAT_SATSolver.py testcase_1.txt testcase_2.txt```


The output will display an answer if it finds one in (1,0,0,1) vector format where 1 means True, 0 means False. If no solution is found, UNSATISFIABLE will be printed. The index position + 1 corresponds to variable number so (1,0,0) indicates variable 1 is True and variables 2 and 3 are False.
