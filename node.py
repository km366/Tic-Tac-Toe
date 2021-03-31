class Node:
    def __init__(self,data):
        self._data = data
        self._children = []
        self._score = None
        self._index = None
    def getChildren(self):
        return self._children
    def getIndex(self):
        return self._index
    def getData(self):
        return self._data
    def getScore(self):
        return self._score
    def setIndex(self, index):
        self._index = index
    def setChild(self,child):
        self._children.append(child)
    def setData(self,data):
        self._data = data
    def setScore(self, score):
        self._score = score
    def __str__(self):
        return str(self.getData())
