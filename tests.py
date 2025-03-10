# Test files before adding to working script
import os
import subprocess as sp
from zipfile import ZipFile
import shutil
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
from time import sleep


colorama_init()

PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
# dir = os.path.expandvars(r"%USERPROFILE%\Desktop\\")
desktopPath = os.path.expandvars(r"%ONEDRIVE%\\Desktop\\")
mimikatz = r"https://github.com/ParrotSec/mimikatz/archive/refs/heads/master.zip"
powersploit = r"https://github.com/PowerShellMafia/PowerSploit/archive/refs/heads/master.zip"
mimikatz_zip = mimikatz.split("heads/")[1]
powersploit_zip = powersploit.split("heads/")[1]

def _setup():
    paths_ = list()
    os.makedirs(desktopPath + "mimikatz", exist_ok=True)
    os.makedirs(desktopPath + "Powersploit", exist_ok=True)
    paths_.append(os.path.join(f"{desktopPath}", "mimikatz"))
    paths_.append(os.path.join(f"{desktopPath}", "Powersploit"))
    return paths_

def _check_cleaned():
    files_to_delete = [os.path.join(desktopPath, f) for f in os.listdir(desktopPath) if any(sub in f.lower() for sub in ["mimikatz", "powersploit", "master"])]
    print(files_to_delete)

    if not files_to_delete:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} No files to delete!\n")
        return False
        
        # Flags for proof of deletion

    sf_file = False 
    sf_dir = False

        # Delete files and directories separately
    while not sf_dir and not sf_file:
        for file in files_to_delete:
            try:
                if os.path.isdir(file): # Check if object is a directory
                    shutil.rmtree(file, ignore_errors=True)  # Delete directory
                    sleep(1)
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Deleted directory: {file}\n")
                    sf_dir = True

                elif os.path.isfile(file): # Check if objet is file
                    os.remove(file)  # Delete file
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Deleted file: {file}\n")
                    sf_file = True

            except PermissionError as e:
                print(f"{Fore.RED}[!] Permission denied: {file} - {e}{Style.RESET_ALL}\n")

def main():
    #for paths in _setup():
    paths = _setup()
    sp.run([PS, "-Command", f"""Invoke-WebRequest {mimikatz} -OutFile {desktopPath}{mimikatz_zip}"""] ,shell=True, text=True)
    sp.run([PS, "-Command",f"""Invoke-WebRequest {powersploit} -OutFile {desktopPath}{powersploit_zip}"""] ,shell=True, text=True)
    mimikatz_zip_path = os.path.join(desktopPath, f"{mimikatz_zip}")
    powersploit_zip_path = os.path.join(desktopPath, f"{powersploit_zip}")

    # Unzip file
    try:
        with ZipFile(mimikatz_zip_path, "r") as mimiObject:
            mimiObject.extractall(path=paths[0])
    except OSError as e:
        print("Mimikatz was blocked by the security solution.\n")
    
    try:
        with ZipFile(powersploit_zip_path, "r") as powerSObject:
            powerSObject.extractall(path=paths[1])
    except OSError as e:
        print("Powersploit was blocked by the security solution.\n")    

    if _check_cleaned():
        print("Files were deleted successfully!\n")

    
def cs_commands():
    commands = ["crowdstrike_test_low", "crowdstrike_test_medium", "crowdstrike_test_high", "crowdstrike_test_critical"]
    for cmd in commands:
        try:
            print(f"\n[+] Running: {cmd}\n ")
            result = sp.run(cmd, shell=True, capture_output=True, text=True)

            if result.stdout:
                print(result.stdout)

        except FileNotFoundError as e:
            print(f"[-] Command not found.\n{cmd}\n")


if __name__ == '__main__':
    cs_commands()