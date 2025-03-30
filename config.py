"""
This config supports 1 or 2 monitor setups and it can semi-dynamically
(with a reload) switch between them.
The reloads can be triggered by manually reloading the config or calling
a script with autorandr, etc.

This config is relatively customized to a specific use-case
It uses bonsai as a layout which means you could create really nested workspaces.
This can be quite confusing in the begining.

It uses qtile-bonsai as a layout.
"""

# Python imports
import os
import subprocess
from time import sleep

# Qtile lib imports
from libqtile import layout, hook, qtile  # type: ignore
from libqtile.config import Match  # type: ignore
from libqtile.utils import send_notification  # type: ignore
from libqtile.log_utils import logger  # type: ignore

# Config files
from core.keymaps import init_keys, init_mouse
from core.layout import init_layout
from core.screens import init_screen
from core.helper import are_monitors_offset, connected_monitors


# --------------- START FILES --------------- #
# ------------------------------------------------------------------
# config.py        |   main file. executed by qtile                |
# ------------------------------------------------------------------
# bar.py           |   generates the bar dynamically               |
# ------------------------------------------------------------------
# keymaps.py       |   generates all keymaps                       |
# ------------------------------------------------------------------
# layout.py        |   sets layout                                 |
# ------------------------------------------------------------------
# screens.py       |   generates screen specific stuff like the bar|
# ------------------------------------------------------------------
# custom_widgets.py|   contains custom widgets                     |
# ------------------------------------------------------------------
# lazy_funcs.py    |   contains all custom lazy functions          |
# ------------------------------------------------------------------
# helper.py        |   contains the helper functions used          |
# ------------------------------------------------------------------
# --------------- END FILES --------------- #


# --------------- START HOOKS --------------- #
# The hooks are called whenever a specific case is triggered.
# They are mostly used for fixing gamma issues, fixing the cursor or loading the autostart file

@hook.subscribe.startup  # type: ignore
def _() -> None:
    # Runs the autostart file. This is run every time qtile is started/restarted
    reset_gamma = os.path.expanduser("~/.scripts/reset_color.sh")
    start_script = os.path.expanduser("~/.config/qtile/scripts/autostart.sh")
    subprocess.call([start_script])
    subprocess.call([reset_gamma])


@hook.subscribe.startup_once  # type: ignore
def _() -> None:
    # fixes the cursor
    subprocess.Popen(['xsetroot', '-cursor_name', 'left_ptr'])


@hook.subscribe.resume  # type: ignore
def _() -> None:
    """
    The reset of the gamma values are necessary, because it gets messed up when the
    screen properties change, the laptop wakes up from sleep, etc.
    """
    sleep(1)
    resetScreenGamma = os.path.expanduser("~/.scripts/reset_color.sh")
    subprocess.check_output([resetScreenGamma, "&"])
    send_notification("arandr", "Gamma reset")


@hook.subscribe.float_change  # type: ignore
def _() -> None:
    """
    Moves a floating window to the front when the floating property is changed
    Sometimes floating windows get stuck in the background when a
    second floating window is returned to fullscreen.
    """
    current_group = qtile.current_group

    if current_group:
        for window in current_group.windows:
            if window.floating:
                window.bring_to_front()


@hook.subscribe.screens_reconfigured  # type: ignore
def _() -> None:
    """
    The reset of the gamma values are necessary, because it gets messed up when the
    screen properties change, the laptop wakes up from sleep, etc.
    """
    send_notification("screens_reconfigured", "Monitorcount changed")
    resetScreenGamma = os.path.expanduser("~/.scripts/reset_color.sh")
    subprocess.check_output([resetScreenGamma])
# --------------- END HOOKS --------------- #


# --------------- START MAIN CONFIG --------------- #
if __name__ in ["config", "__main__"]:

    # --------------- START AMOUNT MONITORS --------------- #
    # Checks if the monitors have the same offset (mirrored)
    # Useful for connecting the Laptop to a second screen you dont see
    # like a projector or similar

    if are_monitors_offset():
        # Determines the amount of monitors connected at start
        # Will influence the rest of the loading
        monitorcount = connected_monitors()
    else:
        # When monitors have no offset config gets loaded as one screen
        monitorcount = 1

    if monitorcount > 2 or monitorcount < 1:
        logger.warning(f"{monitorcount} Monitors not supported. Initializing config for 1 Monitor")
        send_notification("Illegal monitorcount", f"{monitorcount} Monitors not supported")
        monitorcount = 1
    # --------------- END AMOUNT MONITORS --------------- #

    # --------------- START INIT KEYS AND MOUSE --------------- #
    # Sets all the keybinds and groups for the amount of monitors connected.
    # Some of the keybinds differ in functionality when a second monitor is used.
    # Also inits the mouse functionality like resize and move.
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
    # Initializes the screens list
    screens = init_screen(monitorcount)
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
    dgroups_app_rules: list = []  # type: ignore
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
        Match(wm_class='blueman-manager'),
    ])
    auto_fullscreen = True
    focus_on_window_activation = "smart"
    reconfigure_screens = True

    # If things like steam games want to auto-minimize themselves when losing
    # focus, should we respect this or not?
    auto_minimize = True

    # for java ui stuff
    wmname = "LG3D"

    # Printed everytime after qtile loads the config. Makes debugging much easier
    logger.warning("-------------------- QTILE CONFIG LOADED --------------------")
    # --------------- END DEFAULT VALUES --------------- #

# --------------- END MAIN CONFIG --------------- #
