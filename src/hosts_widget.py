import math
from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Static, DataTable, SelectionList, ProgressBar
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup, Container
from textual.screen import Screen,ModalScreen
from rich.text import Text
import ifaddr as ifs
import ipaddress
import threading as th
import asyncio 
from ping3 import ping
from src import hosts
import scapy.all as scapy

class HostWidget(VerticalScroll):
    
    CSS_PATH = "../assets/host-widget.tcss"
    BINDINGS = [("c", "add_row", "add row"),("s", "scan", "Scan hosts")]

    
    hostsTable=[("hostname","time","ip","mac","interface")]
    current_scans=[] # interface name list on which a scan is performed

    def compose(self) -> ComposeResult:
        with VerticalScroll():
            yield DataTable()
        yield ProgressBar(total=100,show_eta=True, id="prog-bar")
        #yield Footer()

    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.hostsTable[0])
        self.query_one(ProgressBar).update(progress=0)
#        for number, row in enumerate(self.hostsTable[1:], start=1):
#            # Adding styled and justified `Text` objects instead of plain strings.
#            label = Text(str(number), style="italic #03AC13", justify="right") 
#            table.add_row(*row,label=label)      
        self.refresh()
        return
 
    def action_add_row(self): #fonction qui scannera le network pour avoir les hosts
        table = self.query_one(DataTable)
        row=("hostbonjour","18.118.218.21","AA:BB:CC:BB:AA:FF")
        label= Text(str(table.row_count), style="italic #03AC13", justify="right")
        table.add_row(*row,label=label)
   
  
    async def action_scan(self): #fonction qui invoque l'écran de scan
        async def launch_thread(interfaces: []):
            method=interfaces[0]
            del interfaces[0]
            if method=="icmp":
                for i in interfaces :
                   self.pingSweep(i)
            elif method=="arp":
                for i in interfaces:
                    self.arp_scan(i)

        self.app.push_screen(ScanScreen(id="scan-screen"),launch_thread)
        return
        # pour le moment on affiche l'interface cliquée
    @work(thread=True)
    async def arp_scan(self,interface):
        table = self.query_one(DataTable)
        bar = self.query_one(ProgressBar)

        scan = Scan(interface)
        nice_name=scan.getNiceName()
        ip_range=scan.getInet() #192.168.1.0/24
        arp_request = scapy.ARP(pdst=ip_range)
        broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
        arp_request_broadcast = broadcast / arp_request
        answered_list = scapy.srp(arp_request_broadcast, timeout=5, verbose=False)[0]

        for element in answered_list:
            ip,mac = element[1].psrc, element[1].hwsrc
            h = hosts.Host(ip=ip,mac=mac)
            label= Text(str(table.row_count), style="italic #03AC13", justify="right")
            row = '',0,ip,mac,nice_name
            self.app.call_from_thread(table.add_row,*row,label=label)
        return ''
   
    @work(thread=True)
    async def pingSweep(self,interface) -> None:
        table = self.query_one(DataTable)
        bar = self.query_one(ProgressBar)
        s = Scan(interface)
        ip,nice_name=s.getIP(),s.getNiceName()

        async for ip,progress,time in s.run():
            bar.update(progress=progress)
            if ip != None and type(time) is float:
                label= Text(str(table.row_count), style="italic #03AC13", justify="right")
                h = hosts.Host(ip=ip)
                #mac=h.getMac()
                ip,mac,hostname=h.getIPmacHostname()
                row=hostname,time,ip,mac,nice_name # Access each IP in that subnet
                self.app.call_from_thread(table.add_row,*row,label=label)
        return None

       # def displayInterfaces(interfaces: list|None): 
       #     # écriture des ips en parallèle, on veut pas rester bloquer lorsque le masque de sous réseau est trop petit
       #     table = self.query_one(DataTable)
       #     for index,interface in enumerate(interfaces):
       #         nice_name,ip,nw_prefix=(interface.nice_name,interface.ips[0].ip,str(interface.ips[0].network_prefix))
       #         row=(nice_name,ip+'/'+nw_prefix)
       #         label= Text(str(table.row_count), style="italic #03AC13", justify="right")
       #         table.add_row(*row,label=label)

    
class Scan():
    def __init__(self,interface):
        self.hosts=[] # ip hosts to scan
        self.interface = interface #object
        self.status=False # True = running, False = not running
        self.nice_name = self.interface.nice_name  # "eth0"
        self.ip = self.interface.ips[0].ip  # 192.168.1.1
        self.nw_prefix = str(self.interface.ips[0].network_prefix) # 24
        self.ipnw = ipaddress.IPv4Interface(self.ip+"/"+self.nw_prefix) # 192.168.1.1/24
        self.inet = str(self.ipnw.network) # 192.168.1.0/24
        self.network = ipaddress.ip_network(self.inet,strict=False) # all possible ips Creates subnet object
        for ip in self.network:
            self.hosts.append(str(ip))
        del self.hosts[-1] # we don't ping broadcast
        self.length=len(self.hosts)
        # avoir notre ip selon l'interface
        # puis le réseau et le masque de sous réseau
        # définir la plage d'ips à balayer
        # pinguer toutes les ips
        # voir les paquets retournés
    def getInet(self):
        return self.inet
    def toggleStatus(self):
        self.status = not self.status
    def getStatus(self):
        return self.status
    def setStatus(self,status):
        self.status=status
    def getNiceName(self):
        return self.nice_name
    def getIP(self):
        return self.ip

    async def run(self):
        if self.nice_name == 'lo':
            return

        async def pingIP(ip : str): #on peut yield les ips qui ont répondu
                    time = await asyncio.to_thread(ping,ip, timeout=1)
                    if time is not None:
                        if type(time) is float and time < 1: # ne pas mettre r == True parce que c'est un float sinon
                            return ip,time
                        else : 
                            return None,None
                    else : 
                        return None,None
                    #return ip if (r or r is not None) else None #faire le vrai ping ici

        tasks = [pingIP(ip) for ip in self.hosts]

            # 2. On exécute tout en parallèle
        #async for index,coro in enumerate(asyncio.as_completed(tasks)):
        #    r = await coro
        #    yield r,math.ceil(index*100/self.length)
        #results = await asyncio.gather(*tasks)
        #for index,ips in enumerate(self.hosts):
        #    r = await pingIP(ips) # ping à faire en parallèle
        #    if r != None:
        #        yield ips,math.ceil(index*100/self.length)
        #    else:
        #        yield None,math.ceil(index*100/self.length)
        for index,finished_task in enumerate(asyncio.as_completed(tasks)):
            result,time = await finished_task
            yield result,math.ceil(index*100/self.length),time


class ScanScreen(ModalScreen):
    CSS_PATH = "../assets/host-widget.tcss"
    BINDINGS=[('q','quit','Quit'),
              ('r','run_scan','Run scan from interface'),
              ('a','run_arp_scan',"Run arp scan")]

    interfaces=[] # rempli avec la biblio ifaddr
     # parsage et ajustement des interfaces

    def compose(self) -> ComposeResult :
        self.interfaces=ifs.get_adapters() # retourne le type IP()
        inetDisplay=[]
        #table = self.query_one(DataTable)
        #table.add_columns('interface','ip','mac')

        for index,interface in enumerate(self.interfaces,start=1) :
            #label = Text(str(index), style="italic #03AC13", justify="right") 
            interfaceName = interface.nice_name+" "+interface.ips[0].ip+'/'+str(interface.ips[0].network_prefix)
            row=(interfaceName,interface)
            inetDisplay.append(row)
            #self.inetDisplay.append(vars(interface))
            #table.add_row(*row,label=label)
        with Horizontal(id="HorizontalList"):
            yield SelectionList[ifs.Adapter](*inetDisplay)
            yield Footer()

    def on_mount(self) -> None:
        self.query_one(SelectionList).border_title = "Wich interface to scan ?"

        return

    def action_quit(self) -> None:
        #self.dismiss(self.interfaces)
        self.app.pop_screen()
    
    def action_run_scan(self) -> None:
        selected_list = self.query_one(SelectionList).selected
        selected_list.insert(0,'icmp')
        self.dismiss(selected_list)
        #toDismiss=[]
        #for i in self.interfaces :
        #    if i.nice_name in selected_list :
        #        toDismiss.append(i)
        #self.dismiss(toDismiss)
        #self.dismiss(self.inetDisplay[index])

    def action_run_arp_scan(self) -> None:
        selected_list = self.query_one(SelectionList).selected
        selected_list.insert(0,'arp')
        self.dismiss(selected_list)
