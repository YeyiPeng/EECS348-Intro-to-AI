#!/usr/bin/python
# -*- coding: utf-8 -*-

from bayes import *
import math, os, pickle, re, operator, copy, random
def crossValidation(k = 10):
    lFileList = []
    for fFileObj in os.walk("reviews/"):
        lFileList = fFileObj[2]
        break
    iTestDataNum = math.floor(float(len(lFileList))/float(float(k)))
    numTestSet = len(lFileList)/int(iTestDataNum)
    lFilesRemained = range(1, len(lFileList))
    lFilesAll = copy.deepcopy(lFilesRemained)
    print 'Total size of entire dataset:, ', len(lFilesRemained)
    lTestDataIndex=[]
    for i in range(numTestSet):
        if int(iTestDataNum) <= len(lFilesRemained):
            lTestDataIndex.append(random.sample(lFilesRemained, int(iTestDataNum))) # Get indices for random one k-th of the entire dataset
            lFilesRemained= list(set(lFilesRemained) - set(lTestDataIndex[i]))
        elif int(iTestDataNum) > len(lFilesRemained):
            lTestDataIndex.append(lFilesRemained)
        # Initalize cross validation measures
    lCVaccuracy = []
    lCVPosPrecision = []
    lCVNegPrecision= []
    lCVPosRecall= []
    lCVNegRecall= []
    lCVPosF1= []
    lCVNegF1= []
    for ii in range(numTestSet): # for each k-th fold
        lTrainDataIndex = list(set(lFilesAll) - set(lTestDataIndex[ii]))
        lTrainData = []
        for j in lTrainDataIndex:
            lTrainData.append(lFileList[j])
        # remove CV pickled files if exist
        f10foldCVPositive = 'dPos10fCVtestBase'
        f10foldCVNegative = 'dNeg10fCVtestBase'
        if os.path.exists(f10foldCVPositive):
            os.remove(f10foldCVPositive)
        if os.path.exists(f10foldCVNegative):
            os.remove(f10foldCVNegative)
        # initialize and train to save to CV pickle files
        classfier = Bayes_Classifier(lTrainData, f10foldCVPositive, f10foldCVNegative)

        iMatchCount = 0 # Number of predictions that match with real sentiment
        iTruePosCount = 0 # Real positive
        iTrueNegCount = 0 # Real positive
        iPredictPos = 0 # Predicted positive
        iPredictNeg = 0 # Predicted negative
        iPredictTruePos = 0 # True predicted positive
        iPredictTrueNeg = 0 # True predicted negative
        testct = 0
        for i in lTestDataIndex[ii]:
            fn = lFileList[i]
            text = classfier.loadFile("reviews/"+fn)
            if fn[7] == '5': # positive movie review
                sTruesentiment = 'positive'
                iTruePosCount += 1
            elif fn[7] == '1':
                sTruesentiment = 'negative'
                iTrueNegCount += 1
            sPredictedsentiment = classfier.classify(text)
            if sPredictedsentiment == 'positive':
                iPredictPos += 1
            elif sPredictedsentiment == 'negative':
                iPredictNeg += 1
            if sPredictedsentiment == sTruesentiment:
                iMatchCount += 1
                if sPredictedsentiment == 'positive':
                    iPredictTruePos += 1
                elif sPredictedsentiment == 'negative':
                    iPredictTrueNeg += 1
            else:
                pass
            testct += 1
        fAccuracy = float(float(iMatchCount)/float(len(lTestDataIndex[ii])))
        fPosPrecision = float(float(iPredictTruePos)/float(iTruePosCount))
        fNegPrecision = float(float(iPredictTrueNeg)/float(iTrueNegCount))
        fPosRecall = float(float(iPredictTruePos)/float(iPredictPos))
        fNegRecall = float(float(iPredictTrueNeg)/float(iPredictNeg))
        fPosF1 = float(float(2)*fPosPrecision*fPosRecall/(fPosPrecision+fPosRecall))
        fNegF1 = float(float(2)*fNegPrecision*fNegRecall/(fNegPrecision+fNegRecall))
        lCVaccuracy.append(fAccuracy)
        lCVPosPrecision.append(fPosPrecision)
        lCVNegPrecision.append(fNegPrecision)
        lCVPosRecall.append(fPosRecall)
        lCVNegRecall.append(fNegRecall)
        lCVPosF1.append(fPosF1)
        lCVNegF1.append(fNegF1)
    print 'average accuracy from CV: ', sum(lCVaccuracy)/float(len(lCVaccuracy))
    print 'average POS precision from CV: ', sum(lCVPosPrecision)/float(len(lCVPosPrecision))
    print 'average NEG precision from CV: ', sum(lCVNegPrecision)/float(len(lCVNegPrecision))
    print 'average POS recall from CV: ', sum(lCVPosRecall)/float(len(lCVPosRecall))
    print 'average NEG recall from CV: ', sum(lCVNegRecall)/float(len(lCVNegRecall))
    print 'average POS F1 from CV: ', sum(lCVPosF1)/float(len(lCVPosF1))
    print 'average NEG F1 from CV: ', sum(lCVNegF1)/float(len(lCVNegF1))

# t = Bayes_Classifier()
crossValidation()
