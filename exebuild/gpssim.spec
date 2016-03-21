# -*- mode: python -*-

import subprocess
from .. import versioning
versionnumberstring = versioning.vcs_version()
exename = 'gpssim-%s.exe' % (versionnumberstring)

with open('versionnumberstring', 'w') as file:
	file.write(versionnumberstring)

major, minor, patch, build = versionnumberstring.split('.')

versionstring =  "VSVersionInfo("
versionstring += 	"ffi=FixedFileInfo("
versionstring += 		"filevers=(%s, %s, %s, %s)," % (major, minor, patch, build)
versionstring += 		"prodvers=(%s, %s, %s, %s)," % (major, minor, patch, build)
versionstring += 		"mask=0x1f,"
versionstring += 		"flags=0x0,"
versionstring += 		"OS=0x4,"
versionstring += 		"fileType=0x1,"
versionstring += 		"subtype=0x0,"
versionstring += 		"date=(0, 0)"
versionstring += 	"),"
versionstring += 	"kids=["
versionstring += 		"StringFileInfo("
versionstring += 			"["
versionstring += 				"StringTable("
versionstring += 					"'040904b0',"
versionstring += 					"["
versionstring += 						"StringStruct('Comments', 'https://bitbucket.org/wjiang/gpssim/'),"
versionstring += 						"StringStruct('CompanyName', 'Wei Li Jiang'),"
versionstring += 						"StringStruct('FileDescription', 'Python GPS Simulator'),"
versionstring += 						"StringStruct('FileVersion', '%s, %s, %s, %s')," % (major, minor, patch, build)
versionstring += 						"StringStruct('InternalName', 'gpssim'),"
versionstring += 						"StringStruct('LegalCopyright', 'Copyright (C) 2013 Wei Li Jiang'),"
versionstring += 						"StringStruct('OriginalFilename', '%s')," % (exename)
versionstring += 						"StringStruct('ProductName', 'gpssim'),"
versionstring += 						"StringStruct('ProductVersion', '%s, %s, %s, %s')" % (major, minor, patch, build)
versionstring += 					"]"
versionstring += 				")"
versionstring += 			"]"
versionstring += 		"),"
versionstring += 		"VarFileInfo([VarStruct('Translation', [1033, 1200])])"
versionstring += 	"]"
versionstring += ")"

with open('versioninfo', 'w') as versionfile:
	versionfile.write(versionstring)

a = Analysis(['../uilauncher.py'],
	hiddenimports=[],
	hookspath=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
	a.scripts,
	a.binaries,
	a.zipfiles,
	a.datas,
	[('gpssim.ico', '../gpssim.ico', 'DATA'), ('versionnumberstring', 'versionnumberstring', 'DATA'), ('u', '', 'OPTION')],
	name=os.path.join('dist', exename),
	debug=False,
	strip=None,
	upx=True,
	console=True,
	version='versioninfo',
	icon='../gpssim.ico')
