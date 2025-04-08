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
    '''Get absolute Desktop path or fallback to AppData'''
    
    try:
        env_vars = {key.lower(): os.environ[key] for key in os.environ}
        
        # Try Desktop first
        for key in ["onedrive", "onedrivecommercial", "onedriveconsumer"]:
            if key in env_vars:
                desktop_path = os.path.join(env_vars[key], "Desktop")
                if os.path.exists(desktop_path):
                    final_path = desktop_path + '\\'
                    return final_path

        if "userprofile" in env_vars:
            desktop_path = os.path.join(env_vars["userprofile"], "Desktop")
            if os.path.exists(desktop_path):
                final_path = desktop_path + '\\'
                return final_path

        # Fallback to AppData if Desktop fails
        appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'SOC_Test')
        os.makedirs(appdata_path, exist_ok=True)
        return appdata_path + '\\'
        
    except Exception as e:
        # Ultimate fallback to AppData
        appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'SOC_Test')
        os.makedirs(appdata_path, exist_ok=True)
        return appdata_path + '\\'


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

# def _self_delete(path):
#     exe_path = path
#     print(f"Deleting {exe_path}\n")

#     delete_cmd = f'''
#     cmd /c ping 127.0.0.1 -n 70 > nul && del "{exe_path}"
#     '''

#     sp.Popen(delete_cmd, shell=True,creationflags=sp.CREATE_NO_WINDOW)

def _self_delete():
    '''Deletes the executable and program-specific files/folders after completion.'''
    try:
        # Get the path of the current executable
        exe_path = sys.executable if getattr(sys, 'frozen', False) else sys.argv[0]
        
        # Get program-specific paths to clean up
        appdata_path = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'SOC_Test')
        specific_paths = [
            appdata_path,
            os.path.join(appdata_path, "ProcDump"),
            os.path.join(appdata_path, "Dump"),
            os.path.join(appdata_path, "mimikatz"),
            os.path.join(appdata_path, "Powersploit"),
            os.path.join(appdata_path, "Logs"),
            os.path.join(appdata_path, "PowerView.ps1"),
            os.path.join(appdata_path, "EICAR.txt"),
            os.path.join(appdata_path, "Procdump.zip"),
            os.path.join(appdata_path, "Mimikatz.zip"),
            os.path.join(appdata_path, "Powersploit.zip")
        ]
        
        # Create a batch file to delete everything
        batch_path = os.path.join(os.path.dirname(exe_path), "delete_me.bat")
        with open(batch_path, "w") as f:
            f.write(f"""
@echo off
:loop
taskkill /F /IM "{os.path.basename(exe_path)}" >nul 2>&1
del "{exe_path}" >nul 2>&1
if exist "{exe_path}" goto loop

:clean_files
{chr(10).join(f'if exist "{path}" {"rd /s /q" if os.path.isdir(path) else "del"} "{path}" >nul 2>&1' for path in specific_paths)}

del "%~f0"
""")
        
        # Run the batch file in a new process
        sp.Popen(f'start /b cmd /c "{batch_path}"', shell=True, creationflags=sp.CREATE_NO_WINDOW)
        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Self-deletion and cleanup initiated.\n")
        
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Error during self-deletion: {e}\n")