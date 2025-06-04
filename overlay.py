import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsBlurEffect, QSystemTrayIcon, QMenu, QAction
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QIcon, QPixmap
from PyQt5.QtCore import QObject, pyqtSignal
import keyboard
import win32gui
import win32con

class OverlayManager(QObject):
    toggle_signal = pyqtSignal()

    def __init__(self):
        super().__init__()
        # Register the hotkey
        keyboard.add_hotkey('ctrl+shift+o', self.toggle_overlay)

    def toggle_overlay(self):
        self.toggle_signal.emit()

class OverlayWindow(QMainWindow):
    def __init__(self, screen_geometry):
        super().__init__()
        # Set window flags to make it stay on top and borderless
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # No window frame
            Qt.WindowStaysOnTopHint |  # Always on top
            Qt.Tool |  # No taskbar icon
            Qt.NoDropShadowWindowHint  # No shadow
        )
        
        # Make the window transparent and click-through
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_NoSystemBackground)
        self.setAttribute(Qt.WA_ShowWithoutActivating)
        
        # Set geometry for this specific screen
        self.setGeometry(screen_geometry)
        
        # Border settings
        self.border_width = 20  # Increased width for better blur effect
        self.border_color = QColor(0, 120, 255, 100)  # More transparent blue
        
        # Create blur effect
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(15)  # Adjust blur intensity
        self.setGraphicsEffect(self.blur_effect)

    def showEvent(self, event):
        super().showEvent(event)
        # Make window click-through using win32gui
        hwnd = self.winId().__int__()
        # Get current window style
        style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
        # Add WS_EX_TRANSPARENT and WS_EX_LAYERED
        style |= win32con.WS_EX_TRANSPARENT | win32con.WS_EX_LAYERED
        # Set the new style
        win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
        
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Create a path for the border
        path = QPainterPath()
        
        # Add outer rectangle
        path.addRect(QRectF(0, 0, self.width(), self.height()))
        
        # Add inner rectangle (creating the border effect)
        inner_rect = QRectF(
            self.border_width,
            self.border_width,
            self.width() - 2 * self.border_width,
            self.height() - 2 * self.border_width
        )
        path.addRect(inner_rect)
        
        # Fill the path with the border color
        painter.setPen(Qt.NoPen)
        painter.setBrush(self.border_color)
        painter.drawPath(path)

def create_tray_icon():
    # Create a simple blue square icon
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(QColor(0, 120, 255))
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, 24, 24, 4, 4)
    painter.end()
    return QIcon(pixmap)

def main():
    app = QApplication(sys.argv)
    
    # Create system tray icon with custom icon
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(create_tray_icon())
    tray_icon.setToolTip('Desktop Overlay (Ctrl+Shift+O to toggle)')
    
    # Create tray menu
    tray_menu = QMenu()
    
    # Create toggle action
    toggle_action = QAction('Toggle Overlay (Ctrl+Shift+O)', tray_menu)
    tray_menu.addAction(toggle_action)
    
    # Create exit action
    exit_action = QAction('Exit', tray_menu)
    tray_menu.addAction(exit_action)
    
    # Set the tray menu
    tray_icon.setContextMenu(tray_menu)
    
    # Show the tray icon
    if not QSystemTrayIcon.isSystemTrayAvailable():
        print("System tray is not available")
        sys.exit(1)
    
    tray_icon.show()
    
    # Create overlay manager for hotkey
    overlay_manager = OverlayManager()
    
    # Create overlay windows for each screen
    windows = []
    for screen in app.screens():
        window = OverlayWindow(screen.geometry())
        window.show()
        windows.append(window)
    
    # Connect signals
    def toggle_overlays():
        for window in windows:
            window.setVisible(not window.isVisible())
    
    toggle_action.triggered.connect(toggle_overlays)
    overlay_manager.toggle_signal.connect(toggle_overlays)
    exit_action.triggered.connect(app.quit)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
