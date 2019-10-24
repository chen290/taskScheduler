import pickle
import sys
from fuzzywuzzy import process

# ========================================================= Class Helper Functions ==================================================================================
def stringConstructer(task, layer):
    string = task.name + '\n'
    for subtasks in task.child:
        string += layer * '   ' + '- ' + stringConstructer(subtasks, layer+1)
    if not task.child:
        string += '\n'
    return string

def stdAddFunc(dic, paramName, data):
    dic[paramName] = data
# ========================================================== Class =================================================================================================#
class Task:
    def __init__(self, taskName):
        self.name = taskName
        self.child = []
        self.parent = None
        self.addiParam = {}

    def __str__(self):
        return stringConstructer(self, 0)
    
    def add(self, childTask):
        if (childTask.name).lower() not in nameSet:
            self.child.append(childTask)
            nameSet[(childTask.name).lower()] = childTask
            childTask.parent = self
        else:
            print("already have this task")
    
    def addTaskName(self, subtaskName):
        task = Task(subtaskName)
        self.add(task)
    
    def updateTaskNameWithAddParam(self, subtaskName, paramName, data, initializer=None, adding=None):
        task = nameSet[(subtaskName.name).lower()]
        if paramName not in task.addiParam:
            task.addiParam[paramName] = initializer
        if not adding:
            task.addiParam[paramName] = data
    
    def removeTask(self, childTask):
        nameSet.pop((childTask.name).lower(), None)
        self.child.remove(childTask)
# ======================================================= End of Class ==================================================================================================#
ROOT = Task('')
nameSet = {}
SAVE_FILE = 'tasks.node'
# ======================================================= Helper Functions ==============================================================================================
def generateNameSet(task):
    for child in task.child:
        if child.name not in nameSet:
            nameSet[(child.name).lower()] = child
            generateNameSet(child)
        else:
            print('error: duplicated name while generating nameset')
    

def getFunction(funcName, funcDict):
    return funcDict[funcName.lower()]

def isCorrect(lst):
    return lst[0][1] >= 80 and (lst[0][1] - lst[1][1] > 10 or lst[0][1] == 100)

def getWord(string, lst):
    tlst = process.extract(string, lst, limit = 2)
    if isCorrect(tlst):
        return tlst[0][0]
    else:
        return None

# ====================================================== User Interact functions =============================================================================================
def flush():
    """
    flashes the saved file to empty
    """
    ROOT = Task('')
    nameSet = {}
    with open(SAVE_FILE, 'wb') as taskFile:
        pickle.dump(ROOT, taskFile)
    generateNameSet(ROOT)

def save():
    global ROOT, nameSet
    with open(SAVE_FILE, 'wb') as taskFile:
        pickle.dump(ROOT, taskFile)

def load():
    global ROOT, nameSet
    try:
        with open(SAVE_FILE, 'rb') as taskFile:
            ROOT = pickle.load(taskFile)
        generateNameSet(ROOT)
    except Exception:
        print('file not found')
        ROOT = Task('')
        nameSet = {}

def removeName(name):
    name = getWord(name, nameSet.keys())
    if not name:
        print('task name not exist')
    else:
        for child in nameSet[name].child:
            removeName(child.name)
        parent = nameSet[name].parent
        parent.removeTask(nameSet[name])

def addTaskName(name):
    ROOT.addTaskName(name)

def addSubTask(*argv):
    name = getWord(argv[0], nameSet.keys())
    if name:
        node = nameSet[name]
        node.addTaskName(argv[1])
    else:
        print('Incorrect Inputs!')

def showTree():
    print(ROOT)

def addTimeLine(*argv):
    start = argv[0]
    end = argv[1]

def rank(*argv):
    name = getWord(argv[0], nameSet.keys())
    if name:
        node = nameSet[name]
        rank = int(argv[1])
        parent = node.parent
        index = (parent.child).index(node)       
        if rank-1 <= index:
            index += 1
            rank -= 1
        parent.child.insert(rank, node)
        (parent.child).pop(index)
    else:
        print('Incorrect task name!')

# ====================================================================================================================================================================

def main(argv):
    global ROOT, nameSet
    funcDict = {'load': load, 'add': addTaskName, 'addsubtask': addSubTask, 'remove': removeName, 'save': save, 'show': showTree, 'rank': rank}
    if argv[0].lower() == 'help':
        print("these are the commands")
        print(list(funcDict.keys()))
        return
    funcName = getWord(argv[0], funcDict.keys())
    if funcName:
        func = getFunction(funcName, funcDict)
        func(*(argv[1:]))
    else:
        print('function name not found')

if __name__== "__main__":
    argv = sys.argv[1:]
    load()
    main(argv)
    save()
    #flush()