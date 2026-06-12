#!/usr/bin/env bash
# SprunglesQT Setup Script
# Applies the SprunglesQT configuration to your system

set -e

echo "🍵 SprunglesQT Setup — stripping bloat, adding speed..."
echo ""

# Copy session file
echo "  [1/6] Installing session file..."
mkdir -p ~/.local/share/xsessions
cp session/sprunglesqt.desktop ~/.local/share/xsessions/sprunglesqt.desktop

# Copy LXQt config override
echo "  [2/6] Applying desktop configuration..."
mkdir -p ~/.config/lxqt
cp config/session.conf ~/.config/lxqt/
cp config/panel.conf ~/.config/lxqt/
cp config/lxqt.conf ~/.config/lxqt/
cp config/env ~/.config/lxqt/

# Disable bloat autostarts
echo "  [3/6] Disabling unnecessary autostarts..."
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
echo "  [4/6] Installing about command..."
cp scripts/about.sh ~/.local/bin/sprunglesqt-about
chmod +x ~/.local/bin/sprunglesqt-about

# Install settings panel
echo "  [5/6] Installing settings panel..."
cp scripts/sprunglesqt-settings.py ~/.local/bin/sprunglesqt-settings
chmod +x ~/.local/bin/sprunglesqt-settings
mkdir -p ~/.local/share/applications
cp session/sprunglesqt-settings.desktop ~/.local/share/applications/
cp session/sprunglesqt-about.desktop ~/.local/share/applications/

# Install desktop entries for menu
echo "  [6/6] Installing desktop entries..."
mkdir -p ~/.local/share/applications
cp session/sprunglesqt-settings.desktop ~/.local/share/applications/
cp session/sprunglesqt-about.desktop ~/.local/share/applications/

echo ""
echo "✅  Done! Select 'SprunglesQT Desktop' from your display manager."
echo "   Run 'sprunglesqt-settings' to configure your desktop."
echo "   Run 'sprunglesqt-about' to see the about dialog."
