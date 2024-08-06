import json
import os
import logging

def load_config():
    if os.path.exists('data_processing_config.json'):
        with open('data_processing_config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"data_sources": []}

def save_config(config):
    with open('data_processing_config.json', 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)

def setup_logging():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        filename='data_processor.log',
                        filemode='a')
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(name)-12s: %(levelname)-8s %(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)

def validate_config(config):
    required_keys = ['source', 'cleaning_operations', 'output']
    for source in config.get('data_sources', []):
        if not all(key in source for key in required_keys):
            raise ValueError(f"Invalid configuration: {source}")
    return True