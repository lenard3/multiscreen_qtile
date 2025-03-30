#!/usr/bin/env bash
# This script enables a presentation mode
# It automates the process of:
#   1. Opening pympress
#   2. Moving the content window to a 'hidden' group on a second screen
#   3. Enables fullscreen for the content window
#   4. Moves focus back to presenter (fails sometimes)
#   5. Disables xset timeout and dpms
#   6. Pauses and waits until the script is quit (resets the xset timeout and dpms to the starting values)
#   7. closes pympress

if ! [[ -x $(which pympress) ]]; then
    echo "pympress is not installed."
    exit 1
fi

# Change this values

# This group is seen by the audience
CONTENT_GROUP="0"
PRESENTER_SCREEN="1"

# This group is seen by you
PRESENTER_GROUP="1"
STANDARD_SCREEN="0"

SCREENS="$(xrandr | grep -c ' connected ')"
XSET_VALUES="$(xset q | grep "timeout" | awk -F" " '{print $2,$4}')"
XSET_DPMS=$(xset q | grep -q "DPMS is Enabled")

if ! pgrep pympress >/dev/null; then
    pympress &
fi

for ((i = 0; i < 10; i++)); do
    sleep 0.2

    # Tries to get the window ID of the pympress content/presenter window
    CONTENT_ID=$(qtile cmd-obj -o root -f windows | grep -B 3 "Pympress Content" | head -n -3 | grep -o '[0-9]*')
    PRESENTER_ID=$(qtile cmd-obj -o root -f windows | grep -B 3 "Pympress Presenter" | head -n -3 | grep -o '[0-9]*')

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
fi

qtile cmd-obj -o screen -f toggle_group -a "${PRESENTER_GROUP}"

# Turn off xset timeout and DPMS
/usr/bin/xset s off -dpms

while true; do
    echo "To exit press 'q'"
    read -rsn1 CONFIRM

    if [[ $CONFIRM == [qQ] ]]; then
        /usr/bin/xset s "${XSET_VALUES}"

        if $XSET_DPMS; then
            /usr/bin/xset dpms
        fi

        if pgrep pympress >/dev/null; then
            pkill pympress
        fi

        break
    fi
done
