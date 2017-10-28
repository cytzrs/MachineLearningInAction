import matplotlib.pyplot as plt

decisionNode = dict(boxstyle="sawtooth", fc="0.8")
leafNode = dict(boxstyle="round4", fc="0.8")
arrow_args = dict(arrowstyle="<-")

def plotNode(nodeTxt, centerPt, parentPt, nodeType):
    createPlot.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
        va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def createPlot():
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    createPlot.ax1 = plt.subplot(111, frameon=False)
    plotNode('a decision node', (0.5, 0.1), (0.1, 0.5), decisionNode)
    plotNode('a leaf node', (0.8, 0.1), (0.3, 0.8), leafNode)
    plt.show()

#createPlot()

def getNumLeafs(myTree):
    numLeafs = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            numLeafs += getNumLeafs(secondDict[key])
        else:
            numLeafs += 1
    return numLeafs

def getTreeDepth(myTree):
    maxDepth = 0
    firstStr = list(myTree.keys())[0]
    secondDict = myTree[firstStr]
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            thisDepth = 1 + getTreeDepth(secondDict[key])
        else:
            thisDepth = 1
        if thisDepth > maxDepth:
            maxDepth = thisDepth
    return maxDepth

def retrieveTree(i):
    listOfTrees = [{'no surfacing': {0: 'no', 1: {'flippers': {0: 'no', 1: 'yes'}}}},
                   {'no surfacing': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}, 1: {'flippers': {0: {'head': {0: 'no', 1: {'flippers': {0: {'head': {0: 'no', 1: 'yes'}}}}}}}}}}}}
                   ]
    return listOfTrees[i]

tree = retrieveTree(0)
print(tree)

numLeafs = getNumLeafs(tree)
depth = getTreeDepth(tree)

print('leafs: {leafs}, depth: {depth}'.format(leafs=numLeafs, depth=depth))

tree = retrieveTree(1)
print(tree)

numLeafs = getNumLeafs(tree)
depth = getTreeDepth(tree)

print('leafs: {leafs}, depth: {depth}'.format(leafs=numLeafs, depth=depth))

def plotMidText(cntrPt, parentPt, txtString):
    xMid = (parentPt[0] - cntrPt[0])/2.0 + cntrPt[0]
    yMid = (parentPt[1] - cntrPt[1])/2.0 + cntrPt[1]
    createPlotPlus.ax1.text(xMid, yMid, txtString)

def plotNodePlus(nodeTxt, centerPt, parentPt, nodeType):
    createPlotPlus.ax1.annotate(nodeTxt, xy=parentPt, xycoords='axes fraction', xytext=centerPt, textcoords='axes fraction',
        va="center", ha="center", bbox=nodeType, arrowprops=arrow_args)

def plotTreePlus(myTree, parentPt, nodeTxt):
    numLeafs = getNumLeafs(myTree)
    #depth = getTreeDepth(myTree)
    firstStr = list(myTree.keys())[0]
    cntrPt = (plotTreePlus.xOff + (1.0 + float(numLeafs))/2.0/plotTreePlus.totalW, plotTreePlus.yOff)
    plotMidText(cntrPt, parentPt, nodeTxt)
    plotNodePlus(firstStr, cntrPt, parentPt, decisionNode)
    secondDict = myTree[firstStr]
    plotTreePlus.yOff = plotTreePlus.yOff - 1.0/plotTreePlus.totalD
    for key in secondDict.keys():
        if type(secondDict[key]).__name__ == 'dict':
            plotTreePlus(secondDict[key], cntrPt, str(key))
        else:
            plotTreePlus.xOff = plotTreePlus.xOff + 1.0/plotTreePlus.totalW
            plotNodePlus(secondDict[key], (plotTreePlus.xOff, plotTreePlus.yOff), cntrPt, leafNode)
            plotMidText((plotTreePlus.xOff, plotTreePlus.yOff), cntrPt, str(key))
    plotTreePlus.yOff = plotTreePlus.yOff + 1.0/plotTreePlus.totalD

def createPlotPlus(inTree):
    fig = plt.figure(1, facecolor='white')
    fig.clf()
    axprops = dict(xticks=[], yticks=[])
    createPlotPlus.ax1 = plt.subplot(111, frameon=False, **axprops)
    plotTreePlus.totalW = float(getNumLeafs(inTree))
    plotTreePlus.totalD = float(getTreeDepth(inTree))
    plotTreePlus.xOff = -0.5/plotTreePlus.totalW;
    plotTreePlus.yOff = 1.0
    plotTreePlus(inTree, (0.5, 1.0), '')
    plt.show()

#createPlotPlus(tree)