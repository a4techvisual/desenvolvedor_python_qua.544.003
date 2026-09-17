# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hidden = collect_submodules('webview')
a = Analysis(['main.py'], pathex=[], binaries=[], datas=[
    ('index', 'index'),
    ('image', 'image'),
    ('font', 'font'),
], hiddenimports=hidden, hookspath=[], hooksconfig={}, runtime_hooks=[], excludes=[], noarchive=False)
pyz = PYZ(a.pure)
exe = EXE(pyz, a.scripts, a.binaries, a.datas, [], name='Git Poltergeist v2.0', debug=False, bootloader_ignore_signals=False, strip=False, upx=True, console=False, icon='image/image.ico')
