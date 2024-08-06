import click
import asyncio
import json
from src.gui_automator import GUIAutomator
from src.plugins.example_plugin import ExamplePlugin

@click.command()
@click.option('--config', default='config/macro_config.json', help='설정 파일 경로')
def run_macro(config):
    """GUI Automator 매크로를 실행합니다."""
    with open(config, 'r') as f:
        config_data = json.load(f)

    automator = GUIAutomator(config_data)
    automator.load_plugins([ExamplePlugin()])
    
    click.echo("3초 후 매크로가 시작됩니다...")
    asyncio.get_event_loop().run_until_complete(asyncio.sleep(3))
    asyncio.get_event_loop().run_until_complete(automator.run_macro())

if __name__ == '__main__':
    run_macro()