import os
import subprocess as sp
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import ctypes
import sys


# Check if user running is NT/AUTHORITY | Administrator
def is_admin():
    '''Returns True if script is running with administrator privileges.'''

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

        

def get_desktop_path(): # DOES NOT WORK:: Need to fix parsing of environment vars and getting absolute Desktop path for user.
        '''Get absloute Desktop path'''

        # Check OneDrive first
        if "ONEDRIVE" in os.environ:
            desktop_path = os.path.join(os.environ["ONEDRIVE"], "\Desktop")
        else:
            desktop_path = os.path.join(os.environ["USERPROFILE"], "\Desktop")
        
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
    

def get_os():
    '''Finds whether the target is a Domain Controller or Endpoint'''

    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")

    output = sp.run([PS, "-Command",'systeminfo /fo csv | ConvertFrom-Csv | select "OS Name" | Format-List'], shell=True, capture_output=True, text=True)
    if "Server" in output.stdout.lower():
        return True
    