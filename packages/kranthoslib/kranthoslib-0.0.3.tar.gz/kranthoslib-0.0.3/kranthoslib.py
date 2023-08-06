########################################################################################################################################################################
#DEPENDENT FUNCTIONS
import sqlite3
import datetime
import discord
from discord.ext import commands
import psycopg2

#SIprefix_int
def SIprefix_int(x:int):
    if isinstance(x, int):
        init_x=str(x)
        numb_let=("K", "M", "B", "T", "Q", "P")
        fact=0
        bool_t=False
        sliced=0
        replaced=""
        while bool_t==False:
            if len(str(x))>3:
                if len(set(numb_let).intersection(set(str(x))))>0:
                    if len(str(x))!=4:
                        x=str(x)[:-1]
                    else:
                        break
                x=str(x)[:-3]
                x+=numb_let[fact]
                fact+=1

            else:
                break
        lenn=len(str(x))-1
        replaced=len(str(init_x))-lenn
        results=str(x)[:int(lenn)] + "," + init_x[len(str(x))-1:len(str(x))] + str(x)[len(str(x))-1]
        return results
    else:
        print(f"{x} has to be an integer.")
#1. Tkinter draw LabelFrame
#change...
#
##POSTGRES
#1 INSERT

#2 SELECT

#3 DELETE

#2. Optimzed Sqlite3
def insert_sqlite3(database_name: str, table_name: str, list_values: list):
    db=sqlite3.connect(database_name)
    c=db.cursor()
    values_in_db="("
    for i in range(len(list_values)-1):
        values_in_db+="?,"
    values_in_db+=("?)")
    values_converted_tuple=tuple(list_values)
    test=f"INSERT INTO {table_name} VALUES{values_in_db}"
    c.execute(str(test), values_converted_tuple)
    db.commit()
    db.close()
def select_sqlite3(database_name: str, table_name: str, selected_value, condition_in_db, condition_outside_db):
    db=sqlite3.connect(database_name)
    c=db.cursor()

    test=f"SELECT {selected_value} FROM {table_name} WHERE {str(condition_in_db)}=?"
    print(test)
    selected=c.execute(str(test), condition_outside_db).fetchone()
    db.commit()
    db.close()
    return selected
#timed_planner


    ##add time...

"""def delete_sqlite3(database_name: str, table_name:str, list_values):

def select_sqlite3(database_name: str, table_name:str, ):"""

######DISCORD ROLES EMBED REACTION
#emoji role
#make a list of lists [["title","a","b","c","d"]]
def reaction_role(title:str,unlock:list, emoji_desc_role:list):
    embed=discord.Embed(title=f"{title}", color=0x000000)
    unlock_str=""
    for i in range(len(unlock)-1):
        unlock_str+=str(unlock[i])
        unlock_str+="\n"
    embed.add_field(name="Unlock:", value=f"{unlock[0]}",inline=False)
    roles_str=""
    for j in range(len(emoji_desc_role)):
        roles_str+=str(emoji_desc_role[j][0])
        roles_str+="-"
        roles_str+=str(emoji_desc_role[j][1])

        ##store roles in database
        ##commands roles


########################################################################################################################################################################
#INDEPENDENT FUNCTIONS

#counts by using mirrored counting method
def mirrored_counter(current_goal: int):
    mirrored_goal=1
    if type(current_goal) is not int:
        raise TypeError
    else:
        while mirrored_goal <= current_goal:
            mirrored_goal*=2
    return mirrored_goal

def result_mc(current_level: int):
    list_mc = []
    current_mc = 1
    for i in range(current_level):
        list_mc.append(current_mc)
        current_mc *= 2
    return list_mc

def level_mc(current_goal: int):
    index_mc = 0
    result_lmc = 1
    while index_mc < current_goal:
        index_mc += 1
        result_lmc *= 2

#prints all the details of the variable (value and type)
def total_print(x):
    if x is None:
        print(f"{x} is None")
    elif (x is not None) and (type(x) is not list) and (type(x) is not tuple):
        print(f"""Type of {x}: {type(x)}
Value of {x}: {x}""")
    elif ((x is not None) and (isinstance(x,(list, tuple)))): 
        print(f"""Type of {x}: {type(x)}
Value of {x}: {x}
Length of {x}: {len(x)}""")

#auto-converter for tuple & list
def tuple_list(x: tuple or list, convert_type: int):
    if x is None or ((type(x) is not list) and (type(x) is not tuple)):
        raise TypeError
    if convert_type == 0:
        if isinstance(x, tuple):
            return x
        elif isinstance(x, list):
            return tuple(x)

    elif convert_type ==1:
        if isinstance(x, tuple):
            return list(x)
        elif isinstance(x, list):
            return x

    elif convert_type != 0 and convert_type !=1:
        raise ValueError

#last or first value from a list or group of lists
def first_last_variable(x: tuple or list, retrieve: int):
    #include test[0][0][0] etc. loop
    if retrieve==0:
        while (type(x[retrieve]) == list) or (type(x[retrieve]) == tuple):
            x[retrieve]=x[retrieve][retrieve]

#planner
def add_planner(plan: list, frag: str):
    plan.append(frag)
    return plan

def delete_planner(plan: list,position:int):
    plan.remove(plan[position])
    return plan

def priority_planner(plan: list, position: int):
    plan[0], plan[position]= plan[position], plan[0]

##C++ MIDI music