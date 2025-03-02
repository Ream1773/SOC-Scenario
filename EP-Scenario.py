import subprocess
from time import sleep
import os
#import re
#import sys


class EPScenario:
    def __init__(self, ps, cmd):
        self.PS = ps
        self.CMD = cmd

    def _get_user(self):
        _user = subprocess.check_output([PS, "-Command", "whoami"], text=True)
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
                # EICAR file not recognized as malicious by Windows?
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
        subprocess.check_output([self.CMD, "-Command", ])
        # Generate CrowdStrike alerts via cmd in proj-notes.txt
        pass

    def dump_lsass(self):
        # Use procdump (sysInternals) to dump lsass.exe
        pass

    def _check_S_solutions(self):
        # Check whether cisco AMP, Symantec, or CrowdStrike is present on the EP.
        pass

    def download_files(self):
        # Based on the previous function, define ways to extract said files mentioned in notes.
        pass

    def surf_limits(self):
        # Check default browser, 
        pass


if __name__ == '__main__':
    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
    CMD = os.path.expandvars(r"%SystemRoot%\system32\cmd.exe")
    EP_obj = EPScenario(ps=PS,cmd=CMD).make_Eicar()