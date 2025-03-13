import os
import subprocess as sp
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style
import ctypes
import sys
import winreg


# Check if user running is NT/AUTHORITY | Administrator
def _is_admin():
    '''Returns True if script is running with administrator privileges.'''

    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def _run_as_admin():
    '''Relaunch the script with admin privileges and keep the output visible'''

    script = os.path.abspath(sys.argv[0])  # Get absolute path of the script
    params = " ".join([f'"{arg}"' for arg in sys.argv[1:]])  # Properly format arguments
    python_exe = sys.executable  # Gets the correct Python interpreter

    # Relaunch using cmd.exe so the window stays open
    cmd = f'start cmd /k "{python_exe} \"{script}\" {params}"'
    
    # Use ShellExecute to elevate privileges
    ctypes.windll.shell32.ShellExecuteW(None, "runas", "cmd.exe", f"/c {cmd}", None, 1)
    
    sys.exit()


def _get_desktop_path():
    '''Get absloute Desktop path'''
    
    env_vars = {key.lower(): os.environ[key] for key in os.environ} # Get environment variables in a case-insensitive way
    
    # Check OneDrive (case-insensitive, multiple possible names)
    for key in ["onedrive", "onedrivecommercial", "onedriveconsumer"]:
        if key in env_vars:
            desktop_path = os.path.join(env_vars[key], "Desktop")
        if os.path.exists(desktop_path):
            final_path = desktop_path + '\\'
            return final_path

    # Fallback to USERPROFILE
    if "userprofile" in env_vars:
        desktop_path = os.path.join(env_vars["userprofile"], "Desktop")
        if os.path.exists(desktop_path):
            final_path = desktop_path + '\\'
            return final_path

    # Check Windows Registry for Desktop location (supports localized names)
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Microsoft\Windows\CurrentVersion\Explorer\User Shell Folders") as reg_key:
            desktop_path, _ = winreg.QueryValueEx(reg_key, "Desktop")
            desktop_path = os.path.expandvars(desktop_path)  # Expand %USERPROFILE% if present
            if os.path.exists(desktop_path):
                final_path = desktop_path + '\\'
                return final_path
    except Exception:
        pass  # If registry access fails, continue to manual input

    # Manual input fallback
    while True:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Could not automatically detect Desktop path.")
        user_input = input(f"{Fore.LIGHTBLUE_EX}[*]{Style.RESET_ALL} Enter the correct Desktop path manually: ").strip()

        if os.path.exists(user_input):
            if user_input[-1] != "\\":
                user_input = user_input + "\\"
                return user_input
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} The entered path does not exist. Please try again.")
    

def _get_os():
    '''Finds whether the target is a Domain Controller or Endpoint'''

    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")

    output = sp.run([PS, "-Command",'Get-CimInstance Win32_OperatingSystem | Select-Object Caption'], shell=True, capture_output=True, text=True)
    if "server" in output.stdout.lower():
        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Detected Windows Server:: Running AD Scenario\n\n")
        return True
    else:
        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Detected Endpoint:: Running EP Scenario\n\n")
        return False