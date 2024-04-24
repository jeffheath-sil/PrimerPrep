# -*- mode: python -*-
import os
import site

typelib_path = 'C:\\msys64\\mingw64\\lib\\girepository-1.0'


block_cipher = None


a1 = Analysis(['PrimerPrep.py'],
             pathex=[],
             binaries=[(os.path.join(typelib_path, tl), 'gi_typelibs') for tl in os.listdir(typelib_path)],
             datas=[ ('PrimerPrep.glade', '.'), ('PrimerPrep.ico', '.'), ('PrimerPrep 18x18.ico', '.'), 
                     ('Help', 'Help'), ('po', 'po') ],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz1 = PYZ(a1.pure, a1.zipped_data,
             cipher=block_cipher)
exe1 = EXE(pyz1,
          a1.scripts,
          exclude_binaries=True,
          name='PrimerPrep',
          debug=False,
          strip=False,
          upx=True,
          console=False )

a2 = Analysis(['PrimerPrepSplash.py'],
             pathex=[],
             binaries=[],
             datas=[ ('PrimerPrepSplash.py', '.'), ('PrimerPrepSplash.png', '.') ],
             hiddenimports=[],
             hookspath = [],
             runtime_hooks = [],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz2 = PYZ(a2.pure, a2.zipped_data,
             cipher=block_cipher)
exe2 = EXE(pyz2,
          a2.scripts,
          exclude_binaries=True,
          name='PrimerPrepSplash',
          debug=False,
          strip=False,
          upx=True,
          onefile = False,
          console=False )

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
               name='PrimerPrep')
