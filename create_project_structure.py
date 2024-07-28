import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def create_file(path, content=''):
    with open(path, 'w') as f:
        f.write(content)

def create_project_structure():
    # 프로젝트 루트 디렉토리
    root = 'travel_planner'
    create_directory(root)

    # config 디렉토리
    create_directory(os.path.join(root, 'config'))
    create_file(os.path.join(root, 'config', '__init__.py'))
    create_file(os.path.join(root, 'config', 'urls.py'))
    create_file(os.path.join(root, 'config', 'wsgi.py'))

    # config/settings 디렉토리
    create_directory(os.path.join(root, 'config', 'settings'))
    create_file(os.path.join(root, 'config', 'settings', '__init__.py'))
    create_file(os.path.join(root, 'config', 'settings', 'base.py'))
    create_file(os.path.join(root, 'config', 'settings', 'development.py'))
    create_file(os.path.join(root, 'config', 'settings', 'production.py'))

    # travel_planner 디렉토리
    create_directory(os.path.join(root, 'travel_planner'))
    create_file(os.path.join(root, 'travel_planner', '__init__.py'))

    # travel_planner/users 디렉토리
    create_directory(os.path.join(root, 'travel_planner', 'users'))
    create_file(os.path.join(root, 'travel_planner', 'users', '__init__.py'))
    create_file(os.path.join(root, 'travel_planner', 'users', 'models.py'))
    create_file(os.path.join(root, 'travel_planner', 'users', 'views.py'))
    create_file(os.path.join(root, 'travel_planner', 'users', 'urls.py'))
    create_file(os.path.join(root, 'travel_planner', 'users', 'forms.py'))
    create_file(os.path.join(root, 'travel_planner', 'users', 'admin.py'))
    create_file(os.path.join(root, 'travel_planner', 'users', 'tests.py'))

    # travel_planner/trips 디렉토리
    create_directory(os.path.join(root, 'travel_planner', 'trips'))
    create_file(os.path.join(root, 'travel_planner', 'trips', '__init__.py'))
    create_file(os.path.join(root, 'travel_planner', 'trips', 'models.py'))
    create_file(os.path.join(root, 'travel_planner', 'trips', 'views.py'))
    create_file(os.path.join(root, 'travel_planner', 'trips', 'urls.py'))
    create_file(os.path.join(root, 'travel_planner', 'trips', 'forms.py'))
    create_file(os.path.join(root, 'travel_planner', 'trips', 'admin.py'))
    create_file(os.path.join(root, 'travel_planner', 'trips', 'tests.py'))
    create_file(os.path.join(root, 'travel_planner', 'trips', 'tasks.py'))

    # travel_planner/destinations 디렉토리
    create_directory(os.path.join(root, 'travel_planner', 'destinations'))
    create_file(os.path.join(root, 'travel_planner', 'destinations', '__init__.py'))
    create_file(os.path.join(root, 'travel_planner', 'destinations', 'models.py'))
    create_file(os.path.join(root, 'travel_planner', 'destinations', 'views.py'))
    create_file(os.path.join(root, 'travel_planner', 'destinations', 'urls.py'))
    create_file(os.path.join(root, 'travel_planner', 'destinations', 'forms.py'))
    create_file(os.path.join(root, 'travel_planner', 'destinations', 'admin.py'))
    create_file(os.path.join(root, 'travel_planner', 'destinations', 'tests.py'))

    # travel_planner/core 디렉토리
    create_directory(os.path.join(root, 'travel_planner', 'core'))
    create_file(os.path.join(root, 'travel_planner', 'core', '__init__.py'))
    create_file(os.path.join(root, 'travel_planner', 'core', 'utils.py'))
    create_file(os.path.join(root, 'travel_planner', 'core', 'middleware.py'))

    # static 디렉토리
    create_directory(os.path.join(root, 'static'))
    create_directory(os.path.join(root, 'static', 'css'))
    create_directory(os.path.join(root, 'static', 'js'))
    create_directory(os.path.join(root, 'static', 'images'))

    # templates 디렉토리
    create_directory(os.path.join(root, 'templates'))
    create_file(os.path.join(root, 'templates', 'base.html'))
    create_directory(os.path.join(root, 'templates', 'users'))
    create_directory(os.path.join(root, 'templates', 'trips'))
    create_directory(os.path.join(root, 'templates', 'destinations'))

    # media 디렉토리
    create_directory(os.path.join(root, 'media'))

    # docs 디렉토리
    create_directory(os.path.join(root, 'docs'))

    # requirements 디렉토리
    create_directory(os.path.join(root, 'requirements'))
    create_file(os.path.join(root, 'requirements', 'base.txt'))
    create_file(os.path.join(root, 'requirements', 'development.txt'))
    create_file(os.path.join(root, 'requirements', 'production.txt'))

    # 루트 레벨 파일들
    create_file(os.path.join(root, 'manage.py'))
    create_file(os.path.join(root, '.gitignore'))
    create_file(os.path.join(root, 'README.md'))
    create_file(os.path.join(root, '.env'))
    create_file(os.path.join(root, 'Dockerfile'))

    # GitHub Actions 워크플로우
    create_directory(os.path.join(root, '.github', 'workflows'))
    create_file(os.path.join(root, '.github', 'workflows', 'main.yml'))

    # locale 디렉토리 (다국어 지원)
    create_directory(os.path.join(root, 'locale'))

    print("Project structure created successfully!")

if __name__ == "__main__":
    create_project_structure()