# Crimson Archive — Omarchy Theme

**Obsidian. Crimson. Antique gold. A desktop for serious work.**

An Omarchy / Hyprland theme built from the **Crimson Archive Complete Brand Kit v3.0**: the Modern Scholar × the Dark Romantic. Quiet obsidian panels, warm ivory text, crimson selection, deliberate gold focus states, and a **small, opt-in ANSI ultraviolet role**. No invented app styling, executable setup scripts, or fonts bundled with the theme.

![Crimson Archive theme preview](preview.png)

## Install on Omarchy

After this repository has been created publicly on GitHub, run **inside the Omarchy terminal** (not Windows PowerShell):

```bash
omarchy theme install https://github.com/calebaiken/omarchy-crimson-archive-theme
```

Omarchy should clone it as `crimson-archive` and switch to it. You can later select it from the Omarchy theme picker, or use:

```bash
omarchy theme set crimson-archive
omarchy theme current
```

### Manual installation with GitHub MFA

If GitHub requires multifactor authentication, download the theme through your signed-in browser instead of trying to use your GitHub password in a terminal:

1. Sign in to GitHub in your browser and complete your MFA prompt.
2. Open the [Crimson Archive repository](https://github.com/calebaiken/Omarch-Crimson-Archive-Theme), select **Code → Download ZIP**, and extract the ZIP on your Omarchy computer.
3. In an Omarchy terminal, set `source_dir` to the extracted folder. GitHub names it similar to `Omarch-Crimson-Archive-Theme-main`; adjust the path if your browser saved it elsewhere.
4. Copy the theme files into Omarchy and select the theme:

   ```bash
   source_dir="$HOME/Downloads/Omarch-Crimson-Archive-Theme-main"
   theme_dir="$HOME/.config/omarchy/themes/crimson-archive"
   mkdir -p "$theme_dir"
   cp -a "$source_dir/colors.toml" "$source_dir/backgrounds" "$source_dir/variants" \
     "$source_dir/preview.png" "$source_dir/icons.theme" \
     "$source_dir"/shell.*.toml "$source_dir/unlock.png" \
     "$source_dir/preview-unlock.png" "$theme_dir/"
   omarchy theme set crimson-archive
   omarchy theme current
   ```

This uses your browser's GitHub sign-in and MFA session; it does not require entering your GitHub password or creating a personal access token in the terminal. If you already have a local checkout, use the same copy commands with `source_dir` set to that checkout.

For older Omarchy versions where `omarchy theme <command>` is unavailable, use the `omarchy-theme-*` commands exposed by your installation. If needed, install manually from a local checkout:

```bash
mkdir -p ~/.config/omarchy/themes/crimson-archive
cp -a colors.toml backgrounds variants preview.png icons.theme shell.*.toml unlock.png preview-unlock.png ~/.config/omarchy/themes/crimson-archive/
omarchy theme set crimson-archive
```

> The displayed URL is a **publishing target**, not a claim that a GitHub repository already exists. Upload the project before attempting remote installation.

## What's themed

- `colors.toml` — official Omarchy palette; paints its terminal, editor, browser, Hyprland and shell integrations.
- `shell.controls.toml` — gold **keyboard focus**, restrained crimson selected states, accessible contrast.
- `shell.menu.toml`, `shell.launcher.toml` — obsidian surfaces and clearly selected rows.
- `shell.notifications.toml`, `shell.lock.toml` — muted borders, warm ivory text, clear auth/alert cues.
- `icons.theme` — **Yaru-red** icon variant (remove if not installed or if you prefer default icons).
- `backgrounds/` — three optimized 16:9 wallpapers, made from the supplied brand assets and original line-work.
- `unlock.png`, `preview-unlock.png` — compact identity imagery.
- `preview.png` — **illustrative theme composition**, not a live desktop screenshot.

Themes installed by URL are filtered by Omarchy for executable config files. We rely on Omarchy's own generation of terminal and Hyprland files rather than shipping executable replacements.

## Wallpapers

| File | Mood | Use |
| --- | --- | --- |
| `01-observatory.webp` | Cosmic Archive | Primary, cinematic but with clear working space |
| `02-instrument-room.webp` | Instrument | Minimal, technical, best when windows are busy |
| `03-parchment-study.webp` | Archive | Warm light wallpaper for daytime or reading |

Cycle them in Omarchy's wallpaper chooser. A wallpaper does not switch the terminal/shell from dark to light mode automatically.

## Optional parchment (light) variant

The root theme is deliberately dark. The separate palette `variants/parchment/colors.toml` uses the exact light-mode identity values from the brand kit. To make a **local companion theme** after installing the main theme:

```bash
source_dir="$HOME/.config/omarchy/themes/crimson-archive"
light_dir="$HOME/.config/omarchy/themes/crimson-archive-parchment"
mkdir -p "$light_dir/backgrounds"
cp "$source_dir/variants/parchment/colors.toml" "$light_dir/colors.toml"
cp "$source_dir/backgrounds/03-parchment-study.webp" "$light_dir/backgrounds/"
cp "$source_dir/preview.png" "$light_dir/preview.png"
# This light variant intentionally has no dark-specific shell overrides.
omarchy theme set crimson-archive-parchment
```

This is **not** a second GitHub-installable remote theme. It is a local alternate with a distinct menu name. To return:

```bash
omarchy theme set crimson-archive
```

## Make it yours

Omarchy builds its own configs from the colors. You can adjust the palette under `~/.config/omarchy/themes/crimson-archive/colors.toml`, then reapply via `omarchy theme set crimson-archive`. Updating from remote GitHub may replace locally edited tracked files — make a copy first.

For typography, optionally install **EB Garamond**, **Inter**, and **JetBrains Mono** through your normal OS package manager, then configure app fonts through Omarchy/user settings; this repository does not silently overwrite your font choices.

## Validation and provenance

Test locally on the host with Python 3.11+ and Pillow:

```bash
python -m pip install -r requirements-dev.txt
python -m unittest discover -s tests -v
```

See [design-token mapping](docs/BRAND_MAPPING.md) and [QA / compatibility notes](docs/QA.md). Recreate image exports using `python scripts/build_assets.py`. The asset generator preserves the **official logo geometry** and the original hero-art aspect ratio. The original brand PDF is intentionally not republished here.

**Source:** owner-supplied Crimson Archive Complete Brand Kit v3.0. **Upstream format:** [Omarchy theming](https://github.com/omacom/omarchy/blob/quattro/docs/theming.md) and [official manual](https://omarchy.org/manual/making-your-own-theme/). **Brand/art:** see [ASSET_LICENSE.md](ASSET_LICENSE.md).

## Publish this repo

**Option A — GitHub website (least setup).** Create a **public, empty** repository in your account with the exact name `omarchy-crimson-archive-theme` (do not initialize it with a README). Extract this ZIP locally, open the new repository's **Add file → Upload files**, and upload the extracted folder's contents, preserving subfolders. Alternatively, after creating that same empty GitHub repository, open a terminal *inside* the extracted theme folder:

```bash
git init -b main
git add .
git commit -m "feat: release Crimson Archive Omarchy theme v1.0"
git remote add origin https://github.com/calebaiken/omarchy-crimson-archive-theme.git
git push -u origin main
```

**Option B — authenticated GitHub CLI.** No website setup needed. In the extracted theme folder:

```bash
git init -b main
git add .
git commit -m "feat: release Crimson Archive Omarchy theme v1.0"
gh repo create calebaiken/omarchy-crimson-archive-theme --public --source=. --remote=origin --push
```

`gh` must already be installed and authenticated. Do not publish the source artwork publicly unless you have the rights to do so (see [artwork licensing](ASSET_LICENSE.md)).

Do not run both remote-creation recipes. After verifying the public repository, it can be [submitted to the Omarchy theme registry](https://github.com/omacom/omarchy-theme-registry).
