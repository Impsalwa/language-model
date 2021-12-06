# -*- coding: utf-8 -*-
"""
Created on Thu Nov 11 18:50:58 2021

@author: Salwa
"""
import numpy as np
import string 

np.random.seed(1234)

#initilize the dictionaries
initial = {} #start of phrase
first_order = {} #second word only 
second_order = {} 

#remove punctuations 
def remove_punct(s):
    return s.translate(str.maketrans('','',string.punctuation))

#add to dictionary 
def add2dict(d, key, value): #key wil represente some starting words or pairs of words like (I am happy) the key is I am and happy the value
    if key not in d:
        d[key] = []
    d[key].append(value)
    

# treverse the data set 
for line in open ('robert.txt'): #loop envery line in the file 
    tokens = remove_punct(line.rstrip().lower()).split() 
    #the first step will be rstrip and lowercase the line
    #the second we will remove punctuation 
    #then split to tokenize the sentence 
    #the result will be list of tokens 
    
    T = len(tokens)
    #print(T)
    for i in range(T):
        t = tokens[i]
        if i == 0:
            # measure the distribution of the first word
            initial[t] = initial.get(t, 0.) + 1
        #normlize the distrebution
        else:
            t_1 = tokens[i-1]
            #case of end of the sentence 
            if i == T-1:
                #measure the probability of endding line 
                add2dict(second_order, (t_1, t), 'END')
            if i == 1: 
            #measure distribution of second word
            #given only first word
                add2dict(first_order, t_1, t)
            else: #not the first or second word 
                t_2 = tokens[i-2]
                add2dict(second_order, (t_2, t_1), t)
#normlize the ditribution 
initial_totale = sum(initial.values())
#♦print(initial_totale)
for t, c in initial.items():
    initial[t] = c / initial_totale

#convert list [cat, dog, mouse, cat, mouse,dog, dog,..]
#to dictionary {cat: 0.2 , dog : 0.3, mouse: 0.2}
        
def list2pdict(ts):
    #the input ts is just list of token 
    #turn each list of probabilities into a dict of probabilities
    d = {}
    n = len(ts)
    #print(n)
    for t in ts:
        d[t] = d.get(t, 0.) +1 #increame the list by 1 each time we loop the token 
        #gives as a result a dict storing the counts 
    for t, c in d.items():
        d[t] = c/n #gives us the probability for each token 
    return d

for t_1, ts in first_order.items():
    #replace list with dictionary of probability
    first_order[t_1] =  list2pdict(ts)
    #print(first_order) #the result is dectionary of dictionaries
for k , ts in second_order.items():
    #replace list with dictionary of probas
    second_order[k] = list2pdict(ts)
    #print(second_order)

def sample_word(d):
    #asample from the uniforn distribution
    #it will be a number from 0 to 1 
    p0 = np.random.random()
    cumulative = 0 #the cumulative sum of the probas
    for t, p in d.items():
        #t is a sample word p is the probability corespend 
        cumulative += p
        if p0 < cumulative:
            return t
    assert(False) #should never get there

#the main function to generate a poem 
def generate():
    for i in range(4):
        #generate 4 lines
        #the empty list that contain the poem
        sentence = []
        #initial word
        w0 = sample_word(initial)
        sentence.append(w0)
        
        #sample second word
        w1 = sample_word(first_order[w0])
        sentence.append(w1)
        #second_order transition untill END 
        while True:
            w2 = sample_word(second_order[(w0, w1)])
            if w2 == 'END':
                break
            sentence.append(w2)
            w0 = w1 
            w1 = w2
        print(' '.join(sentence))
print(generate())
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        