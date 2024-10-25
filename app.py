import sys
import logging
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QPushButton, QTextEdit, 
                             QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QLabel, 
                             QTabWidget, QGridLayout, QScrollArea, QStyleFactory,
                             QProgressBar, QMessageBox)
from PyQt5.QtGui import QFont, QIcon, QPixmap, QCursor
from PyQt5.QtCore import Qt, QThread, pyqtSignal, QObject, QTimer
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
import requests

# 환경 변수 설정
os.environ['WDM_LOG_LEVEL'] = '0'  # webdriver_manager 로그 비활성화

class WorkerSignals(QObject):
    finished = pyqtSignal()
    error = pyqtSignal(str)
    result = pyqtSignal(dict)
    progress = pyqtSignal(int)

class LandInfoRetriever(QThread):
    def __init__(self, address):
        super().__init__()
        self.address = address
        self.signals = WorkerSignals()

    def run(self):
        try:
            self.signals.progress.emit(10)
            
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')
            chrome_options.add_argument('--disable-dev-shm-usage')

            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), 
                                      options=chrome_options)

            self.signals.progress.emit(30)
            driver.get("https://www.eum.go.kr/web/ar/lu/luLandDet.jsp")

            self.signals.progress.emit(50)
            self.input_address(driver)

            self.signals.progress.emit(70)
            info = self.retrieve_land_info(driver)

            driver.quit()
            self.signals.result.emit(info)
            self.signals.progress.emit(100)
            self.signals.finished.emit()
        except Exception as e:
            self.signals.error.emit(str(e))

    def input_address(self, driver):
        try:
            input_field = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'add'))
            )
            input_field.clear()
            input_field.send_keys(self.address)
            search_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), '검색')]"))
            )
            search_button.click()
        except Exception as e:
            raise Exception(f"주소 입력 중 오류 발생: {e}")

    def retrieve_land_info(self, driver):
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'land_info')))
            
            info = {}
            info['토지 이용 계획'] = self.fetch_element_text(driver, 'landUseStatus')
            info['지적도 정보'] = self.fetch_element_text(driver, 'cadastralInfo')
            info['공시지가'] = self.fetch_element_text(driver, 'officialPrice')
            info['토지 대장 정보'] = self.fetch_element_text(driver, 'landRegister')
            info['고시 정보'] = self.fetch_element_text(driver, 'announcementInfo')
            info['용도지역 정보'] = self.fetch_element_text(driver, 'zoningInfo')
            info['환경영향평가'] = self.fetch_element_text(driver, 'environmentalImpact')
            info['과거 토지 이용 내역'] = self.fetch_element_text(driver, 'landUseHistory')
            info['환경 보호 구역'] = self.check_environmental_protection(driver)

            return info
        except Exception as e:
            raise Exception(f"토지 정보 검색 중 오류 발생: {e}")

    def fetch_element_text(self, driver, element_id):
        try:
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, element_id))
            )
            return element.text
        except (TimeoutException, NoSuchElementException):
            return "정보 없음"

    def check_environmental_protection(self, driver):
        try:
            env_protection = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'environmentalProtection'))
            )
            return env_protection.text
        except (TimeoutException, NoSuchElementException):
            return "환경 보호 구역 정보 없음"

class MapAutomationApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.setup_logging()
        self.thread = None
        self.land_info_retriever = None

    def setup_ui(self):
        self.setWindowTitle("토지이음 정보 검색")
        self.setGeometry(100, 100, 1200, 800)
        self.setWindowIcon(QIcon('icon.png'))
        self.setStyle(QStyleFactory.create('Fusion'))

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # 상단 검색 영역
        search_layout = QHBoxLayout()
        self.address_input = QLineEdit()
        self.address_input.setPlaceholderText("주소를 입력하세요")
        self.address_input.setStyleSheet("""
            QLineEdit {
                border: 2px solid #4CAF50;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                min-width: 300px;
            }
            QLineEdit:focus {
                border-color: #45a049;
            }
        """)
        search_layout.addWidget(self.address_input)

        self.search_button = QPushButton("검색")
        self.search_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                font-size: 16px;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.search_button.setCursor(QCursor(Qt.PointingHandCursor))
        self.search_button.clicked.connect(self.start_search)
        search_layout.addWidget(self.search_button)

        main_layout.addLayout(search_layout)

        # 진행 상황 표시 바
        self.progress_bar = QProgressBar()
        self.progress_bar.setStyleSheet("""
            QProgressBar {
                border: 2px solid grey;
                border-radius: 5px;
                text-align: center;
            }
            QProgressBar::chunk {
                background-color: #4CAF50;
                width: 10px;
                margin: 0.5px;
            }
        """)
        main_layout.addWidget(self.progress_bar)

        # 탭 위젯 추가
        self.tab_widget = QTabWidget()
        self.setup_tabs()
        main_layout.addWidget(self.tab_widget)

    def setup_tabs(self):
        # 기본 정보 탭
        basic_info_tab = QWidget()
        basic_info_layout = QGridLayout(basic_info_tab)
        self.basic_info_fields = {
            '토지 이용 계획': QTextEdit(),
            '지적도 정보': QTextEdit(),
            '공시지가': QTextEdit(),
            '토지 대장 정보': QTextEdit()
        }
        for i, (label, text_edit) in enumerate(self.basic_info_fields.items()):
            basic_info_layout.addWidget(QLabel(label), i, 0)
            basic_info_layout.addWidget(text_edit, i, 1)
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-radius: 3px;
                    padding: 5px;
                }
            """)
        self.tab_widget.addTab(basic_info_tab, "기본 정보")

        # 추가 정보 탭
        additional_info_tab = QWidget()
        additional_info_layout = QGridLayout(additional_info_tab)
        self.additional_info_fields = {
            '고시 정보': QTextEdit(),
            '용도지역 정보': QTextEdit(),
            '환경영향평가': QTextEdit(),
            '과거 토지 이용 내역': QTextEdit(),
            '환경 보호 구역': QTextEdit()
        }
        for i, (label, text_edit) in enumerate(self.additional_info_fields.items()):
            additional_info_layout.addWidget(QLabel(label), i, 0)
            additional_info_layout.addWidget(text_edit, i, 1)
            text_edit.setReadOnly(True)
            text_edit.setStyleSheet("""
                QTextEdit {
                    background-color: #f0f0f0;
                    border: 1px solid #cccccc;
                    border-radius: 3px;
                    padding: 5px;
                }
            """)
        self.tab_widget.addTab(additional_info_tab, "추가 정보")

        # 로그 탭
        log_tab = QWidget()
        log_layout = QVBoxLayout(log_tab)
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)
        self.log_text.setStyleSheet("""
            QTextEdit {
                background-color: #f0f0f0;
                border: 1px solid #cccccc;
                border-radius: 3px;
                padding: 5px;
                font-family: Consolas, Monaco, monospace;
            }
        """)
        log_layout.addWidget(self.log_text)
        self.tab_widget.addTab(log_tab, "로그")

    def setup_logging(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)

    def start_search(self):
        address = self.address_input.text()
        if not address:
            QMessageBox.warning(self, "입력 오류", "주소를 입력해주세요.")
            return

        self.progress_bar.setValue(0)
        self.land_info_retriever = LandInfoRetriever(address)
        self.land_info_retriever.signals.result.connect(self.display_info)
        self.land_info_retriever.signals.progress.connect(self.update_progress)
        self.land_info_retriever.signals.error.connect(self.show_error)
        self.land_info_retriever.signals.finished.connect(self.process_finished)
        
        self.search_button.setEnabled(False)
        self.land_info_retriever.start()

    def display_info(self, info):
        for key, value in info.items():
            if key in self.basic_info_fields:
                self.basic_info_fields[key].setText(value)
            elif key in self.additional_info_fields:
                self.additional_info_fields[key].setText(value)
        self.log_info("정보 표시 완료")

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def show_error(self, error_msg):
        QMessageBox.critical(self, "오류", f"처리 중 오류 발생: {error_msg}")
        self.log_error(f"오류 발생: {error_msg}")
        self.search_button.setEnabled(True)

    def process_finished(self):
        self.search_button.setEnabled(True)
        self.log_info("처리 완료")

    def log_info(self, message):
        self.logger.info(message)
        self.log_text.append(f"정보: {message}")

    def log_error(self, message):
        self.logger.error(message)
        self.log_text.append(f"오류: {message}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapAutomationApp()
    window.show()
    sys.exit(app.exec_())
