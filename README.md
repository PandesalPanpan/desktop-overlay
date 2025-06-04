# Desktop Overlay

A customizable desktop overlay application for **Windows** that creates a colored border around your screen(s) to help you stay focused while studying or working.

## Features

- **Multi-monitor support** - Automatically detects and overlays all connected monitors
- **Customizable colors** - Choose any color via color picker dialog
- **Color persistence** - Your chosen color is automatically saved and restored
- **Blur effects** - Smooth, translucent borders with Gaussian blur
- **Click-through overlay** - Won't interfere with normal window interactions
- **System tray integration** - Easy control via system tray icon
- **Global hotkey** - Toggle overlay with F8 key
- **Lightweight** - Minimal system resources usage
- **No installation required** - Standalone executable

## Installation

### Option 1: Download Executable (Recommended)
1. Download `desktop-overlay.exe` from the releases
2. Place it anywhere on your Windows computer
3. Double-click to run

### Option 2: Build from Source
1. Clone or download this repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Build the executable:
   ```bash
   python build.py
   ```
4. Find the executable in the `dist` folder

## Usage

### Starting the Application
- **Executable**: Double-click `desktop-overlay.exe`
- **From source**: Run `python overlay.py`

### Controls

#### System Tray Icon
The application adds a colored square icon to your system tray with these options:
- **Toggle Overlay (F8)** - Show/hide the overlay
- **Change Color...** - Open color picker to customize overlay color
- **Exit** - Close the application

#### Keyboard Shortcuts
- **F8** - Toggle overlay visibility (works globally, even when other apps are focused)

#### Color Customization
1. Right-click the system tray icon
2. Select "Change Color..."
3. Choose your preferred color from the color picker
4. Click OK to apply immediately
5. Your color choice is automatically saved for next time

### Multiple Monitors
The overlay automatically detects all connected monitors and creates borders on each one. When you change colors or toggle visibility, all monitors are updated simultaneously.

### Study/Work Sessions
The overlay is designed to create a visual cue that you're in a focused work mode:
- Choose a specific color for different types of work (blue for studying, green for coding, etc.)
- The subtle border reminds you to stay focused without being distracting
- Toggle on/off easily with F8 when you need breaks

## Configuration

Settings are automatically saved to `overlay_config.json` in the same directory as the executable:
- **Color preferences** - Your last chosen color
- **Future settings** - Additional customization options may be added

## Troubleshooting

### System Tray Icon Not Visible
- Check if your system tray is visible (click the up arrow in the taskbar)
- The icon appears as a colored square matching your overlay color

### Overlay Not Click-Through
- Restart the application if click-through stops working
- Make sure you're running the latest version

### F8 Key Not Working
- Ensure no other application is using F8 as a global hotkey
- Try running the application as administrator if needed

### Color Changes Not Applying
- If colors don't change immediately, try toggling the overlay off and on with F8
- Restart the application if the issue persists

## Technical Details

- **Platform**: Windows-only (uses Windows-specific APIs for click-through functionality)
- **Framework**: PyQt5 for GUI and window management
- **Global hotkeys**: keyboard library for F8 detection
- **Windows integration**: win32gui for click-through functionality
- **Multi-monitor**: Automatic screen detection and overlay placement
- **Transparency**: Advanced layered window techniques with blur effects

## System Requirements

- **Windows 10/11** (required - Windows-only application)
- **Multiple monitor support** (optional)
- **Python 3.7+** (if running from source)

**Note**: This application is designed specifically for Windows and uses Windows-specific APIs. It will not work on macOS or Linux.

## Development

To modify or extend the application:

1. Install development dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run from source:
   ```bash
   python overlay.py
   ```

3. Build new executable:
   ```bash
   python build.py
   ```

## License

This project is open source. Feel free to modify and distribute.

## Changelog

### Latest Version
- **F8 hotkey** for toggle (changed from Ctrl+Shift+O)
- **Color customization** with immediate application
- **Color persistence** across sessions
- **Multi-monitor support**
- **Improved system tray integration**
- **Click-through overlay** that doesn't block interactions
- **Blur effects** for smooth, professional appearance 