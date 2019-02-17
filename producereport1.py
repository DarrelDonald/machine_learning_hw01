#!/usr/bin/python
import os
import random

for x in range(10):
    L = random.randint(1,200)
    K = random.randint(1,50)
    call = "python3 DecisionTree1.py "
    call = call + str(L)
    call = call + " "
    call = call + str(K)
    call = call + " data_sets1/training_set.csv data_sets1/validation_set.csv data_sets1/test_set.csv no"
    os.system(call)
    print("finished call ", x)

for x in range(10):
    L = random.randint(1,200)
    K = random.randint(1,50)
    call = "python3 DecisionTree1.py "
    call = call + str(L)
    call = call + " "
    call = call + str(K)
    call = call + " data_sets2/training_set.csv data_sets2/validation_set.csv data_sets2/test_set.csv no"
    os.system(call)
    print("finished call ", x + 10)
