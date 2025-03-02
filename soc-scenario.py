import subprocess

PS = r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe"

class Scenario:
    def __init__(self):
        pass

    def main():
        subprocess.call(f"{PS} Get-ChildItem", shell=True)
        print("Done...\n")





if __name__ == '__main__':
    obj = Scenario.main()