from PyQt6.QtCore import QSettings, QByteArray, QPoint, QSize

class SettingsRepository:
    def __init__(self, company="MyCompany", app="Dota2Helper"):
        self._settings = QSettings(company, app)

    def save_main_window_state(self, geometry: QByteArray, state: QByteArray):
        self._settings.setValue("mainWindow/geometry", geometry)
        self._settings.setValue("mainWindow/state", state)

    def load_main_window_state(self) -> tuple[QByteArray | None, QByteArray | None]:
        geometry = self._settings.value("mainWindow/geometry")
        state = self._settings.value("mainWindow/state")
        return geometry, state

    # --- НОВЫЙ МЕТОД ---
    def save_overlay_position(self, pos: QPoint):
        self._settings.setValue("overlay/position", pos)

    # --- НОВЫЙ МЕТОД ---
    def load_overlay_position(self) -> QPoint | None:
        pos = self._settings.value("overlay/position", type=QPoint)
        return pos