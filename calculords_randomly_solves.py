# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:15:20 2019

@author: Iqbal Khan
"""
import numpy as np
from datetime import datetime
#best i can come up with is (7*9)-1 and 5(2+3)
#the bot has found 7*5 and ((9*3)+1)*2

# hyperparameters
ops = ["+", "-", "*"]
pla = [25,35,42,62,56,100]
math_orig = [1,2,3,5,7,9,4,6,8]
m = list(math_orig)
instructions = []#first_iteration
real_instructions = []#only record instructions used at the end
relevant_instructions = [] #records instructions that lead to solutions

best_ri = []
best_score = 0
best_pc = []

def main():
    startTime = datetime.now()
    score = 0
    global best_score
    global best_ri
    global best_pc
    gen = 0
    global math_orig
    
    while gen <20000:
        math_orig = list(m)
        gen = gen + 1
        play = list(pla) #cards that can be played
        math = list(math_orig) #cards that can be manipulated to make play cards
        loop = True
        #first_iteration = True
        points = 0 #the value of the card
        cards_played = 0
        ri_index = 0
        global real_instructions
        real_instructions = []
        played_cards = [0 for x in range(6)]
        pc_ind = 0
        global instructions 
        
        instructions = make_decision(len(math_orig)-1, math_orig)#first_iteration = False
        if(check_usable(play, math)):
                #50/50 on whether to play a card or not
                #also check if it is last card
                if(len(play) == 1 or np.random.randint(2)>0):
                    match = np.isin(np.copy(play), np.copy(math))
                    for i in range(0, match.size):
                        if i < match.size and match[i]:#if we can play this card
                            num = play[i]
                            math.remove(num)
                            play.remove(i)
                            match = np.delete(match, i)
                            i = i-1
                            points = points + num
                            cards_played = cards_played + 1
                            played_cards[pc_ind] = num
                            pc_ind = pc_ind + 1
        counter = -1                 
        while(loop): #ends when 0 or 1 cards remain in math, or 0 cards in play
            counter = counter + 1
            if(len(math) < 2):
                loop = False
            else:
                if counter >= len(instructions) or instructions[counter] == "":
                    instructions = make_decision(1, math)
                    counter = 0
                st = instructions[counter].split()
                num1 = int(st[0])
                num2 = int(st[2])
                if(((num1 in math) and num2 in math and num1 != num2) or (num1 == num2 and math.count(num1)>1)): #make the predetermined decision
                    ins = instructions[counter]
                    #record decision
                    real_instructions.append(ins)
                    ri_index = ri_index + 1
                    #add product and subtract base numbers
                    math.append(eval(ins))
                    math.remove(num1)
                    math.remove(num2)
                    
            if(check_usable(play, math)):
                #50/50 on whether to play a card or not
                #also check if it is last card
                if(len(play) == 1 or np.random.randint(2)>0):
                    match = np.isin(np.copy(play), np.copy(math))
                    for i in range(0, match.size):
                        if i < match.size and match[i]:#if we can play this card
                            num = play[i]
                            math.remove(num)
                            play.remove(num)
                            match = np.delete(match, i)
                            i = i-1
                            points = points + num
                            cards_played = cards_played + 1
                            played_cards[pc_ind] = num
                            pc_ind = pc_ind + 1
        score = print_score(points, cards_played,len(math) == 0)
        if(score > best_score):
            best_score = score
            real_instructions.reverse()
            best_ri =print_formula(played_cards)
            best_pc = played_cards
    print(best_score)
    print(best_pc)
    print(best_ri)
    
    print(datetime.now() - startTime)
    
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
                real_instructions.remove(instruction)
                sp = instruction.split()
                #break down the components further
                n1 = print_formula([str(sp[0])])
                n2 = print_formula([str(sp[2])])
                relevant_instructions.append(instruction)
                if (len(n1) == 0 and len(n2) == 0):
                    note.append(instruction)
                    math_orig.remove(int(sp[0]))
                    math_orig.remove(int(sp[2]))
                elif len(n1) == 0:
                    note.append(sp[0]+" "+sp[1]+" "+"("+n2[0]+")")
                    math_orig.remove(int(sp[0]))
                elif len(n2) == 0:
                    note.append("("+n1[0]+")"+" "+sp[1]+" "+sp[2])
                    math_orig.remove(int(sp[2]))
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
    return [i for i in math if i in play]
    
#generates an array of decisions
def make_decision(num_decisions, math):
    #[string, num1, num2]
    r = [] #find a better way to do this (not [[""]*3]*5)
    for i in range(0,num_decisions):
        op_ind = np.random.randint(3)
        math_ind1 = np.random.randint(len(math))
        math_ind2 = np.random.randint(len(math)-1)
        if math_ind1 == math_ind2:
            math_ind2 = len(math)-1
            
        num1 = str(math[math_ind1])
        num2 = str(math[math_ind2])
        r.append(num1 +" "+ ops[op_ind]+" "+num2)
            
    return r

if __name__== "__main__":
  main()

"""
each child will have 5 random instructions
an instruction will be [index, operation, index]
there will be 10-100 children
error check for non-existing variables

"""