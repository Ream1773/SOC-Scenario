# Test files before adding to working script
import os
import subprocess as sp
from subprocess import DEVNULL
from zipfile import ZipFile
import re
import shutil


PS = os.path.expandvars(r"%SystemRoot%\system32\WindowsPowerShell\v1.0\powershell.exe")
dir = os.path.expandvars(r"%USERPROFILE%\Desktop\\")