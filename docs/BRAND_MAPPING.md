# Brand translation — Crimson Archive v3.0 → Omarchy

This theme uses the user's provided **Crimson Archive Master Brand Tokens v3.0** as the authority and Omarchy's official palette names as the implementation layer. It is *not* a global redesign of Omarchy, and never mutates external application state outside Omarchy's established theme workflow.

| Purpose | Brand token / value | Omarchy destination |
|---|---|---|
| Dark ground | `dark.background` / `#121115` | `background` |
| Elevated surface | `dark.surface` / `#1E1B23` | `lighter_background`, shell menu/launcher |
| Subtle surface | `dark.subtleSurface` / `#29242D` | source of warm-neutral selection treatment |
| Primary text | `dark.text` / `#F3EEE6` | `foreground` |
| Secondary text | `dark.textSecondary` / `#BEB3B4` | `dark_foreground` |
| Dark crimson | `dark.crimson` / `#E19BAD` | `accent`, window border, selected accents |
| Crimson hover | `dark.crimsonHover` / `#F0B6C3` | optional hover source, not replacement for strong focus |
| Gold focus | `dark.focus` / `#E0BA76` | controls/lock focus border, dual-tone window border |
| Dark border | `dark.border` / `#4A404B` | idle shell borders |
| Success | `dark.success` / `#83BEA0` | ANSI green |
| Warning | `dark.warning` / `#E6BE7A` | ANSI yellow |
| Danger | `dark.danger` / `#F09FA9` | ANSI red, auth errors |
| Information | `dark.information` / `#A5C7DC` | ANSI blue |
| Optional ultraviolet | `optional_accents.ultraviolet.dark.text` / `#C4A3FF` | **ANSI magenta only** |

Other Omarchy-specific values are deliberately derived from the original colors to provide a complete shell ramp, terminal palette, and readable selection/hover backgrounds. They are *implementation values*, not new universal brand tokens.

### Three deliberate constraints

1. Gold is a precision/focus detail, not the primary fill on every button. Crimson is still the identity/accent.
2. Ultraviolet is used only where the ANSI system needs a magenta hue. No purple wash or global UI accents.
3. Wallpapers are **decorative**, not data graphics. Orbital curves and reticles are conceptual, not measured signals or validated physics simulations.

### Light mode

`variants/parchment/colors.toml` references `light.background=#F5F0E6`, `light.surface=#FFFCF6`, `light.text=#211B1E`, `light.crimson=#7D2037`, `light.goldText=#75531C`. It is offered as a separate *manual* variant so Omarchy's chosen dark theme never surprises the user by switching all apps when a wallpaper changes.

### Design workflow

Visual references: Omarchy upstream theming docs; built-in Tokyo Night and Catppuccin palettes; Omarchy community theme registry. We adopted structure and compatibility requirements, not their palettes or artwork. We intentionally exclude arbitrary launcher scripts and extra animation for stability, legibility, and the small-VM context.
