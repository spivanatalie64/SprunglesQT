#!/usr/bin/env bash
# SprunglesQT Setup Script
# Applies the SprunglesQT configuration to your system

set -e

echo "🍵 SprunglesQT Setup — stripping bloat, adding speed..."
echo ""

# Copy session file
echo "  [1/7] Installing session file..."
mkdir -p ~/.local/share/xsessions
cp session/sprunglesqt.desktop ~/.local/share/xsessions/sprunglesqt.desktop

# Copy LXQt config override
echo "  [2/7] Applying desktop configuration..."
mkdir -p ~/.config/lxqt
cp config/session.conf ~/.config/lxqt/
cp config/panel.conf ~/.config/lxqt/
cp config/lxqt.conf ~/.config/lxqt/
cp config/env ~/.config/lxqt/

# Disable bloat autostarts
echo "  [3/7] Disabling unnecessary autostarts..."
mkdir -p ~/.config/autostart
for f in \
  lxqt-globalkeyshortcuts.desktop \
  lxqt-xscreensaver-autostart.desktop \
  lxqt-notifications.desktop \
  lxqt-runner.desktop \
  lxqt-powermanagement.desktop; do
  cat > ~/.config/autostart/"$f" << EOF
[Desktop Entry]
Type=Application
Hidden=true
EOF
done

# Install about command
echo "  [4/7] Installing about command..."
cp scripts/about.sh ~/.local/bin/sprunglesqt-about
chmod +x ~/.local/bin/sprunglesqt-about

# Install settings panel
echo "  [5/7] Installing settings panel..."
cp scripts/sprunglesqt-settings.py ~/.local/bin/sprunglesqt-settings
chmod +x ~/.local/bin/sprunglesqt-settings

# Install application icons
echo "  [6/7] Installing application icons..."
for size in scalable 16x16 22x22 32x32 48x48 64x64 128x128; do
  mkdir -p ~/.local/share/icons/hicolor/${size}/apps/
done
cp branding/logo.svg ~/.local/share/icons/hicolor/scalable/apps/sprunglesqt.svg
cp branding/settings-icon.svg ~/.local/share/icons/hicolor/scalable/apps/sprunglesqt-settings.svg
cp branding/about-icon.svg ~/.local/share/icons/hicolor/scalable/apps/sprunglesqt-about.svg
gtk-update-icon-cache ~/.local/share/icons/hicolor/ 2>/dev/null || true

# Install desktop entries for application menu
echo "  [7/7] Installing application menu entries..."
mkdir -p ~/.local/share/applications
cp session/sprunglesqt-settings.desktop ~/.local/share/applications/
cp session/sprunglesqt-about.desktop ~/.local/share/applications/

echo ""
echo "✅  Done! Select 'SprunglesQT Desktop' from your display manager."
echo "   Look for SprunglesQT entries in your application menu."
echo "   Run 'sprunglesqt-settings' to configure your desktop."
echo "   Run 'sprunglesqt-about' to see the about dialog."
