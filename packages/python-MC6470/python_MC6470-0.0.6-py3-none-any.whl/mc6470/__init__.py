from .mc6470 import Accelerometer
import sys
import subprocess

#Installing pinned requirements
subprocess.check_call([sys.executable,'-m','pip','install','pip==18.1'])
subprocess.check_call([sys.executable,'-m','pip','install','wheel==0.35.1'])
