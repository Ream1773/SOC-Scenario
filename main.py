import ADScenario
import EPScenario
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

    if includes._get_os():
        AD_obj = ADScenario.ADScenario(PS=PS)
        AD_obj.priv_esc()
        AD_obj.create_scheduled_task()
        AD_obj.delete_scheduled_task()
        includes.sys.exit(0)

    else:
        EP_obj = EPScenario.EPScenario(PS, includes._get_desktop_path())
        EP_obj.make_Eicar()
        EP_obj.dump_lsass()
        EP_obj.download_tools()
        EP_obj.cs_alerts()
        EP_obj.web_filters()
        EP_obj.remove_logs()
        includes.sys.exit(0)


if __name__ == '__main__':
    main()
