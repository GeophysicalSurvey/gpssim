# -*- mode: python -*-
a = Analysis([os.path.join(HOMEPATH,'support\\_mountzlib.py'), os.path.join(HOMEPATH,'support\\unpackTK.py'), os.path.join(HOMEPATH,'support\\useTK.py'), os.path.join(HOMEPATH,'support\\useUnicode.py'), '..\uilauncher.py', os.path.join(HOMEPATH,'support\\removeTK.py')])
pyz = PYZ(a.pure)
exe = EXE(TkPKG(), pyz,
	a.scripts,
	a.binaries,
	a.zipfiles,
	a.datas,
	name=os.path.join('dist', 'gpssim.exe'),
	debug=False,
	strip=False,
	upx=True,
	console=True,
	version='versioninfo')
