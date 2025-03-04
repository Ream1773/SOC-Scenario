import subprocess as sp
import os
import re
import shutil

PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
# dir = r"C:\\Users\\raham\\OneDrive\\Desktop\\"
dir = r"C:\Users\Administrator\Desktop\\"


def func():
    files = list()
    for filename in os.listdir(dir):
        if re.search(r"dump", filename, re.IGNORECASE):
            files.append(filename)
            try:
                for i in range(len(files)):
                    print(files)
                    shutil.rmtree(r"{}{}".format(dir,files[i]), ignore_errors=True)
            except PermissionError as e:
                for i in range(len(files)):
                    os.remove(r"{}{}".format(dir,files[i]))

#func()

def func2():
    files_to_delete = []
    
    # Collect matching filenames
    for filename in os.listdir(dir):
        if "dump" in filename.lower():  # More efficient than regex here
            files_to_delete.append(os.path.join(dir, filename))  # Full path
        else:
            print("Files do not exist!\n")

    # Delete files and directories separately
    for file in files_to_delete:
        try:
            if os.path.isdir(file):  
                shutil.rmtree(file, ignore_errors=True)  # Delete directory
                print(f"[+] Deleted directory: {file}")
            elif os.path.isfile(file):
                os.remove(file)  # Delete file
                print(f"[+] Deleted file: {file}")
        except PermissionError as e:
            print(f"[!] Permission denied: {file} - {e}")

func2()