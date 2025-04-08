import os
import sys

# Add the current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from ADScenario import ADScenario
from EPScenario import EPScenario
import includes
from colorama import init as colorama_init
from colorama import Fore
from colorama import Style

    
def main():
    '''Main function'''

    colorama_init() # Initialize Colors
    
    try: # Check if executable is being run as an Administrator
        if not includes._is_admin(): 
            print(f"{Fore.RED}[!]{Style.RESET_ALL} Relaunching as {Fore.RED}Admin{Style.RESET_ALL}...\n")
            includes._run_as_admin()

        print(f"{Fore.LIGHTGREEN_EX}[*]{Style.RESET_ALL} Running with {Fore.RED}Administrator{Style.RESET_ALL} privileges...\n")

    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Cannot run as admin.\nError: {e}\n")

    
    # Declare Powershell absolute path:
    PS = includes.os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")

    # Get working directory and ensure it exists
    try:
        work_dir = os.path.join(os.environ['LOCALAPPDATA'], 'Temp', 'SOC_Test')
        os.makedirs(work_dir, exist_ok=True)
        work_dir = work_dir + '\\'
        
        # Test write permissions
        test_file = os.path.join(work_dir, "test.tmp")
        with open(test_file, "w") as f:
            f.write("test")
        os.remove(test_file)
        
        print(f"{Fore.LIGHTGREEN_EX}[+]{Style.RESET_ALL} Using working directory: {work_dir}\n")
    except Exception as e:
        print(f"{Fore.RED}[-]{Style.RESET_ALL} Cannot access working directory: {e}\n")
        return

    if includes._get_os():
        AD_obj = ADScenario(PS=PS)
        AD_obj.priv_esc()
        AD_obj.create_scheduled_task()
        AD_obj.delete_scheduled_task()
        includes._self_delete()
        includes.sys.exit(0)

    else:
        try:
            EP_obj = EPScenario(PS, work_dir)
            EP_obj.make_Eicar()
            EP_obj.dump_lsass()
            EP_obj.download_tools()
            EP_obj.run_pv()
            EP_obj.cs_alerts()
            EP_obj.web_filters()
            includes._self_delete()
            includes.sys.exit(0)
        except Exception as e:
            print(f"{Fore.RED}[-]{Style.RESET_ALL} Error in EP scenario: {e}\n")
            includes._self_delete()
            includes.sys.exit(1)


if __name__ == '__main__':
    main()