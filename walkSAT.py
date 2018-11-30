import time
import clause
import os
import matplotlib.pyplot as plt

import random

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
            symbols.add(int(symbol))

        clauses.append(new_clause)
    symLength = len(symbols)
    return clauses, symbols    


def prop_symbols(clause):
    symbols = set()
    for symbol in clause:
            symbols.add(symbol)
    return symbols

#evaluate a propositional logical sentence in a model
def pl_true(clause,model):
    #print("clause:",clause)
    #print("model:",model)
    #returns true if the propositional logical expression is true in the model 
    if len([symbol for symbol in clause if model[int(symbol)] is True]) == 0:
        return False
    return True


def probability(p):
    """Return true with probability p."""
    return p > random.uniform(0.0, 1.0)

def walkSAT_satisfiable(cnf):
    #print(cnf)
    clauses,symbols = getClauses_Symbols(cnf)
    #probability of choosing to do a "random walk" move
    p = 0.5
    #print("clauses:", clauses)
    #print("symbols:", symbols)
    #number of flips allowed before giving up 
    max_flips = 10000
    return walkSAT(clauses,symbols,p,max_flips)

def walkSAT(clauses,symbols,p,max_flips):
    
    # a random assignment of true/false to the symbols in clauses
    model = {s: random.choice([True,False]) for s in symbols}

    
    for i in range(max_flips):
        #print("Loop:",i)
        satisfied, unsatisfied = [], []
        for clause in clauses:
            (satisfied if pl_true(clause, model) else unsatisfied).append(clause)
        if not unsatisfied: #if model satisfies all the clauses
            return model
        clause = random.choice(unsatisfied)
        if probability(p):
            sym = random.choice(list(prop_symbols(clause)))
        else:
            #Flip the symbol in clause that maximizes number of sat. clauses
            def sat_count(sym):
                sym = int(sym)
                #Return the number of clauses satisfied after flipping the symbol
                #print("sym:",type(sym))
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause,model)])
                model[sym] = not model[sym]
                return count
            sym = max(prop_symbols(clause), key=sat_count)
        sym = int(sym)
        model[sym] = not model[sym]
    # If no solution is found within the flip limit, we return failure
    return None 

def output(model):
    print("")
    



if __name__ == "__main__":
    #start_time = time.time()
    #cnf = "(3,-5,6),(-9,2,1)"
    files = [f for f in os.listdir('satisfy2')]
    x_vals = range(len(files))
    #range(len(files))
    y_vals = []
    sat_count = 0
    unsat_count = 0 

    for f in files:
        start_time = time.time()
        cnf = clause.giveInput("satisfy2/" + f)
        if walkSAT_satisfiable(cnf):
            print("All True!" + f + "\n")
            sat_count += 1
        else:
            print("UNSATISFIABLE" + f + "\n")
            unsat_count += 1
        end_time = time.time()
        y_vals.append(end_time - start_time)
    #print("Elapsed Time: %s seconds" % (end_time - start_time))
    
    print("total count: " + str(len(files)))
    print("satisfiable count: " + str(sat_count))
    print("unsatisfiable count: " + str(unsat_count))
    print("average time: "+ str(sum(y_vals)/len(y_vals)))
    plt.plot(x_vals, y_vals)
    plt.show()