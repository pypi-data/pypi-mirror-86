from .mc6470 import Accelerometer
import sys
import subprocess

subprocess.check_call([sys.executable,'-m','pip','install','smbus'])
subprocess.check_call([sys.executable,'-m','pip','install','pip==18.1'])
subprocess.check_call([sys.executable,'-m','pip','install','wheel==0.35.1'])
subprocess.check_call([sys.executable,'-m','pip','install','twine==3.2.0'])
