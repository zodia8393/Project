from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import pyqtSignal
from .cleaning_operations_dialog import CleaningOperationsDialog
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QWidget
from PyQt5.QtCore import pyqtSignal
from .cleaning_operations_dialog import CleaningOperationsDialog

class DataSourceWidget(QFrame):
    deleted = pyqtSignal(QWidget)

    def __init__(self, source, parent=None):
        super().__init__(parent)
        self.source = source
        self.cleaning_operations = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        source_type_layout = QHBoxLayout()
        source_type_layout.addWidget(QLabel('소스 타입:'))
        self.source_type_edit = QLineEdit(self.source.get('source', {}).get('source_type', ''))
        source_type_layout.addWidget(self.source_type_edit)
        layout.addLayout(source_type_layout)

        url_layout = QHBoxLayout()
        url_layout.addWidget(QLabel('URL/경로:'))
        self.url_edit = QLineEdit(self.source.get('source', {}).get('url', ''))
        url_layout.addWidget(self.url_edit)
        layout.addLayout(url_layout)

        cleaning_layout = QHBoxLayout()
        cleaning_layout.addWidget(QLabel('정제 작업:'))
        self.cleaning_button = QPushButton("정제 작업 선택")
        self.cleaning_button.clicked.connect(self.select_cleaning_operations)
        cleaning_layout.addWidget(self.cleaning_button)
        layout.addLayout(cleaning_layout)

        output_type_layout = QHBoxLayout()
        output_type_layout.addWidget(QLabel('출력 타입:'))
        self.output_type_edit = QLineEdit(self.source.get('output', {}).get('output_type', ''))
        output_type_layout.addWidget(self.output_type_edit)
        layout.addLayout(output_type_layout)

        output_path_layout = QHBoxLayout()
        output_path_layout.addWidget(QLabel('출력 경로:'))
        self.output_path_edit = QLineEdit(self.source.get('output', {}).get('path_or_buf', ''))
        output_path_layout.addWidget(self.output_path_edit)
        layout.addLayout(output_path_layout)

        delete_button = QPushButton('삭제')
        delete_button.clicked.connect(self.delete_clicked)
        layout.addWidget(delete_button)

        self.setLayout(layout)
        self.setFrameStyle(QFrame.Box | QFrame.Raised)

    def select_cleaning_operations(self):
        dialog = CleaningOperationsDialog(self)
        if dialog.exec_():
            self.cleaning_operations = dialog.get_selected_operations()
            self.cleaning_button.setText(f"선택된 작업: {len(self.cleaning_operations)}")

    def delete_clicked(self):
        self.deleted.emit(self)

    def get_data(self):
        return {
            'source': {
                'source_type': self.source_type_edit.text(),
                'url': self.url_edit.text()
            },
            'cleaning_operations': self.cleaning_operations,
            'output': {
                'output_type': self.output_type_edit.text(),
                'path_or_buf': self.output_path_edit.text()
            }
        }