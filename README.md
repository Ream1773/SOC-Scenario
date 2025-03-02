<<<<<<< HEAD
# SOC-Scenario
=======
Active Directory
DC:
Create a user test987 with password never expired.  (2 alerts)
add the user to domain admin group. (alert)
net localgroup administrators - CMD (alert)
delete the user from Active directiry. (alert) (Event ID 4729)



Endpoint:
1. EICAR - create txt file named EICAR - add the string and save the file.
X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H* - AMP & symantec
2.
cmd crowdstrike_test_critical
cmd crowdstrike_test_high
cmd crowdstrike_test_medium
cmd crowdstrike_test_low
3. Lssas dmp
Download procdump (sysinternals) 
https://download.sysinternals.com/files/Procdump.zip
accees to the relevant path (cd)
procdump.exe -accepteula -ma lsass.exe lsass.dmp
Delete procdump.

4. Download: (we can make a script which search path of crowdstrike to execute the relevant task)
"C:\Program Files\CrowdStrike" for example. CSFalconService.exe process
Find a way to shut down the security safe browsing.
AMP/Symantec
	a.mimikatz - https://github.com/ParrotSec/mimikatz/archive/refs/heads/master.zip
	b.Powersploit - https://github.com/PowerShellMafia/PowerSploit/archive/refs/heads/master.zip
_______________________________________________________________________________________________
Crowdstrike:
Find a way to shut down the security safe browsing.
	a.mimikatz - https://github.com/ParrotSec/mimikatz/archive/refs/heads/master.zip
	b.Powersploit - https://github.com/PowerShellMafia/PowerSploit/archive/refs/heads/master.zip
The files need to be extractded.

in case the files exist after the extract - Delete the folders.


5. Scheduled task **** pick anyting you want (not malicious)

open via cmd calc.exe

Surfing limitations via cmd / PS
create a script which open chrome and opens the follow links in separate tabs:

https://www.torproject.org/
https://www.nordvpn.com
https://mega.io 
https://www.888sport.com
https://www.xvideos.com 
>>>>>>> 8b66ba4 (first commit - initials README.md and main python file)
