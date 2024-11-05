#!/usr/bin/env bash
# This script enables a presentation mode
# It automates the process of:
#   1. Opening pympress
#   2. Moving the content window to a 'hidden' group on a second screen
#   3. Enables fullscreen for the content window
#   4. Moves focus back to presenter

presentation_mode_off() {
    # Reset the xset timings and enables dpms again
    /usr/bin/xset s 240 5
    /usr/bin/xset dpms 245 245 490
}

presentation_mode_on() {
    # Change this values
    CONTENT_GROUP="0"
    PRESENTER_GROUP="1"
    PRESENTER_SCREEN="1"
    STANDARD_SCREEN="0"
    SCREENS="$(xrandr | grep -c ' connected ')"

    pympress &

    for ((i = 0; i < 10; i++)); do
        sleep 0.2

        # Tries to get the window ID of the pympress content/presenter window
        CONTENT_ID=$(qtile cmd-obj -o root -f windows | grep -B 3 "Pympress Content" | head -n -3 | awk -F': ' '{print $2}' | awk -F ',' '{print $1}')
        PRESENTER_ID=$(qtile cmd-obj -o root -f windows | grep -B 3 "Pympress Presenter" | head -n -3 | awk -F': ' '{print $2}' | awk -F ',' '{print $1}')

        # When ID's are found leave loop
        if [[ -n "${CONTENT_ID}" && -n "${PRESENTER_ID}" ]]; then
            break
        fi
    done

    # Exit script when either content ID or presenter ID cannot be found
    if [[ -z "${CONTENT_ID}" || -z "${PRESENTER_ID}" ]]; then
        echo "pympress took too long to start up"
        echo "Exiting..."
        exit 1
    fi

    # Moves the presenter window to the specified group
    qtile cmd-obj -o screen -f toggle_group -a "${PRESENTER_GROUP}"
    qtile cmd-obj -o window "${PRESENTER_ID}" -f togroup -a "${PRESENTER_GROUP}"

    if [[ "${SCREENS}" == "2" ]]; then
        # Move focus to second screen when two are connected
        qtile cmd-obj -o root -f to_screen -a "${PRESENTER_SCREEN}"
    fi

    # Toggles content group, moves content window to group and puts fullscreen on
    qtile cmd-obj -o screen -f toggle_group -a "${CONTENT_GROUP}"
    qtile cmd-obj -o window "${CONTENT_ID}" -f togroup -a "${CONTENT_GROUP}"
    qtile cmd-obj -o window "${CONTENT_ID}" -f enable_fullscreen

    if [[ "${SCREENS}" == "2" ]]; then
        # Moves focus back to the presenter screen, and toggles the presenter group
        sleep 0.1
        qtile cmd-obj -o root -f to_screen -a "${STANDARD_SCREEN}"
        qtile cmd-obj -o screen -f toggle_group -a "${PRESENTER_GROUP}"
    fi

    xset s off -dpms
}

if [[ -z "$1" || "$1" != "on" && "$1" != "off" ]]; then
    echo "usage: ${0} [on|off]"
    exit 1
fi

if [[ "$1" == "on" ]]; then
    presentation_mode_on
elif [[ "$1" == "off" ]]; then
    presentation_mode_off
fi
