import os
import shutil

def create_directory_structure():
    # 프로젝트 루트 디렉토리
    root_dir = "data_processor"
    
    # 디렉토리 구조
    directories = [
        "src",
        "src/gui",
        "tests",
    ]
    
    # 파일 구조
    files = [
        "src/__init__.py",
        "src/collector.py",
        "src/cleaner.py",
        "src/processor.py",
        "src/encryption.py",
        "src/utils.py",
        "src/gui/__init__.py",
        "src/gui/main_window.py",
        "src/gui/data_source_widget.py",
        "src/gui/cleaning_operations_dialog.py",
        "tests/__init__.py",
        "tests/test_collector.py",
        "tests/test_cleaner.py",
        "tests/test_processor.py",
        "main.py",
        "setup.py",
        "requirements.txt",
        "README.md",
        "LICENSE",
        ".gitignore"
    ]
    
    # 루트 디렉토리 생성
    os.makedirs(root_dir, exist_ok=True)
    
    # 디렉토리 생성
    for directory in directories:
        os.makedirs(os.path.join(root_dir, directory), exist_ok=True)
    
    # 파일 생성
    for file in files:
        open(os.path.join(root_dir, file), 'a').close()
    
    print(f"Project structure created in {root_dir}")

# 스크립트 실행
if __name__ == "__main__":
    create_directory_structure()