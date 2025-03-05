SOC - Scenario

Active Directory (AD-Scenario) & Endpoint (EP-Scenario)

These scripts are made for testing a SOC managed environment by implementing malicious behavior

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
