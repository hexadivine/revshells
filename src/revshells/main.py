from pathlib import Path
from textual.app import App 
from textual.widgets import Static
from textual import on

from revshells.components.ListenerIPAndPort import ListenerIPAndPort
from revshells.components.Listener import Listener
from revshells.components.ShellTypes import ShellTypes
from revshells.components.ListLanguages import ListLanguages
from revshells.components.PayloadArea import PayloadArea

class RevShells(App):
    CSS_PATH = str(Path(__file__).parent / "styles" / "revshells.tcss")
    
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
    
    # make listerner payload selection aware
    @on(ListLanguages.SelectListenerData)
    def change_listener_params(self, message):
        self.listener.context = message.context

    @on(PayloadArea.FilterBy)
    def set_language_to_filter(self, filter):
        self.list_languages.language_filter = filter.language_filter
        self.list_languages.os_filter = filter.os_filter

def main():
    app = RevShells()
    app.run()

if __name__ == "__main__":
    main()