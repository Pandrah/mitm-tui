from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Static, DataTable, SelectionList
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup, Container
from textual.screen import Screen,ModalScreen
from rich.text import Text
import ifaddr as ifs
import ipaddress
import threading as th
import asyncio as asy

class HostWidget(VerticalScroll):
    
    CSS_PATH = "../assets/host-widget.tcss"
    BINDINGS = [("c", "add_row", "add row"),("s", "scan", "Scan hosts")]

    
    hostsTable=[("hostname","ip","mac","interface")]
    current_scans=[] # interface name list on which a scan is performed

    def compose(self) -> ComposeResult:
        yield DataTable()
        

    def action_add_row(self): #fonction qui scannera le network pour avoir les hosts
        table = self.query_one(DataTable)
        row=("hostbonjour","18.118.218.21","AA:BB:CC:BB:AA:FF")
        label= Text(str(table.row_count), style="italic #03AC13", justify="right")
        table.add_row(*row,label=label)
    
    def on_mount(self) -> None:
        table = self.query_one(DataTable)
        table.add_columns(*self.hostsTable[0])
#        for number, row in enumerate(self.hostsTable[1:], start=1):
#            # Adding styled and justified `Text` objects instead of plain strings.
#            label = Text(str(number), style="italic #03AC13", justify="right") 
#            table.add_row(*row,label=label)      
        return
    
    async def action_scan(self): #fonction qui invoque l'écran de scan
        async def launch_thread(interfaces: []):
           if len(interfaces) > 0:
           #     t = th.Thread(target=pingSweep, args=interfaces)
               self.run_worker(self.pingSweep(interfaces))
           #     t.start()

        self.app.push_screen(ScanScreen(id="scan-screen"),self.pingSweep)
        return
        # pour le moment on affiche l'interface cliquée

    @work(thread=True)
    def pingSweep(self,interfaces: []) -> None:

        async def ping(ip : str):
            return "" #faire le vrai ping ici

        table = self.query_one(DataTable)

        for interface in interfaces:
            nice_name,ip,nw_prefix=(interface.nice_name, interface.ips[0].ip, str(interface.ips[0].network_prefix))
            ipnw = ipaddress.IPv4Interface(ip+"/"+nw_prefix) #192.168.1.0/24
            inet = ipnw.network

            #@work(exclusive=True)
            #async def fill():
            network = ipaddress.ip_network(inet) # Creates subnet object
            for ips in network:
                label= Text(str(table.row_count), style="italic #03AC13", justify="right")
                row="hostname",ips,"mac",nice_name # Access each IP in that subnet
                self.app.call_from_thread(table.add_row,*row,label=label)
            #await fill()
        # avoir notre ip selon l'interface
        # puis le réseau et le masque de sous réseau
        # définir la plage d'ips à balayer
        # pinguer toutes les ips
        # voir les paquets retournés
        return None

        def displayInterfaces(interfaces: list|None): 
            # écriture des ips en parallèle, on veut pas rester bloquer lorsque le masque de sous réseau est trop petit
            table = self.query_one(DataTable)

            for index,interface in enumerate(interfaces):

                nice_name,ip,nw_prefix=(interface.nice_name,interface.ips[0].ip,str(interface.ips[0].network_prefix))
                row=(nice_name,ip+'/'+nw_prefix)
                label= Text(str(table.row_count), style="italic #03AC13", justify="right")
                table.add_row(*row,label=label)


class ScanScreen(ModalScreen):
    CSS_PATH = "../assets/host-widget.tcss"
    BINDINGS=[('q','quit','Quit'),
              ('r','run_scan','Run scan from interface')]

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
        self.dismiss(selected_list)
        #toDismiss=[]
        #for i in self.interfaces :
        #    if i.nice_name in selected_list :
        #        toDismiss.append(i)
        #self.dismiss(toDismiss)
        #self.dismiss(self.inetDisplay[index])

class Host():
   hosts=[]
   def __init__(self,hostname="",ip="",mac=""):
       self.ip=ip
       self.hostname=hostname
       self.mac=mac
       return

   def getHostname(ip) -> str:
       return ""

   def getMac(ip) -> str:
       return ""


