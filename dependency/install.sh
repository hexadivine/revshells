#!/usr/bin/bash
#
# Installs dependency to copy payload/listener
#

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
    PKG="wl-clipboard pipx"
    CHECK="wl-copy pipx"
else
    PKG="xclip xsel pipx"
    CHECK="xclip pipx"
fi

# Skip if all required commands are already installed
all_found=true
for cmd in $CHECK; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
        all_found=false
        break
    fi
done

if $all_found; then
    echo "All required commands ($CHECK) already installed. Nothing to do."
    exit 0
fi

echo "Installing: $PKG"
$UPDATE
$PM $PKG

echo "Performing post installation"
pipx ensurepath

echo "Done. Verify with: command -v xclip xsel wl-copy pipx"