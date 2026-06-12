#!/usr/bin/env bash
# SprunglesQT Setup Script
# Applies the SprunglesQT configuration to your system

set -e

echo "🍵 SprunglesQT Setup — stripping bloat, adding speed..."
echo ""

# Copy session file
echo "  [1/9] Installing session file..."
mkdir -p ~/.local/share/xsessions
cp session/sprunglesqt.desktop ~/.local/share/xsessions/sprunglesqt.desktop

# Copy LXQt config override
echo "  [2/9] Applying desktop configuration..."
mkdir -p ~/.config/lxqt
cp config/session.conf ~/.config/lxqt/
cp config/panel.conf ~/.config/lxqt/
cp config/lxqt.conf ~/.config/lxqt/
cp config/env ~/.config/lxqt/

# Install module system
echo "  [3/9] Installing module system..."
mkdir -p /usr/share/sprunglesqt/modules
cp modules/*.module /usr/share/sprunglesqt/modules/
cp scripts/sprunglesqt-modules ~/.local/bin/sprunglesqt-modules
chmod +x ~/.local/bin/sprunglesqt-modules

# Disable OLD LXQt autostart modules
echo "  [4/9] Disabling old LXQt autostart module system..."
mkdir -p ~/.config/autostart
for f in lxqt-*.desktop; do
  cat > ~/.config/autostart/"$f" << EOF
[Desktop Entry]
Type=Application
Hidden=true
X-LXQt-Module=false
EOF
done

# Install NEW SprunglesQT module manager autostart
cat > ~/.config/autostart/sprunglesqt-modules.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=SprunglesQT Modules
Comment=Sequential module launcher for SprunglesQT desktop
Exec=sprunglesqt-modules start
Terminal=false
StartupNotify=false
X-SprunglesQT-ModuleManager=true
EOF

# Install about command
echo "  [5/9] Installing about command..."
cp scripts/about.sh ~/.local/bin/sprunglesqt-about
chmod +x ~/.local/bin/sprunglesqt-about

# Install settings panel
echo "  [6/9] Installing settings panel..."
cp scripts/sprunglesqt-settings.py ~/.local/bin/sprunglesqt-settings
chmod +x ~/.local/bin/sprunglesqt-settings

# Install application icons
echo "  [7/9] Installing application icons..."
for size in scalable 16x16 22x22 32x32 48x48 64x64 128x128; do
  mkdir -p ~/.local/share/icons/hicolor/${size}/apps/
done
cp branding/logo.svg ~/.local/share/icons/hicolor/scalable/apps/sprunglesqt.svg
cp branding/settings-icon.svg ~/.local/share/icons/hicolor/scalable/apps/sprunglesqt-settings.svg
cp branding/about-icon.svg ~/.local/share/icons/hicolor/scalable/apps/sprunglesqt-about.svg
gtk-update-icon-cache ~/.local/share/icons/hicolor/ 2>/dev/null || true

# Install desktop entries for application menu
echo "  [8/9] Installing application menu entries..."
mkdir -p ~/.local/share/applications
cp session/sprunglesqt-settings.desktop ~/.local/share/applications/
cp session/sprunglesqt-about.desktop ~/.local/share/applications/

# Enable only core modules, disable optional ones
echo "  [9/9] Configuring default modules..."
mkdir -p ~/.config/sprunglesqt/modules-enabled
touch ~/.config/sprunglesqt/modules-enabled/policykit
touch ~/.config/sprunglesqt/modules-enabled/panel

echo ""
echo "✅  Done! SprunglesQT is installed with sequential module management."
echo ""
echo "   Modules enabled by default: policykit, panel"
echo "   Optional modules (disabled): globalkeys, notifications, runner, screensaver"
echo ""
echo "   Manage modules:  sprunglesqt-modules list"
echo "                   sprunglesqt-modules enable  <name>"
echo "                   sprunglesqt-modules disable <name>"
echo "   Settings GUI:    sprunglesqt-settings"
echo "   About:           sprunglesqt-about"
echo ""
echo "   Select 'SprunglesQT Desktop' from your display manager."
echo "   Or run 'sprunglesqt-modules start' to launch modules now."
