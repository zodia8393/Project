# Data Processor

Data Processor는 다양한 소스에서 데이터를 수집, 정제, 처리하는 GUI 기반의 Python 애플리케이션입니다.

## 주요 기능

- 다양한 소스(웹, API, 데이터베이스, 파일 시스템 등)에서 데이터 수집
- 데이터 정제 (중복 제거, 결측치 처리, 이상치 제거, 정규화 등)
- 다양한 형식으로 데이터 저장
- 사용자 친화적인 GUI
- 비동기 데이터 처리
- 로깅 및 예외 처리
- 설정 관리
- 중요 데이터 암호화

## 설치

1. 이 저장소를 클론합니다: 
git clone https://github.com/zodia8393/data_processor.git
cd data_processor

2. 가상 환경을 생성하고 활성화합니다:
hon -m venv venv
source venv/bin/activate  
# Windows의 경우: venv\Scripts\activate

3. 필요한 패키지를 설치합니다:
pip install -r requirements.txt

## 사용 방법

1. 애플리케이션을 실행합니다:

python main.py

2. GUI에서 데이터 소스를 추가하고 설정합니다.

3. 정제 작업을 선택합니다.

4. 출력 설정을 구성합니다.

5. '처리 시작' 버튼을 클릭하여 데이터 처리를 시작합니다.

## 개발

### 테스트 실행

테스트를 실행하려면 다음 명령을 사용하세요:

python -m unittest discover tests

### 기여

버그 리포트, 기능 요청, 풀 리퀘스트는 언제나 환영합니다. 중요한 변경사항에 대해서는 먼저 이슈를 열어 논의해주세요.

## 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 [LICENSE](LICENSE) 파일을 참조하세요.

