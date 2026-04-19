#!/bin/bash
# Mommy Security v1.0 - Warmth & Protection For Your OS
# Installer script

set -euo pipefail

if [ "$EUID" -ne 0 ]; then
  echo "Please run as root (sudo ./install.sh)"
  exit 1
fi

UNINSTALL=0

for arg in "$@"; do
    case $arg in
        --uninstall)
        UNINSTALL=1
        shift
        ;;
    esac
done

if [ $UNINSTALL -eq 1 ]; then
    echo "Uninstalling Mommy Security..."
    if command -v systemctl >/dev/null 2>&1; then
        systemctl stop mommy-nullify.timer || true
        systemctl disable mommy-nullify.timer || true
    fi
    rm -f /etc/systemd/system/mommy-nullify.service
    rm -f /etc/systemd/system/mommy-nullify.timer
    if command -v systemctl >/dev/null 2>&1; then
        systemctl daemon-reload
    fi
    
    rm -f /usr/local/bin/mommy-nullify.sh
    rm -f /usr/local/bin/mommyctl
    rm -f /usr/local/bin/mommy-stub.py
    rm -f /etc/dbus-1/system.d/mommy-security.conf
    rm -f /etc/dbus-1/session.d/mommy-security.conf
    rm -f /usr/share/xdg-desktop-portal/portals/mommy-security.portal
    rm -f /usr/share/dbus-1/services/org.freedesktop.impl.portal.MommySecurity.service
    
    if command -v systemctl >/dev/null 2>&1; then
        systemctl unmask systemd-userdbd.socket systemd-homed.socket || true
    fi
    
    echo "Uninstallation complete."
    exit 0
fi

echo "Installing Mommy Security v1.0..."

# Create necessary directories
mkdir -p /etc/dbus-1/system.d
mkdir -p /etc/dbus-1/session.d
mkdir -p /usr/share/xdg-desktop-portal/portals
mkdir -p /usr/local/bin

mkdir -p /usr/share/dbus-1/services

# Copy files
install -Dm644 policy/mommy-security-system.conf /etc/dbus-1/system.d/mommy-security.conf
install -Dm644 policy/mommy-security-session.conf /etc/dbus-1/session.d/mommy-security.conf
install -Dm644 portal/mommy-security.portal /usr/share/xdg-desktop-portal/portals/mommy-security.portal
install -Dm755 scripts/mommy-nullify.sh /usr/local/bin/mommy-nullify.sh
install -Dm755 scripts/mommyctl /usr/local/bin/mommyctl
install -Dm755 scripts/mommy-stub.py /usr/local/bin/mommy-stub.py
install -Dm644 systemd/mommy-nullify.service /etc/systemd/system/mommy-nullify.service
install -Dm644 systemd/mommy-nullify.timer /etc/systemd/system/mommy-nullify.timer

# Create D-Bus service file for auto-activation
cat <<EOF > /usr/share/dbus-1/services/org.freedesktop.impl.portal.MommySecurity.service
[D-BUS Service]
Name=org.freedesktop.impl.portal.MommySecurity
Exec=/usr/local/bin/mommy-stub.py
EOF



# Run immediately
/usr/local/bin/mommy-nullify.sh

# Reload systemd and start timer if on a systemd distro
if command -v systemctl >/dev/null 2>&1; then
    systemctl daemon-reload
    systemctl enable --now mommy-nullify.timer
    systemctl reload dbus.service || true
else
    echo "Non-systemd distro detected. Skipping systemd timer setup."
    # Try to reload dbus manually if possible
    killall -HUP dbus-daemon || true
fi

echo ""
echo "Mommy Security is now protecting your OS ❤️"
