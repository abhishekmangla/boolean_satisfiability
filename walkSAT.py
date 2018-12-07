import time
import clause
import os
import matplotlib.pyplot as plt
import numpy as np

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
    #print("clause:",clause)
    #print("model:",model)
    #returns true if the propositional logical expression is true in the model
    #print("model:", model)
    #print("clause:",clause)
    l = []
    for symbol in clause:
        #print("clause:", clause)
        #print("symbol:",symbol)
        #print("model:", model)
        if int(symbol) >= 0:
            if model[int(symbol)] is True:
                l.append(symbol)
        else:
            if model[abs(int(symbol))] is False:
                l.append(symbol)

        """
            if str(abs(int(symbol))) in clause:
                if model[abs(int(symbol))] is False:
                    if abs(int(symbol)) not in l:
                        l.append(abs(int(symbol)))
            else:
                if model[int(symbol)] is False:
                    l.append(int(symbol))
        """
    if len(l) == 0:
        return False

    return True


def probability(p):
    """Return true with probability p."""
    return p > random.uniform(0.0, 1.0)

def walkSAT_satisfiable(cnf,p,flip):
    #print(cnf)
    clauses,symbols = getClauses_Symbols(cnf)
    #print("clauses:",clauses)
    #probability of choosing to do a "random walk" move
    #p = 0.65
    #print("clauses:", clauses)
    #print("symbols:", symbols)
    #number of flips allowed before giving up
    #max_flips = 1000
    return walkSAT(clauses,symbols,p,flip)

def walkSAT(clauses,symbols,p,max_flips):

    # a random assignment of true/false to the symbols in clauses
    model = {s: random.choice([True,False]) for s in symbols}


    for i in range(max_flips):
        #print("Loop:",i)
        satisfied, unsatisfied = [], []
        for clause in clauses:
            (satisfied if pl_true(clause, model) else unsatisfied).append(clause)
            #print("satisfied:", satisfied)
            #print("unsatisfied:",unsatisfied)
        if not unsatisfied: #if model satisfies all the clauses
            return model
        clause = random.choice(unsatisfied)
        if probability(p):
            sym = random.choice(list(prop_symbols(clause)))
        else:
            #Flip the symbol in clause that maximizes number of sat. clauses
            def sat_count(sym):
                sym = abs(int(sym))
                #Return the number of clauses satisfied after flipping the symbol
                #print("sym:",type(sym))
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause,model)])
                model[sym] = not model[sym]
                return count
            sym = max(prop_symbols(clause), key=sat_count)
        sym = abs(int(sym))
        model[sym] = not model[sym]
    # If no solution is found within the flip limit, we return failure
    return None

def output(model):
    print("")




def walksat_experiment_1():

    files = [f for f in os.listdir('satisfy1/')]
    x_vals = []
    y_vals = []
    ps = [round(x * 0.05, 2) for x in range(0, 21)]
    flips = 500 
    for p in ps:
        #print("@@@@@@@@@@@@@{}@@@@@@@@@".format(p))
        print("@@@ Probability {}".format(p))
        #print("next FLIP")
        x_vals.append(p)
        sat_count = 0
        unsat_count = 0
        for f in files[:5]:
            #print(f)
            #start_time = time.time()
            cnf = clause.giveInput("satisfy1/" + f)
            if walkSAT_satisfiable(cnf,p,flips):
                #print("All True!" + f + "\n")
                sat_count += 1
            else:
                #print("UNSATISFIABLE" + f + "\n")
                unsat_count += 1
            #end_time = time.time()
            #y_vals.append(end_time - start_time)
        y_vals.append((sat_count / 5) * 100)
    print(x_vals)
    x_pos = np.arange(len(x_vals))
    plt.bar(x_pos, y_vals, align="edge",alpha=0.5,width=0.8)
    
    
    #plt.tick_params(axis='x', which='major', pad=20)
    plt.xticks(x_pos, x_vals)
    plt.subplots_adjust(bottom=0.15)
    plt.show()

def walksat_experiment_2():
    print("")

    #SATISFY
    #20var_91cla avg 0.5, 10000 over 1000 files
        # avg satisfy: 0.10994927787780762
        # satisfy = 1000
    #50var_219cla 0.65, 10000 over 100 files
        # avg satisfy = 1.531405007839203
        # satisfy = 99, unsatisfy = 1
    #50var_219cla 0.65, 1000 over 100 files
        # avg satisfy = 0.9309079384803772
        # satisfy = 68, unsatisfy = 32
    #50var_219cla 0.65, 30000 over 100 files
        # avg satisfy = 1.6922698187828065
        # satisfy =  ,unsatisfy =

    #UNSATISFY
    #50var_219ccla 0.65, 1000 over 100 files
        # avg unsatisfy =1.4917813634872437
walksat_experiment_1()