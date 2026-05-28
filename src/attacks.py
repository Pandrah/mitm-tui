from textual.widgets import Select
from src import hosts
class Attack():

    def __init__(self,victim:str="",ip:str="",is_at:str="",forwarding:bool=False):
        self.victim =victim #Host()
        self.ip = ip #ip usurped
        self.is_at = is_at # mac falsly transmitted
        self.forwarding=forwarding

    def getVictim(self):
        if type(self.victim) is hosts.Host :
            return self.victim
        else:
            return Select.NULL
    def getVictimIp(self):
        if self.victim is not None:
            return self.victim.getIp()
        else:
            return Select.NULL
    def getIp(self):
        if self.ip is not None:
            return self.ip
        else: return Select.NULL
    def getIs_at(self):
        if self.is_at  is not None:
            return self.is_at
        else:
            return Select.NULL
    def getForwarding(self):
        return self.forwarding
    def setVictim(self,victim):
        self.victim=victim
    def setIp(self,ip):
        self.ip=ip
    def setIs_at(self,is_at):
        self.is_at=is_at
    def setForwarding(self,forwarding):
        self.forwarding=forwarding
