# QA and compatibility

## Automated checks

`python -m unittest discover -s tests -v` checks:

- Root Omarchy palette (mode, required ramp and ANSI keys, hex validity)
- Optional parchment palette and its exact brand constants
- WCAG-style contrast of normal text, accent and gold focus against base background (>=4.5:1 for these text roles)
- Selection text against selection fill; distinct keyboard focus vs error color
- Theme file naming and presence; static allow-list of shell tokens from the Omarchy upstream 2026 shell template
- Preview 16:9 and 3 wallpapers 2560×1440, WebP validity and sane file size
- Transparent unlock emblem; supplied source artwork checksums and deterministic source manifest

## Human and runtime checks — **required on Omarchy**

This package was built outside an Arch Linux / Hyprland / Omarchy desktop, so **actual Omarchy installation, screenshots, focus, lock-screen rendering and compositor border appearance have not been tested here**. Before calling it fully tested, on the target Omarchy machine:

1. Back up any existing custom theme under `~/.config/omarchy/themes/crimson-archive`.
2. Install from the published GitHub URL, then run `omarchy theme current` and `omarchy dev theme-preview crimson-archive` when available.
3. Inspect terminal (normal/bright ANSI), launcher, notifications, editor and browser. Test selection, hover, keyboard-only navigation, lock-screen password visibility, and errors.
4. Check wallpaper and lock-screen composition at your VM's actual display resolution, including narrow windows and multiple scales.
5. Confirm keyboard input, text scaling, color blindness separation of error/selected/focus cues, and reduced-motion preferences.
6. Test changing to a built-in theme and back, then install-update behavior.

If older builds ignore `shell.<section>.toml`, delete those files or update Omarchy and rely on the core `colors.toml`, which remains a valid theme on its own. If Hyprland rejects the gradient, replace the value with a plain hex `#E19BAD` and reapply.

## Distribution and security

We ship no `.lua`, terminal executable configs, `vscode.json`, auto-run commands, hooks, network requests, or plugins. User-customized fonts stay intact, and media are static PNG/WebP/SVG. GitHub release assets are optional, never required by Omarchy.

## Evidence from this build

Static unit tests: **7 passed / 7 executed** on Python 3.11 with Pillow.
Computed examples (WCAG relative luminance ratio): dark text on obsidian **16.28:1**;
dark crimson accent on obsidian **8.50:1**; gold focus on obsidian **10.26:1**;
parchment body text **14.91:1**. These validate selected color pairs, not all
possible app states or live compositor behavior.

A manual visual-inspection pass corrected duplicated wallpaper/preview branding.
The exported preview images remain illustrations and are not screenshots from Omarchy.
