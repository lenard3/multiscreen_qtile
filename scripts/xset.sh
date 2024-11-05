#!/usr/bin/env bash
# This script is ran by .xprofile
# Otherwise the xset options reset

# Wait until all setup is done and apply settings
sleep 5

# 1. Fixes problem with picom (notifications are still visible)
# 2. Screensaver module
# 3. Turns off screen 2 seconds after manual locking
export XSECURELOCK_NO_COMPOSITE=1
export XSECURELOCK_SAVER="/usr/lib/xsecurelock/dimmer"
export XSECURELOCK_BLANK_TIMEOUT=2

/usr/bin/xset s 240 5
/usr/bin/xset dpms 245 245 490

if pgrep -x "xss-lock" >/dev/null; then
    exit 0
else
    xss-lock -n /usr/lib/xsecurelock/dimmer -- xsecurelock &
fi
