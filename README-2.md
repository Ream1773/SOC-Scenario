TODO:: Implement powersploit, mimikatz, eicar, download & exec, clean-up procedure. 


Active Directory Script: (All based on Event ID's)
 - Create user named "test987" (alert) [Event ID: User created (look it up)]
 - Add the user to the domain admin group (alert) [Event ID: added to admin group (look it up)]
 - Enumerate localgroup Administrators (alert) [Event ID: group enumerated (look it up)]
 - Delete the user from Active Directory [Event ID: User deleted (look it up)]

Enpoint:
 - EICAR - create txt file name EICAR - add string and save the file [X5O!P%@AP[4\PZX54(P^)7CC)7}$EICAR-STANDARD-ANTIVIRUS-TEST-FILE!$H+H*] - If AMP & symantec are installed (Excluding CrowdStrike) Path::Desktop

2. Generate Crowdstrike alerts:

Info: https://thomasquirke.com/2023/12/06/crowdstrike-sample-detections.html
cmd crowdstrike_test_critical 
cmd crowdstrike_test_high
cmd crowdstrike_test_medium
cmd crowdstrike_test_low

3. Dump Lsass
 - Download procdump (sysinternals) 
 - accees to the relevant path (cd) 
 - procdump.exe -accepteula -ma lsass.exe lsass.dmp (Dump command)
 - Delete procdump.

4. Download: (we can make a script which search path of crowdstrike to execute the relevant task)
"C:\Program Files\CrowdStrike" for example.
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



Surfing limitations via cmd / PS
create a script which open chrome and opens the follow links in separate tabs:

https://www.torproject.org/
https://www.nordvpn.com
https://mega.io 
https://www.888sport.com
https://www.xvideos.com 
TODO:: Make one script for DC: make user, add to domain admins, enumerate admin group, delete user


TODO:: Make other script for endpoints, find security solutions e.g crowdstrike, Cisco Secure endpoint,
Symantec, and run attacks according to what is installed on the endpoint 