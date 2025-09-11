from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel

class OverlayWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents)
        
        self.layout = QVBoxLayout(self)
        self.label = QLabel("Dota 2 Helper Initialized")
        self.label.setStyleSheet("""
            background-color: rgba(0, 0, 0, 180);
            color: #E0E0E0;
            font-size: 18px;
            font-weight: bold;
            padding: 8px;
            border-radius: 5px;
        """)
        self.layout.addWidget(self.label)
        self.setLayout(self.layout)
        self.adjustSize()

    def set_text(self, text: str):
        self.label.setText(text)
        self.adjustSize()
        self.show()

    def hide_text(self):
        self.hide()