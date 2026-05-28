import math
from textual import work,on,log
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Static, DataTable, SelectionList, ProgressBar, Select, Switch
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalScroll, HorizontalGroup, VerticalGroup, Container
from textual.screen import Screen,ModalScreen
from rich.text import Text
import ifaddr as ifs
import ipaddress
import threading as th
import asyncio 
from ping3 import ping
from src import hosts
import scapy.all as scapy
import subprocess
from os import getuid
from src import warning,attacks


class AttackWidget(VerticalScroll):
    CSS_PATH = "../assets/attack-widget.tcss"
    BINDINGS= [("n","new_attack","New attack"),
               ('b','pause_resume','pause/resume attack'),
               ('e','edit','Edit attack settings')]
    attacksHeader=[("victim","ip","is_at","forwarding")]

    def compose(self):
        yield DataTable()

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns(*self.attacksHeader[0])
        self.refresh()

    def action_pause_resume(self):
        self.app.warn(msg='l\éespace fonctionne')
    
    def action_new_attack(self):
        def call_back(options:list):#victim,ip,is_at,forwarding):
            victim=options[0]
            ip=options[1]
            is_at=options[2]
            forwarding=options[3]
            attack = attacks.Attack(victim=victim,ip=ip,is_at=is_at,forwarding=forwarding)
            self.app.attacks.append(attack)
            self.drawTable()
            
        self.app.push_screen(NewAttackScreen(id="new-attacks-screen"),call_back)
    
    def action_edit(self):
        if len(self.app.attacks)<1:
            return
        table=self.query_one(DataTable)
        #row_key, _ = table.coordinate_to_cell_key(table.cursor_coordinate)
        edit = self.app.attacks[table.cursor_row]
        def callback(options:list):   
            victim=options[0]
            ip=options[1]
            is_at=options[2]
            forwarding=options[3]
            edit.setVictim(victim)
            edit.setIp(ip)
            edit.setIs_at(is_at)
            edit.setForwarding(forwarding)
            self.drawTable()
        self.app.push_screen(NewAttackScreen(id="new-attacks-screen",edit=edit),callback)

    def drawTable(self)-> None: #function that fill the table 
            table=self.query_one(DataTable)
            table.clear(columns=False)
            for a in self.app.attacks:
                row = (a.getVictimIp(),a.getIp(),a.getIs_at(),a.getForwarding())
                label= Text(str(table.row_count), style="italic #03AC13", justify="right")
                table.add_row(*row,label=label)


    def redraw(self):
        table = self.query_one(DataTable)
        table.clear()
        for a in self.app.attacks : 
            table.add_row(*row)

class NewAttackScreen(ModalScreen):
    CSS_PATH="../assets/attack_screen.tcss"
    BINDINGS=[('q','quit','quit'),
              ('n','new_attack','Create a new attack')]

    def __init__(self,id:str="", edit:attacks.Attack=None):
        super().__init__(id=id)
        self.edit=edit
        

    def compose(self):
        hosts=self.app.hosts
        with Container():
            yield Select(options=[(h.getIp(),h) for h in hosts],id="victim",prompt="Victim's IP", type_to_search=True,allow_blank=True)
            yield Select(options=[(h.getIp(),h.getIp()) for h in hosts],id="ip",prompt="IP",type_to_search=True,allow_blank=True)
            yield Select(options=[(f"{h.getMac()} - {h.getIp()}",str(h.getMac())) for h in hosts],prompt="Is at",id="is_at",type_to_search=True,allow_blank=True)
            yield Switch(id="forwarding")
        yield Footer()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)
        log("Value of changing ")
        log(event.value)

    def on_mount(self):
        self.query_one(Horizontal).border_title="New Attack"
        self.query_one("#victim").border_title="Victim"
        self.query_one("#ip").border_title="IP"
        self.query_one("#is_at").border_title="Is at"

        if self.edit is not None:
            self.query_one('#victim').value=self.edit.getVictim()
            self.query_one('#victim').title=self.edit.getVictimIp()
            self.query_one('#ip').value=self.edit.getIp() 
            self.query_one('#ip').title=self.edit.getIp() 
            self.query_one('#is_at').value=self.edit.getIs_at() 
            self.query_one('#is_at').title=self.edit.getIs_at() 
            self.query_one('#forwarding').value=self.edit.getForwarding() 

        self.query_one(Container).border_title = "New attack"

        v=self.query_one("#victim")
        ip=self.query_one("#ip")
        is_at=self.query_one("#is_at")
        
        hosts=self.app.hosts
        if len(hosts)==0:
            v.prompt="No hosts discovered yet"
            ip.prompt="No hosts discovered yet"
            is_at.prompt="No hosts discovered yet"
            #v.set_options([("N",None)])
            #ip.set_options([("No hosts discovered yet","" )])
            #is_at.set_options([("No hosts discovered yet","")])
        #else :
        #    for h in self.app.hosts:
        #        v.set_options([(h.getMac(),h) for h in hosts])


    def action_quit(self) -> None:
        self.app.pop_screen()

    def action_new_attack(self) -> None:
        v=self.query_one("#victim")
        ip=self.query_one("#ip")
        is_at=self.query_one("#is_at")
        forwarding=self.query_one("#forwarding")
        selected_options = (v.selection,ip.selection,is_at.selection,forwarding.value) # type Host
        log(locals())
        self.dismiss(selected_options)
