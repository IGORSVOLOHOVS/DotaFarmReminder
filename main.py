import sys
from pathlib import Path
from loguru import logger
from PyQt6.QtWidgets import QApplication
from pynput import keyboard
from dependency_injector.wiring import inject, Provide

from containers import Container
from ui import MainWindow
from timer.application import TimerUseCase

def setup_logger():
    log_dir = Path("logs/dota2helper")
    log_dir.mkdir(parents=True, exist_ok=True)
    log_file = log_dir / "{time:YYYY-MM-DD}.log"

    logger.remove()
    logger.add(sys.stderr, level="INFO")
    logger.add(
        log_file,
        level="INFO",
        rotation="10 MB",
        retention="10 days",
        compression="zip",
        serialize=True,
        enqueue=True,
        backtrace=True,
        diagnose=True
    )

@inject
def setup_hotkeys(
    timer_uc: TimerUseCase = Provide[Container.timer_use_case],
    main_window: MainWindow = Provide[Container.main_window]
):
    def on_press(key):
        try:
            if key == keyboard.Key.f8:
                if timer_uc._state.is_running:
                    main_window.on_pause_pressed()
                else:
                    main_window.on_start_pressed()
            elif key == keyboard.Key.f9:
                main_window.on_reset_pressed()
        except Exception as e:
            logger.error(f"Ошибка в обработчике горячей клавиши: {e}")

    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    return listener

def main():
    try:
        container = Container()
        container.config.hint_repo_path.from_value(
            Path(__file__).parent / "hint_manager" / "config"
        )
        container.wire(modules=[sys.modules[__name__]])

        setup_logger()
        app = QApplication(sys.argv)
        app.setStyle("Fusion")

        dark_stylesheet = """
        QWidget { color: #E0E0E0; background-color: #2E2E2E; }
        QMainWindow, QDockWidget { background-color: #252525; }
        QPushButton { background-color: #4A4A4A; border: 1px solid #5A5A5A; padding: 5px; border-radius: 3px; }
        QPushButton:hover { background-color: #5A5A5A; }
        QPushButton:pressed { background-color: #6A6A6A; }
        QPushButton:disabled { color: #888888; background-color: #3A3A3A; }
        QPushButton:checked { background-color: #007BFF; border-color: #0056b3; }
        QGroupBox { border: 1px solid #4A4A4A; margin-top: 10px; }
        QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
        QTextEdit { background-color: #1E1E1E; border: 1px solid #4A4A4A; }
        QComboBox { border: 1px solid #5A5A5A; border-radius: 3px; padding: 3px; }
        QComboBox::drop-down { border: none; }
        """
        app.setStyleSheet(dark_stylesheet)

        window = container.main_window()
        window.showNormal()

        listener = setup_hotkeys()

        exit_code = app.exec()
        listener.stop()
        sys.exit(exit_code)
    except Exception as e:
        logger.exception(f"Критическая ошибка в приложении: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()