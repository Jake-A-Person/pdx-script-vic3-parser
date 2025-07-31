from pdx_script_vic3_parser.parser.commands.command import Command

class ListItem(Command):
    def __init__(self, name: str):
        super().__init__(name,"")

    def to_pdx_script(self) -> str:
        return self.get_name()