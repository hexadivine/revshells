from textual.widgets import Static, Label, TextArea, Button, Select, Input
from textual.reactive import reactive
from textual.containers import Horizontal
from textual.message import Message
from textual import on

from pathlib import Path
import json
from revshells.utils.substitute import substitute
from revshells.utils import encode_to
from revshells.utils.copy_to_clipboard import copy_to_clipboard

ASSETS_DIR = Path(__file__).parent / "../assets"

class PayloadArea(Static):

    DEFAULT_CSS = (Path(__file__).parent / "../styles/PayloadArea.tcss").read_text()

    ip = reactive('')
    port = reactive('')
    payload = reactive('tst')

    class FilterBy(Message):
        def __init__(self, language, os, **kwargs):
            super().__init__(**kwargs)
            self.language_filter = language
            self.os_filter = os

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shell = 'sh'
        self.language_filter = ''
        self.os_filter = ''
        self.encode_type = ''

        with open(f'{ASSETS_DIR}/shells.json') as shells_file:
            self.shells = json.load(shells_file)
        with open(f'{ASSETS_DIR}/shell__meta.json') as shells__meta_file:
            self.shells__meta = json.load(shells__meta_file)
        with open(f'{ASSETS_DIR}/payload_encoders.json') as payload_encoders_file:
            self.payload_encoders = json.load(payload_encoders_file)

        
    def compose(self):
        with Horizontal():
            yield Label('OS: ', id='os-label')
            yield Select(
                options=[(os, os) for os in self.shells__meta],
                id='os-select',
                allow_blank=False
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
                options=[(payload_encoder, payload_encoder) for payload_encoder in self.payload_encoders],
                id='encoding-select',
                prompt='None'
            )
            yield Button("Copy", variant='primary', id='copy-btn')

    def on_mount(self):
        self.query_one("#language-filter-input").focus()

    def watch_ip(self, ip):
        if (self.is_mounted):
            substituted_payload = substitute(self.payload, ip, self.port, self.shell)
            encoded_payload = self._encode(substituted_payload)
            self.query_one("#payload-text", TextArea).text = encoded_payload

    def watch_port(self, port):
        if (self.is_mounted):
            substituted_payload = substitute(self.payload, self.ip, port, self.shell)
            encoded_payload = self._encode(substituted_payload)
            self.query_one("#payload-text", TextArea).text = encoded_payload
    
    def watch_payload(self, payload):
        if (self.is_mounted):
            substituted_payload = substitute(payload, self.ip, self.port, self.shell)
            encoded_payload = self._encode(substituted_payload)
            self.query_one("#payload-text", TextArea).text = encoded_payload
    
    @on(Input.Changed, '#language-filter-input')
    def language_filter_update(self, event):
        self.language_filter = event.value
        self.post_message(self.FilterBy(self.language_filter, self.os_filter))

    @on (Select.Changed, '#os-select')
    def os_filter_update(self, event):
        self.os_filter = event.value
        self.post_message(self.FilterBy(self.language_filter, self.os_filter))

    @on(Select.Changed, '#shell-select')
    def change_shell(self, event):
        self.shell = event.value
        substituted_payload = substitute(self.payload, self.ip, self.port, self.shell)
        encoded_payload = self._encode(substituted_payload)
        self.query_one("#payload-text", TextArea).text = encoded_payload

    @on(Select.Changed, '#encoding-select')
    def change_encoding(self, event):
        self.encode_type = event.value
        substituted_payload = substitute(self.payload, self.ip, self.port, self.shell)
        encoded_payload = self._encode(substituted_payload)
        self.query_one("#payload-text", TextArea).text = encoded_payload

    @on(Button.Pressed, '#copy-btn')
    def copy_payload(self):
        substituted_payload = substitute(self.payload, self.ip, self.port, self.shell)
        encoded_payload = self._encode(substituted_payload)
        self.app.copy_to_clipboard(encoded_payload)
        copy_to_clipboard(encoded_payload)

        self.notify("Payload copied to clipboard!")

    def _encode(self, payload):
        match self.encode_type:
            case "Base32":
                return encode_to.base32(payload)
            case "Base64":
                return encode_to.base64(payload)
            case "URL Encode":
                return encode_to.url_encode(payload)
            case "Safe URL Encode":
                return encode_to.safe_url_encode(payload)
            case "Double URL Encode":
                return encode_to.double_url_encode(payload)
            case "Double Safe URL Encode":
                return encode_to.double_safe_url_encode(payload)
            case _: 
                return payload
