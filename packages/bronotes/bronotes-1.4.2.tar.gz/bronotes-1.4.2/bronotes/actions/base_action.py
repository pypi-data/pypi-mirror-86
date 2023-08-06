"""Base action for bronotes."""
import os
from datetime import datetime
from git import Repo
from git.exc import InvalidGitRepositoryError
from git.exc import GitCommandError
from pathlib import Path
from abc import ABC, abstractmethod


class BronoteAction(ABC):
    """Base bronote action."""

    @property
    @abstractmethod
    def action(self):
        """Name of the action for cli reference."""
        pass

    @property
    @abstractmethod
    def arguments(self):
        """Allow arguments for the action."""
        pass

    @property
    @abstractmethod
    def flags(self):
        """Allow flags for the action."""
        pass

    def __init__(self, cfg):
        """Construct the action."""
        self.cfg = cfg

    @abstractmethod
    def init(self):
        """Construct the child."""
        pass

    @abstractmethod
    def process(self):
        """Process the action."""
        pass

    def sync(self):
        """Sync with git."""
        try:
            repo = Repo(self.cfg.dir)
        except InvalidGitRepositoryError:
            repo = self.repo_init()

        try:
            if not repo.remotes:
                return 'No remotes configured, go figure it out.'
        except AttributeError:
            return 'Git was not configured.'

        repo.git.remote('update')
        commits_behind = len([i for i in repo.iter_commits(
            'master..origin/master')])

        if commits_behind > 0:
            pull_result = repo.git.pull('origin', 'master')
            print(pull_result)

        if repo.is_dirty() or repo.untracked_files:
            self.push(repo)
            return 'Synced with git.'

        return 'No pushing needed.'

    def push(self, repo):
        """Push to git."""
        git = repo.git
        git.add('--all')
        try:
            print(git.commit('-m', f"Automatic sync {datetime.now()}"))
        except GitCommandError:
            pass
        git.push('origin', 'master')

    def repo_init(self):
        """Initialize the git repo."""
        exit_text = 'Cancelled repo initialization.'

        i = input('Notes folder is not a repo, initialize one? (y/n): ')
        if i != 'y':
            return exit_text
        repo = Repo.init(self.cfg.dir)

        i = input('Set up a remote now? (y/n): ')
        if i != 'y':
            return exit_text

        i = input('Origin url: ')
        repo.create_remote('origin', i)
        self.push(repo)

        i = input('Enable auto syncing? (y/n): ')
        if i == 'y':
            self.cfg.enable_autosync()

        return repo

    def find_note(self, filename):
        """Find first occurance of a note traversing from the base folder."""
        for node in os.walk(self.cfg.dir):
            (basepath, dirs, files) = node

            for file in files:
                if filename in file:
                    return Path(f"{basepath}/{file}")
        return False
