import sys
from PyQt5.QtWidgets import QApplication
from src.gui.main_window import MainWindow
from src.utils import setup_logging

def main():
    setup_logging()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()