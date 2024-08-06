# 플러그인 개발

GUI Automator의 기능을 확장하기 위한 플러그인 개발 가이드입니다.

## 기본 구조

플러그인은 `BasePlugin` 클래스를 상속받아 개발합니다. 다음은 기본 구조입니다:

```python
from src.plugins.base_plugin import BasePlugin
from src.actions import Action

class YourPlugin(BasePlugin):
    def get_actions(self):
        return {
            "your_custom_action": self.your_custom_action
        }

    async def pre_action(self, action: Action) -> bool:
        # 액션 실행 전 처리
        return False

    async def post_action(self, action: Action, result: bool) -> None:
        # 액션 실행 후 처리
        pass

    async def your_custom_action(self, action: Action) -> bool:
        # 커스텀 액션 구현
        return True

메서드 설명

get_actions(self)

플러그인에서 제공하는 커스텀 액션과 해당 메서드를 딕셔너리 형태로 반환합니다.


pre_action(self, action: Action) -> bool

모든 액션 실행 전에 호출됩니다.
True를 반환하면 원래 액션은 실행되지 않습니다.


post_action(self, action: Action, result: bool) -> None

모든 액션 실행 후에 호출됩니다.
result는 액션의 실행 결과입니다.


커스텀 액션 메서드

Action 객체를 인자로 받고 bool 값을 반환해야 합니다.



플러그인 등록
개발한 플러그인은 GUIAutomator 객체의 load_plugins 메서드를 통해 등록합니다:

from your_plugin import YourPlugin

automator = GUIAutomator(config)
automator.load_plugins([YourPlugin()])

예시
example_plugin.py를 참조하여 플러그인 개발 방법을 확인하세요.

