# SOC - Scenario

### Active Directory (AD-Scenario) & Endpoint (EP-Scenario)

#### These scripts are made for testing a SOC managed environment by implementing malicious behavior

	For Active Directory:
		- Creates a user and adds them to the "Domain Admins" group
		- Deletes the user from the domain
		- Creates a scheduled task (Persistance PoC) and then removes it

	For Endpoint:
		- Creates an eicar file to test if AV/EDR solutions are running as intended
		- Generates CrowdStrike test alerts
		- Downloads ProcDump from the SysInternals Suite to generate an lsass dump
		- Downloads two infamously malicious tools: Mimikatz & PowerSploit
		- Opens browser to browse to organization-taboo websites (e.g gambling, malware, pornography)

#### Covert to windows PE via: PyInstaller - [python.exe pip install pyinstaller]

##### Example:

`python.exe -m PyInstaller --onefile --clean --hidden-import=colorama --hidden-import=ctypes --hidden-import=webbrowser --hidden-import=zipfile --hidden-import=shutil --name=[Final Executable Name] [Python File Name]`
