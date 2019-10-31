# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 09:15:20 2019

@author: Iqbal Khan
"""
import numpy as np
import pandas as pd

#best i can come up with is (7*9)-1 and 5(2+3)

# hyperparameters
ops = ["+", "-", "*"]
npop = 50 # population size
sigma = 0.1 # noise standard deviation
alpha = 0.001 # learning rate

#TODO allow bot the choice to not use an operation? add a "do nothing" operation?
def main():
    play = np.array([25, 35, 62, 42, 100, 56]) #cards that can be played
    math = np.array([1,2,3,5,7,9]) #cards that can be manipulated to make play cards
    math_orig = np.array([1,2,3,5,7,9])
    loop = True
    #first_iteration = True
    points = 0 #the value of the card
    cards_played = 0
    ri_index = 0
    real_instructions = ["" for x in range(5)] #only record instructions that matter?
    played_cards = [0 for x in range(6)]
    pc_ind = 0
    
    instructions = make_decision(5, True, math)#first_iteration
    #first_iteration = False
    print(instructions)
    
    if(check_usable(play, math)):
            #50/50 on whether to play a card or not
            if(np.random.randint(2)>0):
                match = np.isin(play, math)
                for i in range(0, match.size):
                    if match[i]:
                        num = play[i]
                        play = np.delete(play, i)
                        math = np.delete(math, np.where(math == num)[0][0])
                        points = points + num
                        cards_played = cards_played + 1    
                        played_cards[pc_ind] = num
                        pc_ind = pc_ind + 1
    counter = -1                 
    while(loop): #ends when 0 or 1 cards remain in math, or 0 cards in play
        counter = counter + 1
        if(math.size < 2): #no more instructions, hopefully
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
                    if match[i]:#if we can play this card
                        num = play[i]
                        play = np.delete(play, i)
                        math = np.delete(math, np.where(math == num)[0][0])
                        points = points + num
                        cards_played = cards_played + 1
                        played_cards[pc_ind] = num
                        pc_ind = pc_ind + 1
                        
    print_score(points, cards_played, math.size == 0)
    print_instructions(real_instructions)
    print(played_cards)
    print(print_noteworthy(played_cards, real_instructions, math_orig))
    
#TODO this does not account for repeated use of 1 number
    #does not account for the number 1 being multiplied
    # ^both of the above can be combined into one solution by modifying math_orig
    #does not record the important moves at base, only gives full formula
def print_noteworthy(pc, ins, math):
    note = []
    ind = 0
    while(ind < len(pc) and pc[ind] != 0):
        if(int(pc[ind]) in math):
            1 #do nothing
        else:#number is a product of an operation
            for instruction in ins:
                if (instruction!= "" and eval(instruction) == int(pc[ind])):
                    sp = instruction.split()
                    n1 = print_noteworthy([str(sp[0])], ins, math)
                    n2 = print_noteworthy([str(sp[2])], ins, math)
                    if (len(n1) == 0 and len(n2) == 0):
                        note.append(instruction)
                    elif len(n1) == 0:
                        note.append(sp[0]+" "+sp[1]+" "+"("+n2[0]+")")
                    elif len(n2) == 0:
                        note.append("("+n1[0]+")"+" "+sp[1]+" "+sp[2])
                    else:
                        note.append("("+n1[0]+")"+" "+sp[1]+" "+"("+n2[0]+")")
        
        ind = ind + 1
    
    return(note)
    
def print_score(points, cards_played, isempty):
    v = 0
    if isempty:
        v = v+650
        
    print("Score:")
    print(v+(201*cards_played)+points)

def print_instructions(ri):
    print("Instructions:")
    print(ri)

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