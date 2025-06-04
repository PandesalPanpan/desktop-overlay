import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsBlurEffect, QSystemTrayIcon, QMenu, QAction, QColorDialog, QWidget
from PyQt5.QtCore import Qt, QRect, QRectF, QTimer
from PyQt5.QtGui import QColor, QPainter, QPainterPath, QIcon, QPixmap
from PyQt5.QtCore import QObject, pyqtSignal
import keyboard
import win32gui
import win32con

CONFIG_FILE = "overlay_config.json"

def save_config(color):
    """Save the current color to a config file"""
    try:
        config = {
            "color": {
                "red": color.red(),
                "green": color.green(),
                "blue": color.blue()
            }
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(config, f)
    except Exception as e:
        print(f"Error saving config: {e}")

def load_config():
    """Load the saved color from config file"""
    try:
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                config = json.load(f)
                color_data = config.get("color", {})
                return QColor(
                    color_data.get("red", 0),
                    color_data.get("green", 120),
                    color_data.get("blue", 255)
                )
    except Exception as e:
        print(f"Error loading config: {e}")
    
    # Return default color if loading fails
    return QColor(0, 120, 255)

class OverlayManager(QObject):
    toggle_signal = pyqtSignal()
    color_changed_signal = pyqtSignal(QColor)

    def __init__(self):
        super().__init__()
        # Register the hotkey - F8 is rarely used by applications
        keyboard.add_hotkey('F8', self.toggle_overlay)

    def toggle_overlay(self):
        self.toggle_signal.emit()
    
    def change_color(self, color):
        self.color_changed_signal.emit(color)

class OverlayWindow(QMainWindow):
    def __init__(self, screen_geometry, initial_color):
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
        self.border_color = QColor(initial_color.red(), initial_color.green(), initial_color.blue(), 100)
        
        # Create blur effect and keep reference
        self.blur_effect = QGraphicsBlurEffect(self)
        self.blur_effect.setBlurRadius(15)  # Adjust blur intensity
        self.setGraphicsEffect(self.blur_effect)

    def showEvent(self, event):
        super().showEvent(event)
        # Use a timer to set the click-through properties after the window is fully shown
        QTimer.singleShot(100, self.setup_click_through)

    def setup_click_through(self):
        try:
            # Make window click-through using win32gui
            hwnd = self.winId().__int__()
            # Get current window style
            style = win32gui.GetWindowLong(hwnd, win32con.GWL_EXSTYLE)
            # Add WS_EX_TRANSPARENT for click-through
            style |= win32con.WS_EX_TRANSPARENT
            # Set the new style
            win32gui.SetWindowLong(hwnd, win32con.GWL_EXSTYLE, style)
        except Exception as e:
            print(f"Warning: Could not set click-through: {e}")
        
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

class OverlayWindowManager(QObject):
    def __init__(self, app):
        super().__init__()
        self.app = app
        self.windows = []
        self.current_color = QColor(0, 120, 255)
        self.windows_visible = True
        
    def create_windows(self, color):
        """Create overlay windows for all screens"""
        # Close existing windows
        self.close_windows()
        
        # Create new windows with the specified color
        self.current_color = color
        self.windows = []
        
        for screen in self.app.screens():
            window = OverlayWindow(screen.geometry(), color)
            if self.windows_visible:
                window.show()
            self.windows.append(window)
    
    def close_windows(self):
        """Close all existing windows"""
        for window in self.windows:
            window.close()
            window.deleteLater()
        self.windows = []
    
    def toggle_visibility(self):
        """Toggle visibility of all windows"""
        self.windows_visible = not self.windows_visible
        for window in self.windows:
            window.setVisible(self.windows_visible)
    
    def update_color(self, color):
        """Update color by recreating all windows"""
        self.create_windows(color)

def create_tray_icon(color=QColor(0, 120, 255)):
    # Create a simple colored square icon
    pixmap = QPixmap(32, 32)
    pixmap.fill(Qt.transparent)
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.Antialiasing)
    painter.setBrush(color)
    painter.setPen(Qt.NoPen)
    painter.drawRoundedRect(4, 4, 24, 24, 4, 4)
    painter.end()
    return QIcon(pixmap)

class ColorChanger(QObject):
    color_selected = pyqtSignal(QColor)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        
    def show_color_dialog(self, current_color):
        # Use QTimer to delay the dialog to avoid event loop issues
        QTimer.singleShot(100, lambda: self._show_dialog(current_color))
        
    def _show_dialog(self, current_color):
        try:
            color = QColorDialog.getColor(current_color, None, "Choose Overlay Color")
            if color.isValid():
                self.color_selected.emit(color)
        except Exception as e:
            print(f"Error in color dialog: {e}")

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)  # Prevent app from closing when dialogs close
    
    # Load saved color or use default
    current_color = load_config()
    print(f"Loaded color: {current_color.name()}")
    
    # Create overlay window manager
    window_manager = OverlayWindowManager(app)
    
    # Create system tray icon with custom icon
    tray_icon = QSystemTrayIcon()
    tray_icon.setIcon(create_tray_icon(current_color))
    tray_icon.setToolTip('Desktop Overlay (F8 to toggle)')
    
    # Create tray menu
    tray_menu = QMenu()
    
    # Create toggle action
    toggle_action = QAction('Toggle Overlay (F8)', tray_menu)
    tray_menu.addAction(toggle_action)
    
    # Create color change action
    color_action = QAction('Change Color...', tray_menu)
    tray_menu.addAction(color_action)
    
    # Add separator
    tray_menu.addSeparator()
    
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
    
    # Create color changer
    color_changer = ColorChanger()
    
    # Create initial overlay windows
    window_manager.create_windows(current_color)
    
    # Connect signals
    def update_color(color):
        nonlocal current_color
        current_color = color
        print(f"Color changed to: {color.name()}")
        
        # Save the new color
        save_config(color)
        
        # Update overlay windows by recreating them
        window_manager.update_color(color)
        
        # Update tray icon to match new color
        tray_icon.setIcon(create_tray_icon(color))
    
    def change_overlay_color():
        color_changer.show_color_dialog(current_color)
    
    toggle_action.triggered.connect(window_manager.toggle_visibility)
    color_action.triggered.connect(change_overlay_color)
    color_changer.color_selected.connect(update_color)
    overlay_manager.toggle_signal.connect(window_manager.toggle_visibility)
    exit_action.triggered.connect(app.quit)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
