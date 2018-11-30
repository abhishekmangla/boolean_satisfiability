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

if __name__ == "__main__":
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
    files = [f for f in os.listdir('satisfy1')]
    x_vals = range(100)
    y_vals = []
    sat_count = 0
    for f in files[:100]:
        start_time = time.time()
        cnf = clause.giveInput("satisfy1/" + f)
        if dpll_satisfiable(cnf):
            model,symbols = dpll_satisfiable(cnf)
            # print(output(model,symbols))
            sat_count += 1    
        end_time = time.time()
        # print("Elapsed Time: %s seconds" % (end_time - start_time))
        y_vals.append(end_time - start_time)
    
    print("total count: " + str(len(files)))
    print("satisfiable count: " + str(sat_count))
    print("average time: "+ str(sum(y_vals)/len(y_vals)))
    plt.plot(x_vals, y_vals)
    plt.show()