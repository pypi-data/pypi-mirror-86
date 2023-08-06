"""Contain the main function of bronotes.

Todo:
    * Implement -r where necessary
    * Expand on the config options (user config in file, etc.)
    * Implement something like git syncing
"""
import argparse
from bronotes.config import Cfg
from bronotes.actions.add import ActionAdd
from bronotes.actions.rm import ActionDel
from bronotes.actions.edit import ActionEdit
from bronotes.actions.list import ActionList
from bronotes.actions.mv import ActionMove


def main():
    """Entry point for bronotes."""
    cfg = Cfg()
    actions = [
        ActionAdd(cfg),
        ActionDel(cfg),
        ActionList(cfg),
        ActionEdit(cfg),
        ActionMove(cfg),
    ]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Bronote actions.')

    for action in actions:
        subparser = subparsers.add_parser(
            action.action, help=action.__doc__)

        subparser.set_defaults(action=action)

        for argument in action.arguments.keys():
            argdict = action.arguments[argument]

            subparser.add_argument(
                argument,
                help=argdict['help'],
                nargs=argdict['nargs']
            )

    args = parser.parse_args()

    # List as default action
    if not hasattr(args, 'action'):
        args.action = actions[2]
        args.dir = ''

    args.action.init(args)
    args.action.test_dir()
    print(args.action.process())
