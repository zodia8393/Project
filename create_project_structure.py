import os

def create_directory_structure():
    structure = {
        'backend': {
            'app': {
                'data': ['__init__.py', 'collector.py', 'preprocessor.py', 'feature_engineer.py'],
                'models': ['__init__.py', 'trainer.py', 'predictor.py'],
                'utils': ['__init__.py', 'database.py', 'location.py', 'alerts.py'],
                'api': ['__init__.py', 'routes.py', 'schemas.py'],
                '__init__.py': '',
                'main.py': '',
                'config.py': ''
            },
            'tests': {
                '__init__.py': '',
                'test_data_collector.py': '',
                'test_preprocessor.py': '',
                'test_model.py': '',
                'test_predictor.py': ''
            },
            'requirements.txt': '',
            'run.py': ''
        },
        'frontend': {
            'public': {
                'index.html': '',
                'favicon.ico': '',
                'manifest.json': ''
            },
            'src': {
                'components': {
                    'WeatherWidget.js': '',
                    'PredictionChart.js': '',
                    'AlertList.js': ''
                },
                'pages': {
                    'Home.js': '',
                    'About.js': ''
                },
                'services': {
                    'api.js': ''
                },
                'App.js': '',
                'index.js': '',
                'styles.css': ''
            },
            'package.json': '',
            'README.md': ''
        },
        'docker-compose.yml': '',
        '.gitignore': '',
        'README.md': ''
    }

    def create_structure(base_path, structure):
        for key, value in structure.items():
            path = os.path.join(base_path, key)
            if isinstance(value, dict):
                os.makedirs(path, exist_ok=True)
                create_structure(path, value)
            else:
                if isinstance(value, list):
                    os.makedirs(path, exist_ok=True)
                    for file in value:
                        open(os.path.join(path, file), 'a').close()
                else:
                    open(path, 'a').close()

    base_dir = 'rainfall_prediction_system'
    os.makedirs(base_dir, exist_ok=True)
    create_structure(base_dir, structure)

    print(f"Project structure created in '{base_dir}' directory.")

if __name__ == "__main__":
    create_directory_structure()