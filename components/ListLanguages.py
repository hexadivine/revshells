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
    language_filter = reactive('', recompose=True)
    os_filter = reactive('', recompose=True)

    class SelectPayload(Message):
        def __init__(self, payload, **kwargs):
            super().__init__(**kwargs)
            self.payload = payload
    
    class SelectListenerData(Message):
        def __init__(self, context, **kwargs):
            super().__init__(**kwargs)
            self.context = context

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._load_shells()
        self.filtered_languages = getattr(self, self.shelltype, [])

    def compose(self):
        with VerticalScroll():
            for index, language in enumerate(self.filtered_languages):
                btn = Button(language['name'], 
                                classes='language-button', 
                                id=f'language-button-{index}',
                                variant='primary' if index == 0 else 'default'
                            )
                btn.command = language['command']
                btn.context = language.get('listener_context', {})
                yield btn

    def on_mount(self):
        self.post_message(self.SelectPayload(self.filtered_languages[0]['command']))
        self.post_message(self.SelectListenerData(self.filtered_languages[0].get('listener_context', {})))


    def watch_shelltype(self):
        if (self.is_mounted):
            self.filtered_languages = self._filter_languages()
            if (len(self.filtered_languages) > 0):
                self.post_message(self.SelectPayload(self.filtered_languages[0]['command']))
                self.post_message(self.SelectListenerData(self.filtered_languages[0].get('listener_context', {})))

    def watch_language_filter(self):
        self.filtered_languages = self._filter_languages()
        if (len(self.filtered_languages) > 0):
            self.post_message(self.SelectPayload(self.filtered_languages[0]['command']))
            self.post_message(self.SelectListenerData(self.filtered_languages[0].get('listener_context', {})))

    def watch_os_filter(self):
        self.filtered_languages = self._filter_languages()
        if (len(self.filtered_languages) > 0):
            self.post_message(self.SelectPayload(self.filtered_languages[0]['command']))
            self.post_message(self.SelectListenerData(self.filtered_languages[0].get('listener_context', {})))

    @on(Button.Pressed)
    def select_language(self, event):
        id = event.button.id
        payload, context = self._mark_selected(id)
        self.post_message(self.SelectPayload(payload))
        self.post_message(self.SelectListenerData(context))

    def _load_shells(self):
        with open ('./assets/shell_reverse.json') as reverse_shell_file:
            self.reverse = json.load(reverse_shell_file)
        with open('./assets/shell_bind.json') as bind_shell_file:
            self.bind = json.load(bind_shell_file)
        with open('./assets/shell_msfvenom.json') as msfvenom_shell_file:
            self.msfvenom = json.load(msfvenom_shell_file)
        with open('./assets/shell_hoaxshell.json') as hoaxshell_file:
            self.hoaxshell = json.load(hoaxshell_file)

    def _mark_selected(self, id):
        payload = None
        context = {}
        for i in range(len(self.filtered_languages)):
            try:
                button = self.query_one(f"#language-button-{i}", Button)
                if id == f"language-button-{i}":
                    button.variant = "primary" 
                    payload = button.command
                    context = button.context
                else:
                    button.variant = "default" 
            except:
                pass
        return payload, context

    def _select_first_btn(self):
        first_btn = self.query(Button).first()
        first_btn.variant = 'primary'
        self.post_message(self.SelectPayload(first_btn.command))

    def _filter_languages(self):
        filtered_languages = []
        languages = getattr(self, self.shelltype, [])

        for language in languages:
            if self.language_filter.lower() in language['name'].lower() and ( self.os_filter == 'All' or self.os_filter.lower() in language['meta']):
                filtered_languages.append(language)
        return filtered_languages
