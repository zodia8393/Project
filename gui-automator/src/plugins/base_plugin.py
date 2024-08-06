from abc import ABC, abstractmethod
from typing import Dict, Any
from src.actions import Action

class BasePlugin(ABC):
    @abstractmethod
    def get_actions(self) -> Dict[str, callable]:
        pass

    @abstractmethod
    async def pre_action(self, action: Action) -> bool:
        pass

    @abstractmethod
    async def post_action(self, action: Action, result: bool) -> None:
        pass