class Node:
    def __init__(self,data):
        self._data = data
        self._children = []
        self._win = None
        self._totalWin = None
        self._index = None
    def getChildren(self):
        return self._children
    def getIndex(self):
        return self._index
    def getData(self):
        return self._data
    def getWin(self):
        return self._win
    def getTotalWins(self):
        return self._totalWin
    def setIndex(self, index):
        self._index = index
    def setChild(self,child):
        self._children.append(child)
    def setData(self,data):
        self._data = data
    def setWin(self, win):
        self._win = win
    def setTotalWin(self, total):
        self._totalWin = total
    def __str__(self):
        return str(self.getData())



class Tree:
    def __init__(self):
        self._head = None
    def setHead(self,head):
        self._head = head
    def traverseTree(self):
        self.tt(self._head)
    def getHead(self):
        return self._head
    def getHeight(self, node):
        if len(node.getChildren()) == 0:
            return 0
        return 1 + self.getHeight(node.getChildren()[0])
    def tt(self,node):
        if len(node.getChildren()) == 0:
            return
        for i in node.getChildren():
            print(i.getWin())
            self.tt(i)
    def getNumberOfChildren(self):
        return 1+self.getNumOfChildren(self._head)
    def getNumOfChildren(self, node):
        if len(node.getChildren()) == 0:
            return 0
        sum = len(node.getChildren())
        for n in node.getChildren():
            sum += self.getNumOfChildren(n)
        return sum
    def setTotalWins(self, node):
        if len(node.getChildren()) == 0:
            node.setTotalWin(node.getWin())
            return node.getWin()
        totalWin = node.getWin()
        for n in node.getChildren():
            totalWin += self.setTotalWins(n)
        node.setTotalWin(totalWin)
        return totalWin
