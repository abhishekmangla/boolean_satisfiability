import time
import clause
import os
import matplotlib.pyplot as plt
import pdb
from functools import reduce
import numpy as np

def parser(filename):
    with open(filename, 'r') as file:
        content = file.readlines()
        cnf = ""
        for line in content:
            cnf = cnf + line
    return cnf


def runSAT():
    files = [f for f in os.listdir('3SAT')]
    sat_count = 0
    unsat_count = 0
    for f in files:
        start_time = time.time()
        cnf = parser("3SAT/" + f)
        model = dpll_satisfiable(cnf)
        #print(model)
        #print(model)
        if model:
            print("All True!" + f + "\n")
            sat_count += 1
        else:
            print("UNSATISFIABLE" + f + "\n")
            unsat_count += 1
        end_time = time.time()
        print("Elapsed Time: %s seconds" % (end_time - start_time))


    print("total count: " + str(len(files)))
    print("satisfiable count: " + str(sat_count))



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

def pickSymbol2(clauses, model,symbols):
    combined = model + compliment(model)

    L = sorted(symbols,key=symbols.count,reverse=True)
    np.random.shuffle(L)
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

def dpll_satisfiable(cnf, var):
    clauses,symbols = getClauses_Symbols(cnf)
    #print("clauses: ",clauses)
    #print("symbols: ",symbols)
    return dpll(clauses,symbols,[], var)

def dpll(clauses,symbols,model, var):
    #print("In DPLL...\n clauses: {}\n symbols: {}\n model: {}\n".format(clauses, symbols,model))
    if allTrue(clauses, model):
        return model,symbols
    if someFalse(clauses,model):
        #print("Some False!\n")
        return False,False
    pure = findPureSymbol(clauses, model)
    if pure:
        return dpll(clauses,symbols, model + [pure], var)

    unit = findUnitClause(clauses, model)
    if unit:
        #print("unit was found: ", unit)
        return dpll(clauses, symbols,model + [unit], var)
    pick = None
    if var:
        pick = pickSymbol2(clauses, model,symbols)
    else:
        pick = pickSymbol(clauses, model)
    #print(pick)
    if pick:
        result = dpll(clauses, symbols, model+[pick], var)
        if result:
            return result
        else:
            if pick[0] == "-":
                result = dpll(clauses, symbols, model + [pick], var)
            else:
                result = dpll(clauses, symbols, model + ["-"+pick], var)
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

if __name__ == "__main__":

    """
    s = parser("3SAT/" + "3SAT-N=100-C=430-idx=0.txt")
    #print([f for f in os.listdir('3SAT')])
    print(s)
    """

    """
    (3,-5,6),(-9,2,1) -> (1,0,1,0,0,0,0,0,0)
    """
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

    #unsatisfy

    """
    cnf = "(3,-5,6),(-9,2,1)"
    model,symbols = dpll_satisfiable(cnf)
    if model:
        print("All True!")
        print(symbols)
        print(output(model,symbols))
    else:
        print("UNSATISFIABLE")
    """


    files = [f for f in os.listdir('uf100-430/')]
    x_vals = range(len(files))
    #x_vals = range(len(files))
    #range(len(files))
    y_vals = []
    y_vals2 = []
    sat_count = 0
    sat_count2 = 0
    unsat_count = 0
    unsat_count2 = 0

    for f in files:
        cnf = clause.giveInput("uf100-430/" + f)
        start_time = time.time()
        model = dpll_satisfiable(cnf, False)
        end_time = time.time()
        #print(model)
        #print(model)
        if model:
            print("All True!" + f + "\n")
            # print(output(model,symbols))
            sat_count += 1
            y_vals.append(end_time - start_time)
        else:
            print("UNSATISFIABLE" + f + "\n")
            unsat_count += 1

        # print("Elapsed Time: %s seconds" % (end_time - start_time))


        start_time= time.time()
        model2 = dpll_satisfiable(cnf, True)
        end_time = time.time()
        if model2:
            print("All True!" + f + "\n")
            # print(output(model,symbols))
            sat_count2 += 1

            y_vals2.append(end_time - start_time)
        else:
            print("UNSATISFIABLE" + f + "\n")
            unsat_count2 += 1

        # print("Elapsed Time: %s seconds" % (end_time - start_time))




    print("total count: " + str(len(files)))
    print("satisfiable count: " + str(sat_count))
    print("unsatisfiable count: " + str(unsat_count))
    print("average time: "+ str(sum(y_vals)/len(y_vals)))
    plt.plot(x_vals, y_vals, 'r', x_vals, y_vals2, 'b')
    plt.xlabel("Test case number")
    plt.ylabel("time in seconds")
    plt.legend(['normal DPLL', 'random DPLL'], loc='upper right')
    plt.title("DPLL vs random DPLL for 50 variable benchmark")
    plt.legend()
    plt.show()



    #20 variables 91 clauses: avg time = 0.08641732978820801
    #50 variables 218 clauses: avg time = 9.446

    #Regular algorithm
    #50 variables 218 clauses for 50 files:
        #total count: 1000
        #satisfiable count: 50
        #unsatisfiable count: 0
        #average time: 4.281889734268188

    #unassigned symbol modified to most frequent:
    #50 variables 218 clauses for 50 files:
        #total count: 1000
        #satisfiable count: 50
        #unsatisfiable count: 0
        #average time: 1.6558127450942992

    #least frequent
    #50 variables 218 clauses for 5 files:
        #total count: 1000
        #satisfiable count: 5
        #unsatisfiable count: 0
        #average time: 67.41400866508484
