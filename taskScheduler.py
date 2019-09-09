ROOT = None
def stringConstructer(task, layer):
    string = task.name + '\n'
    for subtasks in task.child:
        string += layer * ' ' + '-' + stringConstructer(subtasks, layer+1)
    return string

def getFeaturesNode(node):
    string = node.name + ','
    for child in node.child:
        string += child.name + ','
    return string

def getFeatures(node, string):
    stringNode = getFeaturesNode(node)
    string[0] += stringNode + '\n'
    if node.child == []:
        return
    for child in node.child:
        getFeatures(child, string)

def save(ROOT):
    file = open("./saved.bin", "w")
    string = ['']
    getFeatures(ROOT, string)
    file.write(string[0])
    file.close()

def load(ROOT):
    file = open("./saved.bin", "rb")
    ROOT = file.read()
    file.close()

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
    task1 = Task("task1")
    task2 = Task("task2")
    task3 = Task("task1.1")
    ROOT = Task("")
    task1.add(task3)
    ROOT.add(task1)
    ROOT.add(task2)
    print(ROOT)
    save(ROOT)

if __name__== "__main__":
  main()