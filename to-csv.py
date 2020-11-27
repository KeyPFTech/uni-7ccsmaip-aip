import numpy as np
import pandas as pd #wireframe
#from pd import ExcelWriter as ew
import matplotlib.pyplot as plt
import math # ceiling value for plot axix max
import seaborn as sns # colour plots

# get data
def get_data(file_names, path):
    for i in file_names:
        stats = readFile(path, i)
        data.append(stats)

# replaces the items data for where the plans are unsuccesful
def replaceFail(stats, code):
    #print(stats)
    memory_data = 0
    for num, info in enumerate(stats):
        if num == 15:
            memory_data = stats[15][13:-4]
            #print("Memory: ", memory_data)
            stats[num-1] = None
        elif num == 16 and code == 22:
            memory_data = stats[17][13:-4]
            stats[num-1] = None # float('inf')  #None #"TODO infinity"
        elif num == 16 and code == 23: #runs out of time
            stats[num-1] = 1800 #maximum time
        elif num == 17 and code == 22:
            stats[num-1] = None #float('inf')
        elif num == 17 and code == 23:
            stats[num-1] = 1800
        elif num == 18:
            stats[num-1] = "Solution not found."
        elif num == 19 and code == 22:
            #print("Mem before = ", type(int(memory_data)))
            stats[num-1] = int(memory_data) #memory_data
        elif num == 19 and code ==23:
            stats[num-1] = int(memory_data)
        elif num == 21:
            stats[num-1] = code
        else:
            stats[num-1] = None
    #print(stats)


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
        #print(stats)
    elif ": 23" in stats[len(stats)-3]:
        #print("plan fail - time")
        replaceFail(stats, 23)
        #print(stats)

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
    df= df.rename(columns={0:"Plan length", 1: "Plan cost", 2:"Expanded state(s)", 3:"Reopened state(s)", 4:"Evaluated state(s)", 5:"Evaluations", 6:"Generates state(s)", 7:"Deadends", 8:"Expanded until last jump", 9:"Reopened until last jump", 10:"Evaluated until last jump", 11:"Generated until last jump", 12:"Number of registered states", 13:"Int hash set load factor", 14:"Int hash set resizes", 15:"Search time", 16:"Total time", 17: "Solution found?", 18:"Peak memory", 19:"Remove intermediate file output.sas", 20:"Search exit code"})
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


path = "plans-satisficing/"
print("SATISFICING")

data = []
get_data(add_file_names, path)
df_sat_add = to_df(data, "satis-add")
print("Complete 1")


data = []
get_data(mas_file_names, path)
df_sat_mas = to_df(data, "satis-mas")
print("Complete 2")


path = "plans-optimal/"
print("OPTIMAL")

data = []
get_data(add_file_names, path)
df_opt_add = to_df(data, "opt-add")
print("Complete 3")


data = []
get_data(mas_file_names, path)
df_opt_mas = to_df(data, "opt-mas")
print("Complete 4")














"""
# Graphs plotting memory time
df = df_sat_add
df_reduce = df[['Search time', 'Peak memory', 'Search exit code']]
print(df_reduce)
#df_reduce.plot(x = 'Search time', y = 'Peak memory', kind = 'scatter')
#xmin, xmax, ymin, ymax = plt.axis()
#print("Limits: xmax", xmax, " ymax", ymax)


for index, row in df_reduce.iterrows():
    #print(row["Search exit code"]) #22 memory limit, 23 time limit
    #print("index: ", index)
    if row["Search exit code"] == 23:
        print("Time limit")
        # todo set search time to the very very edge of graph
        #row["Search time"] = xmax
        old = row["Search time"]
        #print("old: ", old)
        df_reduce.at[index,'Search time'] = xmax
        #df_reduce[row]["Search time"] = xmax
    elif row["Search exit code"] == 22: # finished memory

print(df_reduce)
df_reduce.plot(x = 'Search time', y = 'Peak memory', kind = 'scatter')
plt.show()
# TODO plotting for failed (where exit code ==22 or 23)? ran our of memory as time infinty
"""


"""
# Graphs plotting time time for 2 different df
df1 = df_sat_add[['Search time']]
df1 = df1.rename(columns={'Search time':"add"})

df2 = df_sat_mas[['Search time']]
df2 = df2.rename(columns={'Search time':"mas"})

result = pd.concat([df1, df2], axis=1, join = 'inner')
print("----- RESULT: ", result)
result.plot(x = 'add', y = 'mas', kind = 'scatter') # style = "x"
plt.show()
# TODO plotting for failed (where exit code ==22 or 23)? ran our of memory as time infinty
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


# df_sat_add
# df_sat_mas
# df_opt_add
# df_opt_mas

"""
# plot time x time, satisfied additive and m&s

df1 = df_opt_add[['Search time']] #'Search exit code'
df1 = df1.rename(columns={'Search time':"T add"})
#print(df1)
df2 = df_opt_mas[['Search time']] #'Search exit code'
df2 = df2.rename(columns={'Search time':"T mas"}) #TODO how to plot on axis/infinity
#print(df2)
df_opt_time = pd.concat([df1, df2], axis=1, join = 'inner')
#print("----- RESULT: ", df_opt_time)
df_opt_time = df_opt_time.reset_index(drop=True)
max_val = df_opt_time['T mas'].max()
max_val = int(math.ceil(max_val / 10.0)) * 10
df_opt_time['T mas'] = df_opt_time['T mas'].fillna(max_val)
#print(df_opt_time)
df_opt_time.plot(x = 'T add', y = 'T mas', kind = 'scatter') # style = "x"
#xmin, xmax, ymin, ymax = plt.axis()
#plt.axis((xmin, xmax, ymin, max_val))
plt.ylim(top = max_val)
#plt.yscale('log')
#plt.xscale('log')
plt.title("Time x Time")
plt.xlabel("Additive Heuristic Search Time (s)")
plt.ylabel("Merge & Shrink Heuristic Search Time (s)")
plt.grid()
print(df_opt_time)
plt.show()
#plt.savefig("optimising_timetime.png", bbox_inches='tight')



# plot time x length, all of optimal
df1 = df_opt_add[['Search time', 'Peak memory', 'Search exit code']]
df1['Heuristic'] = "Additive"
df2 = df_opt_mas[['Search time', 'Peak memory', 'Search exit code']]
df2['Heuristic'] = "Merge & Shrink"
df_op = df1.append(df2, sort = False)
#print(df_op)
#print(type(float('inf')))
df_op = df_op.reset_index(drop=True)
max_val = df_op["Search time"].max()
max_val = int(math.ceil(max_val / 10.0)) * 10
print("Max val: ", max_val)
df_op["Search time"] = df_op["Search time"].fillna(max_val)
df_op.plot(x = 'Search time', y = 'Peak memory', kind = 'scatter')
xmin, xmax, ymin, ymax = plt.axis()
print(xmin, xmax, ymin, ymax)
#plt.axis([0, 1800, 0, max_val])
#plt.ylim(top = max_val)
#plt.ylim(top = max_val)
# TODO plt.ylim(top = max_val)
#df_op.to_excel("temp-time_length.xlsx") # Write df to excel
sns.scatterplot(data=df_op, x='Search time', y='Peak memory', hue='Heuristic')
plt.title("Time x Memory")
plt.xlabel("Search Time (s)")
plt.ylabel("Peak Memory (KB)")
plt.grid()
print(df_op)
plt.show()
#plt.savefig("optimising_timememory.png", bbox_inches='tight')
"""





"""
# plot time x time, all of optimal
df1 = df_opt_add[['Search time', 'Search exit code']]
df1 = df1.rename(columns={'Search time':"ADD Search time"})
print(df1)
df2 = df_opt_mas[['Search time', 'Search exit code']]
max_val = df2["Search time"].max()
df2["Search time"] = df2["Search time"].fillna(max_val + 10)
df2 = df2.rename(columns={'Search time':"MAS Search time"})
print(df2)
#df_op = df1.append(df2, sort = False)
result = pd.concat([df1, df2], axis=1, sort = True)

#result.to_excel("temp-time.xlsx") # Write df to excel
print(result)
"""
"""
#print(type(float('inf')))
max_val = df_op["ADD Search time"].max()
if df_op["ADD Search time"].max() < df_op["MAS Search time"].max():
    max_val = df_op["MAS Search time"].max()

df_op["ADD Search time"] = df_op["ADD Search time"].fillna(max_val + 10)
df_op["MAS Search time"] = df_op["MAS Search time"].fillna(max_val + 10)

#print(df_op)

print(df_op)

print("Complete")
"""

"""
for index, row in df_op.iterrows():
    #print(row["Search exit code"]) #22 memory limit, 23 time limit
    #print("index: ", index, "row: ", row)
    print(type(row["Search time"]))
    if row["Search time"].isna():

        print("--TODO infinity here")
"""

"""
print(df_op)
fig, ax = plt.subplots()
colours = np.where(df_op["Heuristic"]=="add",'r','k')
df_op.plot.scatter(x="Search time",y="Peak memory",c=colours, style = "x")
#ax.legend()
plt.show()
#df_op.plot(x = 'Search time', y = 'Peak memory', kind = 'scatter')
#df_op.plot.scatter(x = "Search time", y = "Peak memory")
#plt.show()
# todo different colours for add vs for mas
# todo plot infinity
"""
"""
df1 = df_opt_add[['Search time', 'Peak memory']]
df2 = df_opt_mas[['Search time', 'Peak memory']]
df1.plot(x = "Search time", y = "Peak memory", kind = 'scatter', style = "x")
df2.plot(x = "Search time", y = "Peak memory", kind = 'scatter', style = "o")
plt.show()
"""
