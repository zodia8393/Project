from setuptools import setup, find_packages

setup(
    name='gui-automator',
    version='1.0.0',  # 2023년 6월 최종 버전
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'pyautogui',
        'click',
        'jsonschema',
    ],
    entry_points='''
        [console_scripts]
        gui-automator=src.cli:run_macro
    ''',
)