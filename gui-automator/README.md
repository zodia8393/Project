# GUI Automator

GUI Automator는 Python을 사용하여 개발된 고급 GUI 자동화 매크로 프로그램입니다. 이 프로그램은 작업 화면에서 필요한 버튼을 찾아 자동으로 클릭하는 등의 반복 작업을 자동화합니다.

## 개발 기간

이 프로젝트는 2023년 2월부터 2023년 6월까지 개발되었습니다.

## 기능

- 비동기 처리를 통한 효율적인 실행
- 플러그인 시스템을 통한 확장 가능한 구조
- 커맨드 라인 인터페이스
- JSON 스키마를 이용한 설정 파일 검증
- 화면 요소 인식 및 클릭
- 텍스트 입력 자동화
- 키보드 입력 시뮬레이션

## 설치

1. 이 리포지토리를 클론합니다:
git clone https://github.com/zodia8393/gui-automator.git

2. 프로젝트 디렉토리로 이동합니다:
cd gui-automator

3. 가상 환경을 생성하고 활성화합니다:
python -m venv venv
source venv/bin/activate  
# Windows의 경우: venv\Scripts\activate

4. 필요한 패키지를 설치합니다:
pip install -e .

## 사용 방법

1. `config/macro_config.json` 파일에서 원하는 매크로 동작을 정의합니다.

2. 다음 명령어로 프로그램을 실행합니다:
gui-automator --config config/macro_config.json

## 플러그인 개발

`src/plugins/base_plugin.py`를 상속받아 새로운 플러그인을 개발할 수 있습니다. 자세한 내용은 `docs/api.md`를 참조하세요.

## 테스트

다음 명령어로 단위 테스트를 실행할 수 있습니다:
python -m unittest discover tests

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

