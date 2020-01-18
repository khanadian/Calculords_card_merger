# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:15:20 2019

@author: Iqbal Khan
"""
import numpy as np
import pandas as pd

#best i can come up with is (7*9)-1 and 5(2+3)
#the bot has found 7*5 and ((9*3)+1)*2

# hyperparameters
ops = ["+", "-", "*"]
npop = 50 # population size
math_orig = np.array([1,2,3,5,7,9])
m = math_orig
instructions = []#first_iteration
real_instructions = []#only record instructions used at the end
relevant_instructions = [] #records instructions that lead to solutions

best_ri = []
best_score = 0
best_pc = []

def main():
    score = 0
    global best_score
    global best_ri
    global best_pc
    gen = 0
    global m
    global math_orig
    
    while gen <2500:
        math_orig = m
        gen = gen + 1
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
        
        instructions = make_decision(5, True, math_orig)#first_iteration = False
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
                num1 = int(instructions[counter][1])
                num2 = int(instructions[counter][2])
                if(np.isin(num1, math) and np.isin(num2, math)): #make the predetermined decision
                    ins = instructions[counter][0]
                    #print(ins)
                else: #make a different decision
                    dec = make_decision(1, True, math)
                    ins = dec[0][0]
                    num1 = int(dec[0][1])
                    num2 = int(dec[0][2])
                    
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
        score = print_score(points, cards_played, math.size == 0)
        if(score > best_score):
            best_score = score
            real_instructions.reverse()
            best_ri =print_formula(played_cards)
            best_pc = played_cards
    print(best_score)
    print(best_pc)
    print(best_ri)
    
    
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
                #break down the ocmponents further
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
    if isempty:
        v = v+1000
        
    return(v+(200*cards_played)+points)


def check_usable(play, math):
    return pd.Series(math).isin(play).any()
    
#generates an array of decisions
def make_decision(num_decisions, random, math):
    #[string, num1, num2]
    r = [["","",""],["","",""],["","",""],["","",""],["","",""]] #find a better way to do this (not [[""]*3]*5)
    if random:
        #randomize
        for i in range(0,num_decisions):
            op_ind = np.random.randint(3)
            math_ind1 = np.random.randint(math.size)
            math_ind2 = np.random.randint(math.size-1)
            if math_ind1 == math_ind2:
                math_ind2 = math.size-1
                
            num1 = str(math[math_ind1])
            num2 = str(math[math_ind2])
            r[i][0] = num1 +" "+ ops[op_ind]+" "+num2
            r[i][1] = num1
            r[i][2] = num2
    else:
        print("error")
            
    return r

if __name__== "__main__":
  main()

"""
each child will have 5 random instructions
an instruction will be [index, operation, index]
there will be 10-100 children
error check for non-existing variables

"""