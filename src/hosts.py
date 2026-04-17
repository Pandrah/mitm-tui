from scapy.all import getmacbyip
import socket 
from textual import log

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
            self.getMac()
            self.getHostname()
        except:
            raise("an error occured")

   def getHostname(self) -> str:
       #name = socket.gethostbyaddr(self.ip)[0]
        return "" #str(name)

   def getIp(self) -> str:
       return ""

   def getMac(self) -> str:
       self.mac = getmacbyip(self.ip) # use root permission
       return self.mac

   def getIPmacHostname(self):
       return self.ip,self.mac,self.hostname
