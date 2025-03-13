import os
import subprocess as sp
from time import sleep
import re
import sys
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style


class ADScenario:
    def __init__(self, PS):
        self.PS = PS
        self.TASK_NAME = "TestTask"
        self.NOTEPAD_PATH = r"C:\Windows\System32\\notepad.exe"
        colorama_init()
    
    def _check_AD_module(self):
        '''Check whether the ActiveDirectory Module is installed & installs if it isn't.'''

        try:
            output = sp.check_output([self.PS,"-Command", "Get-Module -ListAvailable -Name ActiveDirectory"], text=True)

            match = re.search(r"\bActiveDirectory\b", output)
            if match:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Module found: {match.group(0)}\n")
            
            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Module not found.\nInstalling....")
                sp.call([self.PS, "-Command", "Install-WindowsFeature -Name RSAT-AD-PowerShell"])
                sleep(2)
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Module installed!\n")

        except sp.CalledProcessError as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Command failed with return code {e.returncode}\nExiting script!\n")
            sys.exit(0)


    def priv_esc(self):
        '''Makes user and adds to domain group -> then deletes'''

        domain = sp.check_output(["powershell", "-Command", "(Get-WmiObject Win32_ComputerSystem).Domain"]).decode().strip()
        print(f"{Fore.LIGHTBLUE_EX}[*]{Style.RESET_ALL}Checking if AD Module is installed..\n")
        self._check_AD_module()
        
        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Confirming Domain: {domain}\n")
        sp.call(f'{self.PS} New-ADUser -Name "test987" -SamAccountName "test987" -UserPrincipalName "test987@{domain}" -AccountPassword (ConvertTo-SecureString "P@55w0rd!123123%" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true', shell=True)
        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Creating User 'test987'...\nDone...\n")
        
        sleep(2) # Sleep to remove output congestion
        
        sp.call([self.PS, "-Command", 'Add-ADGroupMember -Identity "Domain Admins" -Members "test987"'])
        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Added user 'test987' to Domain Admins.\n")

        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Printing PoC info:\n")
        sp.call([self.PS, "-Command", "Get-ADUser -Identity test987 -Properties MemberOf"])

        print("*** CLEANING UP ***\n\n")
        sp.call([self.PS, "-Command", "Remove-ADUser -Identity test987 -Confirm:$False"])

        # Check if user was successfully removed

        try:
            cleaned = sp.check_output([self.PS, "-Command", "Get-ADUser -Identity test987 -Properties MemberOf"], text=True)

            if "Cannot find an object with identity" in cleaned:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL}DONE.\n{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} User Successfully removed.\n")

            else:
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Error cleaning up user. You must manually delete!\n")

        except sp.CalledProcessError as e:
            # This exception will catch non-zero exit status errors from subprocess because of non-zero exit code (User doesn't exist)
            if "Cannot find an object with identity" in e.output:
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL}DONE.\n{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} User Successfully removed.\n")
        except TypeError as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} TypeError occured: {e}\nExiting!")
            sys.exit(1)
        except Exception as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Unexpected error occured: {e}\nCheck logs!\n") # No logger yet
            sys.exit(-1)

    def create_scheduled_task(self):
        '''Creates a Windows scheduled task to run Calculator.'''
        # Implement scheduled task via PS commands
        cmd = f"""
        $TaskName = "{self.TASK_NAME}"
        $TaskAction = New-ScheduledTaskAction -Execute "{self.NOTEPAD_PATH}"
        $TaskTrigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
        $TaskPrincipal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive -RunLevel Highest
        $TaskSettings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
        $Task = New-ScheduledTask -Action $TaskAction -Trigger $TaskTrigger -Principal $TaskPrincipal -Settings $TaskSettings
        Register-ScheduledTask -TaskName $TaskName -InputObject $Task -Force
        """ 
    
        result = sp.run([self.PS, "-Command", cmd], capture_output=True, text=True)
        
        if "Ready" in result.stdout:
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Scheduled task created successfully.\n")
            print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Task runs in 1 minute...\n")
        else:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Failed to create task:", result.stderr)


    def delete_scheduled_task(self):
        '''Deletes the scheduled task after user confirmation.'''

        sleep(4)
        while True:
            choice = input(f"{Fore.RED}[-]{Style.RESET_ALL} Delete scheduled task? (y/n): \n").strip().lower() # Deletes the task according to user input
            if choice.lower() == "y":
                sp.run([self.PS, "-Command", f'Unregister-ScheduledTask -TaskName "{self.TASK_NAME}" -Confirm:$false'], capture_output=True, text=True)
                print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Task deleted.\n")
                break
            elif choice.lower() == "n":
                print(f"{Fore.RED}[-]{Style.RESET_ALL} Task not deleted.\n")
                break
            else:
                print(f"{Fore.RED}[!]{Style.RESET_ALL} Invalid input. Please enter 'y' or 'n'.\n")


if __name__ == '__main__':

    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")

    AD_obj = ADScenario(PS=PS)
    
    AD_obj.priv_esc()
    AD_obj.create_scheduled_task()
    AD_obj.delete_scheduled_task()