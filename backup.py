#!/usr/bin/env python3

import os
import sys
import json

depth = 0
maxDepth = 999
listedDirs = []
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'list.json')
spinner = ['|', '/', '-', '\\']
spinner_i = 0

def GetArg(i):
    if i < 0:
        if abs(i) >= len(sys.argv):
            return ""
        else:
            i = len(sys.argv) - abs(i)
    return sys.argv[i]

def Animation():
    global spinner
    global spinner_i
    global depth
    sys.stdout.write('\rSearching ' + spinner[spinner_i % len(spinner)])
    #i = depth
    #while i > 0:
    #    i -= 1
    #    sys.stdout.write(" ")
    #sys.stdout.write("X")
    sys.stdout.write("\r")
    sys.stdout.flush()
    spinner_i += 1

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
        return a[0: len(b)] == b
    return b[0: len(a)] == a

def FindFiles(path):
    global depth
    global listedDirs
    #depth
    depth = path.count('/') + path.count('\\')
    if depth > maxDepth:
        return
    
    #animation
    Animation()

    #search for file
    try:
        if os.path.isfile(os.path.join(path, ".backupinfo")):
            #print(11111)
            #check if path is already a prefix
            for name in listedDirs:
                if name == path:
                    print("=", path)
                    return
                elif CheckPrefix(name, path):
                    print("WARNING! Found recursive `.backupinfo` between", name, "and", path)
                    return
            
            print("+", path)
            listedDirs.append(path)
            #Stop searching
            return
    except Exception as e:
        print(f"Error accessing 1 {path}: {e}")

    #search in dirs inside
    try:
        for name in os.listdir(path):
            name = os.path.join(path, name)
            if os.path.isdir(name):
                #print(depth, name)
                FindFiles(name)
    except Exception as e:
        print(f"Error accessing {path}: {e}")

def CMD_Mark(path):
    LoadListDirs()
    path = os.path.abspath(path)
    FindFiles(path)
    SaveListedDirs()

def CMD_List():
    global listedDirs
    LoadListDirs()
    for name in listedDirs:
        print(name)

def CMD_Clear():
    global path
    if os.path.exists(path):
        os.remove(path)

def CMD_Backup(output):
    output

if __name__ == '__main__':
    #mark
    if GetArg(-3) == "mark":
        print("mark FOLDER_PATH MAX_DEPTH")
        maxDepth = int(GetArg(-1))
        CMD_Mark(GetArg(-2))
    elif GetArg(-2) == "mark":
        print("mark FOLDER_PATH")
        CMD_Mark(GetArg(-1))
    elif GetArg(-1) == "mark":
        print("mark")
        CMD_Mark(".")
    #list
    elif GetArg(-1) == "list":
        print("list")
        CMD_List()
    #clear
    elif GetArg(-1) == "clear":
        print("clear")
        CMD_Clear()
    #backup
    elif GetArg(-2) == "backup":
        print("backup OUTPUT_PATH")
        CMD_Backup(sys.argv[-1])
    #help
    else:
        print("Commands:")
        print("")
        print("mark")
        print("mark FOLDER_PATH")
        print("mark FOLDER_PATH MAX_DEPTH")
        print("")
        print("list")
        print("")
        print("clear")
        print("")
        print("backup OUTPUT_PATH")
        print("")
