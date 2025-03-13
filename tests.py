import subprocess as sp
import os


# PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe") 
# output = sp.run([PS, "-Command", 'systeminfo /fo csv | ConvertFrom-Csv | select "OS Name" | Format-List'], shell=True, capture_output=True, text=True)
# print(output.stdout)
# if "windows" in output.stdout.lower():
#     print("Endpoint")
# else:
#     print("Domain Controller")

#env = os.path.expandvars(r"%USERPROFILE%")
#desktop_path = os.path.join(env, "\\Desktop")
#print(env, desktop_path)
env = os.environ
# for line in str(env).lower():
#     if "onedrive" in line:
        

print(type(env))
# if "onedrive" in str(env).lower():
#     print(env)