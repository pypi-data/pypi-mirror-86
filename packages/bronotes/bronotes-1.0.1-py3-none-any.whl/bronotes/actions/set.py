"""Set the bronotes config."""
import os
from bronotes.actions.base_action import BronoteAction
from bronotes.config import Text
from pathlib import Path


class ActionSet(BronoteAction):
    """Set config options."""

    action = 'set'
    arguments = {}
    flags = {
        '--dir': {
            'short': '-d',
            'action': 'store',
            'help': 'The new notes directory to use.'
        }
    }

    def init(self, args):
        """Construct the action."""
        if args.dir:
            self.dir = Path(args.dir)
        else:
            self.dir = False

    def process(self):
        """Process the action."""
        if self.dir:
            self.cfg.set_dir(self.dir)

        return Text.I_CONFIG_UPDATE.value
