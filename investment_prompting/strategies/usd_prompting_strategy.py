from abc import ABC, abstractmethod

class UsdPromptingStrategy(ABC):
    """
    Abstract interface for USD investment prompting strategies.
    """

    @abstractmethod
    def execute(self, prompt):
        pass