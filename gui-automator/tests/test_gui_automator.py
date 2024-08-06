import unittest
from unittest.mock import patch, MagicMock
from src.gui_automator import GUIAutomator
from src.actions import Action

class TestGUIAutomator(unittest.TestCase):
    def setUp(self):
        self.config = {
            "delay_between_actions": 0.5,
            "actions": [
                {"type": "click"},
                {"type": "type", "value": "test"},
                {"type": "press", "value": "enter"},
            ]
        }
        self.automator = GUIAutomator(self.config)

    @patch('src.gui_automator.pyautogui')
    async def test_click(self, mock_pyautogui):
        action = Action(type="click")
        result = await self.automator.click(action)
        self.assertTrue(result)
        mock_pyautogui.click.assert_called_once()

    @patch('src.gui_automator.pyautogui')
    async def test_type(self, mock_pyautogui):
        action = Action(type="type", value="test")
        result = await self.automator.type(action)
        self.assertTrue(result)
        mock_pyautogui.typewrite.assert_called_once_with("test")

    @patch('src.gui_automator.pyautogui')
    async def test_press(self, mock_pyautogui):
        action = Action(type="press", value="enter")
        result = await self.automator.press(action)
        self.assertTrue(result)
        mock_pyautogui.press.assert_called_once_with("enter")

    @patch('src.gui_automator.pyautogui')
    async def test_find_and_click(self, mock_pyautogui):
        mock_pyautogui.locateOnScreen.return_value = (0, 0, 10, 10)
        mock_pyautogui.center.return_value = (5, 5)
        
        action = Action(type="find_and_click", image="test.png")
        result = await self.automator.find_and_click(action)
        
        self.assertTrue(result)
        mock_pyautogui.locateOnScreen.assert_called_once_with("test.png", confidence=0.8)
        mock_pyautogui.center.assert_called_once()
        mock_pyautogui.click.assert_called_once_with((5, 5))

if __name__ == '__main__':
    unittest.main()