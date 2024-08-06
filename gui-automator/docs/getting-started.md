# 시작하기

GUI Automator를 사용하기 위한 단계별 가이드입니다.

## 설치

1. 이 리포지토리를 클론합니다:
git clone https://github.com/yourusername/gui-automator.git

2. 프로젝트 디렉토리로 이동합니다:
cd gui-automator

3. 가상 환경을 생성하고 활성화합니다:
python -m venv venv
source venv/bin/activate 
# Windows의 경우: venv\Scripts\activate

4. 필요한 패키지를 설치합니다:
pip install -e .

## 첫 번째 매크로 실행하기

1. `config/macro_config.json` 파일을 열고 원하는 매크로 동작을 정의합니다.

2. 다음 명령어로 프로그램을 실행합니다:
gui-automator --config config/macro_config.json

3. 매크로가 실행되는 것을 확인하세요.

## 다음 단계

- [설정 파일 작성](config-file.md) 문서를 참조하여 더 복잡한 매크로를 만들어보세요.
- [플러그인 개발](plugin-development.md) 가이드를 통해 GUI Automator의 기능을 확장해보세요.

