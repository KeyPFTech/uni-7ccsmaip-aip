import numpy as np
import pandas as pd #wireframe
#from pd import ExcelWriter as ew

def replaceFail(stats, code):
    for num, info in enumerate(stats):
        if num == 18:
            stats[num-1] = "Solution not found."
        elif num == 21:
            stats[num-1] = code
        else:
            stats[num-1] = None
    #stats=stats[:-1]


def readFile(name):
    file = open("plans/"+name, "r")
    read_file = file.readlines()
    stats = read_file[-22:]
    #print("<", stats[len(stats)-2], ">") #code 0 found here, successful run
    if ": 0" in stats[len(stats)-2]:
        print("plan success")
        stats = stats[:21]
        # TODO should run organise from here? (so that only for successful plans as the failed plans to be organised below)
        stats = organise(stats)
        print(stats[20])
    elif ": 22" in stats[len(stats)-3]:
        print("plan fail - memory")
        replaceFail(stats, "search exit code: 22")
    elif ": 23" in stats[len(stats)-3]:
        print("plan fail - time")
        replaceFail(stats, "search exit code: 23")

    #stats=stats[:-1]
    return stats


def organise(stats):
    #remove first 24 characters f each item
    #TODO organise the failed planners to be nan for all fields except "solution found?" and "exit code"
    for num, info in enumerate(stats):
        #print("this: ", i) #i of type str
        #print(num, ": ", info)
        update = ""
        if num < 17:
            search = info.find("] ")
            start_search = search+2
            update = info[start_search:-1] #removes "\n"
        else:
            update = info[:-1]

        stats[num] = update
    #print(stats)
    return stats



#stats = readFile("add-inst1.txt")
"""
file = open("plans/add-inst1.txt", "r")
read_file = file.readlines()
stats = read_file[-22:]
stats = stats[:21]
print(stats) #remove last line
"""

"""
stats1 = organise(stats)
data = [stats1]
#stats1 = np.array(stats1)
#data = stats
stats = readFile("add-inst3.txt")
stats2 = organise(stats)
#stats2 = np.array(stats2)

print("----------- concatenate")
#data = np.concatenate(stats1, stats2)
data.append(stats2)
#data = stats1+stats2
print(data)
print(data[1])
"""

data = []
"""
file_names = ["add-inst1.txt", "add-inst2.txt",
                "add-inst3.txt", "add-inst4.txt",
                "add-inst5.txt", "add-inst6.txt",
                "add-inst7.txt", "add-inst8.txt",
                "add-inst9.txt", "add-inst10.txt",
                "add-inst11.txt", "add-inst12.txt",
                "add-inst13.txt", "add-inst14.txt", # planner for instance 13 failed
                "add-inst15.txt", "add-inst16.txt",
                "add-inst17.txt", "add-inst18.txt",
                "add-inst19.txt", "add-inst20.txt"] # planner for instance 19 & 20 failed

"""
file_names = ["mas-inst1.txt", "mas-inst2.txt",
                "mas-inst3.txt", "mas-inst4.txt",
                "mas-inst5.txt", "mas-inst6.txt",
                "mas-inst7.txt", "mas-inst8.txt",
                "mas-inst9.txt", "mas-inst10.txt",
                "mas-inst11.txt", "mas-inst12.txt",
                "mas-inst13.txt", "mas-inst14.txt", # planner for instance 13 failed
                "mas-inst15.txt", "mas-inst16.txt",
                "mas-inst17.txt", "mas-inst18.txt",
                "mas-inst19.txt", "mas-inst20.txt"] # planner for instance 19 & 20 failed


for i in file_names:
    stats = readFile(i)
    #print(stats)
    #stats = organise(stats)
    data.append(stats)
#print("---loop")
#print(data)

"""
#remove first 24 characters f each item
for num, info in enumerate(stats):
    #print("this: ", i) #i of type str
    #print(num, ": ", info)
    update = ""
    if num < 17:
        update = info[24:-2]
        #print("now this: ", j)
    else:
        update = info[:-1]

    stats[num] = update

#print(stats)
"""

#print("dataframe ---")
df = pd.DataFrame(data)
#print(df)

#transpose, colums become rows & rows become colums
#df_t = df.transpose()
#print(df_t)

#rename colums
df_rn = df.rename(columns={0:"Plan length", 1: "Plan cost", 2:"Expanded state(s)", 3:"Reopened state(s)", 4:"Evaluates state)s)", 5:"Evaluations", 6:"Generates state(s)", 7:"Deadends", 8:"Expanded until last jump", 9:"Reopened until last jump", 10:"Evaluated until last jump", 11:"Generated until last jump", 12:"Number or registeres states", 13:"Int hash set load factor", 14:"Int hash set resizes", 15:"Search time", 16:"Total time", 17: "Solution found?", 18:"Peak memory", 19:"Remove intermediate file output.sas", 20:"Search exit code"}) #, index={0:"instance 1"})
#print("---------")

#print(df_rn)

# Write df to excel
#writer = ew()
df_rn.to_excel("plans/output-mas.xlsx")

""
print("------- first")
print(df_rn.iloc[0,:])
print("------- last")
print(df_rn.iloc[19,:])
""
