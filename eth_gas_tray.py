import sys
import requests
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QColor, QFont
from PyQt5.QtCore import QTimer, Qt
import os

API_URL = "https://ethgas.watch/api/gas/latest"
ICON_PATH = os.path.join(os.path.dirname(__file__), "eth_icon.png")

class GasTrayApp:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.tray = QSystemTrayIcon()
        self.menu = QMenu()

        exit_action = QAction("Выход")
        exit_action.triggered.connect(self.exit_app)
        self.menu.addAction(exit_action)

        self.tray.setContextMenu(self.menu)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_gas_price)
        self.timer.start(60_000)    # Обновление каждую минуту

        self.update_gas_price()
        self.tray.setVisible(True)
        
        sys.exit(self.app.exec_())

    def update_gas_price(self):
        slow = None
        try:
            r = requests.get(API_URL, timeout=5)
            if r.status_code != 200 or not r.content:
                raise ValueError(f"Пустой или ошибочный ответ: HTTP {r.status_code}")
            response = r.json()

            data = response["data"]

            slow = data["oracle"]["slow"]["gwei"]
            normal = data["oracle"]["normal"]["gwei"]
            rapid = data["oracle"]["fast"]["gwei"]

            tooltip = f"⛽ Rapid: {rapid} | Normal: {normal} | Slow: {slow}"

        except Exception as e:
            rapid = None
            tooltip = f"Ошибка: {e}"
        
        if slow is not None and slow <= 99:
            if slow < 1:
                text = f"{slow:.1f}"  # Одна цифра после запятой для значений < 1
            else:
                text = str(int(slow))  # Целое число для значений >= 1
            icon = self.make_icon_with_text(text)
        else:
            if os.path.exists(ICON_PATH):
                icon = QIcon(ICON_PATH)
            else:
                icon = self.make_icon_with_text("ETH")

        self.tray.setIcon(icon)
        self.tray.setToolTip(tooltip)

    def make_icon_with_text(self, text: str) -> QIcon:
        pixmap = QPixmap(16, 16)
        pixmap.fill(QColor("black"))

        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.TextAntialiasing)
        painter.setPen(QColor("white"))
        font = QFont("Arial", 8)
        font.setBold(True)
        painter.setFont(font)
        painter.drawText(pixmap.rect(), Qt.AlignCenter, text)
        painter.end()

        return QIcon(pixmap)

    def exit_app(self):
        self.tray.hide()
        self.app.quit()

if __name__ == "__main__":
    GasTrayApp()