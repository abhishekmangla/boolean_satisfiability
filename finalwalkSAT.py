import time
import clause
import os
import matplotlib.pyplot as plt
import numpy as np
import random

def parser(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
        cnf = ""
        for line in content:
            cnf = cnf + line
    return cnf

def getClauses_Symbols(cnf):
    global symLength
    clauses = []
    symbols = set()
    split_clauses = cnf.split("),")
    for clause in split_clauses:
        clause = clause.replace("(", "").replace(")", "")
        new_clause = []
        for symbol in clause.split(","):
            new_clause.append(symbol)
            if abs(int(symbol)) not in symbols:
                symbols.add(abs(int(symbol)))

        clauses.append(new_clause)
    symLength = len(symbols)
    return clauses, symbols

def prop_symbols(clause):
    symbols = set()
    for symbol in clause:
        if abs(int(symbol)) not in symbols:
            symbols.add(symbol)
    return symbols

#evaluate a propositional logical sentence in a model
def pl_true(clause,model):
    l = []
    for symbol in clause:
        if int(symbol) >= 0:
            if model[int(symbol)] is True:
                l.append(symbol)
        else:
            if model[abs(int(symbol))] is False:
                l.append(symbol)

def probability(p):
    """Return true with probability p."""
    return p > random.uniform(0.0, 1.0)

def walkSAT_satisfiable(cnf,p,flip):
    clauses,symbols = getClauses_Symbols(cnf)
    return walkSAT(clauses,symbols,p,flip)

def walkSAT(clauses,symbols,p,max_flips):
    model = {s: random.choice([True,False]) for s in symbols}
    for i in range(max_flips):
        if i % 1000 == 0:
            print("computing " + str(i))
        satisfied, unsatisfied = [], []
        for clause in clauses:
            (satisfied if pl_true(clause, model) else unsatisfied).append(clause)
        if not unsatisfied: #if model satisfies all the clauses
            return model
        clause = random.choice(unsatisfied)
        if probability(p):
            sym = random.choice(list(prop_symbols(clause)))
        else:
            def sat_count(sym):
                sym = abs(int(sym))
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause,model)])
                model[sym] = not model[sym]
                return count
            sym = max(prop_symbols(clause), key=sat_count)
        sym = abs(int(sym))
        model[sym] = not model[sym]
    # If no solution is found within the flip limit, we return failure
    return None


files = [f for f in os.listdir('uf20-91/')]

output = []
num_vars = 20
# flip_count = int(np.log(num_vars**4) * num_vars * 15)
flip_count = 10000
print("number of flips we will do: " + str(flip_count))
sat_count = 0
unsat_count = 0
times = []
for f in files:
    # cnf = parser('uf20-91/' + f)
    cnf = clause.giveInput('uf20-91/' + f)
    start_time = time.time()
    model = walkSAT_satisfiable(cnf,0.7,flip_count)
    end_time = time.time()
    times.append(end_time-start_time)
    if model:
        print("All True! " + f + "\n")
        sat_count += 1
    else:
        print("UNSATISFIABLE " + f + "\n")
        unsat_count += 1
tup_dup = (min(times), max(times), np.mean(times), np.median(times), np.std(times))
output.append("{}|{}|{}".format(sat_count, unsat_count,tup_dup))
print(output)
