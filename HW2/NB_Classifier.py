# -*- coding: utf-8 -*-
"""
Created on Sun Mar 24 11:36:18 2019

@author: lou
"""

import os

from math import log
from collections import defaultdict

path_train_ham = 'train/ham'
path_train_spam = 'train/spam'
path_test_ham = 'test/ham'
path_test_spam = 'test/spam'


## use train set to count elements
probcounter = {}
probcounter['ham'] = {}
probcounter['spam'] = {}

count_element = []
num = 0
for filename in os.listdir(path_train_ham):
    content = open(os.path.join(path_train_ham, filename), encoding='gb18030',errors='ignore')
    for line in content:
        line = line.strip()
        for element in line.replace(" ' ", "'").strip().split(" "):
            if not element == "":
                num += 1
                if probcounter['ham'].__contains__(element):
                    probcounter['ham'][element] += 1
                else:
                    probcounter['ham'][element] = 1
                    probcounter['spam'][element] = 0
##append count_element[0] value            
count_element.append(num)
          

num = 0
for filename in os.listdir(path_train_spam):
    content = open(os.path.join(path_train_spam, filename), encoding='gb18030',errors='ignore')
    for line in content:
        line = line.strip()
        #pattern = re.compile("[^a-zA-Z']+")
        for element in line.replace(" ' ", "'").strip().split(" "):
            if not element == "":
                num += 1
                if probcounter['spam'].__contains__(element):
                    probcounter['spam'][element] += 1
                else:
                    probcounter['spam'][element] = 1
                    if not probcounter['ham'].__contains__(element):
                        probcounter['ham'][element] = 0
##append count_element[1] value
count_element.append(num)

##number of ham
count_ham = len(os.listdir(path_train_ham))
##number of spam
count_spam = len(os.listdir(path_train_spam))
## total of ham and spam
count = count_ham + count_spam

## use test set to get accuracy.
grade = {}
result = {}
result['ham'] = {}
result['spam'] = {}
result['ham']['F'] = 0
result['ham']['T'] = 0
result['spam']['F'] = 0
result['spam']['T'] = 0

for filename in os.listdir(path_test_ham):
    content = open(os.path.join(path_test_ham, filename), encoding='gb18030', errors='ignore')
    grade['ham'] = log(1.0 * count_ham / count, 2)
    grade['spam'] = log(1.0 * count_spam / count, 2)
    for line in content:
        line = line.strip()
        for element in line.replace(" ' ", "'").strip().split(" "):
            if probcounter['ham'].__contains__(element):
                grade['ham'] += log(1.0*(probcounter['ham'][element]+1)/(count_element[0]+len(probcounter['ham'])),2)
                grade['spam'] += log(1.0*(probcounter['spam'][element] + 1) / (count_element[1] + len(probcounter['spam'])),2)
    if grade['ham'] < grade['spam']:
        result['ham']['F'] += 1
    else:
        result['ham']['T'] += 1

for filename in os.listdir(path_test_spam):
    content = open(os.path.join(path_test_spam, filename), encoding='gb18030',errors='ignore')
    grade['ham'] = log(1.0 * count_ham / count, 2)
    grade['spam'] = log(1.0 * count_spam / count, 2)
    for line in content:
        line = line.strip()
        for element in line.replace(" ' ", "'").strip().split(" "):
            if probcounter['spam'].__contains__(element):
                grade['ham'] += log(1.0*(probcounter['ham'][element] + 1) / (count_element[0] + len(probcounter['ham'])),2)
                grade['spam'] += log(1.0*(probcounter['spam'][element] + 1) / (count_element[1] + len(probcounter['spam'])),2)
    if grade['ham'] < grade['spam']:
        result['spam']['T'] += 1
    else:
        result['spam']['F'] += 1
        
##result
hamaccu = str(1.0 * result['ham']['T'] / (result['ham']['T'] + result['ham']['F']))
spamaccu = str(1.0 * result['spam']['T'] / (result['spam']['T'] + result['spam']['F']))

print ('ham:' + hamaccu  + "\n" + 'spam: ' + spamaccu)
