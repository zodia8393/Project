import asyncio
import pyautogui
import logging
from typing import Dict, Any, List
from src.actions import Action
from src.config_validator import validate_config
from src.plugins.base_plugin import BasePlugin

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GUIAutomator:
    def __init__(self, config: Dict[str, Any]):
        self.config = validate_config(config)
        self.plugins: List[BasePlugin] = []
        self.action_map: Dict[str, callable] = {
            "click": self.click,
            "type": self.type,
            "press": self.press,
            "find_and_click": self.find_and_click,
            "wait": self.wait
        }

    def load_plugins(self, plugin_list: List[BasePlugin]):
        for plugin in plugin_list:
            self.plugins.append(plugin)
            self.action_map.update(plugin.get_actions())

    async def execute_action(self, action: Action) -> bool:
        try:
            for plugin in self.plugins:
                if await plugin.pre_action(action):
                    return True

            result = await self.action_map[action.type](action)

            for plugin in self.plugins:
                await plugin.post_action(action, result)

            return result
        except KeyError:
            logger.error(f"알 수 없는 동작 유형: {action.type}")
            return False
        except Exception as e:
            logger.error(f"동작 실행 중 오류 발생: {e}")
            return False

    async def click(self, action: Action) -> bool:
        pyautogui.click()
        logger.info("클릭 동작을 수행했습니다.")
        return True

    async def type(self, action: Action) -> bool:
        pyautogui.typewrite(action.value)
        logger.info(f"텍스트 입력: {action.value}")
        return True

    async def press(self, action: Action) -> bool:
        pyautogui.press(action.value)
        logger.info(f"키 입력: {action.value}")
        return True

    async def find_and_click(self, action: Action) -> bool:
        start_time = asyncio.get_event_loop().time()
        while asyncio.get_event_loop().time() - start_time < action.timeout:
            try:
                location = pyautogui.locateOnScreen(action.image, confidence=action.confidence)
                if location:
                    center = pyautogui.center(location)
                    pyautogui.click(center)
                    logger.info(f"이미지 '{action.image}'를 찾아 클릭했습니다.")
                    return True
            except pyautogui.ImageNotFoundException:
                pass
            await asyncio.sleep(0.5)
        
        logger.warning(f"이미지 '{action.image}'를 찾을 수 없습니다.")
        return False

    async def wait(self, action: Action) -> bool:
        await asyncio.sleep(action.value)
        logger.info(f"{action.value}초 대기했습니다.")
        return True

    async def run_macro(self):
        for action_config in self.config['actions']:
            action = Action(**action_config)
            if not await self.execute_action(action):
                logger.error("매크로 실행이 중단되었습니다.")
                return
            await asyncio.sleep(self.config.get('delay_between_actions', 0.5))
        
        logger.info("매크로 실행이 완료되었습니다.")