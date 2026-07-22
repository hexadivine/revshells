from textual.widgets import Static, Label, TextArea, Button, Select, Input
from textual.reactive import reactive
from textual.containers import Horizontal
from textual.message import Message
from textual import on

from pathlib import Path
import json
from utils.substitute import substitute

class PayloadArea(Static):

    DEFAULT_CSS = (Path(__file__).parent / "../styles/PayloadArea.tcss").read_text()

    ip = reactive('')
    port = reactive('')
    payload = reactive('tst')

    class FilterBy(Message):
        def __init__(self, language, **kwargs):
            super().__init__(**kwargs)
            self.language_filter = language

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell = 'sh'
        with open('./assets/shells.json') as shells_file:
            self.shells = json.load(shells_file)
            
    def compose(self):
        with Horizontal():
            yield Label('OS: ', id='os-label')
            yield Select(
                options=[("Linux", "Linux"), ("Linux", "Linux")],
                id='os-select'
            )
            yield Label("Name: ", id='language-filter-label')
            yield Input(id='language-filter-input')

        yield TextArea(self.payload, id='payload-text')

        with Horizontal(id='payloads-footer'):
            yield Label("Shell: ", id='shell-label')
            yield Select(
                options=[(shell, shell) for shell in self.shells],
                value=self.shell,
                id='shell-select'
            )
            yield Label("Encoding: ", id='encoding-label')
            yield Select(
                options=[('URL Encode', 'URL Encode')]
            )
            yield Button("Copy", variant='primary', id='copy-btn')

    def watch_ip(self, ip):
        if (self.is_mounted):
            self.query_one("#payload-text", TextArea).text = substitute(self.payload, ip, self.port, self.shell)

    def watch_port(self, port):
        if (self.is_mounted):
            self.query_one("#payload-text", TextArea).text = substitute(self.payload, self.ip, port, self.shell)

    def watch_payload(self, payload):
        if (self.is_mounted):
            self.query_one("#payload-text", TextArea).text = substitute(payload, self.ip, self.port, self.shell)
    
    @on(Input.Changed, '#language-filter-input')
    def language_filter_update(self, event):
        self.post_message(self.FilterBy(event.value))

    @on(Select.Changed, '#shell-select')
    def change_shell(self, event):
        self.shell = event.value
        self.query_one("#payload-text", TextArea).text = substitute(self.payload, self.ip, self.port, event.value)

    @on(Button.Pressed, '#copy-btn')
    def copy_payload(self):
        self.app.copy_to_clipboard(self.payload)
        self.notify("Payload copied to clipboard!")