import os
import sys
import json

depth = 0
listedDirs = []
path = 'list.json'

def SaveListedDirs():
    global listedDirs
    global path
    try:
        with open(path, 'w') as f:
            json.dump(listedDirs, f)
    except Exception as e:
        print(f"Error accessing {path}: {e}")

def LoadListDirs():
    global listedDirs
    global path
    try:
        with open(path, 'r') as f:
            listedDirs = json.load(f)
    except Exception as e:
        print(f"Error accessing {path}: {e}")


def CheckPrefix(a, b):
    if len(a) > len(b):
        return a[0, len(b)] == b
    return b[0, len(a)] == a

def FindFiles(path):
    global depth
    global listedDirs
    depth += 1
    #search for file
    try:
        if os.path.isfile(os.path.join(path, ".backupinfo")):
            #check if path is already a prefix
            for name in listedDirs:
                if CheckPrefix(name, path):
                    print("WARNING! Found recursive `.backupinfo` between", name, "and", path)
                    return
            
            listedDirs.append(path)
            #Stop searching
            #return
    except Exception as e:
        print(f"Error accessing {path}: {e}")

    #search in dirs inside
    try:
        for name in os.listdir(path):
            name = os.path.join(path, name)
            if os.path.isdir(name):
                #print(depth, name)
                FindFiles(name)
    except Exception as e:
        print(f"Error accessing {path}: {e}")
    depth -= 1

def CMD_Check(path):
    LoadListDirs()
    FindFiles(path)
    SaveListedDirs()


def CMD_List():
    global listedDirs
    LoadListDirs()
    for name in listedDirs:
        print(name)

if __name__ == '__main__':
    if sys.argv[-2] == "check":
        CMD_Check(sys.argv[-1])
    elif sys.argv[-1] == "check":
        CMD_Check(".")
    elif sys.argv[-1] == "list":
        CMD_List()
