import pickle
import sys

ROOT = None
SAVE_FILE = 'tasks.node'

def stringConstructer(task, layer):
    string = task.name + '\n'
    for subtasks in task.child:
        string += layer * ' ' + '-' + stringConstructer(subtasks, layer+1)
    return string

def save():
    with open(SAVE_FILE, 'wb') as taskFile:
        pickle.dump(ROOT, taskFile)

def load():
    with open(SAVE_FILE, 'rb') as taskFile:
        ROOT = pickle.load(taskFile)
class Task:
    def __init__(self, taskName):
        self.name = taskName
        self.child = []

    def __str__(self):
        return stringConstructer(self, 0)
    
    def add(self, childTask):
        self.child.append(childTask)
    
    def addTaskName(self, subtaskName):
        task = Task(subtaskName)
        self.child.add(task)

def main():
    

if __name__== "__main__":
  main()