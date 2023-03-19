import subprocess
import re

from .logger import Bzlogger

def BuzzEnum(host):
    try:
        regex_ip = f'{host} \((.*?)\)'
        regex_ttl = 'ttl=(.*?) '
        output = subprocess.run(f"ping -c 1 {host}",stderr=subprocess.PIPE,stdout=subprocess.PIPE,shell=True)

        if output.returncode == 0 or output.returncode == 1:

            Bzlogger.info(f"THE HOST IS UP")
            output = output.stdout
            output = output.decode()
            ip = re.findall(regex_ip,output)[0]
            Bzlogger.info(f"[IP ADDRESS] : {ip}")
            ttl = int(re.findall(regex_ttl,output)[0])
            Bzlogger.info(f"[TIME TO LIVE] : {ttl}s ")

            if ttl<100 :
                Bzlogger.success(f"THE HOST SERVER MOSTLY USING LINUX BASED OPERATION SYSTEM")
            elif 100<ttl<150:
                Bzlogger.success("THE HOST SERVER MOSTLY USING WINDOWS BASED OPERATION SYSTEM")
            elif ttl>200:
                Bzlogger.success("THE HOST SERVER MOSTLY USING SOLARIS BASED OPERATION SYSTEM")
            else :
                Bzlogger.error(f"OS DETECTION FAILED")        

        else :
            Bzlogger.info(f"THE HOST IS DOWN OR SOMEPROBLEM WITH THE NETWORK CONNECTIVITY")

    except :
        Bzlogger.error("Failed to enumurate the ttl of host")
        


