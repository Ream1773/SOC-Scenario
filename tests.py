import os
import subprocess
from subprocess import DEVNULL
from zipfile import ZipFile

PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
dir = r"C:\\Users\\raham\\OneDrive\\Desktop\\"
proc_file = "Procdump.zip"
os.mkdir(dir+"ProcDump")
full_path = dir+"ProcDump"

def get_procdump():
    subprocess.call([PS, "-Command", f"Invoke-WebRequest https://download.sysinternals.com/files/Procdump.zip -OutFile {dir}Procdump.zip"] ,shell=True, text=True)
    joined_path = dir+proc_file
    with ZipFile(joined_path, "r") as procObject:
        procObject.extractall(path=full_path)

get_procdump()
# try:
#     user = subprocess.check_output([PS, "-Command", "whoami"], text=True)
#     new = user.split('\\')
#     _get_user = new[1]
#     cleaned_user = _get_user.replace("\n", "")
#     print(cleaned_user)
#     sleep(2)

#     os.chdir(f"C:\\Users\\{cleaned_user}\\OneDrive\\Desktop")
#     print(os.getcwd())
# except OSError as e:
#     print(f"OSError {e}\n")

CMD = os.path.expandvars(r"%SystemRoot%\system32\cmd.exe")
# try:
#     output = subprocess.check_output("crowdstrike_test_critical", shell=True, text=True , stderr=DEVNULL)
#     for line in output:
#         if "crowdstrike" in line:
#             print("Command ran successfully.\n")
# except subprocess.CalledProcessError as e:
#     print(f"Command did not run successfully.\n")

# output = subprocess.check_output("crowdstrike_test_critical", shell=True , stderr=DEVNULL)
# for line in output:
#     if "crowdstrike" in line:
#         print("Command ran successfully.\n")


