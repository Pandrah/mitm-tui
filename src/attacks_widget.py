import math
from textual import work,on
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
    BINDINGS= [("n","new_attack","New attack")]
    
    attacksHeader=[("victim","ip","is_at","forwarding")]

    def compose(self):
        yield DataTable()

    def on_mount(self):
        table = self.query_one(DataTable)
        table.add_columns(*self.attacksHeader[0])
        self.refresh


    def action_new_attack(self):
        def call_back(victim,ip,is_at):
            attack = Attack(victim,ip,is_at)
            self.app.attacks.append(attack)
        self.app.push_screen(NewAttackScreen(id="new-attacks-screen"),call_back)

class NewAttackScreen(ModalScreen):
    CSS_PATH="../assets/attack_screen.tcss"
    BINDINGS=[('q','quit','quit'),('n','new_attack','Create a new attack')]

    def compose(self):
        hosts=self.app.hosts
        with Container():
            yield Select(options=[(h.getIp(),h) for h in hosts],id="victim",type_to_search=True)
            yield Select(options=[(h.getIp(),h.getIp()) for h in hosts],id="ip",type_to_search=True)
            yield Select(options=[(f"{h.getMac()} - {h.getIp()}",str(h.getMac())) for h in hosts],id="is_at",type_to_search=True)
            yield Switch(id="forwarding_switch")
        yield Footer()

    @on(Select.Changed)
    def select_changed(self, event: Select.Changed) -> None:
        self.title = str(event.value)

    def on_mount(self):
        self.query_one(Horizontal).border_title="New Attack"
        self.query_one("#victim").border_title="Victim"
        self.query_one("#ip").border_title="IP"
        self.query_one("#is_at").border_title="Is at"

        self.query_one(Container).border_title = "New attack"

        v=self.query_one("#victim")
        ip=self.query_one("#ip")
        is_at=self.query_one("#is_at")
        
        hosts=self.app.hosts
        if len(hosts)==0:
            v.set_options([("No hosts discovered yet","None")])
            ip.set_options([("No hosts discovered yet","None" )])
            is_at.set_options([("No hosts discovered yet","None")])
        #else :
        #    for h in self.app.hosts:
        #        v.set_options([(h.getMac(),h) for h in hosts])

            


    def action_quit(self) -> None:
        self.app.pop_screen()

    def action_new_attack(self) -> None:
        v=self.query_one("#victim")
        ip=self.query_one("#ip")
        is_at=self.query_one("#is_at")
        forwarding=self.query_one("#forwarding_switch")
        selected_options = (v.selection,ip.selection,is_at.selection,forwarding) # type Host
        self.dismiss(selected_options)
