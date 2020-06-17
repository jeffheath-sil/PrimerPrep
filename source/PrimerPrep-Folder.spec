# -*- mode: python -*-
import os
import site

typelib_path = os.path.join(site.getsitepackages()[1], 'gnome', 'lib', 'girepository-1.0')


block_cipher = None


a = Analysis(['PrimerPrep.py'],
             pathex=['C:\\Util\\build'],
             binaries=[(os.path.join(typelib_path, tl), 'gi_typelibs') for tl in os.listdir(typelib_path)],
             datas=[ ('PrimerPrep.glade', '.'), ('PrimerPrep.ico', '.'), ('PrimerPrep 18x18.ico', '.'), 
                     ('Help', 'Help'),  ('po', 'po') ],
             hiddenimports=[],
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
          name='PrimerPrep',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='PrimerPrep')
