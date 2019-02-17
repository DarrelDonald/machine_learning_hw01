loadTree = open("decisiontree1result.txt")
tree = loadTree.readline().split(",")
tree.remove('')

test_set = open("data_sets1/test_set.csv")

attributes = test_set.readline().split(",")

yValue = 20

correctPredictions = 0

for line in test_set:
    row = line.split(",")
    treeCursor = 0
    while True:
        if tree[treeCursor] == " yes":
            if int(row[yValue]) == 1:
                correctPredictions = correctPredictions + 1
            break
        elif tree[treeCursor] == " no":
            if int(row[yValue]) == 0:
                correctPredictions = correctPredictions + 1
            break
        elif int(row[int(tree[treeCursor])]) == 0:
            treeCursor = (treeCursor + 1) * 2
        elif int(row[int(tree[treeCursor])]) == 1:
            treeCursor = (treeCursor + 1) * 2 - 1

print(correctPredictions/2000)
"""
for x in tree:
    print(x)
"""