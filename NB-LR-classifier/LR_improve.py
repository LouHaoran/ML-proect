# -*- coding: utf-8 -*-
"""
Created on  Mar 15 15:57:26 2019

@author: lou
"""

import os
import re
from math import exp
class Logistic(object):
    learning_rate = 0.01
    lamb = 0.0001
    weights = {}
    stop_list = set()
    path_train_ham = 'train/ham'
    path_train_spam = 'train/spam'
    path_test_ham = 'test/ham'
    path_test_spam = 'test/spam'
    def __init__(self):
        content = open("./stopwords.txt", "r")
        for line in content:
            Logistic.stop_list.add(re.compile("[^a-zA-Z']+").sub(' ', line).strip())
        self.train()


    def train(self):
        Logistic.weights["bias*"] = 0
        for num in range(0, 200):
            for filename in os.listdir(Logistic.path_train_ham):
                # print filename
                dict = {}
                content = open(os.path.join(Logistic.path_train_ham, filename), encoding='gb18030',errors='ignore')
                for line in content:
                    line = line.strip()
                    
                    for element in line.replace(" ' ", "'").strip().split(" "):
                        ##
                        ##if not element == ""#
                        ##if not fillter stop words use this statement
                        ##
                        if (not element == "") and (element not in Logistic.stop_list):
                            if dict.__contains__(element):
                                dict[element] += 1
                            else:
                                dict[element] = 1
                predict_val = self.predict_ham(dictionary=dict)
                Logistic.weights["bias*"] += Logistic.learning_rate * (
                1 - predict_val) - Logistic.learning_rate * Logistic.lamb * Logistic.weights["bias*"]
                for key in dict:
                    if key in Logistic.weights:
                        Logistic.weights[key] += Logistic.learning_rate * 1.0 * (1 - predict_val) * 1.0 * (dict[key]) - \
                                                 (Logistic.learning_rate * Logistic.lamb * Logistic.weights[key])
                    else:
                        Logistic.weights[key] = 0
            for filename in os.listdir(Logistic.path_train_spam):
                dict = {}
                content = open(os.path.join(Logistic.path_train_spam, filename), encoding='gb18030',errors='ignore')
                for line in content:
                    line = line.strip()
                    for element in line.replace(" ' ", "'").strip().split(" "):
                        if (not element == "") and (element not in Logistic.stop_list):
                            if dict.__contains__(element):
                                dict[element] += 1
                            else:
                                dict[element] = 1
                predict_val = self.predict_ham(dictionary=dict)
                Logistic.weights["bias*"] += Logistic.learning_rate * (
                    0 - predict_val) - Logistic.learning_rate * Logistic.lamb * Logistic.weights["bias*"]
                for key in dict:
                    if key in Logistic.weights:
                        Logistic.weights[key] += Logistic.learning_rate * 1.0 * (0 - predict_val) * 1.0 * dict[key] - \
                                                 (Logistic.learning_rate * Logistic.lamb * Logistic.weights[key])
                    else:
                        Logistic.weights[key] = 0

    def predict_ham(self, dictionary=None):
        val = 0.0
        for element in dictionary:
            if element in Logistic.weights:
                val += Logistic.weights[element] * dictionary[element]
        return 1.0 / (1.0 + exp(-val))


    def test(self):
        result = {}
        result['ham'] = {}
        result['spam'] = {}
        result['ham']['F'] = 0
        result['ham']['T'] = 0
        result['spam']['F'] = 0
        result['spam']['T'] = 0
        for filename in os.listdir(Logistic.path_test_ham):
            dict = {}
            content = open(os.path.join(Logistic.path_test_ham, filename), encoding='gb18030',errors='ignore')
            for line in content:
                line = line.strip()
                for element in line.replace(" ' ", "'").strip().split(" "):
                    if not element == "":
                        if dict.__contains__(element):
                            dict[element] += 1
                        else:
                            dict[element] = 1
            val = Logistic.weights["bias*"]
            for key in dict:
                if key in Logistic.weights:
                    val += Logistic.weights[key] * dict[key]
            if val > 0:
                result['ham']['T'] += 1
            else:
                result['ham']['F'] += 1
        for filename in os.listdir(Logistic.path_test_spam):
            dict = {}
            content = open(os.path.join(Logistic.path_test_spam, filename), encoding='gb18030',errors='ignore')
            for line in content:
                line = line.strip()
                for element in line.replace(" ' ", "'").strip().split(" "):
                    if not element == "":
                        if dict.__contains__(element):
                            dict[element] += 1
                        else:
                            dict[element] = 1
            val = Logistic.weights["bias*"]
            for key in dict:
                if key in Logistic.weights:
                    val += Logistic.weights[key] * dict[key]
            if val > 0:
                result['spam']['F'] += 1
            else:
                result['spam']['T'] += 1
        print ('lambda: ' + str(Logistic.lamb) + "\n" + 'ham: ' + str(1.0 * result['ham']['T'] / (result['ham']['T'] + result['ham']['F'])) + "\n" + 'spam: ' + str(1.0 * result['spam']['T'] / (result['spam']['T'] + result['spam']['F'])))


def main():
    logistic = Logistic()
    logistic.test()
if __name__ == "__main__":
    main()
