from scapy.all import getmacbyip
import socket 
from textual import log
from os import getuid
class Host():
   hosts=[]
   def __init__(self,hostname="",ip="",mac=""):
       self.ip=ip
       self.hostname=hostname
       self.mac=mac
       self.getMissingInfo(ip=True)
       return

   def getMissingInfo(self,ip=False,mac=False): # fill
        try :
            assert ip or mac # one of the two information has to be defined
            #if ip : #get mac
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

   def setMac(self):
       if getuid()!=0:
           log("Root privileges are needed to obtain mac addresses")
           self.mac=str("unavailable")
           return
       self.mac=getmacbyip(self.ip)


   def getMac(self) -> str:
       return self.mac

   def getIPmacHostname(self):
       return self.ip,self.mac,self.hostname
