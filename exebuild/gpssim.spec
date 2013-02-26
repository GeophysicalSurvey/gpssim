# -*- mode: python -*-
a = Analysis(['../uilauncher.py'],
             hiddenimports=[],
             hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,
          name=os.path.join('dist', 'gpssim.exe'),
          debug=False,
          strip=None,
          upx=True,
          console=True , version='versioninfo')
