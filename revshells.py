from pathlib import Path
from textual.app import App 
from textual.widgets import Static
from textual import on

from components.ListenerIPAndPort import ListenerIPAndPort
from components.Listener import Listener
from components.ShellTypes import ShellTypes
from components.ListLanguages import ListLanguages
from components.PayloadArea import PayloadArea

class RevShells(App):
    CSS_PATH = "./styles/revshells.tcss"
    
    def compose(self):
        listener_ip_and_port = ListenerIPAndPort(classes='grid grid-1')
        yield listener_ip_and_port
        
        self.listener = Listener(classes='grid grid-2')
        yield self.listener

        self.shell_types = ShellTypes(classes='grid grid-3')
        yield self.shell_types

        self.list_languages = ListLanguages(classes='grid grid-4')
        yield self.list_languages

        self.payload_area = PayloadArea(classes='grid grid-5')
        yield self.payload_area
    
    @on(ListenerIPAndPort.Update)
    def listener_ip_and_port_update(self, message):
        self.listener.ip = message.ip
        self.listener.port = message.port
        
        self.payload_area.ip = message.ip
        self.payload_area.port = message.port
    
    @on(ShellTypes.Update)
    def shelltype_update(self, message):
        self.list_languages.shelltype = message.shelltype

    @on(ListLanguages.SelectPayload)
    def selectpayload(self, message):
        self.payload_area.payload = message.payload

if __name__ == "__main__":
    app = RevShells()
    app.run()