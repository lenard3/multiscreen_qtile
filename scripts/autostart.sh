#!/usr/bin/env bash

export SESSION_MANAGER="qtile"
export SIGNAL_PASSWORD_STORE=gnome-libsecret

autorandr -c &

# set background
bash "${HOME}"/.config/qtile/scripts/fehbg.sh &
bash "${HOME}"/.config/qtile/scripts/xset.sh &

# Kill if already running
killall -9 picom dunst xfce4-power-manager redshift-gtk udiskie

# Launch notification daemon
dunst \
    -geom "280x50-10+38" -frame_width "1" -font "Source Code Pro Medium 10" \
    -lb "#3D3250FF" -lf "#C4C7C5FF" -lfr "#B07190FF" \
    -nb "#3D3250FF" -nf "#C4C7C5FF" -nfr "#B07190FF" \
    -cb "#2E3440FF" -cf "#BF616AFF" -cfr "#BF616AFF" &

# power manager and picom start
xfce4-power-manager &
picom --config "$HOME"/.config/qtile/picom.conf &

# Start udiskie
udiskie >/dev/null &

# root authentication with rofi
/usr/lib/polkit-gnome/polkit-gnome-authentication-agent-1 &

# apptray wifi, bluetooth and sound-switcher
nm-applet &
blueman-applet &
indicator-sound-switcher &

# Screenshot program
flameshot &

# Keyboard nodeadkeys
setxkbmap -variant nodeadkeys de
setxkbmap -option caps:escape

protonmail-bridge --no-window &
