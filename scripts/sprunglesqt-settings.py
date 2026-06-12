#!/usr/bin/env python3
"""
SprunglesQT Settings Panel
The lightweight settings center for SprunglesQT desktop.
Replaces: lxqt-config, lxqt-config-appearance, lxqt-config-monitor, lxqt-config-session
"""

import sys
import os
import subprocess
import configparser
from pathlib import Path

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QListWidget, QListWidgetItem, QStackedWidget, QLabel,
    QPushButton, QComboBox, QFontComboBox, QGroupBox, QGridLayout,
    QSpinBox, QCheckBox, QTextEdit, QTabWidget, QSplitter,
    QMessageBox, QScrollArea, QFrame, QLineEdit, QFileDialog,
    QSlider, QSizePolicy, QStyleFactory
)
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QFont, QIcon, QPalette, QColor, QPixmap, QPainter, QPen, QFontDatabase, QPolygonF
from PyQt6.QtCore import QPointF


# ─── Constants ───────────────────────────────────────────────────────────────

CONFIG_DIR = Path.home() / ".config" / "lxqt"
SESSION_CONF = CONFIG_DIR / "session.conf"
LXQT_CONF = CONFIG_DIR / "lxqt.conf"
PANEL_CONF = CONFIG_DIR / "panel.conf"
AUTOSTART_DIR = Path.home() / ".config" / "autostart"

STYLESHEET = """
QMainWindow {
    background-color: #2b2b2b;
}
QListWidget {
    background-color: #1e1e1e;
    border: none;
    border-right: 1px solid #3c3c3c;
    color: #d4d4d4;
    font-size: 13px;
    padding: 4px;
}
QListWidget::item {
    padding: 10px 16px;
    border-radius: 4px;
    margin: 2px 4px;
}
QListWidget::item:selected {
    background-color: #3d427e;
    color: #ffffff;
}
QListWidget::item:hover {
    background-color: #333333;
}
QStackedWidget {
    background-color: #2b2b2b;
}
QLabel#pageTitle {
    font-size: 20px;
    font-weight: bold;
    color: #e0e0e0;
    padding-bottom: 8px;
}
QLabel#pageDesc {
    font-size: 12px;
    color: #9a9a9a;
    padding-bottom: 16px;
}
QLabel {
    color: #d4d4d4;
    font-size: 13px;
}
QGroupBox {
    border: 1px solid #3c3c3c;
    border-radius: 6px;
    margin-top: 12px;
    padding-top: 16px;
    color: #e0e0e0;
    font-weight: bold;
}
QGroupBox::title {
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
}
QPushButton {
    background-color: #3d427e;
    color: #ffffff;
    border: none;
    border-radius: 4px;
    padding: 8px 20px;
    font-size: 13px;
    min-height: 20px;
}
QPushButton:hover {
    background-color: #4e54a0;
}
QPushButton:pressed {
    background-color: #2e3366;
}
QPushButton#danger {
    background-color: #6b2020;
}
QPushButton#danger:hover {
    background-color: #8a2a2a;
}
QComboBox {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
    min-height: 20px;
}
QComboBox::drop-down {
    border: none;
    width: 24px;
}
QComboBox QAbstractItemView {
    background-color: #1e1e1e;
    color: #d4d4d4;
    selection-background-color: #3d427e;
    border: 1px solid #3c3c3c;
}
QFontComboBox {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
}
QSpinBox {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
}
QCheckBox {
    color: #d4d4d4;
    font-size: 13px;
    spacing: 8px;
}
QCheckBox::indicator {
    width: 18px;
    height: 18px;
    border-radius: 3px;
    border: 1px solid #3c3c3c;
    background-color: #1e1e1e;
}
QCheckBox::indicator:checked {
    background-color: #3d427e;
    border-color: #3d427e;
}
QTextEdit {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    font-family: monospace;
    font-size: 12px;
}
QLineEdit {
    background-color: #1e1e1e;
    color: #d4d4d4;
    border: 1px solid #3c3c3c;
    border-radius: 4px;
    padding: 6px 12px;
    font-size: 13px;
}
QScrollBar:vertical {
    background-color: #1e1e1e;
    width: 8px;
    border: none;
}
QScrollBar::handle:vertical {
    background-color: #3c3c3c;
    border-radius: 4px;
    min-height: 30px;
}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0;
}
QFrame#separator {
    background-color: #3c3c3c;
    max-height: 1px;
}
"""


# ─── Page Widgets ────────────────────────────────────────────────────────────

class DisplayPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_current()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Display")
        title.setObjectName("pageTitle")
        desc = QLabel("Configure monitors, resolution, and refresh rate")
        desc.setObjectName("pageDesc")
        layout.addWidget(title)
        layout.addWidget(desc)

        # Monitor group
        mon_group = QGroupBox("Monitors")
        mon_layout = QVBoxLayout(mon_group)

        self.monitor_list = QComboBox()
        mon_layout.addWidget(QLabel("Select monitor:"))
        mon_layout.addWidget(self.monitor_list)
        self.monitor_list.currentIndexChanged.connect(self.on_monitor_change)

        # Resolution
        res_layout = QHBoxLayout()
        res_layout.addWidget(QLabel("Resolution:"))
        self.res_combo = QComboBox()
        res_layout.addWidget(self.res_combo, 1)
        mon_layout.addLayout(res_layout)

        # Refresh
        ref_layout = QHBoxLayout()
        ref_layout.addWidget(QLabel("Refresh rate:"))
        self.ref_combo = QComboBox()
        ref_layout.addWidget(self.ref_combo, 1)
        mon_layout.addLayout(ref_layout)

        # Apply button
        self.apply_btn = QPushButton("Apply Display Settings")
        self.apply_btn.clicked.connect(self.apply_display)
        mon_layout.addWidget(self.apply_btn)

        layout.addWidget(mon_group)
        layout.addStretch()

    def load_current(self):
        """Read current xrandr state and populate widgets."""
        try:
            output = subprocess.check_output(
                ["xrandr", "--current"], stderr=subprocess.DEVNULL, timeout=5
            ).decode()
        except Exception:
            self.monitor_list.addItem("No display detected")
            return

        self.monitors = {}
        current_mon = None
        for line in output.splitlines():
            if " connected " in line:
                current_mon = line.split()[0]
                self.monitors[current_mon] = {"resolutions": [], "current": None}
                self.monitor_list.addItem(current_mon)
            elif current_mon and "connected" not in line and line.strip():
                parts = line.strip().split()
                if parts and "x" in parts[0] and parts[0][0].isdigit():
                    res = parts[0]
                    hz = parts[1].split("*")[0] if len(parts) > 1 else "60"
                    is_current = "*" in parts[1] if len(parts) > 1 else False
                    if res not in [r[0] for r in self.monitors[current_mon]["resolutions"]]:
                        self.monitors[current_mon]["resolutions"].append((res, hz, is_current))
                    if is_current:
                        self.monitors[current_mon]["current"] = (res, hz)

        if self.monitor_list.count() > 0:
            self.monitor_list.setCurrentIndex(0)
            self.on_monitor_change(0)

    def on_monitor_change(self, index):
        if index < 0:
            return
        mon_name = self.monitor_list.currentText()
        if mon_name not in self.monitors:
            return
        mon = self.monitors[mon_name]

        self.res_combo.blockSignals(True)
        self.ref_combo.blockSignals(True)

        self.res_combo.clear()
        seen_res = set()
        for res, hz, _ in mon["resolutions"]:
            if res not in seen_res:
                self.res_combo.addItem(res)
                seen_res.add(res)

        if mon["current"]:
            idx = self.res_combo.findText(mon["current"][0])
            if idx >= 0:
                self.res_combo.setCurrentIndex(idx)
            self.update_refresh_rates(mon["current"][0])

        self.res_combo.blockSignals(False)
        self.ref_combo.blockSignals(False)

    def update_refresh_rates(self, res):
        self.ref_combo.clear()
        mon_name = self.monitor_list.currentText()
        if mon_name in self.monitors:
            hz_list = []
            for r, hz, _ in self.monitors[mon_name]["resolutions"]:
                if r == res:
                    hz_list.append(hz)
            for hz in sorted(set(hz_list), key=float, reverse=True):
                self.ref_combo.addItem(f"{hz} Hz", hz)

    def apply_display(self):
        mon = self.monitor_list.currentText()
        res = self.res_combo.currentText()
        hz = self.ref_combo.currentData()
        if not mon or not res or not hz:
            QMessageBox.warning(self, "Error", "Please select valid settings")
            return
        try:
            subprocess.run(
                ["xrandr", "--output", mon, "--mode", res, "--rate", str(hz), "--primary"],
                check=True, timeout=10
            )
            QMessageBox.information(self, "Display", "Settings applied successfully!")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "Error", f"Failed to apply settings:\n{e}")


class AppearancePage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_current()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Appearance")
        title.setObjectName("pageTitle")
        desc = QLabel("Theme, fonts, and visual style")
        desc.setObjectName("pageDesc")
        layout.addWidget(title)
        layout.addWidget(desc)

        # Qt Style
        style_group = QGroupBox("Qt Style")
        style_layout = QGridLayout(style_group)
        style_layout.addWidget(QLabel("Widget style:"), 0, 0)
        self.style_combo = QComboBox()
        self.style_combo.addItems(QStyleFactory.keys())
        style_layout.addWidget(self.style_combo, 0, 1)
        layout.addWidget(style_group)

        # Fonts
        font_group = QGroupBox("Fonts")
        font_layout = QGridLayout(font_group)
        font_layout.addWidget(QLabel("Interface font:"), 0, 0)
        self.font_combo = QFontComboBox()
        font_layout.addWidget(self.font_combo, 0, 1)

        font_layout.addWidget(QLabel("Font size:"), 1, 0)
        self.size_spin = QSpinBox()
        self.size_spin.setRange(6, 48)
        self.size_spin.setValue(10)
        font_layout.addWidget(self.size_spin, 1, 1)
        layout.addWidget(font_group)

        # Buttons
        btn_layout = QHBoxLayout()
        self.apply_btn = QPushButton("Apply Appearance")
        self.apply_btn.clicked.connect(self.apply_appearance)
        btn_layout.addStretch()
        btn_layout.addWidget(self.apply_btn)
        layout.addLayout(btn_layout)
        layout.addStretch()

    def load_current(self):
        config = configparser.ConfigParser()
        config.read(str(LXQT_CONF))
        if config.has_section("Qt"):
            style = config.get("Qt", "style", fallback="Fusion")
            idx = self.style_combo.findText(style)
            if idx >= 0:
                self.style_combo.setCurrentIndex(idx)

            font_str = config.get("Qt", "font", fallback="")
            if font_str:
                parts = font_str.split(",")
                if len(parts) >= 2:
                    self.font_combo.setCurrentText(parts[0])
                    try:
                        self.size_spin.setValue(int(parts[1]))
                    except ValueError:
                        pass

    def apply_appearance(self):
        """Write appearance settings to lxqt.conf."""
        config = configparser.ConfigParser()
        if LXQT_CONF.exists():
            config.read(str(LXQT_CONF))

        if not config.has_section("Qt"):
            config.add_section("Qt")

        style = self.style_combo.currentText()
        config.set("Qt", "style", style)

        font_name = self.font_combo.currentFont().family()
        font_size = str(self.size_spin.value())
        config.set("Qt", "font", f"{font_name},{font_size},-1,5,400,0,0,0,0,0,0,0,0,0,0,1,,0,0")

        try:
            with open(str(LXQT_CONF), "w") as f:
                config.write(f)

            # Apply immediately
            QApplication.setStyle(style)
            font = QFont(font_name, int(font_size))
            QApplication.setFont(font)

            QMessageBox.information(self, "Appearance",
                "Settings saved! Log out and back in for full effect.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")


class SessionPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
        self.load_current()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)

        title = QLabel("Session")
        title.setObjectName("pageTitle")
        desc = QLabel("Window manager, autostart, and session behavior")
        desc.setObjectName("pageDesc")
        layout.addWidget(title)
        layout.addWidget(desc)

        # Window Manager
        wm_group = QGroupBox("Window Manager")
        wm_layout = QGridLayout(wm_group)
        wm_layout.addWidget(QLabel("Window manager:"), 0, 0)
        self.wm_combo = QComboBox()
        self.wm_combo.addItems(["bspwm", "openbox", "i3", "herbstluftwm", "qtile", "awesome", "dwm", "other"])
        self.wm_combo.setEditable(True)
        wm_layout.addWidget(self.wm_combo, 0, 1)
        self.wm_apply = QPushButton("Set Window Manager")
        wm_layout.addWidget(self.wm_apply, 1, 1)
        layout.addWidget(wm_group)

        # Autostart
        autostart_group = QGroupBox("Autostart Applications")
        autostart_layout = QVBoxLayout(autostart_group)

        self.autostart_list = QListWidget()
        self.autostart_list.setAlternatingRowColors(True)
        autostart_layout.addWidget(self.autostart_list)

        as_btn_layout = QHBoxLayout()
        self.add_as_btn = QPushButton("Add Application")
        self.remove_as_btn = QPushButton("Remove Selected")
        self.remove_as_btn.setObjectName("danger")
        as_btn_layout.addWidget(self.add_as_btn)
        as_btn_layout.addWidget(self.remove_as_btn)
        as_btn_layout.addStretch()
        autostart_layout.addLayout(as_btn_layout)

        layout.addWidget(autostart_group)

        # Connections
        self.wm_apply.clicked.connect(self.apply_wm)
        self.add_as_btn.clicked.connect(self.add_autostart)
        self.remove_as_btn.clicked.connect(self.remove_autostart)
        self.refresh_autostart()

    def load_current(self):
        config = configparser.ConfigParser()
        config.read(str(SESSION_CONF))
        if config.has_section("General"):
            wm = config.get("General", "window_manager", fallback="bspwm")
            idx = self.wm_combo.findText(wm)
            if idx >= 0:
                self.wm_combo.setCurrentIndex(idx)
            else:
                self.wm_combo.setEditText(wm)

    def apply_wm(self):
        wm = self.wm_combo.currentText().strip().lower()
        if not wm:
            QMessageBox.warning(self, "Error", "Please enter a window manager")
            return

        os.makedirs(str(CONFIG_DIR), exist_ok=True)

        # Check if WM is installed
        wm_path = subprocess.run(["which", wm], capture_output=True, text=True, timeout=5)
        if wm_path.returncode != 0:
            reply = QMessageBox.question(self, "Not Found",
                f"'{wm}' is not in your PATH. Set it anyway?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            if reply == QMessageBox.StandardButton.No:
                return

        try:
            # Write session.conf
            config = configparser.ConfigParser()
            config["General"] = {"__userfile__": "true", "window_manager": wm}
            with open(str(SESSION_CONF), "w") as f:
                config.write(f)

            # Write .desktop entry for DM
            desktop_dir = Path.home() / ".local" / "share" / "xsessions"
            desktop_dir.mkdir(parents=True, exist_ok=True)
            with open(desktop_dir / "sprunglesqt.desktop", "w") as f:
                f.write(f"""[Desktop Entry]
Type=Application
Exec=startlxqt
TryExec=lxqt-session
DesktopNames=SprunglesQT;LXQt
Name=SprunglesQT Desktop
Comment=The ultra-lightweight Qt desktop
""")
            QMessageBox.information(self, "Session",
                f"Window manager set to '{wm}'.\nLog out to use SprunglesQT.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save:\n{e}")

    def refresh_autostart(self):
        self.autostart_list.clear()
        AUTOSTART_DIR.mkdir(parents=True, exist_ok=True)
        for f in sorted(AUTOSTART_DIR.iterdir()):
            if f.suffix == ".desktop":
                config = configparser.ConfigParser()
                config.read(str(f))
                name = "Unknown"
                if config.has_section("Desktop Entry"):
                    name = config.get("Desktop Entry", "Name", fallback=f.stem)
                hidden = False
                if config.has_section("Desktop Entry"):
                    hidden = config.getboolean("Desktop Entry", "Hidden", fallback=False)
                if not hidden:
                    item = QListWidgetItem(f"{name}  ({f.name})")
                    item.setData(Qt.ItemDataRole.UserRole, str(f))
                    self.autostart_list.addItem(item)

    def add_autostart(self):
        path, _ = QFileDialog.getOpenFileName(
            self, "Select Application", "/usr/share/applications",
            "Desktop files (*.desktop);;All files (*)"
        )
        if not path:
            return

        # Parse the .desktop file
        config = configparser.ConfigParser()
        config.read(path)
        name = "App"
        exec_cmd = ""
        if config.has_section("Desktop Entry"):
            name = config.get("Desktop Entry", "Name", fallback="App")
            exec_cmd = config.get("Desktop Entry", "Exec", fallback="")

        if not exec_cmd:
            QMessageBox.warning(self, "Error", "Could not parse Exec line")
            return

        # Create autostart entry
        dest = AUTOSTART_DIR / f"{Path(path).stem}.desktop"
        with open(str(dest), "w") as f:
            f.write(f"""[Desktop Entry]
Type=Application
Name={name}
Exec={exec_cmd}
Terminal=false
""")
        self.refresh_autostart()

    def remove_autostart(self):
        item = self.autostart_list.currentItem()
        if not item:
            QMessageBox.warning(self, "Error", "Select an item to remove")
            return
        path = item.data(Qt.ItemDataRole.UserRole)
        reply = QMessageBox.question(self, "Confirm",
            f"Remove '{item.text()}' from autostart?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            try:
                Path(path).unlink()
                self.refresh_autostart()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to remove:\n{e}")


class AboutPage(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Logo area
        logo_label = QLabel()
        pixmap = self.create_logo(96)
        logo_label.setPixmap(pixmap)
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(logo_label)

        name = QLabel("SprunglesQT")
        name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = QFont()
        font.setPointSize(28)
        font.setBold(True)
        name.setFont(font)
        name.setStyleSheet("color: #9b59b6;")
        layout.addWidget(name)

        ver = QLabel("Version 2.4 — Based on LXQt")
        ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        ver.setStyleSheet("color: #9a9a9a; font-size: 13px;")
        layout.addWidget(ver)

        separator = QFrame()
        separator.setObjectName("separator")
        separator.setFrameShape(QFrame.Shape.HLine)
        layout.addWidget(separator)
        layout.addSpacing(12)

        desc = QLabel(
            "The ultra-lightweight Qt desktop.\n"
            "Stripped of bloat, built for speed, powered by caffeine.\n\n"
            "A fork of LXQt — only the essentials remain:\n"
            "session, panel, taskbar, and your workflow.\n\n"
            '"Your coffee-break digital twin"'
        )
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("color: #b0b0b0; font-size: 13px; line-height: 1.6;")
        layout.addWidget(desc)

        layout.addSpacing(16)

        repo = QLabel(
            '<a href="https://github.com/spivanatalie64/SprunglesQT" '
            'style="color: #756cf0;">github.com/spivanatalie64/SprunglesQT</a>'
        )
        repo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        repo.setOpenExternalLinks(True)
        repo.setStyleSheet("font-size: 13px;")
        layout.addWidget(repo)

        layout.addStretch()

    def create_logo(self, size):
        pixmap = QPixmap(size, size)
        pixmap.fill(Qt.GlobalColor.transparent)
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Coffee cup body
        painter.setPen(QColor("#9b59b6"))
        painter.setBrush(QColor("#6f42c1"))
        painter.drawRoundedRect(size//6, size//3, size*3//5, size*5//12, 4, 4)

        # Coffee surface
        painter.setBrush(QColor("#e8d5f5").lighter(130))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRoundedRect(size//5, size//3 + 4, size*9//20, size//8, 2, 2)

        # Handle
        painter.setPen(QPen(QColor("#9b59b6"), 3))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        cx = size * 2 // 3 + 4
        cy = size * 5 // 12
        painter.drawArc(cx, cy, size//4, size//3, 0, 180 * 16)

        # Steam
        painter.setPen(QPen(QColor("#b8a0d4"), 2))
        for dx in [-1, 0, 1]:
            sx = size // 3 + dx * size // 5
            sy = size // 4
            painter.drawLine(sx, sy, sx - 4, sy - 10)
            painter.drawLine(sx - 4, sy - 10, sx, sy - 20)

        # Lightning bolt
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QColor("#f1c40f"))
        s = size
        poly = QPolygonF([
            QPointF(s * 9 / 16, s * 5 / 8),
            QPointF(s * 7 / 16, s * 7 / 8),
            QPointF(s * 9 / 16, s * 7 / 8),
            QPointF(s * 7 / 16, s),
            QPointF(s * 5 / 8, s * 3 / 4),
            QPointF(s * 9 / 16, s * 3 / 4),
        ])
        painter.drawPolygon(poly)

        painter.end()
        return pixmap


# ─── Main Window ─────────────────────────────────────────────────────────────

class SprunglesSettings(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("SprunglesQT Settings")
        self.setMinimumSize(800, 560)
        self.setup_ui()

    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Navigation sidebar
        self.nav = QListWidget()
        self.nav.setIconSize(QSize(0, 0))
        self.nav.setMaximumWidth(200)
        self.nav.setMinimumWidth(180)
        self.nav.setSpacing(2)

        # Pages stack
        self.pages = QStackedWidget()

        # Create pages
        self.display_page = DisplayPage()
        self.appearance_page = AppearancePage()
        self.session_page = SessionPage()
        self.about_page = AboutPage()

        self.pages.addWidget(self.display_page)
        self.pages.addWidget(self.appearance_page)
        self.pages.addWidget(self.session_page)
        self.pages.addWidget(self.about_page)

        # Nav items
        pages_data = [
            ("🖥️  Display", 0),
            ("🎨  Appearance", 1),
            ("⚙️  Session", 2),
            ("☕  About SprunglesQT", 3),
        ]
        for label, idx in pages_data:
            item = QListWidgetItem(label)
            item.setData(Qt.ItemDataRole.UserRole, idx)
            self.nav.addItem(item)

        self.nav.setCurrentRow(0)
        self.nav.currentRowChanged.connect(self.on_nav_change)
        self.pages.setCurrentIndex(0)

        layout.addWidget(self.nav)
        layout.addWidget(self.pages, 1)

    def on_nav_change(self, row):
        if row >= 0:
            self.pages.setCurrentIndex(row)


# ─── Entry Point ─────────────────────────────────────────────────────────────

def main():
    QApplication.setStyle("Fusion")

    app = QApplication(sys.argv)
    app.setApplicationName("SprunglesQT Settings")
    app.setStyleSheet(STYLESHEET)

    # Set dark palette
    palette = QPalette()
    palette.setColor(QPalette.ColorRole.Window, QColor("#2b2b2b"))
    palette.setColor(QPalette.ColorRole.WindowText, QColor("#d4d4d4"))
    palette.setColor(QPalette.ColorRole.Base, QColor("#1e1e1e"))
    palette.setColor(QPalette.ColorRole.AlternateBase, QColor("#333333"))
    palette.setColor(QPalette.ColorRole.ToolTipBase, QColor("#323232"))
    palette.setColor(QPalette.ColorRole.ToolTipText, QColor("#d4d4d4"))
    palette.setColor(QPalette.ColorRole.Text, QColor("#d4d4d4"))
    palette.setColor(QPalette.ColorRole.Button, QColor("#2b2b2b"))
    palette.setColor(QPalette.ColorRole.ButtonText, QColor("#d4d4d4"))
    palette.setColor(QPalette.ColorRole.BrightText, QColor("#ffffff"))
    palette.setColor(QPalette.ColorRole.Highlight, QColor("#3d427e"))
    palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    app.setPalette(palette)

    window = SprunglesSettings()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
