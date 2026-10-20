"""Offline Omarchy structure and brand QA; not a substitute for VM tests."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import re
import tomllib
import unittest

from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
REQUIRED = {
    'mode', 'accent', 'selection', 'muted',
    'background', 'dark_background', 'darker_background','lighter_background',
    'foreground', 'dark_foreground','light_foreground','bright_foreground',
    'red','yellow','orange','green','cyan','blue','magenta','brown',
    'bright_red','bright_yellow','bright_green','bright_cyan','bright_blue',
    'bright_magenta',
}
SHELL = {
    'controls': {'normal-color','normal-fill-alpha','normal-border','normal-border-width','normal-border-alpha',
                 'hover-cursor-color','hover-cursor-fill-alpha','hover-cursor-border','hover-cursor-border-width',
                 'hover-cursor-border-alpha','focus-color','focus-fill-alpha','focus-border','focus-border-width',
                 'focus-border-alpha','selected-color','selected-fill-alpha','selected-border','selected-border-width',
                 'selected-border-alpha','pressed-fill-alpha','selection-fill-alpha'},
    'menu': {'background','background-alpha','text','border','border-alpha','border-width','scrim','scrim-alpha',
             'selected-background','selected-background-alpha','selected-text','selected-border',
             'selected-border-alpha','selected-border-width'},
    'launcher': {'background','background-alpha','text','border','border-alpha','border-width','scrim','scrim-alpha',
                 'selected-background','selected-background-alpha','selected-text','selected-border',
                 'selected-border-alpha','selected-border-width'},
    'notifications': {'background','background-alpha','text','border','border-alpha','border-width','countdown'},
    'lock': {'background','background-alpha','text','placeholder','text-error','border','border-active',
             'border-error','border-alpha','selection','selection-alpha'}
}
BRAND_DARK = dict(background='#121115', lighter_background='#1E1B23',
                  foreground='#F3EEE6', dark_foreground='#BEB3B4',
                  accent='#E19BAD', red='#F09FA9', yellow='#E6BE7A',
                  green='#83BEA0', blue='#A5C7DC', magenta='#C4A3FF')
BRAND_LIGHT = dict(background='#F5F0E6', lighter_background='#FFFCF6',
                   foreground='#211B1E', dark_foreground='#5F5759',
                   accent='#7D2037', red='#9A2939', yellow='#85551B',
                   green='#2F684E', blue='#325F7C', magenta='#6D28D9')


def luminance(rgb):
    comps = [int(rgb[i:i+2],16)/255 for i in (1,3,5)]
    linear = [c/12.92 if c <= 0.04045 else ((c+0.055)/1.055)**2.4 for c in comps]
    return sum(x*w for x,w in zip(linear,(0.2126,0.7152,0.0722)))


def contrast(a,b):
    lum1, lum2 = sorted((luminance(a),luminance(b)),reverse=True)
    return (lum1+0.05)/(lum2+0.05)


class TestTheme(unittest.TestCase):
    def test_complete_canonical_palettes(self):
        for path,mode in [(ROOT/'colors.toml','dark'),
                          (ROOT/'variants/parchment/colors.toml','light')]:
            with self.subTest(path=path):
                palette=tomllib.loads(path.read_text())
                self.assertEqual(palette['mode'],mode)
                self.assertTrue(REQUIRED <= palette.keys(),REQUIRED - palette.keys())
                for key,value in palette.items():
                    if key=='mode' or key.startswith('hyprland_'):continue
                    self.assertRegex(value, r'^#[0-9a-fA-F]{6}$',key)
                if mode == 'dark':
                    self.assertLess(luminance(palette['darker_background']),
                                    luminance(palette['dark_background']))
                    self.assertLess(luminance(palette['dark_background']),
                                    luminance(palette['background']))
                else:
                    self.assertLess(luminance(palette['darker_background']),
                                    luminance(palette['dark_background']))
                    self.assertLess(luminance(palette['dark_background']),
                                    luminance(palette['background']))

    def test_brand_fidelity(self):
        for file,exact in [(ROOT/'colors.toml',BRAND_DARK),
                           (ROOT/'variants/parchment/colors.toml',BRAND_LIGHT)]:
            data=tomllib.loads(file.read_text())
            for key,expected in exact.items():
                with self.subTest(file=file.name,key=key):
                    self.assertEqual(data[key],expected)

    def test_accessible_text_and_selection(self):
        for file in (ROOT/'colors.toml',ROOT/'variants/parchment/colors.toml'):
            with self.subTest(file=file):
                c=tomllib.loads(file.read_text())
                for role in ('foreground','accent','dark_foreground'):
                    self.assertGreaterEqual(contrast(c[role],c['background']),4.5,role)
                self.assertGreaterEqual(contrast(c['bright_foreground'],c['selection']),4.5)
                self.assertNotEqual(c['red'],c['accent'])
        dark=tomllib.loads((ROOT/'colors.toml').read_text())
        self.assertGreaterEqual(contrast('#E0BA76',dark['background']),4.5)

    def test_shell_overrides_are_supported_and_parseable(self):
        self.assertEqual(set(ROOT.glob('shell.*.toml')),
                         {ROOT/f'shell.{s}.toml' for s in SHELL})
        for section,keys in SHELL.items():
            file=ROOT/f'shell.{section}.toml'
            with self.subTest(section=section):
                cfg=tomllib.loads(file.read_text())
                self.assertEqual(set(cfg),keys,'unexpected or missing shell token')
                for key,val in cfg.items():
                    if key.endswith('alpha') or key.endswith('-alpha'):
                        self.assertIsInstance(val,(int,float))
                        self.assertGreaterEqual(val,0)
                        self.assertLessEqual(val,1)
                    elif 'color' in key or key in {
                            'background','border','text','scrim','placeholder',
                            'selected-background','selected-border','selected-text',
                            'countdown','border-active','border-error','text-error','selection'}:
                        self.assertRegex(val,r'^#[a-fA-F0-9]{6}$',key)
        c=tomllib.loads((ROOT/'shell.controls.toml').read_text())
        self.assertEqual(c['focus-border'],'#E0BA76')
        self.assertNotEqual(c['focus-border'],c['normal-border'])
        self.assertEqual(c['focus-border-width'],2)

    def test_theme_distribution_safety(self):
        for file in ROOT.iterdir():
            self.assertFalse(file.name in {'hyprland.lua','neovim.lua','gum_env.lua',
                                'alacritty.toml','foot.ini','ghostty.conf',
                                'kitty.conf','vscode.json'})
        self.assertEqual((ROOT/'icons.theme').read_text().strip(),'Yaru-red')
        self.assertTrue((ROOT/'README.md').is_file())
        self.assertTrue((ROOT/'LICENSE').is_file())

    def test_wallpaper_and_previews(self):
        walls=list((ROOT/'backgrounds').glob('*.webp'))
        self.assertEqual(len(walls),3)
        for file in walls:
            with self.subTest(file=file.name):
                self.assertLess(file.stat().st_size,1_800_000)
                with Image.open(file) as im:
                    im.verify()
                with Image.open(file) as im:
                    self.assertEqual(im.size,(2560,1440))
                    self.assertEqual(im.format,'WEBP')
        for name in ('preview.png','preview-unlock.png'):
            with Image.open(ROOT/name) as im:
                self.assertEqual(im.size,(1920,1080))
                self.assertEqual(im.format,'PNG')
        with Image.open(ROOT/'unlock.png') as im:
            self.assertEqual(im.mode,'RGBA')
            self.assertEqual(im.size,(512,512))
            self.assertLess(im.getchannel('A').getextrema()[0],255)

    def test_original_approved_sources_intact(self):
        manifest=json.loads((ROOT/'assets/SOURCE_SHA256.json').read_text())
        self.assertEqual(len(manifest),7)
        for path,expected_sha in manifest.items():
            with self.subTest(path=path):
                self.assertTrue(path.startswith('assets/brand-src/'))
                self.assertEqual(hashlib.sha256((ROOT/path).read_bytes()).hexdigest(),expected_sha)

if __name__ == '__main__':
    unittest.main()
