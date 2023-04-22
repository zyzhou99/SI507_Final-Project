import json

class TreeNode():
  def __init__(self, groups=[], left=None, right=None, reipes=[]):
    self.groups = groups  # for leaf nodes, len(groups) == 1
    self.left = left
    self.right = right
    self.reipes = reipes  # only leaf nodes have this attribute

treeGroups = {
    #'mealType': ["lunch/dinner","lunch","dinner","breakfast"],
    'cuisineType': ["american","french","eastern europe","mediterranean","chinese","japanese","italian"],
    'calories': ['0-350','350-700','700-1000','1000-1300','1300-10000']
}

def buildTree(treeType, groups):
    with open('./json/cache.json') as file:
        cache = json.load(file)
    def buildHelper(curGroups,treeType):

        mid = len(curGroups) // 2
        if len(curGroups) > 1:
            left = buildHelper(curGroups[:mid],treeType)
            right = buildHelper(curGroups[mid:],treeType)
        else:
            left = right = None
        root = TreeNode(curGroups, left, right)

        if len(curGroups) == 1:
            now_reipes=[]
            for ca in cache:
               if treeType=="calories":
                   if float(curGroups[0].split('-')[0]) <=float(cache[ca].get(treeType))<float(curGroups[0].split('-')[1]):
                       now_reipes.append(ca)
               elif cache[ca].get(treeType)[0]==curGroups[0]:
                   now_reipes.append(ca)
            root.reipes = now_reipes
        return root
    return buildHelper(groups,treeType)

def serialize(cur):
    if cur.left is None and cur.right is None:
        return {
            'nodeType': 'leaf', 
            'groups': cur.groups, 
            'reipes': cur.reipes
        }
    else:
        return {
            'nodeType': 'internal', 
            'groups': cur.groups, 
            'left': serialize(cur.left),
            'right': serialize(cur.right)
        }

def saveTree(root, treeFile):
    treeDict = serialize(root)
    with open(treeFile, 'w') as file:
        json.dump(treeDict, file)

def deserialize(treeDict):
    if treeDict['nodeType'] == 'leaf':
        return TreeNode(treeDict['groups'], None, None, treeDict['reipes'])
    else:
        return TreeNode(treeDict['groups'], deserialize(treeDict['left']), deserialize(treeDict['right']))



def loadTree(treeFile):
    with open(treeFile) as file:
        tree = json.load(file)
    return deserialize(tree)

def add():
    for treeType, groups in treeGroups.items():
        root = buildTree(treeType, groups)
        saveTree(root, './json/{}.json'.format(treeType))

def search(self,value):
    cur = self
    cur2=self
    while cur != None:
        print(cur.groups)
        if cur.groups == [value]:
            return cur
        else:
            cur=cur.left

        if cur2.groups==[value]:
            return cur2
        else:
            cur2=cur2.right

    return None


def FindNode(self, x):
    return _FindNode1(self,self, x)

def _FindNode1(self, t, value):
    if t == None:
        return None
    elif t.groups == [value.lower()]:
        return t
    else:
        p = _FindNode1(t.left,t.left, value)
    if p != None:
        return p
    else:
        return _FindNode1(t.right,t.right, value)


def main():
    for treeType, groups in treeGroups.items():
        root = buildTree(treeType, groups)
        saveTree(root, './json/{}.json'.format(treeType))

if __name__ == '__main__':
    main()