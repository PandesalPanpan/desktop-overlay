import PyInstaller.__main__
import os
import time
import sys

def build_executable():
    # Try to remove existing executable if it exists
    exe_path = os.path.join('dist', 'desktop-overlay.exe')
    if os.path.exists(exe_path):
        try:
            os.remove(exe_path)
        except PermissionError:
            print("Error: Cannot remove existing executable. Please make sure it's not running.")
            print("1. Close any running instances of desktop-overlay")
            print("2. Wait a few seconds")
            print("3. Try running this script again")
            sys.exit(1)

    # Wait a moment to ensure file system is ready
    time.sleep(1)

    # Run PyInstaller
    PyInstaller.__main__.run([
        'overlay.py',
        '--onefile',
        '--noconsole',
        '--name=desktop-overlay',
        '--icon=NONE',
        '--add-data=README.md;.',
        '--clean'  # Clean PyInstaller cache
    ])

if __name__ == '__main__':
    build_executable() 