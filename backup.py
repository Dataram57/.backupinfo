#!/usr/bin/env python3

import os
import sys
import json
import shutil

subDepth = 0
depth = 0
maxDepth = 999
listedDirs = []
path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'list.json')
logpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs.txt')
spinner = ['|', '/', '-', '\\']
spinner_i = 0

def copy_entire_folder_with_progress(src_folder, dst_parent_folder):
    try:
        dst_folder = os.path.join(dst_parent_folder, os.path.basename(src_folder))

        # Remove existing destination if it exists
        try:
            if os.path.exists(dst_folder):
                shutil.rmtree(dst_folder)
        except:
            Log("Failed to remove copy:", src_path, dst_folder)

        # Collect all files to copy
        files_to_copy = []
        try:
            for root, dirs, files in os.walk(src_folder):
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path, src_folder)
                    files_to_copy.append((full_path, os.path.join(dst_folder, relative_path)))
        except:
            Log("Failed to explore:", src_path, dst_folder)

        total_files = len(files_to_copy)
        copied_files = 0

        for src_path, dst_path in files_to_copy:
            #
            try:
                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
            except:
                Log("Failed to make dirs:", src_path, dst_folder)
            #
            try:
                shutil.copy2(src_path, dst_path)
            except:
                Log("Failed to copy:", src_path, dst_folder)
            #
            copied_files += 1
            percent = (copied_files / total_files) * 100
            print(f"\n\rCopying ({copied_files}/{total_files}) [{percent:.2f}%] {src_path} ", end='')

        print("\nCopy complete.")

    except Exception as e:
        print(f"\nError accessing {src_folder}: {e}")

def Log(message):
    global logpath
    try:
        with open(logpath, 'a') as f:
            f.write(message + '\n')
    except Exception as e:
        print("Couldn't log,", message)

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
    depth = path.count('/') + path.count('\\') - subDepth
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
    global subDepth
    subDepth = path.count('/') + path.count('\\')
    print("Scanning", path)
    FindFiles(path)
    SaveListedDirs()

def CMD_List():
    global listedDirs
    LoadListDirs()
    for name in listedDirs:
        print(name)

def CMD_Logs():
    global logpath
    try:
        with open(logpath, 'r') as f:
            print(f.read())
    except FileNotFoundError:
        print("Log file not found.")

def CMD_ClearList():
    global path
    if os.path.exists(path):
        os.remove(path)

def CMD_ClearLogs():
    global logpath
    if os.path.exists(logpath):
        os.remove(logpath)

def CMD_Clear():
    CMD_ClearList()
    CMD_ClearLogs()

def CMD_Backup(output):
    global listedDirs
    LoadListDirs()
    output = os.path.abspath(output)
    print("")
    print("Backup will be done at", output)
    print("It is recommended to format this partition earlier for faster writing.")
    print("")
    if input("Type y to continue: ") != "y":
        return
    print("")
    print("Starting copying")
    print("")
    for name in listedDirs:
        print(name)
        copy_entire_folder_with_progress(name, output)


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
    #logs
    elif GetArg(-1) == "logs":
        print("logs")
        CMD_Logs()
    #clear
    elif GetArg(-2) == "clear":
        if GetArg(-1) == "list":
            print("clear list")
            CMD_ClearList()
        elif GetArg(-1) == "logs":
            print("clear logs")
            CMD_ClearLogs()
    elif GetArg(-1) == "clear":
        print("clear")
        CMD_Clear()
    #backup
    elif GetArg(-2) == "backup":
        print("backup OUTPUT_PATH")
        CMD_Backup(sys.argv[-1])
    #help
    else:
        print("\nmark - scans the current directory to find and save paths of directories with .backupinfo files" +"\nmark FOLDER_PATH - scans this FOLDER_PATH to find and save paths of directories with .backupinfo files" + "\nmark FOLDER_PATH MAX_DEPTH - scans this FOLDER_PATH to find and save paths of directories with .backupinfo files, with a max depth scan equal to MAX_DEPTH." + "\n" +"\nlist - lists saved paths with .backupinfo files" + "\n" +"\nlogs - prints logs" +"\n" +"\nclear - clears the list and logs" + "\nclear list - clears the list" + "\nclear logs - clears logs" +"\n" +"\nbackup OUTPUT_PATH - backup directories from the list with paths to them into the OUTPUT_PATH")
        print("")
    #key
    input("Press Enter to continue...")

