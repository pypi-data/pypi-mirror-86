"""Contain the main function of bronotes."""
import argparse
from bronotes.config import Cfg
from bronotes.actions.add import ActionAdd
from bronotes.actions.rm import ActionDel
from bronotes.actions.edit import ActionEdit
from bronotes.actions.list import ActionList
from bronotes.actions.mv import ActionMove
from bronotes.actions.set import ActionSet


def add_arguments(subparser, action):
    """Add an actions arguments to a subparser."""
    for argument in action.arguments.keys():
        argdict = action.arguments[argument]

        subparser.add_argument(
            argument,
            help=argdict['help'],
            nargs=argdict['nargs']
        )


def add_flags(subparser, action):
    """Add an actions flags to a subparser."""
    for flag in action.flags.keys():
        flagdict = action.flags[flag]

        subparser.add_argument(
            flagdict['short'],
            flag,
            action=flagdict['action'],
            help=flagdict['help']
        )


def add_subparser(subparsers, action):
    """Add a subparser based on a actions arguments and flags."""
    subparser = subparsers.add_parser(
        action.action, help=action.__doc__)

    subparser.set_defaults(action=action)
    add_arguments(subparser, action)
    add_flags(subparser, action)


def main():
    """Entry point for bronotes."""
    cfg = Cfg()
    actions = [
        ActionAdd(cfg),
        ActionDel(cfg),
        ActionList(cfg),
        ActionEdit(cfg),
        ActionMove(cfg),
        ActionSet(cfg),
    ]
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='Bronote actions.')

    for action in actions:
        add_subparser(subparsers, action)

    args = parser.parse_args()

    cfg.init()

    # List as default action
    if not hasattr(args, 'action'):
        args.action = actions[2]
        args.dir = ''

    args.action.init(args)
    print(args.action.process())
