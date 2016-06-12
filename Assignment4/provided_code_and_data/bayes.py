#!/usr/bin/python
# -*- coding: utf-8 -*-
# Name: Yeyi PENG, ypg016; Yuanqi SHEN, ysj784; Yamin LI, ylf245
# Date: 05/13/2016
# Description: Naïve Bayes Classifier with Laplace Smoothing
# Group work statement:
# All group members were present and contributing during all work on this project

import math, os, pickle, re, copy, random

class Bayes_Classifier:

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""
        self.posDict = {} # dictionary for positive reviews
        self.negDict = {} # dictionary for negative reviews

        # if the pickled files exist, load them into memory
        try:
            self.posDict = self.load('posDict.dat')
            self.negDict = self.load('negDict.dat')
        # otherwise train the system
        except IOError:
            self.posDict, self.negDict = self.train()

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        posDict = {}
        negDict = {}

        # get all file names in 'revews' directory
        lFileList = []
        for fFileObj in os.walk('movies_reviews/'):
            lFileList = fFileObj[2]
            break

        # deal with the content/text of each file
        for fileName in lFileList:
            content = self.loadFile('movies_reviews/' + fileName)
            splitedWords = self.tokenize(content)
            for wd in splitedWords:
                # if the 7th character of file name is '1', it's a neg review
                if fileName[7] == '1':
                    if wd in negDict:
                        negDict[wd] += 1
                    else:
                        negDict[wd] = 1
                # otherwise (7th char is '5') it's a pos review
                else:
                    if wd in posDict:
                        posDict[wd] += 1
                    else:
                        posDict[wd] = 1

        # save dictionaries to local
        self.save(posDict, 'posDict.dat')
        self.save(negDict, 'negDict.dat')

        return posDict, negDict

    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        splitedWords = self.tokenize(sText)
        # Laplace Smoothing, adding the number of unigrams to total
        posTotal = float(sum(self.posDict.values()) + len(splitedWords))
        negTotal = float(sum(self.negDict.values()) + len(splitedWords))
        p_pos = 0.0
        p_neg = 0.0

        for wd in splitedWords:
            # positive, Laplace Smoothing, adding 1
            if wd in self.posDict:
                p_pos += math.log(float(self.posDict[wd] + 1) / posTotal)
            else:
                p_pos += math.log(1 / posTotal)
            # negative, Laplace Smoothing, adding 1
            if wd in self.negDict:
                p_neg += math.log(float(self.negDict[wd] + 1) / negTotal)
            else:
                p_neg += math.log(1 / negTotal)

        if abs(p_pos - p_neg) <= 0.2:
            return 'neutral'
        elif p_pos - p_neg > 0.2:
            return 'positive'
        elif p_pos - p_neg < -0.2:
            return 'negative'

    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""
        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt

    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""
        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()

    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""
        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText):
        """Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order)."""
        lTokens = []
        sToken = ""
        for c in sText:
            if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-" or c == "'":
                sToken += c
            else:
                if sToken != "":
                    lTokens.append(sToken)
                    sToken = ""
                # remove the following codes to ignore punctuations

                # if c.strip() != "":
                    #     lTokens.append(str(c.strip()))

        if sToken != "":
            lTokens.append(sToken)
        return lTokens

    def crossValidation(self, t = 10, k = 10):
        """calculation evaluations for a (default) 10-fold cross validaton"""
        accuracy = [] # accuracies of every fold
        posPrecision = [] # pos precisions of every fold
        negPrecision= [] # neg precisions of every fold
        posRecall= [] # pos recall of every fold
        negRecall= [] # neg recall of every fold
        posFValue= [] # pos f-value of every fold
        negFValue= [] # neg f-value of every fold

        lFileList = []
        for fFileObj in os.walk('movies_reviews/'):
            lFileList = fFileObj[2]
            break
        filelist = lFileList
        for t in range(0, t):
            print "Cross Validation Trial", t + 1
            random.shuffle(filelist)
            for i in range(0, k):
                print "\tFold", i + 1
                testSet = filelist[(i * 1386) : (i * 1386 + 1390)] # generate test set
                self.trainCV(testSet, filelist)
                self.classifyCV(testSet, accuracy, posPrecision, negPrecision, posRecall, negRecall, posFValue, negFValue)

            print '\tAverage accuracy:', float(sum(accuracy)) / float(len(accuracy))
            print '\tAverage pos precision:', float(sum(posPrecision)) / float(len(posPrecision))
            print '\tAverage neg precision:', float(sum(negPrecision)) / float(len(negPrecision))
            print '\tAverage pos recall:', float(sum(posRecall)) / float(len(posRecall))
            print '\tAverage neg recall:', float(sum(negRecall)) / float(len(negRecall))
            print '\tAverage pos FValue:', float(sum(posFValue)) / float(len(posFValue))
            print '\tAverage neg FValue:', float(sum(negFValue)) / float(len(negFValue))

    def trainCV(self, testSet, filelist):
        """Trains the Naive Bayes Sentiment Classifier for Cross Validation"""
        posDictCV = {}
        negDictCV = {}
        trainingSet = copy.deepcopy(filelist)

        # remove test set from total data set
        for fileName in testSet:
            trainingSet.remove(fileName)

        # training, similar to self.train()
        for fileName in trainingSet:
            content = self.loadFile('movies_reviews/' + fileName)
            splitedWords = self.tokenize(content)
            for wd in splitedWords:
                if fileName[7] == '1':
                    if wd in negDictCV:
                        negDictCV[wd] += 1
                    else:
                        negDictCV[wd] = 1
                else:
                    if wd in posDictCV:
                        posDictCV[wd] += 1
                    else:
                        posDictCV[wd] = 1
        self.save(posDictCV, 'posDictCV.dat')
        self.save(negDictCV, 'negDictCV.dat')

    def classifyCV(self, testSet, accuracy, posPrecision, negPrecision, posRecall, negRecall, posFValue, negFValue):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """
        posDictCV = self.load('posDictCV.dat')
        negDictCV = self.load('negDictCV.dat')

        posTotal = 0 # number of total pos reviews
        negTotal = 0 # number of total neg reviews
        posClaasification = 0 # numer of pos classification results
        negClaasification = 0 # numer of neg classification results
        correctPos = 0 # correct pos classification
        correctNeg = 0 # True predicted negative

        for fileName in testSet:
            # mark the classification of current review
            if fileName[7] == '1':
                negTotal += 1
                classification = 'negative'
            else:
                posTotal += 1
                classification = 'positive'

            # classification, similar to self.claasification()
            content = self.loadFile('movies_reviews/' + fileName)
            splitedWords = self.tokenize(content)
            p_pos = 0.0
            p_neg = 0.0
            smoothedPosTotal = float(sum(posDictCV.values()) + len(splitedWords))
            smoothedNegTotal = float(sum(negDictCV.values()) + len(splitedWords))

            for wd in splitedWords:
                if wd in posDictCV:
                    p_pos += math.log(float(posDictCV[wd] + 1) / smoothedPosTotal)
                else:
                    p_pos += math.log(1 / smoothedPosTotal)
                if wd in negDictCV:
                    p_neg += math.log(float(negDictCV[wd] + 1) / smoothedNegTotal)
                else:
                    p_neg += math.log(1 / smoothedNegTotal)
            if p_pos - p_neg >= 0:
                result = 'positive'
                posClaasification += 1
            else:
                result = 'negative'
                negClaasification += 1

            if result == classification:
                if result == 'positive':
                    correctPos += 1
                else:
                    correctNeg += 1

        # calculate evaluations
        _accuracy = float(correctPos + correctNeg) / float(len(testSet))
        _posPrecision = float(correctPos) / float(posTotal)
        _negPrecision = float(correctNeg) / float(negTotal)
        _posRecall = float(correctPos) / float(posClaasification)
        _negRecall = float(correctNeg) / float(negClaasification)
        _posFValue = 2.0 * _posPrecision * _posRecall / (_posPrecision + _posRecall)
        _negFValue = 2.0 * _negPrecision * _negRecall / (_negPrecision + _negRecall)

        # append the evaluations to corresponding lists
        accuracy.append(_accuracy)
        posPrecision.append(_posPrecision)
        negPrecision.append(_negPrecision)
        posRecall.append(_posRecall)
        negRecall.append(_negRecall)
        posFValue.append(_posFValue)
        negFValue.append(_negFValue)
