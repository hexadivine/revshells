from pathlib import Path
from textual.app import App 
from textual.widgets import Static

from textual import on
from components.ListenerIPAndPort import ListenerIPAndPort
from components.Listener import Listener
from components.PayloadArea import PayloadArea

class RevShells(App):
    CSS_PATH = "./styles/revshells.tcss"
    
    def compose(self):
        listener_ip_and_port = ListenerIPAndPort(classes='grid grid-1')
        yield listener_ip_and_port
        
        self.listener = Listener(classes='grid grid-2')
        yield self.listener

        for i in range(0, 5):
            if i == 0 or i==4 or i==1:
                continue
            yield Static(f"{i+1}", classes=f"grid grid-{i+1}")

        self.payload_area = PayloadArea(classes='grid grid-5')
        yield self.payload_area
    
    @on(ListenerIPAndPort.Update)
    def listener_ip_and_port_update(self, message):
        self.listener.ip = message.ip
        self.listener.port = message.port
        
        self.payload_area.ip = message.ip
        self.payload_area.port = message.port

if __name__ == "__main__":
    app = RevShells()
    app.run()