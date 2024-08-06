# GUI Automator API 문서

이 문서에서는 GUI Automator의 주요 클래스와 메서드에 대해 설명합니다.

## GUIAutomator 클래스

### `__init__(self, config: Dict[str, Any])`

GUIAutomator 객체를 초기화합니다.

- `config`: 매크로 설정을 담은 딕셔너리

### `load_plugins(self, plugin_list: List[BasePlugin])`

플러그인을 로드합니다.

- `plugin_list`: 로드할 플러그인 객체 리스트

### `async run_macro(self)`

설정된 매크로를 실행합니다.

## Action 클래스

액션의 속성을 정의하는 데이터 클래스입니다.

- `type`: 액션 타입 (예: "click", "type", "press")
- `value`: 액션의 값 (선택적)
- `image`: 이미지 파일 경로 (선택적)
- `confidence`: 이미지 인식 신뢰도 (기본값: 0.8)
- `timeout`: 타임아웃 시간 (초, 기본값: 10)

## BasePlugin 클래스

플러그인 개발을 위한 기본 클래스입니다.

### `get_actions(self) -> Dict[str, callable]`

플러그인에서 제공하는 액션과 해당 메서드를 반환합니다.

### `async pre_action(self, action: Action) -> bool`

액션 실행 전에 호출되는 메서드입니다.

### `async post_action(self, action: Action, result: bool) -> None`

액션 실행 후에 호출되는 메서드입니다.

자세한 사용 예제는 `example_plugin.py`를 참조하세요.