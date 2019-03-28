# -*- mode: python -*-

block_cipher = None


a = Analysis(['MyShow.py'],
             pathex=['D:\\Program Files\\Python3.6.4\\Lib\\site-packages\\PyQt5\\Qt\x08in', 'D:\\Program Files\\Python3.6.4\\Lib\\site-packages\\PyQt5\\Qt\\plugins', 'E:\\34 Gold Time Management\\ÀúÊ·°æ±¾\\My Py Gui(V1.6)\\1'],
             binaries=[],
             datas=[],
             hiddenimports=['queue'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='MyShow',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , icon='Calender.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='MyShow')
