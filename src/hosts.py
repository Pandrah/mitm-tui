from scapy.all import getmacbyip
import socket 
from textual import log
from os import getuid
import subprocess
import re
from textual.widgets import RichLog
import asyncio
class Host():
   hosts=[]
   def __init__(self,hostname="",ip="",mac="",interface_name="",method=""):
       self.ip=ip
       self.hostname=hostname
       self.mac=mac
       self.hostname=hostname
       self.interface_name=interface_name #name of the interface from which the host has been detected e.g. "eth0"
       self.method=method # method of detection (arp or ping for the moment)
       return

   def setMissingInfo(self,ip=False,mac=False): # fill
        try :
            assert ip or mac # one of the two information has to be defined
            if ip : #get mac
            #elif mac : #get ip
                log("getting mac adress")
                self.setMac()
                self.getHostname()
            
        except:
            raise("an error occured")

   def getHostname(self) -> str:
       #name = socket.gethostbyaddr(self.ip)[0]
        return self.hostname #str(name)

   def getIp(self) -> str:
       return self.ip

   def getInterface(self) -> str:
       return self.interface_name
    
   def getMethod(self) -> str:
       return self.method

   def setMac(self):
       if getuid()!=0:
           log("Root privileges are needed to obtain mac addresses")
           self.mac=str("unavailable")
           return
       self.mac=getmacbyip(self.ip)
       if type(self.mac) is not str:
           self.mac="Unavailable"

   def getMac(self) -> str:
       return self.mac

   def getIPmacHostname(self):
       return self.ip,self.mac,self.hostname

   async def pingHost(self):
        proc = await asyncio.create_subprocess_exec("ping","-c1",ip,stdout=asyncio.subprocess.DEVNULL) # subprocess.run(['ping','-c1',ip])
        await proc.wait()
        if proc.returncode == 0 :
            return True
        else:
            return False

   async def resolveHostname(self):
        #l.write(f"resolving hostname of {self.ip}")
        proc = subprocess.run(["nmap","-sL",self.ip],capture_output=True) 
        if proc.returncode == 0 :
            match = re.search(r"(?<=Nmap scan report for ).+(?=\s\(\d+\.\d+\.\d+\.\d+)",proc.stdout.decode())
            if match !=None:
                self.hostname = match.group()
            #l.write(f'resolved hostname {self.hostname}')
            return True
        else:
            return False
