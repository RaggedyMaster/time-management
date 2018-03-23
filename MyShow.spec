# -*- mode: python -*-

block_cipher = None


a = Analysis(['MyShow.py'],
             pathex=['D:\\Program Files\\Python3.6.4\\Lib\\site-packages\\PyQt5\\Qt\\plugins', 'D:\\Program Files\\Python3.6.4\\Lib\\site-packages\\Crypto', 'E:\\My Py Gui(V1.1)\\My Py Gui'],
             binaries=[],
             datas=[],
             hiddenimports=['queue--paths=D:\\Program Files\\Python3.6.4\\Lib\\site-packages\\PyQt5\\Qt\x08in'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='MyShow',
          debug=False,
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
