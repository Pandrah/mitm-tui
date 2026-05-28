
class Attack():

    def __init__(self,victim:str="",ip:str="",is_at:str="",forwarding:bool=False):
        self.victim =victim #Host()
        self.ip = ip #ip usurped
        self.is_at = is_at # mac falsly transmitted

    def getVictim(self):
        return self.victim
    def getVictimIp(self):
        return self.victim.getIp()
    def getIp(self):
        return self.ip
    def getIs_at(self):
        return self.is_at
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
