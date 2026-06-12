#!/usr/bin/env bash
# SprunglesQT Setup Script
# Applies the SprunglesQT configuration to your system

set -e

echo "🍵 SprunglesQT Setup — stripping bloat, adding speed..."
echo ""

# Copy session file
echo "  [1/4] Installing session file..."
mkdir -p ~/.local/share/xsessions
cp session/sprunglesqt.desktop ~/.local/share/xsessions/sprunglesqt.desktop

# Copy LXQt config override
echo "  [2/4] Applying desktop configuration..."
mkdir -p ~/.config/lxqt
cp config/session.conf ~/.config/lxqt/
cp config/panel.conf ~/.config/lxqt/
cp config/lxqt.conf ~/.config/lxqt/
cp config/env ~/.config/lxqt/

# Disable bloat autostarts
echo "  [3/4] Disabling unnecessary autostarts..."
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
echo "  [4/4] Installing about command..."
cp scripts/about.sh ~/.local/bin/sprunglesqt-about
chmod +x ~/.local/bin/sprunglesqt-about

echo ""
echo "✅  Done! Select 'SprunglesQT Desktop' from your display manager."
echo "   Run 'sprunglesqt-about' to see the about dialog."
