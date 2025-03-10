# Test files before adding to working script
import os
import subprocess as sp
import time

PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")


def get_desktop_path():
    # Check OneDrive first
    if "ONEDRIVE" in os.environ:
        desktop_path = os.path.join(os.environ["ONEDRIVE"], "Desktop")
    else:
        desktop_path = os.path.join(os.environ["USERPROFILE"], "Desktop")
    
    # Validate the path
    if os.path.exists(desktop_path):
        return desktop_path
    else:
        print(f"[-] Detected desktop path does not exist: {desktop_path}\n")
        while True:
            user_input = input("🔍 Enter the correct Desktop path manually: \n").strip()
            if os.path.exists(user_input):
                return user_input
            else:
                print("[-] The entered path does not exist. Please try again.")

# Get the desktop path


TASK_NAME = "CalcSimulationTask"
CALC_PATH = r"C:\Windows\System32\calc.exe"  # Path to Calculator

def create_scheduled_task():
    """Creates a Windows scheduled task to run Calculator."""
    cmd = [
        "schtasks", "/create",
        "/tn", TASK_NAME,
        "/tr", CALC_PATH,
        "/sc", "once",
        "/st", (time.strftime("%H:%M:%S", time.localtime(time.time() + 15))),  # Runs in 30 seconds
        "/rl", "highest",
        "/f"
    ]
    
    result = sp.run(cmd, capture_output=True, text=True)
    
    if "SUCCESS" in result.stdout:
        print("[+] Scheduled task created successfully.\n")
        print("[+] Task runs in 5 seconds...\n")
    else:
        print("[-] Failed to create task:", result.stderr)


def delete_scheduled_task():
    """Deletes the scheduled task after user confirmation."""

    while True:
        choice = input("RED Delete scheduled task? (y/n): \n").strip().lower()
        if choice == "y":
            sp.run(["schtasks", "/delete", "/tn", TASK_NAME, "/f"], capture_output=True, text=True)
            print("[+] Task deleted.\n")
            break
        elif choice == "n":
            print("[-] Task not deleted.\n")
            break
        else:
            print("[!] Invalid input. Please enter 'y' or 'n'.\n")

    
if __name__ == '__main__':
    # desktop_path = get_desktop_path()
    # print(f"✅ Final Desktop Path: {desktop_path}")
    # create_scheduled_task()
    # time.sleep(5)  # Give user some time to inspect
    # delete_scheduled_task()
    print(time.strftime("%H:%M:%S", time.localtime(time.time() + 10)))