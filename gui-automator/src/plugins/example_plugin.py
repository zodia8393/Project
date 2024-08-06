import logging
from src.plugins.base_plugin import BasePlugin
from src.actions import Action

logger = logging.getLogger(__name__)

class ExamplePlugin(BasePlugin):
    def get_actions(self):
        return {
            "custom_action": self.custom_action
        }

    async def pre_action(self, action: Action) -> bool:
        logger.info(f"Example plugin: 동작 전 - {action.type}")
        return False

    async def post_action(self, action: Action, result: bool) -> None:
        logger.info(f"Example plugin: 동작 후 - {action.type}, 결과: {result}")

    async def custom_action(self, action: Action) -> bool:
        logger.info(f"Example plugin: 커스텀 동작 실행 - {action.value}")
        return True