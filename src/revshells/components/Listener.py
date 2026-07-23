from textual.widgets import Static, Label, Select, TextArea, Button
from textual.containers import Horizontal
from textual import on
from textual.reactive import reactive

import json
from pathlib import Path

from revshells.utils.substitute import substitute
from revshells.utils.copy_to_clipboard import copy_to_clipboard

ASSETS_DIR = Path(__file__).parent / "../assets"

class Listener(Static):
    DEFAULT_CSS = (Path(__file__).parent / "../styles/Listener.tcss").read_text()
   
    listener_payload = reactive("nc -lvnp {port}")
    ip = reactive('')
    port = reactive('4444')
    context = reactive({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with open(f'{ASSETS_DIR}/listeners.json') as listener_file:
            self.listeners = json.load(listener_file)

    def compose(self):
        with Horizontal():
            yield Label("Type: ", id='listener-type-label')
            yield Select(
                    options=[(listener, self.listeners[listener]) for listener in self.listeners ],
                    value=self.listener_payload,
                    id='listener-type-select'
                )
        with Horizontal():
            yield TextArea(self.listener_payload, id="listener-type-textarea")
            yield Button("Copy", id="copy-listener", variant="primary")


    def watch_ip(self, ip):
        if (self.is_mounted):
            self.query_one("#listener-type-textarea", TextArea).text = substitute(self.listener_payload, ip, self.port, context=self.context)
    
    def watch_port(self, port):
        if (self.is_mounted):
            self.query_one("#listener-type-textarea", TextArea).text = substitute(self.listener_payload, self.ip, port, context=self.context)

    def watch_context(self, context):
        if (self.is_mounted):
            listener = substitute(self.listener_payload, self.ip, self.port, context=context)
            self.query_one("#listener-type-textarea", TextArea).text = listener

    @on(Select.Changed)
    def change_listener_type(self, event):
        self.listener_payload = event.value
        listener = substitute(self.listener_payload, self.ip, self.port, context=self.context)
        self.query_one('#listener-type-textarea', TextArea).text = listener
 
    @on(Button.Pressed, '#copy-listener')
    def copy_listener(self):
        listener = substitute(self.listener_payload, self.ip, self.port, context=self.context)
        self.app.copy_to_clipboard(listener)
        copy_to_clipboard(listener)
        self.notify("Listener copied to clipboard!")

    # Custom method to replace placeholder
    def substitute_ip_and_port(self, listener_payload, ip, port):
        return listener_payload.replace('{ip}', ip).replace('{port}', port)
