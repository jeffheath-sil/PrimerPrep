# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# define the analysis, archive and executable for the main PrimerPrep.py script
a1 = Analysis(['PrimerPrep.py'],
	# path to Python executable and other essential DLL files
	pathex=['C:\\msys64\\mingw64\\bin'],
	binaries=[],
	# extra files required, along with destination folder
	datas=[('PrimerPrep.glade', '.'), ('PrimerPrep.ico', '.'),
		('Help', 'Help'), ('translations', 'translations')],
	hiddenimports=[],
	hookspath=[],
	runtime_hooks=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher,
	noarchive=False)
pyz1 = PYZ(a1.pure, a1.zipped_data,
	cipher=block_cipher)
exe1 = EXE(pyz1,
	a1.scripts,
	exclude_binaries=True,
	name='PrimerPrep',  # Name of the output executable
	debug=False,
	strip=False,
	upx=True,
	contents_directory='.',
	windowed=True,
	console=False,
	icon='PrimerPrep.ico')

# define the analysis, archive and executable for the PrimerPrepSplash.py script
a2 = Analysis(['PrimerPrepSplash.py'],
	# path to Python executable and other essential DLL files
	pathex=['C:\\msys64\\mingw64\\bin'],
	binaries=[],
	# extra files required, along with destination folder
	datas=[('PrimerPrepSplash.png', '.')],
	hiddenimports=[],
	hookspath=[],
	runtime_hooks=[],
	win_no_prefer_redirects=False,
	win_private_assemblies=False,
	cipher=block_cipher,
	noarchive=False)
pyz2 = PYZ(a2.pure, a2.zipped_data,
	cipher=block_cipher)
exe2 = EXE(pyz2,
	a2.scripts,
	exclude_binaries=True,
	name='PrimerPrepSplash',  # Name of the output executable
	debug=False,
	strip=False,
	upx=True,
	contents_directory='.',
	windowed=True,
	console=False,
	icon='PrimerPrep.ico')

coll = COLLECT(exe1,
	a1.binaries,
	a1.zipfiles,
	a1.datas,
	exe2,
	a2.binaries,
	a2.zipfiles,
	a2.datas,
	strip=False,
	upx=True,
	name='PrimerPrep')  # Name of the final folder/package
