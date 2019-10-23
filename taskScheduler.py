import pickle
import sys

class Task:
    def __init__(self, taskName):
        self.name = taskName
        self.child = []
        self.parent = None

    def __str__(self):
        return stringConstructer(self, 0)
    
    def add(self, childTask):
        if childTask.name not in nameSet:
            self.child.append(childTask)
            nameSet[childTask.name] = childTask
            childTask.parent = self
        else:
            print("already have this task")
    
    def addTaskName(self, subtaskName):
        task = Task(subtaskName)
        self.add(task)
    
    def removeTask(self, childTask):
        nameSet.pop(childTask.name, None)
        self.child.remove(childTask)

ROOT = Task('')
nameSet = {}
SAVE_FILE = 'tasks.node'


def generateNameSet(task):
    for child in task.child:
        if child.name not in nameSet:
            nameSet[child.name] = child
            generateNameSet(child)
        else:
            print('error: duplicated name while generating nameset')
    
def flush():
    """
    flashes the saved file to empty
    """
    ROOT = Task('')
    nameSet = {}
    with open(SAVE_FILE, 'wb') as taskFile:
        pickle.dump(ROOT, taskFile)
    generateNameSet(ROOT)

def stringConstructer(task, layer):
    string = task.name + '\n'
    for subtasks in task.child:
        string += layer * '   ' + '- ' + stringConstructer(subtasks, layer+1)
    return string

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
    if name not in nameSet:
        print('task name not exist')
    else:
        for child in nameSet[name].child:
            removeName(child.name)
        parent = nameSet[name].parent
        parent.removeTask(nameSet[name])

def addTaskName(name):
    ROOT.addTaskName(name)

def addSubTask(*argv):
    try:
        node = nameSet[argv[0]]
        node.addTaskName(argv[1])
    except Exception:
        print('Incorrect Inputs!')

def showTree():
    print(ROOT)

def getFunction(funcName, funcDict):
    return funcDict[funcName.lower()]

def main(argv):
    global ROOT, nameSet
    funcDict = {'load': load, 'add': addTaskName, 'addsubtask': addSubTask, 'remove': removeName, 'save': save, 'show': showTree}
    func = getFunction(argv[0], funcDict)
    func(*(argv[1:]))

if __name__== "__main__":
    argv = sys.argv[1:]
    load()
    main(argv)
    save()
    #flush()