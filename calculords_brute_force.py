# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:15:20 2019

@author: Iqbal Khan
"""
import numpy as np
import pandas as pd
from datetime import datetime
#best i can come up with is (7*9)-1 and 5(2+3)

#proper name for this file is brute force


# hyperparameters
ops = ["+", "-", "*"]
npop = 50 # population size
sigma = 0.1 # noise standard deviation
alpha = 0.001 # learning rate
math_orig = np.array([1,2,3,5,7,9])
m = np.copy(math_orig)
instructions = []#first_iteration
real_instructions = []#only record instructions used at the end
relevant_instructions = [] #records instructions that lead to solutions
t1 = 0

best_ri = []
best_score = 0
best_pc = []

def main():
    startTime = datetime.now()
    global t1
    t1 = datetime.now()
    recurse([], m, None, None, None)
    
    print(datetime.now() - startTime)
    
    print(best_score)
    print(best_pc)
    print(best_ri)
    
def recurse(st, math, x, i1, i2):
    global t1
    m = np.copy(math)
    if x:
        e = [eval(x)]
        m = np.append(math, e)
        m = np.delete(m, i1)
        if (i1 < i2):
            m = np.delete(m, i2-1)
        else:
            m = np.delete(m, i2)
    
    for index in range(0, len(m)):
        
        for op in ops:
            for ind in range(0, len(m)):
                if index != ind and (op == "-" or (op != "-" and index < ind)):
                    s = st + [[str(m[index])+" "+str(op)+" "+str(m[ind]), str(m[index]), str(m[ind])]]
                    if len(st) == 0:
                            print(s)
                            print(datetime.now() - t1)
                            t1 = datetime.now()
                    #print(s)
                    if(len(s) == 5):
                        play_cards(s)
                    else:
                        x = str(m[index])+str(op)+str(m[ind])
                        recurse(s, m, x, index, ind)
       
def play_cards(s):
    global best_ri
    global best_pc
    global best_score
    global m
    play = np.array([25, 35, 62, 42, 100, 56]) #cards that can be played
    math = np.array([1,2,3,5,7,9]) #cards that can be manipulated to make play cards
    loop = True
    #first_iteration = True
    points = 0 #the value of the card
    cards_played = 0
    ri_index = 0
    global real_instructions
    real_instructions = ["" for x in range(5)]
    played_cards = [0 for x in range(6)]
    pc_ind = 0
    global instructions 
    instructions = s
    if(check_usable(play, math)):
        #50/50 on whether to play a card or not
        #also check if it is last card
        match = np.isin(play, math)
        for i in range(0, match.size):
            if i < match.size and match[i] and not_in_others(play[i], instructions, 0):#if we can play this card
                num = play[i]
                math = np.delete(math, np.where(math == num)[0][0])
                play = np.delete(play, i)
                match = np.delete(match, i)
                i = i-1
                points = points + num
                cards_played = cards_played + 1
                played_cards[pc_ind] = num
                pc_ind = pc_ind + 1
    counter = -1                 
    while(loop): #ends when 0 or 1 cards remain in math, or 0 cards in play
        counter = counter + 1
        if(math.size < 2):
            loop = False
        else:
            num1 = int(instructions[counter][1])
            num2 = int(instructions[counter][2])
            if(np.isin(num1, math) and np.isin(num2, math)): #make the predetermined decision
                ins = instructions[counter][0]
                #print(ins)
                
            #record decision
            real_instructions[ri_index] = ins
            ri_index = ri_index + 1
            
            #add product and subtract base numbers
            math = np.append(math, eval(ins))
            math = np.delete(math, np.where(math == num1)[0][0])
            math = np.delete(math, np.where(math == num2)[0][0])
            
            
        
        if(check_usable(play, math)):
            #50/50 on whether to play a card or not
            #also check if it is last card
            match = np.isin(play, math)
            for i in range(0, match.size):
                if i < match.size and match[i] and not_in_others(play[i], instructions, counter):#if we can play this card
                    num = play[i]
                    math = np.delete(math, np.where(math == num)[0][0])
                    play = np.delete(play, i)
                    match = np.delete(match, i)
                    i = i-1
                    points = points + num
                    cards_played = cards_played + 1
                    played_cards[pc_ind] = num
                    pc_ind = pc_ind + 1
    score = print_score(points, cards_played, math.size == 0)
    if(score > best_score):
        best_score = score
        real_instructions.reverse()
        m = np.copy(math_orig)
        best_ri = print_formula(played_cards)
        best_pc = played_cards

def not_in_others(num, instructions, index): #TODO DOES NOT ACCOUNT FOR DUPLICATE NUMBERS
    for ind in range(index+1, len(instructions)):
        if str(num) == instructions[ind][1] or str(num) == instructions[ind][2]:
            return False
    return True

def print_formula(pc):
    global real_instructions
    global m
    global relevant_instructions
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
                relevant_instructions.append(instruction)
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
    
def print_score(points, cards_played, isempty):
    v = 0
    if isempty:
        v = v+1000
        
    return(v+(200*cards_played)+points)


def check_usable(play, math):
    return pd.Series(math).isin(play).any()

if __name__== "__main__":
  main()

"""
each child will have 5 random instructions
an instruction will be [index, operation, index]
there will be 10-100 children
error check for non-existing variables

"""
