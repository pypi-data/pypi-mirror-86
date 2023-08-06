"""Add a note or directory."""
import os
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text
from pathlib import Path


class ActionAdd(BronoteAction):
    """Add a note or directory."""

    action = 'add'
    arguments = {
        'argument': {
            'help': 'The dir or file to create.',
            'nargs': None
        }
    }
    flags = {}

    def init(self, args):
        """Construct the action."""
        if args.argument:
            self.path = Path(os.path.join(self.cfg.dir, args.argument))
        else:
            self.path = False

    def process(self):
        """Process the action."""
        if not self.path:
            return 'No arguments given for the add action.'

        argtype = self.__test_pathtype()

        if os.path.exists(self.path):
            if argtype == 'file':
                return Text.I_FILE_EXISTS.value
            else:
                return Text.I_DIR_EXISTS.value

        if argtype == 'dir':
            os.makedirs(self.path)
        else:
            file = self.__create_file()
            return file

        return f"Created {self.path}"

    def __create_file(self):
        """Create the new file."""
        try:
            with open(self.path, 'w'):
                pass
            return f"Created {self.path}"
        except FileNotFoundError:
            return Text.E_FILE_NOT_FOUND.value

    def __test_pathtype(self):
        """Is the given path a file or dir."""
        if str(self.path)[-1] == '/':
            return 'dir'
        else:
            return 'file'
