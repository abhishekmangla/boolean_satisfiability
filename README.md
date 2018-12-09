# boolean_satisfiability

Our programs are in python and we used all standard python libraries. We used the textbook (Artificial Intelligence: A Modern Approach)'s online code base as a launchpad for the basic implementations of DPLL and walkSAT. We added a lot of our code for running experiments, modifying the algorithms, adding timeouts, etc. The source code for our experiments which we used to generate the graphs in final report are in the "experiments" directory.

The "assets" directory has graphs and images that we used in our final report.

## our final algorithm: walkSAT modified
```python walksat_final.py```
How does it take input?
It will output an answer if it finds one in (1,0,0,1) format where 1 means True, 0 means False. Index + 1 corresponds to variable number.
