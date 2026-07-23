from textual.widgets import Static, Button
from textual.containers import Horizontal
from textual import on
from textual.message import Message

class ShellTypes(Static):
    SHELLTYPES = ["reverse", "bind", "msfvenom", "hoaxshell"]

    class Update(Message):
        def __init__(self, shelltype, **kwargs):
            super().__init__(**kwargs)
            self.shelltype = shelltype

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.shelltype = "reverse"

    def compose(self):
        with Horizontal():
            yield Button("Reverse", 
                            id='reverse', 
                            variant="primary"
                        )
            yield Button("Bind", 
                            id='bind', 
                        )
            yield Button("MSFVenom", 
                            id='msfvenom', 
                        )
            yield Button("HoaxShell", 
                            id='hoaxshell', 
                        )

    @on(Button.Pressed)
    def change_shell_type(self, event):
        self.shelltype = event.button.id
        self.post_message(self.Update(self.shelltype))
        # change clicked button varient to primary
        for shelltype in self.SHELLTYPES:
            self.query_one(f"#{shelltype}").variant = self.change_varient(shelltype)

    def change_varient(self, id):
        return "primary" if self.shelltype==id else "default"