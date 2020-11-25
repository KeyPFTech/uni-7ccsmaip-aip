import numpy as np
import pandas as pd #wireframe
#from pd import ExcelWriter as ew

# replaces the items data for where the plans are unsuccesful
def replaceFail(stats, code):
    for num, info in enumerate(stats):
        if num == 18:
            stats[num-1] = "Solution not found."
        elif num == 21:
            stats[num-1] = code
        else:
            stats[num-1] = None
    #stats=stats[:-1]

# reads files from txt to array, call to organise successful plans and replace array info for unsuccesful plans
def readFile(name):
    file = open("plans/"+name, "r")
    read_file = file.readlines()
    stats = read_file[-22:]
    #print("<", stats[len(stats)-2], ">") #code 0 found here, successful run
    if ": 0" in stats[len(stats)-2]:
        print("plan success")
        stats = stats[:21]
        stats = organise(stats)  # call organise from here? (so that only for successful plans as the failed plans to be organised below)
        #print("::", enumerate(stats))
        #temp = remove_front_back("search exit code: 7102", 18, len("search exit code: 1072"))
        #print("<", temp, ">")
        remove_fluff(stats) #TODO

    elif ": 22" in stats[len(stats)-3]:
        print("plan fail - memory")
        replaceFail(stats, 22)
    elif ": 23" in stats[len(stats)-3]:
        print("plan fail - time")
        replaceFail(stats, 23)

    #stats=stats[:-1]
    return stats

# removes redundant infor of timestep at the beginning and/or the whitespace at the end
def organise(stats):
    for num, info in enumerate(stats):
        #print("this: ", i) #i of type str
        #print(num, ": ", info)
        update = ""
        if num < 17:
            search = info.find("] ")
            start_search = search+2
            update = info[start_search:-1] # makes character selction
        else:
            update = info[:-1]

        stats[num] = update
    #print(stats)
    return stats


def remove_front_back(data, front, back):
    data = data[front:back]
    #print("::", data)
    return data


def switcher(col_val, data):
    switch={
        0: data[13:-9], #remove_front_back(data, 13, -9), # Plan length
        1: data[11: len(data)], #Plan cost
        2: data[9 : -10], # Expanded state(s)
        3: data[9 : -10], # Reopened state(s)
        4: data[10 : -10], # Evaluated state(s)
        5: data[13 : len(data)], # Evaluations
        6: data[10 : -10], # Generates state(s)
        7: data[11 : -10], # Deadends
        8: data[26 :-10], # Expanded until last jump
        9: data[26 : -10], # Reopened until last jump
        10: data[27 : -10], # Evaluated until last jump
        11: data[27 : -10], # Generated until last jump
        12: data[29 : len(data)], # Number of registered states
        13: data, # Int hash set load factor
        14: data[22 : len(data)], # Int hash set resizes
        15: data[13 : -1], # Search time
        16: data[12 : -1], # Total time
        17: data, # Solution found?, string: found vs not found
        18: data[13 : -3], # Peak memory
        19: data, # Remove intermediate file output.sas, string
        20: data[18 : len(data)] # Search exit code
    }
    return switch.get(col_val, None)


# TODO
def remove_fluff(stats):
    for col, data in enumerate(stats):
        update = ""
        if int(col) == 13:
            search = data.find("= ")
            start_search = search+2 #for "= "
            end = len(data)
            update = float(data[start_search:end])
            print("--Updated: ", update, ", Type: ", type(update))
        elif int(col) in [15, 16]: #floats
            n_data = switcher(col, data)
            update = float(n_data)
            print("--Updated: ", update, ", Type: ", type(update))
        elif int(col) in [17, 19]:
            update = str(data)
            print("--Updated: ", update, ", Type: ", type(update))
            #print("Helloooooo")
        else:
            n_data = switcher(col, data)
            #print("New data: ", n_data)
            update = int(n_data) #string
            print("--Updated: ", n_data, ", Type: ", type(update))

        stats[col] = update

    print(stats)

    """
    for row in enumerate(stats):
        for col, info_item in enumerate(stats):
            stats = switcher(col, info_item)
    """
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
"""

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


"""
for index, row in df.items(): #iterrows
    #df.at[i, 0] = content[12:]
    print("--, ", index)
"""
#rename colums
df_rn = df.rename(columns={0:"Plan length", 1: "Plan cost", 2:"Expanded state(s)", 3:"Reopened state(s)", 4:"Evaluated state(s)", 5:"Evaluations", 6:"Generates state(s)", 7:"Deadends", 8:"Expanded until last jump", 9:"Reopened until last jump", 10:"Evaluated until last jump", 11:"Generated until last jump", 12:"Number of registered states", 13:"Int hash set load factor", 14:"Int hash set resizes", 15:"Search time", 16:"Total time", 17: "Solution found?", 18:"Peak memory", 19:"Remove intermediate file output.sas", 20:"Search exit code"}) #, index={0:"instance 1"})
#print("---------")

#print(df_rn)

# Write df to excel
#writer = ew()
df_rn.to_excel("plans/output.xlsx")



""
print("------- first")
print(df_rn.iloc[0,:])
print("------- last")
print(df_rn.iloc[19,:])
""
