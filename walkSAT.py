import time


import random

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


def prop_symbols(clause):
    symbols = set()
    for symbol in clause:
            symbols.add(symbol)
    return symbols

#evaluate a propositional logical sentence in a model
def pl_true(clause,model):
    print("clause:",clause)
    print("model:",model)
    #returns true if the propositional logical expression is true in the model 
    if len([symbol for symbol in clause if model[symbol] is True]) == 0:
        return False
    return True


def probability(p):
    """Return true with probability p."""
    return p > random.uniform(0.0, 1.0)

def walkSAT_satisfiable(cnf):
    print(cnf)
    clauses,symbols = getClauses_Symbols(cnf)
    #probability of choosing to do a "random walk" move
    p = 0.5
    print("clauses:", clauses)
    print("symbols:", symbols)
    #number of flips allowed before giving up 
    max_flips = 10000
    return walkSAT(clauses,symbols,p,max_flips)

def walkSAT(clauses,symbols,p,max_flips):
    
    # a random assignment of true/false to the symbols in clauses
    model = {s: random.choice([True,False]) for s in symbols}

    
    for i in range(max_flips):
        print(i)
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
                #Return the number of clauses satisfied after flipping the symbol
                model[sym] = not model[sym]
                count = len([clause for clause in clauses if pl_true(clause,model)])
                model[sym] = not model[sym]
                return count
            sym = max(prop_symbols(clause), key=sat_count)
        model[sym] = not model[sym]
    # If no solution is found within the flip limit, we return failure
    return None 



if __name__ == "__main__":
    start_time = time.time()
    cnf = "(3,-5,6),(-9,2,1)"
    
    walkSAT_satisfiable(cnf)
    end_time = time.time()
    print("Elapsed Time: %s seconds" % (end_time - start_time))