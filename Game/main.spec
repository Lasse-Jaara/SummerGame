# -*- mode: python ; coding: utf-8 -*-
import os

# Include Assets folder and all contents
datas = []
assets_folder = 'Assets'
for root, dirs, files in os.walk(assets_folder):
    for file in files:
        full_path = os.path.join(root, file)
        rel_path = os.path.relpath(root, '.')  # keep folder structure
        datas.append((full_path, rel_path))

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
