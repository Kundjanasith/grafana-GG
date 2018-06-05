import os
import time
import datetime
import subprocess

command = "nvidia-smi --query-gpu=timestamp,name,pci.bus_id,driver_version,pstate,pcie.link.gen.max,pcie.link.gen.current,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used --format=csv -l 1 >> data.csv"
os.system(command)

#c1 = "nvidia-smi"
#c2 = "--query-gpu=timestamp,name,pci.bus_id,driver_version,pstate,pcie.link.gen.max,pcie.link.gen.current,temperature.gpu,utilization.gpu,utilization.memory,memory.total,memory.free,memory.used"
#c3 = "--format=csv"
#c4 = "-l"
#c5 = "1"
#line = subprocess.check_output(["tail","-2","data.csv"])
#print(line)
