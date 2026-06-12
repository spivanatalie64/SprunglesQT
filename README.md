
# ☕ SprunglesQT

**The ultra-lightweight Qt desktop — stripped of bloat, built for speed.**

SprunglesQT is a minimalistic fork of LXQt that removes every non-essential component while keeping the panel and core workflow intact. It's designed for people who want a functional desktop that stays out of their way and sips resources instead of gulping them.

---

## ✨ What's Different

| Feature | LXQt | SprunglesQT |
|---|---|---|
| Desktop icons (pcmanfm) | ✅ Installed | ❌ Removed |
| Notification daemon | ✅ Running | ❌ Removed |
| App runner (Alt+F2) | ✅ Running | ❌ Removed |
| Power management daemon | ✅ Running | ❌ Removed |
| Global keyboard shortcuts daemon | ✅ Running | ❌ Disabled |
| Screen saver | ✅ Running | ❌ Disabled |
| About dialog | ✅ Installed | ❌ Removed |
| Admin tools | ✅ Installed | ❌ Removed |
| Archive manager | ✅ Installed | ❌ Removed |
| Sudo GUI | ✅ Installed | ❌ Removed |
| OpenSSH askpass | ✅ Installed | ❌ Removed |
| Portal backend | ✅ Installed | ❌ Removed |
| Fancy menu (Panel) | ✅ Default | ❌ Replaced with simple menu |
| Quick launch bar (Panel) | ✅ Default | ❌ Removed |
| Removable devices (Panel) | ✅ Default | ❌ Removed |
| Volume control (Panel) | ✅ Default | ❌ Removed |
| **Panel** | ✅ | ✅ **Kept & optimized** |
| **Taskbar** | ✅ | ✅ **Kept** |
| **System tray** | ✅ | ✅ **Kept** |
| **Desktop switcher** | ✅ | ✅ **Kept** |
| **World clock** | ✅ | ✅ **Kept** |

## 📦 What You Get

After stripping, these packages are all that remain of LXQt:

- `lxqt-session` — Session manager
- `lxqt-panel` — The bar. Minimal widgets: menu, taskbar, desktop switcher, tray, clock
- `lxqt-policykit` — Privilege escalation (kept for security)
- `liblxqt` — Core library
- `lxqt-menu-data` — Menu definitions
- `lxqt-qtplugin` — Qt platform integration
- `lxqt-globalkeys` — Library kept (daemon disabled)
- `lxqt-config` — System configuration tools (kept for convenience)
- `lxqt-themes` — Visual theme support

## 🚀 Installation

```bash
# Clone the repo
git clone https://github.com/spivanatalie64/SprunglesQT.git
cd SprunglesQT

# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh
```

### Manual installation

```bash
# Install the session file
cp session/sprunglesqt.desktop ~/.local/share/xsessions/

# Apply configs
cp config/panel.conf ~/.config/lxqt/
cp config/session.conf ~/.config/lxqt/
cp config/lxqt.conf ~/.config/lxqt/
cp config/env ~/.config/lxqt/
```

Then log out and select **SprunglesQT Desktop** from your display manager.

## 🧹 What Was Removed

| Package | Reason |
|---|---|
| `pcmanfm-qt` | Desktop icons & file manager — unnecessary background process |
| `lxqt-notificationd` | Notification daemon — saves ~50MB RSS |
| `lxqt-runner` | Alt+F2 app launcher — saves ~60MB RSS |
| `lxqt-powermanagement` | Power management daemon — saves ~40MB RSS |
| `lxqt-globalkeysd` | Global keyboard shortcuts daemon — saves ~35MB RSS |
| `lxqt-about` | About dialog — never used |
| `lxqt-admin` | Admin tools — never used |
| `lxqt-archiver` | Archive manager — alternative preferred |
| `lxqt-sudo` | Sudo GUI — terminal is lighter |
| `lxqt-openssh-askpass` | SSH password prompt — terminal works fine |
| `xdg-desktop-portal-lxqt` | Portal backend — unnecessary on X11 |

## ⚡ Resource Comparison

| Metric | Stock LXQt | SprunglesQT |
|---|---|---|
| **Running processes** | ~8 daemons | **3 essential** (session, panel, policykit) |
| **Memory (RSS)** | ~400MB+ | **~150MB** |
| **Packages removed** | — | **10 packages** (~8MB disk) |
| **Panel widgets** | 8 plugins | **5 essential** |

## 🧰 Included Panel Widgets

- **Main Menu** — Simple application menu (replaced fancymenu)
- **Taskbar** — Window management (essential)
- **Desktop Switcher** — Virtual desktop navigation
- **System Tray** — Background app indicators
- **World Clock** — Date and time display

## 🔧 Extending

SprunglesQT is designed to be a base you build on. Want something back?

```bash
# Add back notifications (if you really need them)
sudo pacman -S lxqt-notificationd

# Add back the app runner
sudo pacman -S lxqt-runner
```

Or install lighter alternatives:
- **Notifications:** `dunst` (~15MB vs ~50MB for lxqt-notificationd)
- **App launcher:** `rofi` or `dmenu` (~5MB vs ~60MB for lxqt-runner)
- **File manager:** `pcmanfm-qt` only when you need it (don't run in daemon mode)

## 🫶 Philosophy

> **"Your coffee-break digital twin"**

SprunglesQT doesn't get in your way. It boots fast, idles quiet, and gets out of your way the moment you need to work. The panel is there for window management and a clock — everything else is bloat.

Built for servers with a screen. For terminals with a GUI. For people who make coffee while their desktop loads.

## 📜 License

SprunglesQT is a fork of [LXQt](https://lxqt-project.org/), licensed under GPL-2.0+.
