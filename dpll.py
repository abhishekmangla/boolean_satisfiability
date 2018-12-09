import time
import clause
import os
import matplotlib.pyplot as plt
import numpy as np
import pdb
import re
#Input CNF into clauses, symbols for dpll
def getClauses_Symbols(cnf):
    clauses = []
    symbols = []
    split_clauses = cnf.split("),")
    for clause in split_clauses:
        clause = clause.replace("(", "").replace(")", "")
        new_clause = []
        for symbol in clause.split(","):
            new_clause.append(symbol)
            symbols.append(symbol)

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

def pickSymbol_most_freq(clauses, model,symbols):
    combined = model + compliment(model)

    L = sorted(symbols,key=symbols.count,reverse=True)
    for s in L:
        if s[0] != "-" and s not in combined:
            return s
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
        print("HERE")
        return None, None

def dpll_satisfiable2(cnf, start_time, timeout=1):
    clauses,symbols = getClauses_Symbols(cnf)
    #print("clauses: ",clauses)
    #print("symbols: ",symbols)
    try:
        return dpll2(clauses,symbols,[],start_time,timeout)
    except ValueError:
        print("HERE")
        return None, None

def dpll2(clauses, symbols, model, start_time, timeout):
    #print("In DPLL...\n clauses: {}\n symbols: {}\n model: {}\n".format(clauses, symbols,model))
    # print(time.time() - start_time)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time > timeout:
        raise ValueError("timeout")
    if allTrue(clauses, model):
        return model,symbols
    if someFalse(clauses,model):
        #print("Some False!\n")
        return False,False
    pure = findPureSymbol(clauses, model)
    if pure:
        return dpll2(clauses,symbols, model + [pure], start_time, timeout)

    unit = findUnitClause(clauses, model)
    if unit:
        #print("unit was found: ", unit)
        return dpll2(clauses, symbols,model + [unit], start_time, timeout)
    pick = pickSymbol_most_freq(clauses, model, symbols)
    if pick:
        result = dpll2(clauses, symbols, model+[pick], start_time, timeout)
        if result:
            return result
        else:
            if pick[0] == "-":
                result = dpll2(clauses, symbols, model + [pick], start_time, timeout)
            else:
                result = dpll2(clauses, symbols, model + ["-"+pick], start_time, timeout)
            if result:
                return result
            else:
                return False

def dpll(clauses, symbols, model, start_time, timeout):
    #print("In DPLL...\n clauses: {}\n symbols: {}\n model: {}\n".format(clauses, symbols,model))
    # print(time.time() - start_time)
    end_time = time.time()
    elapsed_time = end_time - start_time
    if elapsed_time > timeout:
        raise ValueError("timeout")
    if allTrue(clauses, model):
        return model,symbols
    if someFalse(clauses,model):
        #print("Some False!\n")
        return False,False
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
    s = [abs(int(a)) for a in symbols]
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
This experiment sets a time limit of 1 seconds on dpll_satisfiable. And then
it finds how many test cases from each directory we could solve given that timeout
This experiment gives us an understanding of what size of problems DPLL is good
at solving until the time constraints get out of hand.
"""
def experiment_one():
    all_subdirs = filter(lambda x: 'git' not in x and "ipynb" not in x and len(x) > 1, [x[0] for x in os.walk(".")])
    all_subdirs = sorted(all_subdirs, key=lambda x: int(re.findall(r"[\w']+", x)[0][2:]))
    x_vals = all_subdirs
    y_vals = []
    dirs_solving = all_subdirs[:]
    for subdir in dirs_solving:
        files_in_subdir = [f for f in os.listdir(subdir)]
        sat_count = 0
        for f in files_in_subdir[:]:
            start_time = time.time()
            cnf = clause.giveInput(subdir + "/" + f)
            model, symbols = dpll_satisfiable(cnf, start_time,1)
            print(model, symbols)
            if model and symbols:
                sat_count += 1
        y_vals.append(sat_count)

    y_pos = np.arange(len(dirs_solving))

    plt.bar(y_pos, y_vals, align='center', alpha=0.5)
    plt.xticks(y_pos, map(lambda x: int(re.findall(r"[\w']+", x)[0][2:]), dirs_solving))
    plt.ylabel('Successfully solved')
    plt.xlabel("Number of variables")
    plt.title('Number of variables in CNF vs number of problems solved')
    plt.show()

"""
This experiment sets a time limit of 1 seconds on dpll_satisfiable. And then
it finds how many test cases from each directory we could solve given that timeout
This experiment gives us an understanding of what size of problems DPLL is good
at solving until the time constraints get out of hand.
"""
def experiment_two():
    all_subdirs = filter(lambda x: 'git' not in x and "ipynb" not in x and len(x) > 1 and "CBS" in x, [x[0] for x in os.walk(".")])
    all_subdirs = sorted(all_subdirs, key=lambda x: int(re.findall(r"[\w']+", x)[0].split("_")[3][1:]))
    x_vals = all_subdirs
    y_vals = []
    dirs_solving = all_subdirs[:]
    for subdir in dirs_solving:
        files_in_subdir = [f for f in os.listdir(subdir)]
        sat_count = 0
        times = []
        for f in files_in_subdir[:1]:
            start_time = time.time()
            cnf = clause.giveInput(subdir + "/" + f)
            model, symbols = dpll_satisfiable(cnf, start_time,float("inf"))
            end_time = time.time()
            print(model, symbols)
            if model and symbols:
                times.append(end_time-start_time)
        y_vals.append(np.mean(times))

    y_pos = np.arange(len(dirs_solving))

    plt.bar(y_pos, y_vals, align='center', alpha=0.5)
    plt.xticks(y_pos, map(lambda x: int(re.findall(r"[\w']+", x)[0].split("_")[3][1:]), dirs_solving))
    plt.ylabel('Time to solve (seconds)')
    plt.xlabel("Number of clauses")
    plt.title('100 variables with different number of clauses vs time to solve')
    plt.show()


"""
In This experiment, we compare performance of picking most frequent
symbols versus picking symbols randomly as done in vanilla dpll
Pick the 25 vars benchmark and run on all 1000 testcases.
We compare time performance between both vanilla and this modified DPLL.
"""
def experiment_three():
    y_vals_vanilla = []
    y_vals_optimized = []
    files_in_subdir = [f for f in os.listdir("uf20-91/")]
    sat_count = 0
    times = []
    for f in files_in_subdir[:]:
        start_time = time.time()
        cnf = clause.giveInput("uf20-91/" + f)
        model, symbols = dpll_satisfiable(cnf, start_time,float("inf"))
        end_time = time.time()
        print(model, symbols)
        if model and symbols:
            sat_count += 1
            y_vals_vanilla.append(end_time-start_time)

        # start_time = time.time()
        # cnf = clause.giveInput("uf20-91/" + f)
        # model, symbols = dpll_satisfiable2(cnf, start_time,float("inf"))
        # end_time = time.time()
        print(model, symbols)
        # if model and symbols:
        #     y_vals_optimized.append(end_time-start_time)

    print(sat_count, len(files_in_subdir))
    x_vals = list(range(len(y_vals_vanilla)))
    print(len(x_vals))
    print(len(y_vals_vanilla))
    print(len(y_vals_optimized))
    plt.plot(x_vals, y_vals_vanilla, 'r--')

    # plt.plot(x_vals, y_vals_vanilla, 'r--', x_vals, y_vals_optimized, 'g--')
    plt.ylabel('Time to solve (seconds)')
    plt.xlabel("test case number")
    plt.title('25 variables vs time to solve')
    plt.show()


if __name__ == "__main__":
    """
    (3,-5,6),(-9,2,1) -> (1,0,1,0,0,0,0,0,0)
    """
    # experiment_one()
    # experiment_two()
    experiment_three()
    #satisfy
    #cnf = "(3,-5,6),(-9,2,1)"

    #unsatisfy
    #cnf = "(1),(-1)"

    #satisfy
    #cnf =  "(-9,3,-15,0),(-12,-4,-15,0),(6,14,-17,0)"

    #unsatisfy
    #cnf = "(1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3),(-1,2,3),(-1,2,-3),(-1,-2,3),(-1,-2,-3)"

    #satisfy
    #cnf = "(-1,2,3),(1,3,4),(1,3,-4),(1,-3,4),(1,-3,-4),(-2,-3,4),(-1,2,-3),(-1,-2,3)"

    #unsatisfy
    #cnf = "(-1,2,4),(-2,3,4),(1,-3,4),(1,-2,-4),(2,-3,-4),(-1,3,-4),(1,2,3),(-1,-2,-3)"
    #pdb.set_trace()
    # files = [f for f in os.listdir('UF250.1065.100/')]
    # x_vals = range(1)
    # y_vals = []
    # sat_count = 0
    # for f in files[:1]:
    #     start_time = time.time()
    #     cnf = clause.giveInput("UF250.1065.100/" + f)
    #     model,symbols = dpll_satisfiable(cnf)
    #     if model and symbols:
    #         # print(output(model,symbols))
    #         sat_count += 1
    #     end_time = time.time()
    #     # print("Elapsed Time: %s seconds" % (end_time - start_time))
    #     y_vals.append(end_time - start_time)
    #
    # print("total count: " + str(len(files)))
    # print("satisfiable count: " + str(sat_count))
    # print("average time: "+ str(sum(y_vals)/len(y_vals)))
    # plt.plot(x_vals, y_vals)
    # plt.show()
