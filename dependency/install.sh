#!/usr/bin/bash
# Installs dependency to copy payload/listener


set -e

# Pick package manager
UPDATE=":"
if command -v apt-get >/dev/null; 
then 
    UPDATE="sudo apt-get update"
    PM="sudo apt-get install -y"
elif command -v dnf >/dev/null; 
then 
    PM="sudo dnf install -y"; 
elif command -v pacman >/dev/null; 
then 
    PM="sudo pacman -S --noconfirm";
elif command -v zypper >/dev/null; 
then 
    PM="sudo zypper install -y"; 
elif command -v apk >/dev/null; 
then 
    PM="sudo apk add"; 
else
    echo "No supported package manager found (apt/dnf/pacman/zypper/apk)."
    echo "Please install xclip, xsel, or wl-clipboard manually."
    exit 1
fi

# Decide which tool(s) to install based on session type
if [ "$XDG_SESSION_TYPE" = "wayland" ] || [ -n "$WAYLAND_DISPLAY" ]; then
    PKG="wl-clipboard"
    CHECK="wl-copy"
else
    PKG="xclip xsel"
    CHECK="xclip"
fi

# Skip if already installed
if command -v "$CHECK" >/dev/null; then
    echo "$CHECK already installed. Nothing to do."
    exit 0
fi

echo "Installing: $PKG"
$UPDATE
$PM $PKG

echo "Done. Verify with: command -v xclip xsel wl-copy"