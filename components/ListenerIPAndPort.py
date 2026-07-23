from pathlib import Path
from textual.widget import Widget
from textual.widgets import Input, Label, Static, Select
from textual.containers import Horizontal
from textual.message import Message
from textual import on
from textual.reactive import reactive
from utils.get_ip import get_ip
from utils.get_interfaces import get_interfaces

INTERFACES = get_interfaces()
DEFAULT_INTERFACE = 'tun0' if 'tun0' in INTERFACES else 'lo'
DEFAULT_IP = get_ip(DEFAULT_INTERFACE)

class ListenerIPAndPort(Static):
    DEFAULT_CSS = (Path(__file__).parent / "../styles/ListenerIPAndPort.tcss").read_text()

    ip = reactive(DEFAULT_IP)

    class Update(Message):
        def __init__(self, ip, port):
            super().__init__()
            self.ip = ip 
            self.port = port

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.interface = DEFAULT_INTERFACE
        self.port = '4444'

    def compose(self):
        with Horizontal(classes='field-row'):
            yield Label("Interface: ", id='int-label')
            yield Select(
                        options=[(interface, interface) for interface in INTERFACES],
                        value=self.interface,
                        prompt="-",
                        allow_blank=False,
                        id='interface'
                    )
        with Horizontal(classes='field-row'):
            yield Label("IP: ", id='ip-label')
            yield Input(self.ip, id='ip')
            yield Label("Port: ", id='port-label')
            yield Input(self.port, id='port')


    @on(Select.Changed)
    def set_ip(self, event):
        self.ip = get_ip(event.value)
        self.query_one("#ip", Input).value = self.ip
        self.post_message(self.Update(self.ip, self.port))


    @on(Input.Changed)
    def change_ip_and_port(self, event):
        setattr(self, event.input.id, event.value)
        self.post_message(self.Update(self.ip, self.port))