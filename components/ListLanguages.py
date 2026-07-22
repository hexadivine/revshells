from textual.widgets import Static, Button
from textual.reactive import reactive
from textual.containers import VerticalScroll
from textual.message import Message
from utils.substitute import substitute
from textual import on
from pathlib import Path
import json

class ListLanguages(Static):
    DEFAULT_CSS = (Path(__file__).parent / "../styles/ListLanguages.tcss").read_text()

    shelltype = reactive('reverse', recompose=True)

    class SelectPayload(Message):
        def __init__(self, payload, **kwargs):
            super().__init__(**kwargs)
            self.payload = payload

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_shells()

    def compose(self):
        languages = getattr(self, self.shelltype, [])
        with VerticalScroll():
            for index, language in enumerate(languages):
                btn = Button(language['name'], 
                            classes='language-button', 
                            id=f'language-button-{index}',
                            variant='primary' if index == 0 else 'default'
                            )
                btn.command = language['command']
                yield btn

    def on_mount(self):
        languages = getattr(self, self.shelltype, [])
        self.post_message(self.SelectPayload(languages[0]['command']))

    def watch_shelltype(self):
        if (self.is_mounted):
            languages = getattr(self, self.shelltype, [])
            self.post_message(self.SelectPayload(languages[0]['command']))

    @on(Button.Pressed)
    def select_language(self, event):
        id = event.button.id
        payload = self._mark_selected(id)
        self.post_message(self.SelectPayload(payload))
        # self.notify(event.value)

    def _load_shells(self):
        with open ('./assets/shell_reverse.json') as reverse_shell_file:
            self.reverse = json.load(reverse_shell_file)
        with open('./assets/shell_bind.json') as bind_shell_file:
            self.bind = json.load(bind_shell_file)
        # with open('./../assets/shell_reverse.json') as reverse_shell_file:
        #     self.reverse = json.load(reverse_shell_file)
        # with open('./../assets/shell_reverse.json') as reverse_shell_file:
        #     self.reverse = json.load(reverse_shell_file)

    def _mark_selected(self, id):
        languages = getattr(self, self.shelltype, [])
        payload = None
        for i in range(len(languages)):
            button = self.query_one(f"#language-button-{i}", Button)
            if id == f"language-button-{i}":
                button.variant = "primary" 
                payload = button.command
            else:
                button.variant = "default" 

        return payload

    def _select_first_btn(self):
        first_btn = self.query(Button).first()
        first_btn.variant = 'primary'
        self.post_message(self.SelectPayload(first_btn.command))