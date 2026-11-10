#!/usr/bin/env python3
"""
Aegis Keymaster — Entry point
Professional touch-typing tutor for Lubuntu (PySide6 + Cyberpunk Neon UI)
"""

import sys
from pathlib import Path

# Ensure src is on the path when running as script
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont

from ui.main_window import MainWindow


def main():
    QApplication.setHighDpiScaleFactorRoundingPolicy(
        Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )

    app = QApplication(sys.argv)
    app.setApplicationName("Aegis Keymaster")
    app.setOrganizationName("Aegis")
    app.setApplicationVersion("0.2.0-neon")

    font = QFont("Segoe UI", 13)
    if not font.exactMatch():
        font = QFont("Ubuntu", 13)
    app.setFont(font)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
