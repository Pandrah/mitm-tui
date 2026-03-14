from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Static, DataTable
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup, Container
from textual.screen import Screen,ModalScreen
from rich.text import Text
import ifaddr as ifs
import ipaddress


class HostWidget(VerticalScroll):
    hostsTable=[("hostname","ip","mac","interface"),
                ("lua","1.12.156.133","AC:BC:CC:CD:EF:CD"),
                ("lua","1.12.156.133","AC:BC:CC:CD:EF:CD"),
                ("lua","1.12.156.133","AC:BC:CC:CD:EF:CD")]

    CSS_PATH = "../assets/host-widget.tcss"
    BINDINGS = [("c", "add_row", "Scan hosts"),("s", "scan", "Scan hosts")]
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
    

    def action_scan(self): #fonction qui invoque l'écran de scan

        def displayInterfaces(interfaces: list|None): #fonction qui scannera le network pour avoir les hosts

            table = self.query_one(DataTable)

            for index,interface in enumerate(interfaces):

                nice_name,ip,nw_prefix=(interface.nice_name,interface.ips[0].ip,str(interface.ips[0].network_prefix))
                row=(nice_name,ip+'/'+nw_prefix)
                label= Text(str(table.row_count), style="italic #03AC13", justify="right")
                table.add_row(*row,label=label)
#            if interface_row is not None:
#                label= Text(str(table.row_count), style="italic #03AC13", justify="right")
#                table.add_row(interface_row,label=label)

        self.app.push_screen(ScanScreen(id="scan-screen"),displayInterfaces)
    # pour le moment on affiche l'interface cliquée

    def pingSweep(interface:str) -> None:
        
        # avoir notre ip selon l'interface
        # puis le réseau et le masque de sous réseau
        # définir la plage d'ips à balayer
        # pinguer toutes les ips
        # voir les paquets retournés
        return None

class ScanScreen(ModalScreen):
    CSS_PATH = "../assets/host-widget.tcss"
    BINDINGS=[('q','quit','Quit'),
              ('r','run_scan','Run scan from interface')]

    interfaces=[] # rempli avec la biblio ifaddr
    inetDisplay=[] # parsage et ajustement des interfaces

    def compose(self) -> ComposeResult :
        yield DataTable()
    
    def on_mount(self) -> None:

        self.interfaces=ifs.get_adapters()

        table = self.query_one(DataTable)
        table.add_columns('interface','ip','mac')

        for index,interface in enumerate(self.interfaces,start=1) :
            label = Text(str(index), style="italic #03AC13", justify="right") 
            row=(interface.nice_name,interface.ips[0].ip+'/'+str(interface.ips[0].network_prefix))
            #self.inetDisplay.append(vars(interface))
            table.add_row(*row,label=label)
        return

    def action_quit(self) -> None:
        #self.dismiss(self.interfaces)
        self.app.pop_screen()
    
    def action_run_scan(self) -> None:
        table = self.query_one(DataTable)
        row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)

        index=table.get_row_index(row_key)
        nice_name=table.get_row_at(index)[0] # première colonne = nice_name

        table.remove_row(row_key)
        
        for i in self.interfaces :
            if i.nice_name==nice_name:
                self.dismiss([i])
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


