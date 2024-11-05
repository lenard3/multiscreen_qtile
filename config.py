# Copyright (c) 2010 Aldo Cortesi
# Copyright (c) 2010, 2014 dequis
# Copyright (c) 2012 Randall Ma
# Copyright (c) 2012-2014 Tycho Andersen
# Copyright (c) 2012 Craig Barnes
# Copyright (c) 2013 horsik
# Copyright (c) 2013 Tao Sauvage
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""
The assets for the topbar are taken from:
https://github.com/Darkkal44/CozyTile

It uses qtile-bonsai as a layout.

This config is relatively customized to a specific use-case
It uses bonsai as a layout which means
you could create really nested workspaces.
This can be quite confusing in the begining

This config supports 1 or 2 monitor setups and it can semi-dynamically
(with a reload) switch between them
"""

# Python imports
import os
import subprocess
from time import sleep

# Qtile lib imports
from libqtile import layout, hook
from libqtile.config import Match
from libqtile.utils import send_notification

# Config files
from keymaps import init_keys, init_mouse
from layout import init_layout
from screens import screenConfig


# --------------- START FILES --------------- #
# -----------------------------------------------------------
# config.py |   main file. executed by qtile                |
# -----------------------------------------------------------
# bar.py    |   generates the bar dynamically               |
# -----------------------------------------------------------
# keymaps.py|   generates all keymaps                       |
# -----------------------------------------------------------
# layout.py |   sets layout                                 |
# -----------------------------------------------------------
# screens.py|   generates screen specific stuff like the bar|
# -----------------------------------------------------------
# --------------- END FILES --------------- #


# --------------- START HOOKS --------------- #
@hook.subscribe.startup
def start_once() -> None:
    # Runs the autostart file. This is run every time qtile is started/restarted
    start_script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    reset_gamma = os.path.expanduser("~/.config/qtile/scripts/reset_color.sh")
    subprocess.call([start_script])
    subprocess.call([reset_gamma])


@hook.subscribe.startup_once
def start_always() -> None:
    # fixes the cursor
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.resume
def reset_screen_gamma() -> None:
    sleep(1)
    resetScreenGamma = os.path.expanduser("~/.config/qtile/scripts/reset_color.sh")
    subprocess.check_output([resetScreenGamma])
    send_notification("arandr", "Gamma reset")


# Detects changes in screen configuration and reloads the qtile config
# This hook can be quite unpredictable. It sometimes gets fired up to 10 times
# when you plug in a monitor
# The reset of the screen gamma is necessary for me, because it creates a blue
# hue when resuming or restarting
@hook.subscribe.screens_reconfigured
def screenReconfigured() -> None:
    send_notification("screens_reconfigured", "Monitorcount changed")
    resetScreenGamma = os.path.expanduser("~/.config/qtile/scripts/reset_color.sh")
    subprocess.check_output([resetScreenGamma])
# --------------- END HOOKS --------------- #


# --------------- START MAIN CONFIG --------------- #
if __name__ in ["config", "__main__"]:
    # --------------- START AMOUNT MONITORS --------------- #
    # Determines the amount of monitors connected at start
    # Will influence the rest of the loading
    monitorcount_script = os.path.expanduser("~/.scripts/connected_monitors.sh")
    monitorcount = int(subprocess.check_output([monitorcount_script]))
    # --------------- END AMOUNT MONITORS --------------- #

    # --------------- START INIT KEYS AND MOUSE --------------- #
    keys_groups = init_keys(monitorcount)
    keys = keys_groups[0]
    groups = keys_groups[1]
    mouse = init_mouse()
    # --------------- END INIT KEYS AND MOUSE --------------- #

    # --------------- START INIT LAYOUTS --------------- #
    # Initializes all layouts configured (currently bonsai)
    layouts = init_layout()
    # --------------- END INIT LAYOUTS --------------- #

    # --------------- START INIT SCREENS --------------- #
    # screenConfig returns a tuple of the screens and topbar(s)
    screen_tuple = screenConfig(monitorcount)

    # Sets the screen and widget_screen vars to the correct values
    if len(screen_tuple) == 2:
        # 1 Monitor
        screens = screen_tuple[0]
        widgets_screen1 = screen_tuple[1]
    elif len(screen_tuple) == 3:
        # 2 Monitors
        screens = screen_tuple[0]
        widgets_screen1 = screen_tuple[1]
        widgets_screen2 = screen_tuple[2]
    # --------------- END INIT SCREENS --------------- #

    # Widget default settings
    widget_defaults = dict(
        font='JetBrainsMono Nerd Font',
        fontsize=12,
        padding=5,
    )
    # same as widget_defaults
    extension_defaults = widget_defaults.copy()

    # --------------- START DEFAULT VALUES --------------- #
    # Different default variables
    main = None
    dgroups_key_binder = None
    dgroups_app_rules = []  # type: List
    follow_mouse_focus = False
    bring_front_click = False
    cursor_warp = False
    floating_layout = layout.Floating(float_rules=[
        # Run the utility of `xprop` to see the wm class and name of an X client.
        *layout.Floating.default_float_rules,
        Match(wm_class='confirmreset'),  # gitk
        Match(wm_class='makebranch'),  # gitk
        Match(wm_class='maketag'),  # gitk
        Match(wm_class='ssh-askpass'),  # ssh-askpass
        Match(title='branchdialog'),  # gitk
        Match(title='pinentry'),  # GPG key password entry
    ])
    auto_fullscreen = True
    focus_on_window_activation = "smart"
    reconfigure_screens = True

    # If things like steam games want to auto-minimize themselves when losing
    # focus, should we respect this or not?
    auto_minimize = True

    # for java ui stuff
    wmname = "LG3D"
    # --------------- END DEFAULT VALUES --------------- #

# --------------- END MAIN CONFIG --------------- #
