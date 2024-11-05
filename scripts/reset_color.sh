#!/usr/bin/env bash
# This scripts resets the gamma for the monitor, so that the blue hue disappears

MONITORS="$(xrandr | grep -F ' connected ' | awk '{print $1}')"

ARRAY=($MONITORS)

for MONITOR in "${ARRAY[@]}"; do
    xrandr --output "$MONITOR" --gamma 1:1:1
done
