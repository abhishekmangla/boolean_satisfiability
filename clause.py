from functools import reduce

def giveInput(filename):
    #uf20-03.txt : satisfy
    #uuf50-01 : ?
    with open(filename, 'r') as file:
        content = file.readlines()
        cnf = ""
        skip_count = 0
        for line in content:
            if line[0] == "%":
                break
            if skip_count < 8:
                skip_count += 1
                continue
            arr = line.split()
            if arr[-1] == '0': 
                new_phrase = reduce(lambda x, y: x + "," + y, arr[:-1])
                cnf += "(" + new_phrase + "),"

    return cnf.rstrip(",")


#print(giveInput("satisfy1/uf20-01.cnf"))
