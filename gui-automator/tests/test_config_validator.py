import unittest
from src.config_validator import validate_config

class TestConfigValidator(unittest.TestCase):
    def test_valid_config(self):
        config = {
            "delay_between_actions": 0.5,
            "actions": [
                {"type": "click"},
                {"type": "type", "value": "test"},
                {"type": "press", "value": "enter"},
            ]
        }
        self.assertEqual(validate_config(config), config)

    def test_invalid_config_missing_actions(self):
        config = {
            "delay_between_actions": 0.5
        }
        with self.assertRaises(ValueError):
            validate_config(config)

    def test_invalid_config_wrong_action_type(self):
        config = {
            "actions": [
                {"type": "invalid_action"}
            ]
        }
        with self.assertRaises(ValueError):
            validate_config(config)

    def test_invalid_config_wrong_confidence(self):
        config = {
            "actions": [
                {"type": "find_and_click", "image": "test.png", "confidence": 2.0}
            ]
        }
        with self.assertRaises(ValueError):
            validate_config(config)

if __name__ == '__main__':
    unittest.main()