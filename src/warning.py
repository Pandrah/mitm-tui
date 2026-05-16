from textual import work
from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, TextArea, Static, DataTable, SelectionList, ProgressBar
from textual.containers import Horizontal, Vertical, VerticalScroll, HorizontalGroup, VerticalGroup, Container
from textual.screen import Screen,ModalScreen
from rich.text import Text



class WarningScreen(ModalScreen):
    CSS_PATH = "../assets/warning.tcss"
    BINDINGS=[('q','quit','Quit')]
    
    def __init__(self, msg: str = "",id:str=""):
        super().__init__(id=id)
        self.msg=msg

    def setMsg(self,msg):
        self.msg = msg

    def compose(self) -> ComposeResult :
        with Horizontal():
            yield Static(self.msg)
            yield Footer()

    def on_mount(self) -> None:
        self.query_one(Static).border_title = "Warning"
        return

    def action_quit(self) -> None:
        #self.dismiss(self.interfaces)
        self.app.pop_screen()
    



