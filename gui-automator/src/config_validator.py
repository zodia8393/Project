import jsonschema
from typing import Dict, Any

config_schema = {
    "type": "object",
    "properties": {
        "delay_between_actions": {"type": "number", "minimum": 0},
        "actions": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "type": {"type": "string"},
                    "value": {},
                    "image": {"type": "string"},
                    "confidence": {"type": "number", "minimum": 0, "maximum": 1},
                    "timeout": {"type": "number", "minimum": 0}
                },
                "required": ["type"]
            }
        }
    },
    "required": ["actions"]
}

def validate_config(config: Dict[str, Any]) -> Dict[str, Any]:
    try:
        jsonschema.validate(instance=config, schema=config_schema)
        return config
    except jsonschema.exceptions.ValidationError as e:
        raise ValueError(f"설정 파일이 유효하지 않습니다: {e}")