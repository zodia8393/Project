from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QScrollArea, QProgressBar, QTextEdit, QMessageBox
from PyQt5.QtCore import Qt
from .data_source_widget import DataSourceWidget
from ..processor import DataProcessor
import asyncio
import json
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.config = self.load_config()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('데이터 처리 설정')
        self.setGeometry(100, 100, 600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        main_layout.addWidget(scroll_area)

        scroll_content = QWidget()
        self.scroll_layout = QVBoxLayout(scroll_content)
        scroll_area.setWidget(scroll_content)

        for source in self.config['data_sources']:
            self.add_data_source_widget(source)

        button_layout = QHBoxLayout()
        add_button = QPushButton('새 데이터 소스 추가')
        add_button.clicked.connect(self.add_data_source)
        button_layout.addWidget(add_button)

        save_button = QPushButton('설정 저장')
        save_button.clicked.connect(self.save_config)
        button_layout.addWidget(save_button)

        process_button = QPushButton('처리 시작')
        process_button.clicked.connect(self.start_processing)
        button_layout.addWidget(process_button)

        main_layout.addLayout(button_layout)

        self.progress_bar = QProgressBar()
        main_layout.addWidget(self.progress_bar)

        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        main_layout.addWidget(self.log_text)

    def add_data_source_widget(self, source=None):
        if source is None:
            source = {
                'source': {'source_type': ''},
                'cleaning_operations': {},
                'output': {'output_type': ''}
            }
        widget = DataSourceWidget(source)
        widget.deleted.connect(self.remove_data_source_widget)
        self.scroll_layout.addWidget(widget)

    def add_data_source(self):
        self.add_data_source_widget()

    def remove_data_source_widget(self, widget):
        self.scroll_layout.removeWidget(widget)
        widget.deleteLater()

    def save_config(self):
        self.config['data_sources'] = []
        for i in range(self.scroll_layout.count()):
            widget = self.scroll_layout.itemAt(i).widget()
            if isinstance(widget, DataSourceWidget):
                self.config['data_sources'].append(widget.get_data())
        self.save_config_to_file(self.config)
        QMessageBox.information(self, '알림', '설정이 저장되었습니다.')

    def start_processing(self):
        self.save_config()
        self.progress_bar.setValue(0)
        self.log_text.clear()

        for source in self.config['data_sources']:
            processor = DataProcessor()
            asyncio.ensure_future(self.process_data_source(processor, source))

    async def process_data_source(self, processor, config):
        try:
            await processor.collect_data(**config['source'])
            self.log_text.append(f"데이터 수집 완료: {config['source']['source_type']}")
            self.progress_bar.setValue(33)

            processor.clean_data(config['cleaning_operations'])
            self.log_text.append("데이터 정제 완료")
            self.progress_bar.setValue(66)

            processor.save_data(**config['output'])
            self.log_text.append(f"데이터 저장 완료: {config['output']['output_type']}")
            self.progress_bar.setValue(100)

            self.log_text.append(f"{config['source']['source_type']} 처리 완료")
        except Exception as e:
            self.log_text.append(f"오류 발생: {str(e)}")

    @staticmethod
    def load_config():
        if os.path.exists('data_processing_config.json'):
            with open('data_processing_config.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return {"data_sources": []}

    @staticmethod
    def save_config_to_file(config):
        with open('data_processing_config.json', 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)