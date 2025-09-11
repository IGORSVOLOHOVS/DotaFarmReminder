from PyQt6.QtCore import Qt, QPoint
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
        self.is_movable = False
        self.offset = QPoint()
        
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
        self._update_mouse_transparency()

    def set_text(self, text: str):
        self.label.setText(text)
        self.adjustSize()
        self.show()

    def _update_mouse_transparency(self):
        self.setAttribute(Qt.WidgetAttribute.WA_TransparentForMouseEvents, not self.is_movable)

    def set_movable(self, movable: bool):
        self.is_movable = movable
        self._update_mouse_transparency()
        
        current_style = self.label.styleSheet()
        border_style = "border: 1px dashed #FFA500;"
        
        # Remove existing border style before adding a new one
        current_style = current_style.replace(border_style, "")
        
        if movable:
            self.label.setStyleSheet(current_style + border_style)
        else:
            self.label.setStyleSheet(current_style)

    def mousePressEvent(self, event):
        if self.is_movable and event.button() == Qt.MouseButton.LeftButton:
            self.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.is_movable and event.buttons() & Qt.MouseButton.LeftButton:
            self.move(self.pos() + event.pos() - self.offset)