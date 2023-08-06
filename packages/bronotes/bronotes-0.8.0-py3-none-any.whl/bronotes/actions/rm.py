"""Delete a note or directory."""
import os
from pathlib import Path
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text


class ActionDel(BronoteAction):
    """Delete a note or directory."""

    action = 'rm'
    arguments = {
        'argument': {
            'help': 'The dir or file to create.',
            'nargs': None
        }
    }
    flags = {}

    def init(self, args):
        """Construct the action."""
        self.path = Path(os.path.join(self.cfg.dir, args.argument))

    def process(self):
        """Process the action."""
        if self.path.is_dir():
            try:
                self.path.rmdir()
            except OSError:
                return Text.E_DIR_NOT_EMPTY.value
        else:
            self.path.unlink()

        return f"Removed {self.path}."
