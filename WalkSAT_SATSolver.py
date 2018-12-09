import time
import clause
import os
import matplotlib.pyplot as plt
import numpy as np
#from dpll import *
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
    l = []
    for symbol in clause:
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
    clauses,symbols = getClauses_Symbols(cnf)
    return walkSAT(clauses,symbols,p,flip)

def walkSAT(clauses,symbols,p,max_flips):
    # a random assignment of true/false to the symbols in clauses
    model = {s: random.choice([True,False]) for s in symbols}
    for i in range(max_flips):
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
                sym = abs(int(sym))
                #Return the number of clauses satisfied after flipping the symbol
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause,model)])
                model[sym] = not model[sym]
                return count
            sym = max(prop_symbols(clause), key=sat_count)
        sym = abs(int(sym))
        model[sym] = not model[sym]
    # If no solution is found within the flip limit, we return failure
    return None







def walksat_experiment_1():

    files = [f for f in os.listdir('satisfy1/')]
    x_vals = []
    y_vals = []
    ps = [round(x * 0.1, 2) for x in range(1, 11)]
    flips = 20000
    for p in ps:
        #print("@@@@@@@@@@@@@{}@@@@@@@@@".format(p))
        print("@@@ Probability {}".format(p))
        #print("next FLIP")
        x_vals.append(p)
        sat_count = 0
        unsat_count = 0
        for f in files:
            print(f)
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
        y_vals.append( str((sat_count / len(files) ) * 100) + "%")
    print(x_vals)
    x_pos = np.arange(len(x_vals))
    plt.figure(figsize=(10,8))
    plt.ylabel('Successfully Solved %')
    plt.xlabel("Probability P")
    plt.title('Value of Probability P vs Percentage of Problems Solved')
    plt.bar(x_pos, y_vals, align="center",alpha=0.5)
    plt.xticks(x_pos, x_vals)
    plt.show()

def walksat_experiment_2():
    #F = ['175var','200var','225var','250var']
    files = [f for f in os.listdir('satisfy1')]
    output = []
    num_vars = 20
    flip = int(np.log(num_vars**4) * num_vars * 15)
    sat_count = 0
    sat2_count = 0
    unsat_count = 0
    unsat2_count = 0
    wsat_times = []
    for f in files:
        #print(f)
        cnf = clause.giveInput('satisfy1/' + f)
        s = time.time()
        model = walkSAT_satisfiable(cnf,0.7,flip)
        e = time.time()
        wsat_times.append((e - s) if model else 0)
        if model:
            print("All True!" + f + "\n")
            sat_count += 1
        else:
            print("UNSATISFIABLE" + f + "\n")
            unsat_count += 1
        new_start_time = time.time()
        model, symbols = dpll_satisfiable(cnf, new_start_time, (e-s))
        new_end_time = time.time()

        if model:
            print("Dpll All True!" + f + "\n")
            sat2_count += 1
        else:
            print("Dpll UNSATISFIABLE" + f + "\n")
            unsat2_count += 1

    plt.plot(range(len(files)), wsat_times)
    plt.xlabel("test case number")
    plt.ylabel("time to find solution in seconds")
    plt.title("WalkSAT modified with max_flips based on model")
    plt.show()
    print(wsat_times)
    print(sat2_count)
    print(sat_count)


def displayOutput(model,symbols):
    high = max(list(symbols))
    out = []
    j = 0
    for i in range(1,high+1):
        if i in model:
            if model[i] is True:
                j = 1
            else:
                j = 0
        else:
            j = 0
        out.append(j)
    out = str(out).replace("[", "(").replace("]",")")
    return out

if __name__ == "__main__":
    cnf = "(3,-5,6),(-9,2,1)"
    clauses, symbols = getClauses_Symbols(cnf)
    model = walkSAT_satisfiable(cnf,0.7,10000)
    print(model)
    if model:
        print("All True! "+ "\n")
        print(displayOutput(model,symbols))
    else:
        print("UNSATISFIABLE " + "\n")
    """
    files = [f for f in os.listdir('satisfy1')]

    output = []
    #num_vars = 20
    # flip_count = int(np.log(num_vars**4) * num_vars * 15)
    flip_count = 10000
    #print("number of flips we will do: " + str(flip_count))
    sat_count = 0
    unsat_count = 0
    times = []
    for f in files[:1]:
        # cnf = parser('uf20-91/' + f)
        cnf = clause.giveInput('satisfy1/' + f)
        start_time = time.time()
        model = walkSAT_satisfiable(cnf,0.7,flip_count)
        print(model)
        end_time = time.time()
        times.append(end_time-start_time)
        if model:
            print(model)
            print("All True! " + f + "\n")
            sat_count += 1
        else:
            print("UNSATISFIABLE " + f + "\n")
            unsat_count += 1
    tup_dup = (min(times), max(times), np.mean(times), np.median(times), np.std(times))
    output.append("{}|{}|{}".format(sat_count, unsat_count,tup_dup))
    print(output)
    """