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
    



if __name__ == "__main__":
    #start_time = time.time()
    #cnf = "(3,-5,6),(-9,2,1)"
    """
    cnf = "(1,2,3),(1,2,-3),(1,-2,3),(1,-2,-3),(-1,2,3),(-1,2,-3),(-1,-2,3),(-1,-2,-3)"
    if walkSAT_satisfiable(cnf):
        print(walkSAT_satisfiable(cnf))
        print("True")
    else:
        print("False")
    """
    
    files = [f for f in os.listdir('satisfy2')]
    x_vals = range(10)
    #range(len(files))
    #y_vals = []
    #sat_count = 0
    #unsat_count = 0 
    rfile = open("1.resultWALK_satisfy_100files_50_219.txt","w")
    
    ps = [round(x * 0.1,2) for x in range(5, 9)]
    flips = [x for x in range(1000,30000,1000)]
    for p in ps:
        #print("@@@@@@@@@@@@@{}@@@@@@@@@".format(p))
        for flip in flips: 
            print("@@@{} p @@@@@@{} flips@@@@@@@@@".format(p,flip))
            #print("next FLIP")
            y_vals = []
            sat_count = 0
            unsat_count = 0 
            for f in files[:10]:
                start_time = time.time()
                cnf = clause.giveInput("satisfy2/" + f)
                if walkSAT_satisfiable(cnf,p,flip):
                    #print("All True!" + f + "\n")
                    sat_count += 1
                else:
                    #print("UNSATISFIABLE" + f + "\n")
                    unsat_count += 1
                end_time = time.time()
                y_vals.append(end_time - start_time)
    #print("Elapsed Time: %s seconds" % (end_time - start_time))
            rfile.write("Probability: {}, MaxFips: {}\n".format(str(p), str(flip)))
            rfile.write("Avgerage time: {}\n".format(str(sum(y_vals)/len(y_vals))))
            rfile.write("satisfiable count: {}, unsatisfiable count: {}\n".format(str(sat_count),str(unsat_count)))
            rfile.write("")
    rfile.close()
    """
    print("total count: " + str(len(files)))
    print("satisfiable count: " + str(sat_count))
    print("unsatisfiable count: " + str(unsat_count))
    print("average time: "+ str(sum(y_vals)/len(y_vals)))
    """
    #plt.plot(x_vals, y_vals)
    #plt.show()
    

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
