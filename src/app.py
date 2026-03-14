from src import hosts

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Static, DataTable
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup, Container

class WiresharkContainer(VerticalScroll):
    BORDER_TITLE="Wireshark"
    packets=[]

class HostsContainer(VerticalScroll):
    BORDER_TITLE="Hosts"
    hosts=[]

class AttacksContainer(VerticalScroll):
    BORDER_TITLE="Attacks"
    attacks=[]

class mitmApp(App):

    """A Textual app to manage mitm arp attacks"""

    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
    CSS_PATH = "../assets/layout.tcss"
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""

        with Container(id="app-layout"):
            with WiresharkContainer(id="wireshark-container"):
                for number in range(15):
                    yield Static(f"Vertical layout, child {number}")

            with HostsContainer(id="hosts-container"):
                yield hosts.HostWidget(id="host-widget")
            
            with AttacksContainer(id="attacks-container"):
                yield Static("Attack container")

        yield Header()
        yield Footer()

    def action_toggle_dark(self) -> None:
        """An action to toggle dark mode."""
        self.theme = ("textual-dark" if self.theme == "textual-light" else "textual-light")



def main():
    app=mitmApp()
    app.run()
