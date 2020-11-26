import numpy as np
import pandas as pd #wireframe
#from pd import ExcelWriter as ew

# get data
def get_data(file_names, path):
    for i in file_names:
        stats = readFile(path, i)
        data.append(stats)

# replaces the items data for where the plans are unsuccesful
def replaceFail(stats, code):
    for num, info in enumerate(stats):
        if num == 18:
            stats[num-1] = "Solution not found."
        elif num == 21:
            stats[num-1] = code
        else:
            stats[num-1] = None


# reads files from txt to array, call to organise successful plans and replace array info for unsuccesful plans
def readFile(path, name):
    file = open(path + name, "r")
    read_file = file.readlines()
    stats = read_file[-22:]
    if ": 0" in stats[len(stats)-2]:
        #print("plan success")
        stats = stats[:21]
        stats = organise(stats)  # call organise from here? (so that only for successful plans as the failed plans to be organised below)
        remove_fluff(stats) #TODO

    elif ": 22" in stats[len(stats)-3]:
        #print("plan fail - memory")
        replaceFail(stats, 22)
    elif ": 23" in stats[len(stats)-3]:
        #print("plan fail - time")
        replaceFail(stats, 23)

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


#
def switcher(col_val, data):
    switch={
        0: data[13:-9], # Plan length
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
            #print("--Updated: ", update, ", Type: ", type(update))
        elif int(col) in [15, 16]: #floats
            n_data = switcher(col, data)
            update = float(n_data)
            #print("--Updated: ", update, ", Type: ", type(update))
        elif int(col) in [17, 19]:
            update = str(data)
            #print("--Updated: ", update, ", Type: ", type(update))
        else:
            n_data = switcher(col, data)
            update = int(n_data) #string
            #print("--Updated: ", n_data, ", Type: ", type(update))

        stats[col] = update

    #print(stats)

    return stats


# list to dataframe, rename columns and print to excel
def to_df(data, name):
    df = pd.DataFrame(data)
    df= df.rename(columns={0:"Plan length", 1: "Plan cost", 2:"Expanded state(s)", 3:"Reopened state(s)", 4:"Evaluated state(s)", 5:"Evaluations", 6:"Generates state(s)", 7:"Deadends", 8:"Expanded until last jump", 9:"Reopened until last jump", 10:"Evaluated until last jump", 11:"Generated until last jump", 12:"Number of registered states", 13:"Int hash set load factor", 14:"Int hash set resizes", 15:"Search time", 16:"Total time", 17: "Solution found?", 18:"Peak memory", 19:"Remove intermediate file output.sas", 20:"Search exit code"}) #, index={0:"instance 1"})
    path = "output-" + name + ".xlsx"
    df.to_excel(path) # Write df to excel
    return df


### MAIN ###
add_file_names = ["add-inst1.txt", "add-inst2.txt",
                "add-inst3.txt", "add-inst4.txt",
                "add-inst5.txt", "add-inst6.txt",
                "add-inst7.txt", "add-inst8.txt",
                "add-inst9.txt", "add-inst10.txt",
                "add-inst11.txt", "add-inst12.txt",
                "add-inst13.txt", "add-inst14.txt", # planner for instance 13 failed
                "add-inst15.txt", "add-inst16.txt",
                "add-inst17.txt", "add-inst18.txt",
                "add-inst19.txt", "add-inst20.txt"] # planner for instance 19 & 20 failed

mas_file_names = ["mas-inst1.txt", "mas-inst2.txt",
                "mas-inst3.txt", "mas-inst4.txt",
                "mas-inst5.txt", "mas-inst6.txt",
                "mas-inst7.txt", "mas-inst8.txt",
                "mas-inst9.txt", "mas-inst10.txt",
                "mas-inst11.txt", "mas-inst12.txt",
                "mas-inst13.txt", "mas-inst14.txt", # planner for instance 13 failed
                "mas-inst15.txt", "mas-inst16.txt",
                "mas-inst17.txt", "mas-inst18.txt",
                "mas-inst19.txt", "mas-inst20.txt"] # planner for instance 19 & 20 failed

data = []
path = "plans-satisficing/"
print("SATISFICING")
get_data(add_file_names, path)
df_sat_add = to_df(data, "satis-add")
print("Complete 1")

df = df_sat_add
print(df)

# TODO graphs

"""
data = []
get_data(mas_file_names, path)
df_sat_mas = to_df(data, "satis-mas")
print("Complete 2")

data = []
path = "plans-optimal/"
print("OPTIMAL")
get_data(add_file_names, path)
df_sat_add = to_df(data, "opt-add")
print("Complete 3")


data = []
get_data(add_file_names, path)
df_sat_add = to_df(data, "opt-mas")
print("Complete 4")
"""







"""
for index, row in df.items(): #iterrows
    #df.at[i, 0] = content[12:]
    print("--, ", index)
"""

"""
print("------- first")
print(df.iloc[0,:])
print("------- last")
print(df.iloc[19,:])
"""
