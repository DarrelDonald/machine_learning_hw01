#!/usr/bin/python
import math
import sys
import random

validation_set = open(sys.argv[4])

test_set = open(sys.argv[5])

training_set = open(sys.argv[3])

result = open("reports_" + sys.argv[3].split("/")[0], "a")

attributes = training_set.readline().split(",")

numberOfRows = 0
for x in training_set:
    numberOfRows = numberOfRows + 1

L = int(sys.argv[1])

K = int(sys.argv[2])

# 20 is the y attribute
yValue = 20

if sys.argv[6] == "yes":
    printOut = True
else:
    printOut = False


# posNeg is a tuple (positive results, negative results)
def entropy(posNeg):
    if posNeg[0] == 0 and posNeg[1] == 0:
        return 1
    probPos = posNeg[0] / (posNeg[0] + posNeg[1])
    probNeg = posNeg[1] / (posNeg[0] + posNeg[1])
    if probNeg == 0 or probPos == 0:
        return 0
    result = probPos * math.log(probPos, 2)
    result = result + probNeg * math.log(probNeg, 2)
    return -1 * result


def vi(posNeg):
    if posNeg[0] == 0 and posNeg[1] == 0:
        return 1
    probPos = posNeg[0] / (posNeg[0] + posNeg[1])
    probNeg = posNeg[1] / (posNeg[0] + posNeg[1])
    return probPos * probNeg


def GainVI(parentPosNeg, childPosNeg):
    result = vi(parentPosNeg)
    total = parentPosNeg[0] + parentPosNeg[1]
    yesWeight = childPosNeg[0] + childPosNeg[1]
    yesWeight = yesWeight / total
    yesChildVI = vi((childPosNeg[0], childPosNeg[1]))
    noWeight = childPosNeg[2] + childPosNeg[3]
    noWeight = noWeight / total
    noChildVI = vi((childPosNeg[2], childPosNeg[3]))
    result = result - (yesWeight * yesChildVI)
    result = result - (noWeight * noChildVI)
    return result


# childPosNeg the left node posNeg followed by the right nodes in one tuple
def Gain(parentPosNeg, childPosNeg):
    result = entropy(parentPosNeg)
    total = parentPosNeg[0] + parentPosNeg[1]
    yesWeight = childPosNeg[0] + childPosNeg[1]
    yesWeight = yesWeight / total
    yesChildEntropy = entropy((childPosNeg[0], childPosNeg[1]))
    noWeight = childPosNeg[2] + childPosNeg[3]
    noWeight = noWeight / total
    noChildEntropy = entropy((childPosNeg[2], childPosNeg[3]))
    result = result - (yesWeight * yesChildEntropy)
    result = result - (noWeight * noChildEntropy)
    return result


# move file pointer back to top of data
def reset(file):
    file.seek(0)
    file.readline()


def findBest(reamainingAttributes, rowsLeft):
    reset(training_set)

    yesValues = 0
    noValues = 0
    currentRow = 0

    for line in training_set:

        if rowsLeft[currentRow] == 0:
            currentRow = currentRow + 1
            continue

        row = line.split(",")

        if int(row[yValue]) == 1:
            yesValues = yesValues + 1

        elif int(row[yValue]) == 0:
            noValues = noValues + 1
        currentRow = currentRow + 1

    rootPosNeg = (yesValues, noValues)

    maxGain = 0

    for currentAttribute in reamainingAttributes:

        # to keep count of the values encountered
        yesValues0 = 0
        yesValues1 = 0
        noValues0 = 0
        noValues1 = 0
        currentRow = 0

        reset(training_set)
        for line in training_set:

            if rowsLeft[currentRow] == 0:
                currentRow = currentRow + 1
                continue

            row = line.split(",")

            if int(row[currentAttribute]) == 0:
                if int(row[yValue]) == 0:
                    noValues0 = noValues0 + 1

                elif int(row[yValue]) == 1:
                    noValues1 = noValues1 + 1

            elif int(row[currentAttribute]) == 1:
                if int(row[yValue]) == 0:
                    yesValues0 = yesValues0 + 1

                elif int(row[yValue]) == 1:
                    yesValues1 = yesValues1 + 1

            currentRow = currentRow + 1

        childPosNeg = (yesValues1, yesValues0, noValues1, noValues0)
        gain = Gain(rootPosNeg, childPosNeg)
        if gain >= maxGain:
            maxGain = gain
            bestAttribute = currentAttribute

    return bestAttribute


def findBestVI(reamainingAttributes, rowsLeft):
    reset(training_set)

    yesValues = 0
    noValues = 0
    currentRow = 0

    for line in training_set:

        if rowsLeft[currentRow] == 0:
            currentRow = currentRow + 1
            continue

        row = line.split(",")

        if int(row[yValue]) == 1:
            yesValues = yesValues + 1

        elif int(row[yValue]) == 0:
            noValues = noValues + 1
        currentRow = currentRow + 1

    rootPosNeg = (yesValues, noValues)

    maxGain = 0

    for currentAttribute in reamainingAttributes:

        # to keep count of the values encountered
        yesValues0 = 0
        yesValues1 = 0
        noValues0 = 0
        noValues1 = 0
        currentRow = 0

        reset(training_set)
        for line in training_set:

            if rowsLeft[currentRow] == 0:
                currentRow = currentRow + 1
                continue

            row = line.split(",")

            if int(row[currentAttribute]) == 0:
                if int(row[yValue]) == 0:
                    noValues0 = noValues0 + 1

                elif int(row[yValue]) == 1:
                    noValues1 = noValues1 + 1

            elif int(row[currentAttribute]) == 1:
                if int(row[yValue]) == 0:
                    yesValues0 = yesValues0 + 1

                elif int(row[yValue]) == 1:
                    yesValues1 = yesValues1 + 1

            currentRow = currentRow + 1

        childPosNeg = (yesValues1, yesValues0, noValues1, noValues0)
        gain = GainVI(rootPosNeg, childPosNeg)
        if gain >= maxGain:
            maxGain = gain
            bestAttribute = currentAttribute

    return bestAttribute


def buildTree(remainingAttributes, rowsLeft, currentTree, position, level):
    reset(training_set)

    yes = 0
    no = 0
    currentRow = 0

    for line in training_set:

        if rowsLeft[currentRow] == 0:
            currentRow = currentRow + 1
            continue

        row = line.split(",")

        if int(row[yValue]) == 1:
            yes = yes + 1

        elif int(row[yValue]) == 0:
            no = no + 1

        currentRow = currentRow + 1

    # if no rows remain return currentTree
    if 1 not in rowsLeft:
        if yes > no:
            currentTree[position] = "yes"
        else:
            currentTree[position] = "no"
        return currentTree

    rootPosNeg = (yes, no)

    reset(training_set)
    if len(remainingAttributes) == 1:
        yes = 0
        no = 0
        currentRow = 0
        for line in training_set:

            if rowsLeft[currentRow] == 0:
                currentRow = currentRow + 1
                continue

            row = line.split(",")
            if int(row[remainingAttributes[0]]) == 1:
                yes = yes + 1
            else:
                no = no + 1

            currentRow = currentRow + 1

        if yes > no:
            currentTree[position] = "yes"
        else:
            currentTree[position] = "no"
        return currentTree

    elif entropy(rootPosNeg) == 0:
        if yes > no:
            currentTree[position] = "yes"
        else:
            currentTree[position] = "no"
        return currentTree

    currentTree[position] = findBest(remainingAttributes, rowsLeft)

    # copy of remaining attributes without the exhausted attribute
    attributeRemoved = remainingAttributes.copy()
    attributeRemoved.remove(currentTree[position])

    currentRow = 0
    yes = rowsLeft.copy()
    no = rowsLeft.copy()

    reset(training_set)
    for line in training_set:
        row = line.split(",")
        if rowsLeft[currentRow] == 0:
            currentRow = currentRow + 1
            continue
        if int(row[currentTree[position]]) == 1:
            no[currentRow] = 0
        elif int(row[currentTree[position]]) == 0:
            yes[currentRow] = 0
        currentRow = currentRow + 1

    subTree = buildTree(attributeRemoved, yes, currentTree, (position + 1) * 2 - 1, level + 1)
    for x in range(len(currentTree)):
        if currentTree[x] == "":
            currentTree[x] = subTree[x]
    subTree = buildTree(attributeRemoved, no, currentTree, (position + 1) * 2, level + 1)
    for x in range(len(currentTree)):
        if currentTree[x] == "":
            currentTree[x] = subTree[x]

    return currentTree


def buildTreeVI(remainingAttributes, rowsLeft, currentTree, position, level):
    reset(training_set)

    yes = 0
    no = 0
    currentRow = 0

    for line in training_set:

        if rowsLeft[currentRow] == 0:
            currentRow = currentRow + 1
            continue

        row = line.split(",")

        if int(row[yValue]) == 1:
            yes = yes + 1

        elif int(row[yValue]) == 0:
            no = no + 1

        currentRow = currentRow + 1

        # if no rows remain return currentTree
    if 1 not in rowsLeft:
        if yes > no:
            currentTree[position] = "yes"
        else:
            currentTree[position] = "no"
        return currentTree

    rootPosNeg = (yes, no)

    reset(training_set)
    if len(remainingAttributes) == 1:
        yes = 0
        no = 0
        currentRow = 0
        for line in training_set:

            if rowsLeft[currentRow] == 0:
                currentRow = currentRow + 1
                continue

            row = line.split(",")
            if int(row[remainingAttributes[0]]) == 1:
                yes = yes + 1
            else:
                no = no + 1

            currentRow = currentRow + 1

        if yes > no:
            currentTree[position] = "yes"
        else:
            currentTree[position] = "no"
        return currentTree

    elif vi(rootPosNeg) == 0:
        if yes > no:
            currentTree[position] = "yes"
        else:
            currentTree[position] = "no"
        return currentTree

    currentTree[position] = findBestVI(remainingAttributes, rowsLeft)

    # copy of remaining attributes without the exhausted attribute
    attributeRemoved = remainingAttributes.copy()
    attributeRemoved.remove(currentTree[position])

    currentRow = 0
    yes = rowsLeft.copy()
    no = rowsLeft.copy()

    reset(training_set)
    for line in training_set:
        row = line.split(",")
        if rowsLeft[currentRow] == 0:
            currentRow = currentRow + 1
            continue
        if int(row[currentTree[position]]) == 1:
            no[currentRow] = 0
        elif int(row[currentTree[position]]) == 0:
            yes[currentRow] = 0
        currentRow = currentRow + 1

    subTree = buildTreeVI(attributeRemoved, yes, currentTree, (position + 1) * 2 - 1, level + 1)
    for x in range(len(currentTree)):
        if currentTree[x] == "":
            currentTree[x] = subTree[x]
    subTree = buildTreeVI(attributeRemoved, no, currentTree, (position + 1) * 2, level + 1)
    for x in range(len(currentTree)):
        if currentTree[x] == "":
            currentTree[x] = subTree[x]

    return currentTree


def printTree(tree, node):
    if tree[node] == "yes":
        print(" 1", end='')
        return
    elif tree[node] == "no":
        print(" 0", end='')
        return

    line = ""
    for i in range(int(math.log((node + 1), 2) // 1)):
        line = line + "|\t"
    print("\n", line, attributes[tree[node]], " = 0 :", end='')
    printTree(tree, (node + 1) * 2)
    print("\n", line, attributes[tree[node]], " = 1 :", end='')
    printTree(tree, (node + 1) * 2 - 1)


def testTree(tree, test_set):
    correctPredictions = 0
    total = 0

    reset(test_set)
    for line in test_set:
        total = total + 1
        row = line.split(",")
        treeCursor = 0
        while True:
            if tree[treeCursor] == "yes":
                if int(row[yValue]) == 1:
                    correctPredictions = correctPredictions + 1
                break
            elif tree[treeCursor] == "no":
                if int(row[yValue]) == 0:
                    correctPredictions = correctPredictions + 1
                break
            elif int(row[int(tree[treeCursor])]) == 0:
                treeCursor = (treeCursor + 1) * 2
            elif int(row[int(tree[treeCursor])]) == 1:
                treeCursor = (treeCursor + 1) * 2 - 1
    return correctPredictions / total


def postPruning(tree):
    bestTree = tree


    for i in range(L):
        treeCopy = tree.copy()
        M = random.randint(1, K)
        for j in range(M):
            listForP = []
            position = 0
            N = 0
            for x in treeCopy:
                if x != "" and x != "yes" and x != "no":
                    N = N + 1
                    listForP.append(position)
                position = position + 1
            P = random.randint(1, N)
            yes = 0
            no = 0
            reset(training_set)
            for line in training_set:
                row = line.split(",")
                treeCursor = 0
                while True:
                    if treeCursor == listForP[P - 1]:
                        while True:
                            if tree[treeCursor] == "yes":
                                yes = yes + 1
                                break
                            elif tree[treeCursor] == "no":
                                no = no + 1
                                break
                            elif int(row[int(tree[treeCursor])]) == 0:
                                treeCursor = (treeCursor + 1) * 2
                            elif int(row[int(tree[treeCursor])]) == 1:
                                treeCursor = (treeCursor + 1) * 2 - 1
                    if tree[treeCursor] == "yes":
                        break
                    elif tree[treeCursor] == "no":
                        break
                    elif int(row[int(tree[treeCursor])]) == 0:
                        treeCursor = (treeCursor + 1) * 2
                    elif int(row[int(tree[treeCursor])]) == 1:
                        treeCursor = (treeCursor + 1) * 2 - 1

            if yes > no:
                treeCopy[P] = "yes"
            elif no >= yes:
                treeCopy[P] = "no"

        if testTree(treeCopy, validation_set) > testTree(tree, validation_set):
            bestTree = treeCopy

    return bestTree



rowsLeft = [1] * numberOfRows


remainingAttributes = [None] * 20
for x in range(20):
    remainingAttributes[x] = x

tree = buildTree(remainingAttributes, rowsLeft, [""] * 2 ** 20, 0, 0)
treeVI = buildTreeVI(remainingAttributes, rowsLeft, [""] * 2 ** 20, 0, 0)
pruned = postPruning(tree)
prunedVI = postPruning(treeVI)

if printOut:
    print("Information Gain Heuristic:\n\n")
    printTree(tree, 0)
    print("\n\n\n\nInformation Gain Heuristic - Post Pruning:\n\n")
    printTree(pruned, 0)
    print("\n\n\n\nVariance Impurity Heuristic\n\n")
    printTree(treeVI, 0)
    print("\n\n\n\nVariance Impurity Heuristic - Post Pruning\n\n")
    printTree(prunedVI, 0)

result.write(str(sys.argv))
result.write("\n\nig accuracy: ")
result.write(str(testTree(tree, test_set)))
result.write("\n\nvi accuracy: ")
result.write(str(testTree(treeVI, test_set)))
result.write("\n\npruned ig accuracy: ")
result.write(str(testTree(pruned, test_set)))
result.write("\n\npruned vi accuracy: ")
result.write(str(testTree(prunedVI, test_set)))
result.write("\n\n")
