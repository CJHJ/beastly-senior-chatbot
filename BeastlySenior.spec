# -*- mode: python -*-

from kivy.deps import sdl2, glew

def getResource(identifier, *args, **kwargs):
    if identifier == 'pygame_icon.tiff':
        raise IOError()
    return _original_getResource(identifier, *args, **kwargs)

import pygame.pkgdata
_original_getResource = pygame.pkgdata.getResource
pygame.pkgdata.getResource = getResource

block_cipher = None


a = Analysis(['C:\\Users\\CJHJ\\Documents\\yugeChatBot\\new-ver\\main.py'],
             pathex=['C:\\Users\\CJHJ\\Documents\\yugeChatBot\\new-ver'],
             binaries=None,
             datas=None,
             hiddenimports=['dbm.dumb'],
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
          name='BeastlySenior',
          debug=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe, Tree('C:\\Users\\CJHJ\\Documents\\yugeChatBot\\new-ver'),
               a.binaries,
               a.zipfiles,
               a.datas,
               *[Tree(p) for p in (sdl2.dep_bins + glew.dep_bins)],
               strip=False,
               upx=True,
               name='BeastlySenior')
