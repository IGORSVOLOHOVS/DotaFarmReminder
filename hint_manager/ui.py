from PyQt6.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QRadioButton
from PyQt6.QtCore import pyqtSignal

class RoleSelectionWidget(QWidget):
    role_changed = pyqtSignal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)
        group_box = QGroupBox("Выберите роль")
        self.layout.addWidget(group_box)
        
        vbox = QVBoxLayout()
        group_box.setLayout(vbox)
        
        self.roles = {
            "Carry": QRadioButton("Керри"),
            "Support": QRadioButton("Саппорт"),
            "Offlane": QRadioButton("Танк (Оффлейн)"),
        }
        
        for role_id, radio_button in self.roles.items():
            radio_button.toggled.connect(lambda checked, r=role_id: self.on_role_toggled(checked, r))
            vbox.addWidget(radio_button)
            
        self.roles["Support"].setChecked(True)

    def on_role_toggled(self, checked: bool, role_id: str):
        if checked:
            self.role_changed.emit(role_id.lower())