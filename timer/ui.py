from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLabel, QFrame
from PyQt6.QtCore import pyqtSignal

class TimerWidget(QWidget):
    start_pressed = pyqtSignal()
    pause_pressed = pyqtSignal()
    reset_pressed = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        
        self.time_label = QLabel("00:00")
        self.time_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        
        self.start_button = QPushButton("Старт")
        self.pause_button = QPushButton("Пауза")
        self.reset_button = QPushButton("Сброс")
        
        self.start_button.clicked.connect(self.start_pressed.emit)
        self.pause_button.clicked.connect(self.pause_pressed.emit)
        self.reset_button.clicked.connect(self.reset_pressed.emit)
        
        self.layout.addWidget(self.time_label)
        self.layout.addWidget(self.start_button)
        self.layout.addWidget(self.pause_button)
        self.layout.addWidget(self.reset_button)

        self.set_running_state(False)

    def update_time(self, formatted_time: str):
        self.time_label.setText(formatted_time)

    def set_running_state(self, is_running: bool):
        self.start_button.setDisabled(is_running)
        self.pause_button.setDisabled(not is_running)