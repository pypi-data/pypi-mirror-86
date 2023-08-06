"""Base action for bronotes."""
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
