from math import log
import operator
from decisionTree import treePlotter

def calcShannonEntropy(dataSet):
    numEntries = len(dataSet)
    labelCounts = {}
    for fectVec in dataSet:
        currentLabel = fectVec[-1]
        if currentLabel not in labelCounts:
            labelCounts[currentLabel] = 0
        labelCounts[currentLabel] += 1
    shannonEntropy = 0.0
    for key in labelCounts:
        prob = float(labelCounts[key])/numEntries
        shannonEntropy -= prob * log(prob, 2)
    return shannonEntropy

def createDataSet():
    dataSet = [
        [1, 1, 'yes'],
        [1, 1, 'yes'],
        [1, 0, 'no'],
        [0, 1, 'no'],
        [0, 1, 'no']
    ]
    labels = ['no surfacing', 'flippers']
    return dataSet, labels

myDat, labels = createDataSet()

print(myDat)
print(labels)

entropy = calcShannonEntropy(myDat)
print('entropy: {ent}'.format(ent=entropy))

myDat[0][-1] = 'mynot'
entropy = calcShannonEntropy(myDat)
print('again entropy: {ent}'.format(ent=entropy))

def splitDataSet(dataSet, axis, value):
    retDataSet = []
    for featVec in dataSet:
        if featVec[axis] == value:
            reducedFeatVec = featVec[:axis]
            reducedFeatVec.extend(featVec[axis + 1:])
            retDataSet.append(reducedFeatVec)
    return retDataSet

splitData = splitDataSet(myDat, 1, 0)
print(splitData)

def chooseBestFeatureToSplit(dataSet):
    numFeatures = len(dataSet[0]) - 1
    baseEntropy = calcShannonEntropy(dataSet)
    bestInfoGain = 0.0
    bestFeature = -1
    for i in range(numFeatures):
        featList = [example[i] for example in dataSet]
        uniqueVals = set(featList)
        newEntropy = 0.0
        for value in uniqueVals:
            subDataSet = splitDataSet(dataSet, i, value)
            prob = len(subDataSet)/float(len(dataSet))
            newEntropy += prob * calcShannonEntropy(subDataSet)
        infoGain = baseEntropy - newEntropy
        if infoGain > bestInfoGain:
            bestInfoGain = infoGain
            bestFeature = i
    return bestFeature

bestFeature = chooseBestFeatureToSplit(myDat)
print(bestFeature)

def majorityCnt(classList):
    classCount = {}
    for vote in classList:
        if vote not in classCount.keys():
            classCount[vote] = 0
        classCount[vote] += 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

def createTree(dataSet, labels):
    classList = [example[-1] for example in dataSet]
    if classList.count(classList[0]) == len(classList): #all the instances in a branch are the same class, then you'll create a leaf node or terminating block
        return classList[0]
    if len(dataSet[0]) == 1: #run out of attributes on which to split, if our dataset has run out of attributes but the class labels are not all the same,
                            # you must decide what to call that leaf node,it this situtaion, you'll take a majority vote.
        return majorityCnt(classList)
    bestFeat = chooseBestFeatureToSplit(dataSet)
    bestFeatLabel = labels[bestFeat]
    myTree = {bestFeatLabel: {}}
    del(labels[bestFeat])
    featValues = [example[bestFeat] for example in dataSet]
    uniqueVals = set(featValues)
    for value in uniqueVals:
        subLabels = labels[:]
        myTree[bestFeatLabel][value] = createTree(splitDataSet(dataSet, bestFeat, value), subLabels)
    return myTree

myTree = createTree(myDat, labels)
print(myTree)

def classify(inputTree, featLabels, testVec):
    firstStr = list(inputTree.keys())[0]
    secondDict = inputTree[firstStr]
    featIndex = featLabels.index(firstStr)
    for key in secondDict.keys():
        if testVec[featIndex] == key:
            if type(secondDict[key]).__name__ == 'dict':
                classLabel = classify(secondDict[key], featLabels, testVec)
            else:
                classLabel = secondDict[key]
    return classLabel

treeData, treeLabels = createDataSet()
treeDict = treePlotter.retrieveTree(0)
classLabel = classify(treeDict, treeLabels, [1, 0])
print(classLabel)
classLabel = classify(treeDict, treeLabels, [1, 1])
print(classLabel)