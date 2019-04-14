# -*- coding: utf-8 -*-
"""
Created on Wed Feb 13 22:18:45 2019

@author: lou
"""

import pandas as pd
import numpy as np
import math
import sys
import random
import copy

class Node:
    def __init__(self,val, majClass):
        self.value = val
        self.leftChild = None
        self.rightChild = None
        self.majorityClass = majClass
        self.orderNumber = -1

    def printTree(self, count):
        if self:
            if ((self.value == 0) or (self.value == 1)):
                print ("{}".format(self.value))
            else:
                if self.leftChild:
                    if ((self.leftChild.value == 0) or (self.leftChild.value == 1)):
                        for x in range(0, count):
                            print ("|",end = " ")
                        print ("{} = 0 : {}".format(str(self.value), self.leftChild.value))
                    else:
                        for x in range(0, count):
                            print ("|",end = " ")
                        print ("{} = 0 :".format(str(self.value)))
                        count = count+1;
                        count = self.leftChild.printTree(count)

                if self.rightChild:
                    if ((self.rightChild.value == 0) or (self.rightChild.value == 1)):
                        for x in range(0, count):
                            print ("|",end = " ")
                        print ("{} = 1 : {}".format(str(self.value), self.rightChild.value))
                        count = count - 1
                    else:
                        for x in range(0, count):
                            print ("|",end = " ")
                        print ("{} = 1 :".format(str(self.value)))
                        count = count+1
                        count = self.rightChild.printTree(count)
                        count = count -1
                    return count

    def insert(self, parentNode, child_attribute, position, majClass):
        if (self.value == parentNode):
            if (position == 0):
                if self.leftChild:
                    return False
                else:
                    self.leftChild = Node(child_attribute, majClass)
            else:
                if self.rightChild:
                    return False
                else:
                    self.rightChild = Node(child_attribute, majClass)
            return True

        elif ((self.leftChild == None) and (self.rightChild == None)):
            return False

        elif self.leftChild:
            tmp = self.leftChild.insert(parentNode, child_attribute, position, majClass)
            if (tmp == False):
                if self.rightChild:
                    tmp = self.rightChild.insert(parentNode, child_attribute, position, majClass)
            return tmp

        elif self.rightChild:
            return (self.rightChild.insert(parentNode, child_attribute, position, majClass))

    def validating(self,x):
        if ((self.value == 0) or (self.value == 1)):
            return self.value
        else:
            if(x[self.value]==0):
                return(self.leftChild.validating(x))
            else:
                return(self.rightChild.validating(x))

    def inOrderOrdering(self, orderNum):
        if self:
            if self.leftChild:
                orderNum = self.leftChild.inOrderOrdering(orderNum)

            if ((self.value != 0) and (self.value != 1)):
                orderNum = orderNum+1
                self.orderNumber = orderNum

            if self.rightChild:
                orderNum = self.rightChild.inOrderOrdering(orderNum)

            return orderNum

    def replaceNode(self,P):
        if self:
            if (self.orderNumber==P):
                self.leftChild = None
                self.rightChild = None
                self.value = self.majorityClass
                return
            elif(P<self.orderNumber):
                self.leftChild.replaceNode(P)
            else:
                self.rightChild.replaceNode(P)
            return
        return

class Tree:
    def __init__(self):
        self.root = None

    def insert(self, parentNode, child_attribute, position, majClass):
        if self.root:
            return self.root.insert(parentNode, child_attribute, position, majClass)
        else:
            self.root = Node (child_attribute, majClass)
            return True

    def printTree(self):
        self.root.printTree(0)

    def validating(self,x):
        y = self.root.validating(x)
        return y

    def inOrderOrdering(self):
        numberOfNonLeafNodes = self.root.inOrderOrdering(0)
        return numberOfNonLeafNodes

    def replaceNode(self,P):
        self.root.replaceNode(P)
        return

def majorityClass(df):
    Class1_training_examples =  df[df['Class']==1].shape[0]
    Class0_training_examples =  df[df['Class']==0].shape[0]
    if (Class0_training_examples >= Class1_training_examples):
        return 0
    else:
        return 1

def finding_base_entropy(df):
    Class1_training_examples =  df[df['Class']==1].shape[0]
    Class0_training_examples =  df[df['Class']==0].shape[0]
    Total_training_examples = df.shape[0]
    if ((Class0_training_examples == 0)or(Class1_training_examples == 0)):
        base_entropy = 0
    else:
        base_entropy = -((Class1_training_examples/Total_training_examples)* math.log2(Class1_training_examples/Total_training_examples))-((Class0_training_examples/Total_training_examples)* math.log2(Class0_training_examples/Total_training_examples))
    return base_entropy

def find_best_attribute_informationGain(df):
    columns_list = df.columns.values
    columns_list = [x for x in columns_list if x != 'Class']
    base_entropy = finding_base_entropy(df)
    gain = np.ones([1,len(columns_list)])* base_entropy
    Total_training_examples = df.shape[0]
    gain_df = pd.DataFrame(gain, columns = columns_list)
    for y in columns_list:

        S0 = df[df[y]==0]
        rowsS0 = S0.shape[0]
        S0Entropy = finding_base_entropy(S0)

        S1 = df[df[y]==1]
        rowsS1 = S1.shape[0]
        S1entropy = finding_base_entropy(S1)

        gain_df[y] = base_entropy - (((rowsS0/Total_training_examples)*S0Entropy)+((rowsS1/Total_training_examples)*S1entropy))

    max_gain_column = gain_df.values.argmax();
    best_attribute = df.columns[max_gain_column]
    return best_attribute

def finding_base_variance(df):
    K1 =  df[df['Class']==1].shape[0]
    K0 =  df[df['Class']==0].shape[0]
    K = df.shape[0]

    if ((K0 ==0) or (K1 == 0)):
        return 0
    else:
        base_variance = (K0/K)*(K1/K)
    return base_variance

def find_best_attribute_variance(df):
    columns_list = df.columns.values
    columns_list = [x for x in columns_list if x != 'Class']
    base_variance = finding_base_variance(df)
    gain = np.ones([1,len(columns_list)])* base_variance
    Total_training_examples = df.shape[0]
    gain_df = pd.DataFrame(gain, columns = columns_list)
    for y in columns_list:

        S0 = df[df[y]==0]
        rowsS0 = S0.shape[0]
        S0Variance = finding_base_variance(S0)

        S1 = df[df[y]==1]
        rowsS1 = S1.shape[0]
        S1Variance = finding_base_variance(S1)

        gain_df[y] = base_variance - (((rowsS0/Total_training_examples)*S0Variance)+((rowsS1/Total_training_examples)*S1Variance))

    max_gain_column = gain_df.values.argmax();
    best_attribute = df.columns[max_gain_column]
    return best_attribute

def building_decision_tree(df, parentNode, position, decisionTree, majClass, typeHeuristic):
    if(len(set(df['Class']))==1):
        leafNodeClass = set(df['Class']).pop()
        decisionTree.insert(parentNode, leafNodeClass, position, majClass)
        return
    else:
        checkDF = df.drop('Class', 1)
        if (checkDF.empty):
            leafNodeClass = majClass
            decisionTree.insert(parentNode, leafNodeClass, position, majClass)
            return
        else:
            if (typeHeuristic == "informationGain"):
                best_attribute = find_best_attribute_informationGain(df)
            elif(typeHeuristic == "varianceImpurity"):
                best_attribute = find_best_attribute_variance(df)

            ds0 = split(df, best_attribute, 0)
            ds1 = split (df, best_attribute, 1)

            decisionTree.insert(parentNode, best_attribute, position, majClass)
            building_decision_tree(ds0,best_attribute,0, decisionTree, majorityClass(ds0), typeHeuristic)
            building_decision_tree(ds1,best_attribute,1, decisionTree, majorityClass(ds1), typeHeuristic)
            return

def validation(decisionTree, data_set):
    NumberOfRows = data_set.shape[0]
    NumberOfWrongChoices = 0
    for idx, row in data_set.iterrows():
        x = decisionTree.validating(row)
        y = data_set.iloc[idx,-1]
        if (x!=y):
            NumberOfWrongChoices= NumberOfWrongChoices+1
    accuracy = (NumberOfRows-NumberOfWrongChoices)/NumberOfRows
    return(accuracy)

def split(df, split_on_attribute, value):
    ds = df[(df[split_on_attribute]==value)]
    ds = ds.drop(split_on_attribute, 1)
    return(ds)

def pruning(D,Vset,L, K):
    DBest = copy.deepcopy(D)
    for i in range(1,L+1):
        DHash = copy.deepcopy(D)
        M = random.randint(1,K)
        for j in range(1,M+1):
            N = DHash.inOrderOrdering()
            if (N==0):
                break
            else:
                P = random.randint(1,N)
                DHash.replaceNode(P)
        DHashAccuracy = validation(DHash,Vset)
        DBestAccuracy = validation(DBest,Vset)
        if (DHashAccuracy > DBestAccuracy):
            DBest = copy.deepcopy(DHash)
    return DBest

def printing(DTree,toPrint):
    if (toPrint == "yes"):
        DTree.printTree()
    elif(toPrint == "no"):
        print("Not printing the decision tree")
    else:
        print ("Please type 'yes' to print the decision trees, 'no' to not print the decision tree")
    print()
    return

def mainFunction(trainSet , validateSet , testSet , toPrint , L , K):
    print()
    print("======================================================================")
    print()
    print("Information Gain Heuristic")
    decisionTree_informationGain = Tree()
    building_decision_tree(trainSet,'Null',-1, decisionTree_informationGain, majorityClass(trainSet), "informationGain")
    printing(decisionTree_informationGain, toPrint)
    print("Accuracy for training set before pruning = {0:.4f}".format(validation(decisionTree_informationGain, trainSet)))
    print("Accuracy for validation set before pruning = {0:.4f}".format(validation(decisionTree_informationGain, validateSet)))
    print("Accuracy for test set before pruning = {0:.4f}".format(validation(decisionTree_informationGain, testSet)))
    print()

    print("After Pruning")
    new_decisionTree_informationGain = pruning (decisionTree_informationGain,validateSet,L,K)
    print("Accuracy for training set before pruning with L = {0} and K = {1} is = {2:.4f}".format(L,K,validation(new_decisionTree_informationGain, trainSet)))
    print("Accuracy for validation set before pruning with L = {0} and K = {1} is = {2:.4f}".format(L,K,validation(new_decisionTree_informationGain, validateSet)))
    print("Accuracy for test set before pruning with L = {0} and K = {1} is = {2:.4f}".format(L,K,validation(new_decisionTree_informationGain, testSet)))

    LList = [100,200,300,400,500]
    KList = [25,50]
    #
    # print("information gain Heuristic After Pruning")
    # print()
    # print(" L\t K\tTraining\tValidate\tTest")
    # for x in LList:
    #     for y in KList:
    #         new_decisionTree_informationGain = pruning (decisionTree_informationGain,validateSet,x,y)
    #         print("{0}\t{1}\t{2:.4f}\t\t{3:.4f}\t\t{4:.4f}".format(x,y,validation(new_decisionTree_informationGain, trainSet),validation(new_decisionTree_informationGain, validateSet),validation(new_decisionTree_informationGain, testSet)))
    #         print()

    print("======================================================================")
    print()
    print("Variance Impurity Heuristic")
    decisionTree_varianceImpurity = Tree()
    building_decision_tree(trainSet,'Null',-1, decisionTree_varianceImpurity, majorityClass(trainSet), "varianceImpurity")
    printing(decisionTree_varianceImpurity, toPrint)
    print("Accuracy for training set before pruning = {0:.4f}".format(validation(decisionTree_varianceImpurity, trainSet)))
    print("Accuracy for validation set before pruning = {0:.4f}".format(validation(decisionTree_varianceImpurity, validateSet)))
    print("Accuracy for test set before pruning = {0:.4f}".format(validation(decisionTree_varianceImpurity, testSet)))
    print()



    print("After Pruning")
    new_decisionTree_varianceImpurity = pruning (decisionTree_varianceImpurity,validateSet,L,K)
    print("Accuracy for training set after pruning with L = {0} and K = {1} is = {2:.4f}".format(L,K,validation(new_decisionTree_varianceImpurity, trainSet)))
    print("Accuracy for validation set after pruning with L = {0} and K = {1} is = {2:.4f}".format(L,K,validation(new_decisionTree_varianceImpurity, validateSet)))
    print("Accuracy for test set after pruning with L = {0} and K = {1} is = {2:.4f}".format(L,K,validation(new_decisionTree_varianceImpurity, testSet)))
    print()

    # print("Variance Impurity Heuristic After Pruning")
    # print()
    # print(" L\t K\tTraining\tValidate\tTest")
    # for x in LList:
    #     for y in KList:
    #         new_decisionTree_varianceImpurity = Tree()
    #         new_decisionTree_varianceImpurity = pruning (decisionTree_varianceImpurity,validateSet,x,y)
    #         print("{0}\t{1}\t{2:.4f}\t\t{3:.4f}\t\t{4:.4f}".format(x,y,validation(new_decisionTree_varianceImpurity, trainSet),validation(new_decisionTree_varianceImpurity, validateSet),validation(new_decisionTree_varianceImpurity, testSet)))
    #         print()
    # print("======================================================================")
    return

# The Main program begins here.

L = int(sys.argv[1])
K = int(sys.argv[2])
training_set = pd.read_csv(sys.argv[3])
validation_set = pd.read_csv(sys.argv[4])
test_set = pd.read_csv(sys.argv[5])
toPrint = sys.argv[6]

mainFunction(training_set,validation_set, test_set, toPrint, L, K)
        
       
        
        
        

