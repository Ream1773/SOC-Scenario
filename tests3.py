import subprocess as sp
import os
import re
import shutil

PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
dir = r"C:\\Users\\raham\\OneDrive\\Desktop\\"

def func():
    #output = str(sp.check_output([PS, "-Command", f"ls {dir}"]))
    pattern = r".\*dump.*"

    for filename in os.listdir(dir):
        if re.search(pattern, filename):
            print(filename)

func()