from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton
from PyQt5.QtCore import Qt

class CleaningOperationsDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("정제 작업 선택")
        self.selected_operations = {}
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        operations = [
            "remove_duplicates", "handle_missing_values", "normalize_column_names",
            "convert_data_types", "remove_outliers", "normalize_data",
            "handle_categorical_data", "clean_text_data", "format_dates"
        ]

        for op in operations:
            cb = QCheckBox(op)
            cb.stateChanged.connect(self.update_selected_operations)
            layout.addWidget(cb)

        button_box = QHBoxLayout()
        ok_button = QPushButton("확인")
        ok_button.clicked.connect(self.accept)
        cancel_button = QPushButton("취소")
        cancel_button.clicked.connect(self.reject)
        button_box.addWidget(ok_button)
        button_box.addWidget(cancel_button)

        layout.addLayout(button_box)
        self.setLayout(layout)

    def update_selected_operations(self, state):
        sender = self.sender()
        if state == Qt.Checked:
            self.selected_operations[sender.text()] = {}
        else:
            self.selected_operations.pop(sender.text(), None)

    def get_selected_operations(self):
        return self.selected_operations