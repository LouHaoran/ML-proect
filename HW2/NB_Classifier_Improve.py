# -*- coding: utf-8 -*-
"""
Created on  Mar 14 15:57:26 2019

@author: lou
"""

import os
import re
from math import log
from collections import defaultdict
path_train_ham = 'train/ham'
path_train_spam = 'train/spam'
path_test_ham = 'test/ham'
path_test_spam = 'test/spam'
dict = {}
dict['ham'] = {}
dict['spam'] = {}

stop_list = set()
content = open("./stopwords.txt", "r")
for line in content:
    stop_list.add(re.compile("[^a-zA-Z']+").sub(' ', line).strip())

count_element = []
num = 0
for filename in os.listdir(path_train_ham):
    content = open(os.path.join(path_train_ham, filename),  encoding='gb18030',errors='ignore')
    for line in content:
        line = line.strip()
        ## count the word not in stoplist
        for element in line.replace(" ' ", "'").strip().split(" "):
            if (not element == "") and (element.lower() not in stop_list):
                num += 1
                if dict['ham'].__contains__(element):
                    dict['ham'][element] += 1
                else:
                    dict['ham'][element] = 1
                    dict['spam'][element] = 0
           
count_element.append(num)
          

num = 0
for filename in os.listdir(path_train_spam):
    content = open(os.path.join(path_train_spam, filename),  encoding='gb18030',errors='ignore')
    for line in content:
        line = line.strip()
        for element in line.replace(" ' ", "'").strip().split(" "):
            if (not element == "") and (element.lower() not in stop_list):
                num += 1
                if dict['spam'].__contains__(element):
                    dict['spam'][element] += 1
                else:
                    dict['spam'][element] = 1
                    dict['ham'][element] = 0
count_element.append(num)

count_ham = len(os.listdir(path_train_ham))
count_spam = len(os.listdir(path_train_spam))
count = count_ham + count_spam

grade = {}
result = {}
result['ham'] = {}
result['spam'] = {}
result['ham']['F'] = 0
result['ham']['T'] = 0
result['spam']['F'] = 0
result['spam']['T'] = 0

for filename in os.listdir(path_test_ham):
    content = open(os.path.join(path_test_ham, filename),  encoding='gb18030',errors='ignore')
    grade['ham'] = log(1.0 * count_ham / count, 2)
    grade['spam'] = log(1.0 * count_spam / count, 2)
    for line in content:
        line = line.strip()
        ##pattern = re.compile("[^a-zA-Z]+")
        for element in line.replace(" ' ", "'").strip().split(" "):
            if dict['ham'].__contains__(element):
                grade['ham'] += log(1.0*(dict['ham'][element]+1)/(count_element[0]+len(dict['ham'])),2)
                grade['spam'] += log(1.0*(dict['spam'][element] + 1) / (count_element[1] + len(dict['spam'])),2)
    if grade['ham'] < grade['spam']:
        result['ham']['F'] += 1
    else:
        result['ham']['T'] += 1

for filename in os.listdir(path_test_spam):
    content = open(os.path.join(path_test_spam, filename),  encoding='gb18030',errors='ignore')
    grade['ham'] = log(1.0 * count_ham / count, 2)
    grade['spam'] = log(1.0 * count_spam / count, 2)
    for line in content:
        line = line.strip()
        pattern = re.compile("[^a-zA-Z]+")
        for element in pattern.sub(' ', line).strip().split(" "):
            if dict['spam'].__contains__(element):
                grade['ham'] += log(1.0*(dict['ham'][element] + 1) / (count_element[0] + len(dict['ham'])),2)
                grade['spam'] += log(1.0*(dict['spam'][element] + 1) / (count_element[1] + len(dict['spam'])),2)
    if grade['ham'] < grade['spam']:
        result['spam']['T'] += 1
    else:
        result['spam']['F'] += 1

hamaccu = str(1.0 * result['ham']['T'] / (result['ham']['T'] + result['ham']['F']))
spamaccu = str(1.0 * result['spam']['T'] / (result['spam']['T'] + result['spam']['F']))

print ('ham:' + hamaccu  + "\n" + 'spam: ' + spamaccu)


