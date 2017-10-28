from numpy import *
from numpy import array
import operator
import matplotlib
import matplotlib.pyplot as plt
from os import listdir

def createDataSet():
    group = array([[1.0, 1.1], [1.0, 1.0], [0, 0], [0, 0.1]])
    labels = ['A', 'A', 'B', 'B']
    return group, labels


_group, _labels = createDataSet()

print(_group)
print("-------------")
print(_labels)

def classify0(inX, dataSet, labels, k):
    dataSetSize = dataSet.shape[0]
    _tile = tile(inX, (dataSetSize, 1))
    diffMat = _tile - dataSet
    sqDiffMat = diffMat**2
    sqDistances = sqDiffMat.sum(axis=1)
    distances = sqDistances**0.5
    #print(distances)
    sortedDistIndicies = distances.argsort()
    #print(sortedDistIndicies)
    classCount = {}
    for i in range(k):
        voteIlabel = labels[sortedDistIndicies[i]]
        classCount[voteIlabel] = classCount.get(voteIlabel, 0) + 1
    sortedClassCount = sorted(classCount.items(), key=operator.itemgetter(1), reverse=True)
    return sortedClassCount[0][0]

ret = classify0([1, 1], _group, _labels, 3)

print(ret)

def file2matrix(filename):
    fr = open(filename)
    numberOfLines = len(fr.readlines())
    returnMat = zeros((numberOfLines, 3))
    classLabelVector = []
    fr = open(filename)
    index = 0
    for line in fr.readlines():
        line = line.strip()
        listFromLine = line.split('\t')
        returnMat[index, :] = listFromLine[0: 3]
        classLabelVector.append(listFromLine[-1])
        index += 1
    return returnMat, classLabelVector

returnMat, labelVector = file2matrix('datingTestSet.txt')

print("----------------datingTestSet")
print(returnMat)
print(labelVector)

def plot(src1, src2):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(src1, src2, c='b', marker='o')
    plt.show()

#plot(returnMat[:, 2], returnMat[:, 0])


print('--auto Norm---')
def autoNorm(dataSet):
    minVals = dataSet.min(0)
    maxVals = dataSet.max(0)
    ranges = maxVals - minVals
    normDataSet = zeros((shape(dataSet)))
    m = dataSet.shape[0]
    print(m)
    normDataSet = dataSet - tile(minVals, (m, 1))
    normDataSet = normDataSet/tile(ranges, (m, 1))
    return normDataSet, ranges, maxVals, minVals

normMat, ranges, maxVals, minVals = autoNorm(returnMat)

print(normMat)
print(ranges)
print(maxVals)
print(minVals)

def datingClassTest():
    hoRation = 0.10
    datingDataMat, datingLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, maxVals, minVals = autoNorm(datingDataMat)
    m = normMat.shape[0]
    numTestVecs = int(m*hoRation)
    errorCount = 0.0
    for i in range(numTestVecs):
        r = normMat[numTestVecs: m, :]
        classifierResult = classify0(normMat[i, :], normMat[numTestVecs: m, :], datingLabels[numTestVecs: m], 3)
        print('the classifier came back with: {result}, the real answer is: {label}'.format(result=classifierResult, label=datingLabels[i]))
        if classifierResult != datingLabels[i]:
            errorCount += 1.0
    print('the total error rate is: {total}, {rate}'.format(total=errorCount, rate=errorCount/float(numTestVecs)))

datingClassTest()

def classifyPerson():
    resultList = ['not at all', 'in small doses', 'in large doses']
    percentTats = float(input("percentage of time spent playing video games?"))
    ffMiles = float(input("frequent filer miles earned per year?"))
    iceCream = float(input("liters of ice cream consumed per year?"))
    datingDataMat, datringLabels = file2matrix('datingTestSet.txt')
    normMat, ranges, maxVals, minVals = autoNorm(datingDataMat)
    inArr = array([ffMiles, percentTats, iceCream])
    classifierResult = classify0((inArr - minVals)/ranges, normMat, datringLabels, 4)
    #r = resultList[classifierResult - 1]
    #print(r)
    print('You will probably like this person: {probality}'.format(probality=classifierResult))

#classifyPerson()

def img2vector(filename):
    returnVect = zeros((1, 1024))
    fr = open(filename)
    for i in range(32):
        lineStr = fr.readline()
        for j in range(32):
            returnVect[0, 32 * i + j] = int(lineStr[j])
    return returnVect

testVector = img2vector('./digits/testDigits/0_13.txt')
print(testVector)
print(testVector[0, 0: 31])
print(testVector[0, 32: 63])

testVector = img2vector('./digits/testDigits/1_13.txt')
print(testVector)
print(testVector[0, 0: 31])
print(testVector[0, 32: 63])

testVector = img2vector('./digits/testDigits/0_11.txt')
print(testVector)
print(testVector[0, 0: 31])
print(testVector[0, 32: 63])

def handwritingClassTest():
    hwLabels = []
    trainingFileList = listdir('./digits/trainingDigits')
    m = len(trainingFileList)
    trainingMat = zeros((m, 1024))
    for i in range(m):
        fileNameStr = trainingFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        hwLabels.append(classNumStr)
        trainingMat[i, :] = img2vector('./digits/trainingDigits/{fn}'.format(fn=fileNameStr))
    testFileList = listdir('./digits/testDigits')
    errorCount = 0.0
    mTest = len(testFileList)
    for i in range(mTest):
        fileNameStr = testFileList[i]
        fileStr = fileNameStr.split('.')[0]
        classNumStr = int(fileStr.split('_')[0])
        vectorUnderTest = img2vector('./digits/testDigits/{fn}'.format(fn=fileNameStr))
        classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
        print('the classifier came back with: {result}, the real answer is {answer}'.format(result=classifierResult, answer=classNumStr))
        if classifierResult != classNumStr:
            errorCount += 1.0
    print('the total number of errors is {total}, error rate is {rate}'.format(total=errorCount, rate=(errorCount/float(mTest))))

handwritingClassTest()