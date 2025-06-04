import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QGraphicsBlurEffect
from PyQt5.QtCore import Qt, QRect, QRectF
from PyQt5.QtGui import QColor, QPainter, QPainterPath

class OverlayWindow(QMainWindow):
    def __init__(self, screen_geometry):
        super().__init__()
        # Set window flags to make it stay on top and borderless
        self.setWindowFlags(
            Qt.FramelessWindowHint |  # No window frame
            Qt.WindowStaysOnTopHint |  # Always on top
            Qt.Tool  # No taskbar icon
        )
        
        # Make the window transparent
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        # Set geometry for this specific screen
        self.setGeometry(screen_geometry)
        
        # Border settings
        self.border_width = 20  # Increased width for better blur effect
        self.border_color = QColor(0, 120, 255, 100)  # More transparent blue
        
        # Create blur effect
        self.blur_effect = QGraphicsBlurEffect()
        self.blur_effect.setBlurRadius(15)  # Adjust blur intensity
        self.setGraphicsEffect(self.blur_effect)
        
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

def main():
    app = QApplication(sys.argv)
    
    # Create an overlay window for each screen
    windows = []
    for screen in app.screens():
        window = OverlayWindow(screen.geometry())
        window.show()
        windows.append(window)
    
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
