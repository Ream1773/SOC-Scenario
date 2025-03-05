import os
import subprocess
from time import sleep
import sys
import re

# TODO:: Create scheduled task (calc.exe)

class ADScenario:
    def __init__(self, PS):
        self.PS = PS

    def _check_AD_module(self):
        ''' 
            Check whether the ActiveDirectory Module is installed & installs if it isn't.
        '''   
        try:
            output = subprocess.check_output([self.PS,"-Command", "Get-Module -ListAvailable -Name ActiveDirectory"], text=True)

            match = re.search(r"\bActiveDirectory\b", output)
            if match:
                print(f"Module found: {match.group(0)}\n")
            
            else:
                print("Module not found.\nInstalling....")
                subprocess.call([self.PS, "-Command", "Install-WindowsFeature -Name RSAT-AD-PowerShell"])
                sleep(2)
                print("Module installed!\n")

        except subprocess.CalledProcessError as e:
            print(f"Command failed with return code {e.returncode}\nExiting script!\n")
            sys.exit(0)


    def win_event_gen(self):
        '''
            Makes user and adds to domain group -> then deletes
        '''

        domain = subprocess.check_output(["powershell", "-Command", "(Get-WmiObject Win32_ComputerSystem).Domain"]).decode().strip()
        print("Checking if AD Module is installed..\n")
        self._check_AD_module()
        
        print(f"Confirming Domain: {domain}\n")
        subprocess.call(f'{self.PS} New-ADUser -Name "test987" -SamAccountName "test987" -UserPrincipalName "test987@{domain}" -AccountPassword (ConvertTo-SecureString "P@55w0rd!123123%" -AsPlainText -Force) -Enabled $true -PasswordNeverExpires $true', shell=True)
        print("Creating User 'test987'...\nDone...\n")
        
        sleep(2) # sleep for asthetics
        
        subprocess.call([self.PS, "-Command", 'Add-ADGroupMember -Identity "Domain Admins" -Members "test987"'])
        print("Added user 'test987' to Domain Admins.\n")

        print("Printing PoC info:\n")
        subprocess.call([self.PS, "-Command", "Get-ADUser -Identity test987 -Properties MemberOf"])

        print("*** CLEANING UP ***\n\n")
        subprocess.call([self.PS, "-Command", "Remove-ADUser -Identity test987 -Confirm:$False"])

        # Check if user was successfully removed

        try:
            cleaned = subprocess.check_output([self.PS, "-Command", "Get-ADUser -Identity test987 -Properties MemberOf"], text=True)

            if "Cannot find an object with identity" in cleaned:
                print("DONE.\nUser Successfully removed.\n")

            else:
                print("Error cleaning up user. You must manually delete!\n")

        except subprocess.CalledProcessError as e:
            # This exception will catch non-zero exit status errors from subprocess because of non-zero exit code (User doesn't exist)
            if "Cannot find an object with identity" in e.output:
                print("DONE.\nUser Successfully removed.\n")
        except TypeError as e:
            print(f"TypeError occured: {e}\nExiting!")
            sys.exit(1)
        except Exception as e:
            print(f"Unexpected error occured: {e}\nCheck logs!\n") # Need to implement logger
            sys.exit(-1)


if __name__ == '__main__':

    PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
    obj = ADScenario(PS=PS).win_event_gen()