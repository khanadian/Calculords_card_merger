# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:15:20 2019

@author: Iqbal Khan
"""
import numpy as np
import pandas as pd
from collections import Counter
from datetime import datetime

#Very imconsistent with pla = [205] and math = [1,2,3,4,5,6], even though theres more than 1 way to make the number
#TODO does not work if pla has 0 in it

# hyperparameters
ops = ["+", "-", "*"]
npop = 50 # population size
pla = [1, 3] #cards that can be played
math_orig = np.copy([1, 3]) #cards that can be manipulated to make play cards
gens = 50
math = []
instructions = []#first_iteration
real_instructions = []#only record instructions used at the end
relevant_instructions = [] #records instructions that lead to solutions
all_info = []
first_play = False
#TODO does not work if first_play = False, pla = [5,4,40] and math = [5,4,2]. should play 5 and 4, but plays 40
#TODO list does not work properly on pla = math = [1,3]
def main():
    startTime = datetime.now()
    counter = 0
    alpha = [0]
    global all_info
    global instructions
    next_gen = [False] * npop
    while(counter < gens):
        a = run_gen(next_gen)
        if (alpha[0] < a[0]):
            alpha = a
            
        #populate first 10% through strongest
        next_gen = []
        sols = len(all_info)
        iterate = 0
        if (sols > int(round(npop/10))):
            iterate = int(round(npop/10))
        elif (sols > 0):
            iterate = sols
        
        for i in range(0, iterate):
            next_gen = next_gen + [all_info[i][3]]
        
        #populate next 60% through mixing
        instructions = []
        for i in range(0, int(round(6*npop/10))):
            nums = np.copy(math_orig)
            not_done = True
            new_instructions = []
            ind = 0
            while not_done and ind < len(all_info):
                inst = all_info[ind]
                skip = False
                for formula in inst[3]:
                    if np.random.randint(2) > 0 and not_done and not skip:
                        #ensure that formula is valid
                        sp = formula.split()
                        if np.isin(int(sp[0]), nums) and np.isin(int(sp[2]), nums):
                            if int(sp[0]) != int(sp[2]) or (int(sp[0]) == int(sp[2]) and len(np.where(nums == int(sp[0]))[0]) > 1):
                                new_instructions = np.append(new_instructions, formula)
                                nums = np.delete(nums, np.where(nums == int(sp[0]))[0][0])
                                nums = np.delete(nums, np.where(nums == int(sp[2]))[0][0])
                                nums = np.append(nums, eval(formula))
                                ind = 0
                                skip = True
                        if len(new_instructions) == 6:
                            not_done = False
                if not skip:
                    ind = ind + 1
            next_gen = next_gen + [list(new_instructions)]
                    
        #populate last 30% randomly
        
        while(len(next_gen) < npop):
            new_instructions = make_decision(5, math_orig)
            inst2 = []
            for instruction in new_instructions:
                inst2 = inst2 + [instruction]
            next_gen = next_gen + [inst2]
            
        all_info = []
        counter = counter + 1
    
    print(alpha)
    print(datetime.now() - startTime)
    
def run_gen(next_gen):
    global all_info
    global relevant_instructions
    child = 0 
    while child < npop:
        play_cards(child, next_gen[child])
        relevant_instructions = []
        child = child + 1
    
    all_info.sort(key=lambda tup:tup[0], reverse = True)
    if(len(all_info)>0):
        alpha = np.copy(all_info[0])
    else:
        alpha = [-1]
    #dictionary of formulas
    formulae = []
    for child in all_info:
        for instruction in child[3]:
            #make sure that 5 * 7 = 7 * 5
            sp = instruction.split()
            formulae.append(sp[2] + " " + sp[1] + " " + sp[0])
            formulae.append(instruction)
    dic = Counter(formulae)
    
    #now divide the score by diversity
    for child in all_info:
        sum = 1
        for instruction in child[3]:
            sum = sum + dic[instruction]-1
        child[0] = child[0]/sum
    all_info.sort(key=lambda tup:tup[0], reverse = True) # sort by score
    return(alpha)
    
    
    
def play_cards(child, parent_ins):
    global math
    global math_orig
    play = np.copy(pla) #cards that can be played
    math = np.copy(math_orig) #cards that can be manipulated to make play cards
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
    if parent_ins:
        instructions = parent_ins
    else:
        instructions = make_decision(5, math_orig)#first_iteration = True
    if(check_usable(play, math)):
        #50/50 on whether to play a card or not
        #also check if it is last card
        if(play.size == 1 or np.random.randint(2)>0):
            match = np.isin(play, math)
            for i in range(0, match.size):
                if i < match.size and match[i]:#if we can play this card
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
            if counter >= len(instructions) or instructions[counter] == "":
                instructions = make_decision(1, math)
                counter = 0
            st = instructions[counter].split()
            num1 = int(st[0])
            num2 = int(st[2])
            if(np.isin(num1, math) and np.isin(num2, math)): #make the predetermined decision
                ins = instructions[counter]
            else: #make a different decision
                dec = make_decision(1, math)
                ins = dec[0]
                st = ins.split()
                num1 = int(st[0])
                num2 = int(st[2])
                
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
            if(play.size == 1 or np.random.randint(2)>0):
                match = np.isin(play, math)
                for i in range(0, match.size):
                    if i < match.size and match[i]:#if we can play this card
                        num = play[i]
                        math = np.delete(math, np.where(math == num)[0][0])
                        play = np.delete(play, i)
                        match = np.delete(match, i)
                        i = i-1
                        points = points + num
                        cards_played = cards_played + 1
                        played_cards[pc_ind] = num
                        pc_ind = pc_ind + 1
                        
        if (play.size == 0):
            loop = False
    score = print_score(points, cards_played, math.size == 0)
    math = np.copy(math_orig)
    real_instructions.reverse()
    info = [score, played_cards, print_formula(played_cards), relevant_instructions]
    math_orig = np.copy(math)
    if (info[0] != 0):
        all_info.append(info)
    
    

def print_formula(pc):
    global real_instructions
    global math_orig
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
                #break down the components further
                n1 = print_formula([str(sp[0])])
                n2 = print_formula([str(sp[2])])
                relevant_instructions.append(instruction)
                if (len(n1) == 0 and len(n2) == 0):
                    note.append(instruction)
                    math_orig = np.delete(math_orig, np.where(math_orig == int(sp[0]))[0][0])
                    math_orig = np.delete(math_orig, np.where(math_orig == int(sp[2]))[0][0])
                elif len(n1) == 0:
                    note.append(sp[0]+" "+sp[1]+" "+"("+n2[0]+")")
                    math_orig = np.delete(math_orig, np.where(math_orig == int(sp[0]))[0][0])
                elif len(n2) == 0:
                    note.append("("+n1[0]+")"+" "+sp[1]+" "+sp[2])
                    math_orig = np.delete(math_orig, np.where(math_orig == int(sp[2]))[0][0])
                else:
                    note.append("("+n1[0]+")"+" "+sp[1]+" "+"("+n2[0]+")")
                      
                done = True
        
        done = False
        ind = ind + 1
    return(note)
    
def print_score(points, cards_played, isempty):
    v = 0
    if isempty and first_play:
        v = v+1000
        
    return(v+(200*cards_played)+points)


def check_usable(play, math):
    return pd.Series(math).isin(play).any()
    
#generates an array of decisions
def make_decision(num_decisions, math):
    #[string, num1, num2]
    r = ["","","","",""] #find a better way to do this (not [[""]*3]*5)
    for i in range(0,num_decisions):
        op_ind = np.random.randint(3)
        math_ind1 = np.random.randint(math.size)
        math_ind2 = np.random.randint(math.size-1)
        if math_ind1 == math_ind2:
            math_ind2 = math.size-1
            
        num1 = str(math[math_ind1])
        num2 = str(math[math_ind2])
        r[i] = num1 +" "+ ops[op_ind]+" "+num2
            
    return r

if __name__== "__main__":
  main()

"""
each child will have 5 random instructions
an instruction will be [index, operation, index]
there will be 10-100 children
error check for non-existing variables

"""