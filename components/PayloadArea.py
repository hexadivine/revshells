from textual.widget import Widget 
from textual.widgets import Label
from textual.reactive import reactive

class PayloadArea(Widget):
    ip = reactive('')
    port = reactive('')

    def compose(self):
        yield Label(self.ip, id='payload-ip')
        yield Label(self.port, id='payload-port')
    
    def watch_ip(self, ip):
        if (self.is_mounted):
            self.query_one("#payload-ip", Label).update(ip)
    
    def watch_port(self, port):
        if (self.is_mounted):
            self.query_one("#payload-port", Label).update(port)