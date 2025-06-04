import PyInstaller.__main__

PyInstaller.__main__.run([
    'overlay.py',
    '--onefile',
    '--noconsole',
    '--name=desktop-overlay',
    '--icon=NONE',
    '--add-data=README.md;.'
]) 