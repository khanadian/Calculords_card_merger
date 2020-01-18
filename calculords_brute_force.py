# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:15:20 2019
@author: Iqbal Khan
"""
import numpy as np
import pandas as pd
from datetime import datetime

#pla = [25, 35, 62, 42, 100, 56] #cards that can be played
#math_orig = [1,2,3,5,7,9] #cards that can be manipulated to make play cards


# hyperparameters
ops = ["+", "-", "*"]
pla = [50,18,32,25] #cards that can be played
math_orig = [5,6,3,8,2,1] #cards that can be manipulated to make play cards
m = np.copy(math_orig)
real_instructions = []#only record instructions used at the end
t1 = 0 #variable used for real time measurement

best_ri = [] #real instructions for best solution
best_score = 0 #score of best solution
best_pc = [] #cards played of best solution

sum_set = {} #set of solutions found. stored as {(solution tuple): (uses_all_numbers)}

def main():
    startTime = datetime.now()
    global t1
    t1 = datetime.now()
    recurse([], m, None, None, None)
    
    print(datetime.now() - startTime)
    
    print(best_score)
    print(best_pc)
    print(best_ri)
    
#goes through all possible equation permutations
def recurse(st, math, x, i1, i2):
    global t1
    global sum_set
    global best_score
    global best_pc
    global best_ri
    global real_instructions
    global m
    
    ma = np.copy(math)
    if x:
        e = [eval(x)]
        ma = np.append(math, e)
        ma = np.delete(ma, i1)
        if (i1 < i2):
            ma = np.delete(ma, i2-1)
        else:
            ma = np.delete(ma, i2)
    
    for index in range(0, len(ma)):
        
        for op in ops:
            for ind in range(0, len(ma)):
                if index != ind and (op == "-" or (op != "-" and index < ind)):
                    s = st + [[str(ma[index])+" "+str(op)+" "+str(ma[ind]), str(ma[index]), str(ma[ind])]]
                    if len(st) == 0:
                            print(s)
                            print(datetime.now() - t1)
                            t1 = datetime.now()
                            
                    #print(s)
                    if(len(s) == len(math_orig)-1):
                        real_instructions = []
                        for ins in s:
                            real_instructions = real_instructions + [ins[0]]
                        real_instructions.reverse()
                        ns = reverse_check(s)
                        if ns not in sum_set or (ns in sum_set and sum_set[ns] == False):
                            tup = reverse_calculate(s)
                            sum_set[ns] = tup[1]
                            pc = tup[0]
                            sc = print_score(sum(pc), len(pc), sum_set[ns])
                            if sc > best_score:
                                best_score = sc
                                best_pc = pc
                                m = np.copy(math_orig)
                                best_ri = print_formula(pc)
                    else:
                        x = str(ma[index])+str(op)+str(ma[ind])
                        recurse(s, ma, x, index, ind)
                        
#checks to make sure a playable number is not used in later equations
def not_in_others(num, instructions):
    for ind in range(0, len(instructions)):
        if str(num) == instructions[ind][1] or str(num) == instructions[ind][2]:
            #check if this instruction evaluates to another playable number
            t_num = eval(instructions[ind][0])
            if (t_num in pla):
                return False
            else:
                t_inst = instructions.copy()
                del t_inst[ind]
                return not_in_others(t_num, t_inst)
    return True

#returns a lists of strings that show how all of the played cards were formed
def print_formula(pc):
    global real_instructions
    global m
    note = []
    ind = 0
    done = False
    while(ind < len(pc) and pc[ind] != 0):
        for instruction in real_instructions:
            if (instruction!= "" and not done and eval(instruction) == int(pc[ind])):
                real_instructions = np.asarray(real_instructions)
                real_instructions = np.delete(real_instructions, np.where(real_instructions == instruction)[0][0])
                sp = instruction.split()
                #break down the ocmponents further
                n1 = print_formula([str(sp[0])])
                n2 = print_formula([str(sp[2])])
                if (len(n1) == 0 and len(n2) == 0):
                    note.append(instruction)
                    m = np.delete(m, np.where(m == int(sp[0]))[0][0])
                    m = np.delete(m, np.where(m == int(sp[2]))[0][0])
                elif len(n1) == 0:
                    note.append(sp[0]+" "+sp[1]+" "+"("+n2[0]+")")
                    m = np.delete(m, np.where(m == int(sp[0]))[0][0])
                elif len(n2) == 0:
                    note.append("("+n1[0]+")"+" "+sp[1]+" "+sp[2])
                    m = np.delete(m, np.where(m == int(sp[2]))[0][0])
                else:
                    note.append("("+n1[0]+")"+" "+sp[1]+" "+"("+n2[0]+")")
                      
                done = True
        
        done = False
        ind = ind + 1
    return(note)


#given a set of statements/operations, finds the score and also returns if all cards were used
def reverse_calculate(instructions, index = -1):
    if eval(instructions[index][0]) in pla:
        return ([eval(instructions[index][0])], True)
    else:
        ins1 = list(instructions)
        ins2 = list(instructions)
        ins1.pop(index)
        ins2.pop(index)
        i1 = -2
        i2 = -2
        for i in range(len(instructions)):
            if i1 == -2 and eval(instructions[i][0]) == instructions[index][1]:
                i1 = i
            elif (i2 == -2 and eval(instructions[i][0]) == instructions[index][2]):
                i2 = i
                
        if (i1 == -2):
            num1 = [int(instructions[index][1])]
            if num1[0] not in pla:
                num1 = []
        else:
            num1 = reverse_calculate(ins1, num1)
            
        if (i2 == -2):
            num2 =[int(instructions[index][2])]
            if num2[0] not in pla:
                num2 = []
        else:
            num2 = reverse_calculate(ins2, num2)
            
        bool1 = (i1 == -2 and (int(instructions[index][1]) in pla))# or (i1 != -2 and uses_all(ins1, i1))
        bool2 = (i2 == -2 and (int(instructions[index][2]) in pla))# or (i2 != -2 and uses_all(ins2, i2))
        return (num1 + num2, bool1 and bool2)

# this method ensures that we don't unnecessarily run play_cards(). cuts down runtime from 2 hours to 5 minutes
def reverse_check(instructions):
    dic = {}
    for i in range(len(instructions)):
        e = eval(instructions[-i][0])
        if e in pla and not_in_others(e, instructions):
            dic[e] = 1
    if len(dic) != 0:
        return tuple(list(dic.keys())) #TODO is there a better way to do this?

#calculates the score
def print_score(points, cards_played, isempty):
    v = 0
    if isempty:
        v = v+1000
        
    return(v+(200*cards_played)+points)

#checks if any math cards are playable
def check_usable(play, math):
    return pd.Series(math).isin(play).any()

if __name__== "__main__":
  main()
