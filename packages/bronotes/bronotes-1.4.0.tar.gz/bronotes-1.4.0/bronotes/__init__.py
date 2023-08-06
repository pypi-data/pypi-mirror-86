"""Contain the main function of bronotes."""
import argparse
import logging
from bronotes.config import cfg
from bronotes.actions.add import ActionAdd
from bronotes.actions.rm import ActionDel
from bronotes.actions.edit import ActionEdit
from bronotes.actions.list import ActionList
from bronotes.actions.mv import ActionMove
from bronotes.actions.set import ActionSet
from bronotes.actions.completions import ActionCompletions
from bronotes.actions.show import ActionShow
from bronotes.actions.sync import ActionSync

actions = [
    ActionAdd(cfg),
    ActionDel(cfg),
    ActionList(cfg),
    ActionEdit(cfg),
    ActionMove(cfg),
    ActionSet(cfg),
    ActionCompletions(cfg),
    ActionShow(cfg),
    ActionSync(cfg),
]


def add_arguments(subparser, action):
    """Add an actions arguments to a subparser."""
    for argument in action.arguments.keys():
        argdict = action.arguments[argument]

        subparser.add_argument(
            argument,
            help=argdict['help'],
            nargs=argdict['nargs']
        ).complete = {
            "zsh": f"_files -W {cfg.dir}",
        }


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


def get_main_parser():
    """Get the main parser."""
    cfg.init()
    parser = argparse.ArgumentParser(prog='bnote')
    parser.add_argument(
        '-d',
        '--debug',
        action='store_true',
        help='Set loglevel to debug.'
    )
    subparsers = parser.add_subparsers(
        help='Bronote actions.', metavar='action')

    for action in actions:
        add_subparser(subparsers, action)

    return parser


def main():
    """Entry point for bronotes."""
    parser = get_main_parser()

    args = parser.parse_args()

    if not hasattr(args, 'action'):
        list_action = ActionList(cfg)
        args.action = list_action
        args.dir = ''

    args.action.init(args)

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    try:
        if args.action.action == 'completions':
            print(args.action.process(parser))
        else:
            print(args.action.process())
    except Exception as exc:
        logging.debug(exc)
        print("There was an uncaught exception, \
use --debug to show more info. And throw some output and what you \
were doing to the dev while you're at it.")
