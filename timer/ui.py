from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class TimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("UI for Timer Component"))
        self.setLayout(self.layout)