#!/usr/bin/env bash

autorandr -c &

# set background
bash "${HOME}"/.config/qtile/scripts/fehbg.sh
bash "${HOME}"/.config/qtile/scripts/xset.sh &

# Kill if already running
killall -9 picom sxhkd dunst xfce4-power-manager redshift-gtk

# Launch notification daemon
dunst \
    -geom "280x50-10+38" -frame_width "1" -font "Source Code Pro Medium 10" \
    -lb "#3D3250FF" -lf "#C4C7C5FF" -lfr "#B07190FF" \
    -nb "#3D3250FF" -nf "#C4C7C5FF" -nfr "#B07190FF" \
    -cb "#2E3440FF" -cf "#BF616AFF" -cfr "#BF616AFF" &

# power manager and picom start
export SESSION_MANAGER="qtile"
xfce4-power-manager &
picom --config "$HOME"/.config/qtile/picom.conf &

# Start udiskie
udiskie --config=~/.config/udiskie/config.yml &

# root authentication with rofi
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# apptray wifi and bluetooth
nm-applet &
blueman-applet &

# Screenshot program
flameshot &

# Keyboard nodeadkeys
setxkbmap -variant nodeadkeys de
setxkbmap -option caps:escape

if pgrep -x "redshift" >/dev/null || pgrep -x "redshift-gtk" >/dev/null; then
    pkill -x "redshift"
    pkill -x "redshift-gtk"

    redshift-gtk &>/dev/null
fi
