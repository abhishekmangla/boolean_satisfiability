import time
import clause
import os
import matplotlib.pyplot as plt
import numpy as np
import pdb
import re

def parser(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
        cnf = ""
        for line in content:
            cnf = cnf + line
    return cnf

#Input CNF into clauses, symbols for dpll
def getClauses_Symbols(cnf):
    clauses = []
    symbols = set()
    split_clauses = cnf.split("),")
    for clause in split_clauses:
        clause = clause.replace("(", "").replace(")", "")
        new_clause = []
        for symbol in clause.split(","):
            new_clause.append(symbol)
            symbols.add(int(symbol))

        clauses.append(new_clause)
    return clauses, symbols

#If every clause in clauses is True in model
def allTrue(clauses, model):

    for clause in clauses:
        if len([symbol for symbol in clause if symbol in model]) == 0:
            return False
    return True
#If some clause in clauses is false in model
def someFalse(clauses, model):
    #The compliment of each model
    comp = compliment(model)
    for clause in clauses:
        if len([symbol for symbol in clause if symbol not in comp]) == 0:
            return True
    return False
def compliment(model):
    result = []
    for each in model:
        if each[0] == "-":
            result.append(each[1:])
        else:
            result.append("-"+each)
    return result

def findPureSymbol(clauses, model):
    modelcomp = compliment(model)
    #print("modelcomp:", modelcomp)
    candidates = []
    for clause in clauses:
        if len([symbol for symbol in clause if symbol in model]) == 0:
            #clause not yet satisified by model
            candidates = candidates + [symbol for symbol in clause]
    candidatescomp = compliment(candidates)
    #print("candidates: ",candidates)
    #print("candidatescomp:",candidatescomp)
    pure = [symbol for symbol in candidates if symbol not in candidatescomp]
    #print("pure was found: ",pure)
    for symbol in pure:
        if symbol not in model and symbol not in modelcomp:
            return symbol
    return False

def findUnitClause(clauses, model):
    modelcomp = compliment(model)
    for clause in clauses:
        remaining = [symbol for symbol in clause if symbol not in modelcomp]
        if len(remaining) == 1:
            if remaining[0] not in model:
                return remaining[0]
    return False

def pickSymbol(clauses, model):
    combined = model + compliment(model)
    for clause in clauses:
        for symbol in clause:
            if symbol[0] != "-" and symbol not in combined:
                return symbol
    return False

def dpll_satisfiable(cnf, start_time, timeout=1):
    clauses,symbols = getClauses_Symbols(cnf)
    #print("clauses: ",clauses)
    #print("symbols: ",symbols)
    try:
        return dpll(clauses,symbols,[],start_time,timeout)
    except ValueError:
        return None, None

def dpll(clauses, symbols, model, start_time, timeout):
    #print("In DPLL...\n clauses: {}\n symbols: {}\n model: {}\n".format(clauses, symbols,model))

    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time > timeout:
        raise ValueError("timeout")
    if allTrue(clauses, model):
        #print("All True!\n")
        return model,symbols
    if someFalse(clauses,model):
        #print("Some False!\n")
        return False
    pure = findPureSymbol(clauses, model)
    if pure:
        return dpll(clauses,symbols, model + [pure], start_time, timeout)

    unit = findUnitClause(clauses, model)
    if unit:
        #print("unit was found: ", unit)
        return dpll(clauses, symbols,model + [unit], start_time, timeout)
    pick = pickSymbol(clauses, model)
    if pick:
        result = dpll(clauses, symbols, model+[pick], start_time, timeout)
        if result:
            return result
        else:
            if pick[0] == "-":
                result = dpll(clauses, symbols, model + [pick], start_time, timeout)
            else:
                result = dpll(clauses, symbols, model + ["-"+pick], start_time, timeout)
            if result:
                return result
            else:
                return False

def output(model,symbols):
    s = [abs(a) for a in symbols]
    #low = min(s)
    high = max(s)
    out = []
    for i in range(1, high+1):
        if str(i) in model:
            i = 1
        elif "-"+str(i) in model:
            i = 0
        else:
            i = 0
        out.append(i)
    out = str(out).replace("[", "(").replace("]",")")
    return out




files = [f for f in os.listdir('3SAT') if "N=100-" in f]

output = []
num_vars = 100
sat_count = 0
unsat_count = 0
times = []
for f in files:
    cnf = parser("3SAT/" + f)
    start_time = time.time()
    model, symbols = dpll_satisfiable(cnf,start_time)
    end_time = time.time()
    times.append(end_time-start_time)
    if model and symbols:
        print("All True! " + f)
        sat_count += 1
    else:
        print("UNSATISFIABLE " + f)
        unsat_count += 1
tup_dup = (min(times), max(times), np.mean(times), np.median(times), np.std(times))
output.append("{}|{}|{}".format(sat_count, unsat_count,tup_dup))
print(output)
