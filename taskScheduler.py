import pickle
import sys

ROOT = None
nameSet = {}
SAVE_FILE = 'tasks.node'
NAME_FILE = 'tasks.name'

def stringConstructer(task, layer):
    string = task.name + '\n'
    for subtasks in task.child:
        string += layer * ' ' + '-' + stringConstructer(subtasks, layer+1)
    return string

def save():
    with open(SAVE_FILE, 'wb') as taskFile:
        pickle.dump(ROOT, taskFile)
    with open(NAME_FILE, 'wb') as nameFile:
        pickle.dump(nameSet, nameFile)

def load():
    with open(SAVE_FILE, 'rb') as taskFile:
        ROOT = pickle.load(taskFile)
    with open(NAME_FILE, 'rb') as nameFile:
        nameSet = pickle.load(nameFile)
class Task:
    def __init__(self, taskName):
        self.name = taskName
        self.child = []

    def __str__(self):
        return stringConstructer(self, 0)
    
    def add(self, childTask):
        self.child.append(childTask)
        if childTask not in nameSet:
            nameSet.add(childTask)
    
    def addTaskName(self, subtaskName):
        task = Task(subtaskName)
        self.child.add(task)

def main():
    try:
        load()
    except Exception:
        ROOT = Task('')
    if (sys.argv[1] == 'add'):
        ROOT.addTaskName(sys.argv[2])
    if (sys.argv[1] == 'addSubTask'):
        node = nameSet[sys.argv[2]]
        node.addTaskName(sys.argv[4])
    if (sys.argv[1] == 'show'):
        print(ROOT)
    save()


if __name__== "__main__":
  main()