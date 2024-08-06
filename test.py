import os

def create_project_structure():
    # 프로젝트 구조 정의
    structure = {
        "src": {
            "__init__.py": "",
            "gui_automator.py": "",
            "actions.py": "",
            "config_validator.py": "",
            "cli.py": "",
            "plugins": {
                "__init__.py": "",
                "base_plugin.py": "",
                "example_plugin.py": ""
            }
        },
        "tests": {
            "__init__.py": "",
            "test_gui_automator.py": "",
            "test_config_validator.py": ""
        },
        "config": {
            "macro_config.json": "{}"
        },
        "docs": {
            "index.md": "",
            "api.md": ""
        },
        "requirements.txt": "",
        "setup.py": "",
        "README.md": "",
        "LICENSE": "",
        ".gitignore": ""
    }

    def create_structure(base_path, structure):
        for name, content in structure.items():
            path = os.path.join(base_path, name)
            if isinstance(content, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, content)
            else:
                with open(path, 'w') as f:
                    f.write(content)

    # 프로젝트 루트 디렉토리 생성
    root_dir = "gui-automator"
    os.makedirs(root_dir, exist_ok=True)

    # 구조 생성
    create_structure(root_dir, structure)

    print(f"프로젝트 구조가 '{root_dir}' 디렉토리에 생성되었습니다.")

if __name__ == "__main__":
    create_project_structure()