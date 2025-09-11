from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(QLabel("UI for Overlay Component"))
        self.setLayout(self.layout)