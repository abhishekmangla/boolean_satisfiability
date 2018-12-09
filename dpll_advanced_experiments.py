import time
import clause
import os
import matplotlib.pyplot as plt
import pdb
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

def dpll_satisfiable(cnf):
    clauses,symbols = getClauses_Symbols(cnf)
    #print("clauses: ",clauses)
    #print("symbols: ",symbols)
    return dpll(clauses,symbols,[])

def dpll_satisfiable2(cnf):
    clauses,symbols = getClauses_Symbols(cnf)
    #print("clauses: ",clauses)
    #print("symbols: ",symbols)
    return dpll2(clauses,symbols,[])

def pickSymbol2(clauses, model,symbols):
    combined = model + compliment(model)

    L = sorted(symbols,key=symbols.count,reverse=True)
    for s in L:
        if s[0] != "-" and s not in combined:
            return s
    return False

def dpll2(clauses,symbols,model):
    #print("In DPLL...\n clauses: {}\n symbols: {}\n model: {}\n".format(clauses, symbols,model))
    if allTrue(clauses, model):
        return model,symbols
    if someFalse(clauses,model):
        #print("Some False!\n")
        return False,False
    pure = findPureSymbol(clauses, model)
    if pure:
        return dpll2(clauses,symbols, model + [pure])

    unit = findUnitClause(clauses, model)
    if unit:
        #print("unit was found: ", unit)
        return dpll2(clauses, symbols,model + [unit])
    pick = pickSymbol2(clauses, model,symbols)
    #print(pick)
    if pick:
        result = dpll2(clauses, symbols, model+[pick])
        if result:
            return result
        else:
            if pick[0] == "-":
                result = dpll2(clauses, symbols, model + [pick])
            else:
                result = dpll2(clauses, symbols, model + ["-"+pick])
            if result:
                return result
            else:
                return False

def dpll(clauses,symbols,model):
    #print("In DPLL...\n clauses: {}\n symbols: {}\n model: {}\n".format(clauses, symbols,model))
    if allTrue(clauses, model):
        print("All True!\n")
        return model,symbols
    if someFalse(clauses,model):
        print("Some False!\n")
        return False
    pure = findPureSymbol(clauses, model)
    if pure:
        return dpll(clauses,symbols, model + [pure])

    unit = findUnitClause(clauses, model)
    if unit:
        #print("unit was found: ", unit)
        return dpll(clauses, symbols,model + [unit])
    pick = pickSymbol(clauses, model)
    if pick:
        result = dpll(clauses, symbols, model+[pick])
        if result:
            return result
        else:
            if pick[0] == "-":
                result = dpll(clauses, symbols, model + [pick])
            else:
                result = dpll(clauses, symbols, model + ["-"+pick])
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

"""
In This experiment, we compare performance of picking most frequent
symbols versus picking symbols randomly as done in vanilla dpll
Pick the 25 vars benchmark and run on all 1000 testcases.
We compare time performance between both vanilla and this modified DPLL.
"""
def experiment_three():
    y_vals_vanilla = []
    y_vals_optimized = []
    files_in_subdir = [(id, f) for id, f in enumerate(os.listdir("uf20-91/")) if id % 100 == 0]
    files = list(map(lambda x: x[1], files_in_subdir))
    for f in files:
        # start_time = time.time()
        # cnf = clause.giveInput("uf20-91/" + f)
        # model, symbols = dpll_satisfiable(cnf)
        # end_time = time.time()
        # # print(model, symbols)
        # if model and symbols:
        #     y_vals_vanilla.append(end_time-start_time)

        start_time = time.time()
        cnf = clause.giveInput("uf20-91/" + f)
        model, symbols = dpll_satisfiable2(cnf)
        end_time = time.time()
        print(model, symbols)
        if model and symbols:

            y_vals_optimized.append(end_time-start_time)

    x_vals = list(map(lambda x: x[0], files_in_subdir))
    print(y_vals_vanilla)
    print(y_vals_optimized)
    plt.plot(x_vals, y_vals_vanilla, 'r--', x_vals, y_vals_vanilla, 'y')
    plt.legend()
    # plt.plot(x_vals, y_vals_vanilla, 'r--', x_vals, y_vals_optimized, 'g--')
    plt.ylabel('Time to solve (seconds)')
    plt.xlabel("test case number")
    plt.title('25 variables vs time to solve')
    plt.show()

experiment_three()
