# 설정 파일 작성

GUI Automator의 설정 파일은 JSON 형식으로 작성됩니다. 이 문서에서는 설정 파일의 구조와 사용 가능한 옵션에 대해 설명합니다.

## 기본 구조

```json
{
  "delay_between_actions": 0.5,
  "actions": [
    {
      "type": "action_type",
      "value": "action_value",
      "image": "image_path.png",
      "confidence": 0.8,
      "timeout": 10
    }
  ]
}

delay_between_actions: 각 액션 사이의 대기 시간 (초)
actions: 실행할 액션들의 배열

액션 타입
각 액션은 다음과 같은 속성을 가질 수 있습니다:

type: 액션의 종류 (필수)
value: 액션에 필요한 값 (선택적)
image: 이미지 파일 경로 (선택적)
confidence: 이미지 인식 신뢰도 (선택적, 기본값: 0.8)
timeout: 타임아웃 시간 (초, 선택적, 기본값: 10)

사용 가능한 액션 타입과 그 설명은 액션 타입 문서를 참조하세요.

예시
{
  "delay_between_actions": 0.5,
  "actions": [
    {
      "type": "find_and_click",
      "image": "login_button.png",
      "confidence": 0.9
    },
    {
      "type": "type",
      "value": "username"
    },
    {
      "type": "press",
      "value": "tab"
    },
    {
      "type": "type",
      "value": "password"
    },
    {
      "type": "press",
      "value": "enter"
    },
    {
      "type": "wait",
      "value": 5
    }
  ]
}

이 예시는 로그인 버튼을 찾아 클릭하고, 사용자 이름과 비밀번호를 입력한 후 엔터를 누르는 매크로를 정의합니다.

7. `docs/action-types.md`:

```markdown
# 액션 타입

GUI Automator에서 사용 가능한 액션 타입과 그 설명입니다.

## 기본 액션

1. `click`
   - 설명: 현재 마우스 위치를 클릭합니다.
   - 필요한 속성: 없음

2. `type`
   - 설명: 지정된 텍스트를 입력합니다.
   - 필요한 속성: 
     - `value`: 입력할 텍스트

3. `press`
   - 설명: 지정된 키를 누릅니다.
   - 필요한 속성:
     - `value`: 누를 키 (예: "enter", "tab", "esc")

4. `find_and_click`
   - 설명: 지정된 이미지를 화면에서 찾아 클릭합니다.
   - 필요한 속성:
     - `image`: 찾을 이미지 파일 경로
   - 선택적 속성:
     - `confidence`: 이미지 인식 신뢰도 (0.0 ~ 1.0)
     - `timeout`: 최대 대기 시간 (초)

5. `wait`
   - 설명: 지정된 시간 동안 대기합니다.
   - 필요한 속성:
     - `value`: 대기 시간 (초)

## 플러그인 액션

플러그인을 통해 추가된 커스텀 액션들도 사용할 수 있습니다. 예를 들어:

6. `custom_action`
   - 설명: ExamplePlugin에서 제공하는 커스텀 액션
   - 필요한 속성:
     - `value`: 커스텀 액션에 전달할 값

각 플러그인의 문서를 참조하여 사용 가능한 추가 액션을 확인하세요.