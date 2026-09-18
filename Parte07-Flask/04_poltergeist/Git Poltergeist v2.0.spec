# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['C:/Users/ALUNO/Rômulo Delalíbera Júnior/desenvolvedor_python_qua.544.003/Parte07-Flask/04_poltergeist/main.pyw'],
    pathex=[],
    binaries=[],
    datas=[],
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
    name='Git Poltergeist v2.0',
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
    icon=['C:/Users/ALUNO/Rômulo Delalíbera Júnior/desenvolvedor_python_qua.544.003/Parte07-Flask/04_poltergeist/image/image.ico'],
)
