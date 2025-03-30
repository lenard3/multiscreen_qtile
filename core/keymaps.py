# This file contains all keymaps and builds them according
# to the amount of monitors connected

# Qtile lib imports
from libqtile.lazy import lazy  # type: ignore
from libqtile.config import (Click, Drag, EzKey, KeyChord, Group,
                             Key, ScratchPad, DropDown)  # type: ignore
from libqtile.log_utils import logger  # type: ignore

# Python imports
from os.path import expanduser

from core.lazy_funcs import (update_brightness, call_rofi_rbw, resize_window,
                             move_window, goToGroup, goToGroupAndMoveWindow)
from core.traverse import up, down, left, right

# default variables
MOD = "mod4"  # Super key (Windows Key)
TERMINAL = "kitty"
ROFI_RUN = "rofi -show"


def keymaps() -> list[object]:
    """
    This function creates all static keybindings that never change
    return: list of all keybindings
    """
    return [
        # spawns a TERMINAL with a vertical split
        # (to the right of the current window)
        EzKey("M-v", lazy.layout.spawn_split(TERMINAL, "x")),
        # spawns a TERMINAL with a horizontal split
        # (under the current window)
        EzKey("M-c", lazy.layout.spawn_split(TERMINAL, "y")),
        # spawns a TERMINAL "ontop" of the current window
        # and creates a new tab/level
        EzKey("M-S-<Return>", lazy.layout.spawn_tab(TERMINAL, new_level=True)),
        # spawns a TERMINAL always as a new tab (on the highest level)
        EzKey("M-<Return>", lazy.layout.spawn_tab(TERMINAL, new_level=False)),

        # Motions to move focus. The names are compatible with built-in layouts.
        EzKey("M-h", lazy.layout.left()),
        EzKey("M-l", lazy.layout.right()),
        EzKey("M-k", lazy.layout.up()),
        EzKey("M-j", lazy.layout.down()),
        # EzKey("M-h", lazy.function(left)),
        # EzKey("M-l", lazy.function(right)),
        # EzKey("M-k", lazy.function(up)),
        # EzKey("M-j", lazy.function(down)),
        EzKey("M-d", lazy.layout.prev_tab()),
        EzKey("M-f", lazy.layout.next_tab()),

        # Resize operations for tiled and floating windows
        EzKey("M-C-h", resize_window("left", 50)),
        EzKey("M-C-l", resize_window("right", 50)),
        EzKey("M-C-k", resize_window("up", 50)),
        EzKey("M-C-j", resize_window("down", 50)),

        # Swap windows/tabs with neighbors or move floating windows around
        EzKey("M-S-h", move_window("left")),
        EzKey("M-S-l", move_window("right")),
        EzKey("M-S-k", move_window("up")),
        EzKey("M-S-j", move_window("down")),
        EzKey("M-S-d", move_window("previous")),
        EzKey("M-S-f", move_window("next")),

        EzKey("M-o", lazy.layout.select_container_outer()),
        EzKey("M-i", lazy.layout.select_container_inner()),
        EzKey("M-r", lazy.layout.normalize(), desc="Reset layout"),

        # Same as the TERMINAL "spawning" just with the application launcher
        # The opened application spawns the same way
        EzKey("A-v", lazy.layout.spawn_split(f"{ROFI_RUN} drun", "x")),
        EzKey("A-c", lazy.layout.spawn_split(f"{ROFI_RUN} drun", "y")),
        EzKey("A-<Space>", lazy.layout.spawn_tab(f"{ROFI_RUN} drun")),
        EzKey("A-S-<Space>", lazy.layout.spawn_tab(f"{ROFI_RUN} drun", new_level=True)),

        # Second "level" of the keyboard
        # Press MOD+w to enter it
        KeyChord(
            [MOD],
            "w",
            [
                # Toggle branch-selection MODe to split/tab over containers of
                # multiple windows. Manipulate using
                # select_branch_out()/select_branch_in()
                EzKey("C-v", lazy.layout.toggle_container_select_mode()),

                EzKey("o", lazy.layout.pull_out(position="next")),
                EzKey("u", lazy.layout.pull_out_to_tab()),

                EzKey("r", lazy.layout.rename_tab()),

                # Directional commands to merge windows with
                # their neighbor into subtabs.
                KeyChord(
                    [],
                    "m",
                    [
                        EzKey("h", lazy.layout.merge_to_subtab("left")),
                        EzKey("l", lazy.layout.merge_to_subtab("right")),
                        EzKey("j", lazy.layout.merge_to_subtab("down")),
                        EzKey("k", lazy.layout.merge_to_subtab("up")),

                        # Merge entire tabs with each other as splits
                        EzKey("S-h", lazy.layout.merge_tabs("previous")),
                        EzKey("S-l", lazy.layout.merge_tabs("next")),
                    ],
                ),

                # Directional commands for push_in() to move
                # window inside neighbor space.
                KeyChord(
                    [],
                    "i",
                    [
                        EzKey("j", lazy.layout.push_in("down")),
                        EzKey("k", lazy.layout.push_in("up")),
                        EzKey("h", lazy.layout.push_in("left")),
                        EzKey("l", lazy.layout.push_in("right")),

                        # It's nice to be able to push directly into the deepest
                        # neighbor node when desired. The default bindings above
                        # will have us push into the largest neighbor container.
                        EzKey(
                            "S-j",
                            lazy.layout.push_in("down",
                                                dest_selection="mru_deepest"),
                            ),
                        EzKey(
                            "S-k",
                            lazy.layout.push_in("up",
                                                dest_selection="mru_deepest"),
                            ),
                        EzKey(
                            "S-h",
                            lazy.layout.push_in("left",
                                                dest_selection="mru_deepest"),
                            ),
                        EzKey(
                            "S-l",
                            lazy.layout.push_in("right",
                                                dest_selection="mru_deepest"),
                            ),
                    ],
                ),
            ]
        ),

        # Toggle between different layouts as defined below
        # Key([MOD], "Tab", lazy.next_layout(), desc="Toggle between layouts"),
        # EzKey("M-q", lazy.window.kill(), desc="Kill focused window"),
        # Key([MOD], "q", lazy.window.kill(), desc="Kill focused window"),
        EzKey("M-q", lazy.window.kill(), desc="Kill focused window"),

        # EzKey("M-S-r", lazy.restart(), desc="Restart qtile"),
        # EzKey("M-S-q", lazy.shutdown(), desc="Shutqtile"),
        Key([MOD, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
        Key([MOD, "control"], "r", lazy.reload_config(), desc="Reload config"),
        Key([MOD, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

        # CUSTOM KEYBINDINGS

        # starts the powermenu to restart, shutdown, etc.
        Key([MOD], "x",
            lazy.spawn("arcolinux-powermenu"),
            desc="Starts the powermenu"
            ),

        # dmenu. app launcher, run commands, search files,
        # connect to past ssh connections and switch windows
        EzKey("A-d", lazy.spawn(f"{ROFI_RUN} run")),
        EzKey("A-s", lazy.spawn(f"{ROFI_RUN} ssh -terminal {TERMINAL}")),
        EzKey("A-w", lazy.spawn(f"{ROFI_RUN} window")),
        EzKey("A-k", lazy.spawn(f"{ROFI_RUN} kill")),
        EzKey("M-p", call_rofi_rbw),
        # Key([MOD], "d",
        #     lazy.spawn("rofi -show run"),
        #     desc="Launches dmenu"
        # ),
        Key([MOD], "m",
            lazy.window.toggle_maximize(),
            desc="Toggle maximize"
            ),

        # Changes the state of the currently focused window to float, or not
        # The floating window stays always on top of all other windows
        EzKey("A-f", lazy.window.toggle_floating()),
        # Key([MOD], "f", lazy.window.toggle_floating()),

        # Can be buggy, when laptop is sleeping with a fullscreen window
        # When it happens the topbar no longer spawns when fullscreen is disabled
        # Just reload the qtile config when that happens
        Key([MOD, "shift"], "m",
            lazy.window.toggle_fullscreen(),
            lazy.hide_show_bar("top"),
            desc="Toggle fullscreen"
            ),

        # Special XF86-Keys
        Key([], "XF86AudioRaiseVolume", lazy.spawn("volume-up")),
        Key([], "XF86AudioLowerVolume", lazy.spawn("volume-down")),
        Key([], "XF86AudioMute", lazy.spawn("amixer set Master toggle")),
        Key([], "XF86AudioMicMute", lazy.spawn("amixer set Capture toggle")),
        Key([], "XF86MonBrightnessUp",
            lazy.spawn("brightnessctl set +5%"),
            update_brightness()),
        Key([], "XF86MonBrightnessDown",
            lazy.spawn("brightnessctl set 5%-"),
            update_brightness()),

        # lock and settings
        EzKey("M-A-l", lazy.spawn("xset s activate")),

        # Screenshot Keys
        Key([], "Print", lazy.spawn("flameshot gui"), desc="Opens Flameshot"),

        Key([MOD], "period", lazy.next_screen(),
            desc="Moves Focus to next monitor"),

    ]


def init_keys(monitorcount: int) -> tuple[list[object], list[Group]]:
    """
    Generates the keymaps and appends the switch group and go to group functions
    param: monitorcount: The amount of monitors connected
    return: keys: all keybindings
    return: groups: all generated groups/scratchpads
    """
    if monitorcount > 2 or monitorcount < 1:
        logger.warning(f"{monitorcount} Monitors is not supported. Initializing config for 1 Monitor.")
        monitorcount = 1

    keys = keymaps()

    if monitorcount == 1:
        # creates 10 Groups (Desktops) for a single connected monitor
        groups = [Group(i) for i in "1234567890"]
        for i in groups:
            keys.extend([
                # Switches to Group
                Key([MOD],
                    i.name,
                    lazy.group[i.name].toscreen(),
                    desc="Switch to group {}".format(i.name)),

                # Moves window to Group
                Key([MOD, "shift"],
                    i.name,
                    lazy.window.togroup(i.name, switch_group=True),
                    desc="Move and switch window to group {}".format(i.name))
            ])

    if monitorcount == 2:
        # creates 10 Groups (Desktops) for a dual monitor setup
        # The last group (0) is hidden and only used for the "presentation mode"
        groups = [
            Group("1", screen_affinity=0),
            Group("2", screen_affinity=0),
            Group("3", screen_affinity=0),
            Group("4", screen_affinity=0),
            Group("5", screen_affinity=1),
            Group("6", screen_affinity=1),
            Group("7", screen_affinity=1),
            Group("8", screen_affinity=1),
            Group("9", screen_affinity=1),
            Group("0", screen_affinity=1)
        ]
        for i in groups:
            keys.append(Key([MOD],
                            i.name,
                            goToGroup(i.name),
                            desc="Switch to group {}".format(i.name)))

            keys.append(Key([MOD, "shift"],
                            i.name,
                            goToGroupAndMoveWindow(i.name),
                            desc="Move & switch window to group{}".format(i.name)))

    # ScratchPad for quick access to floating version of terminal
    groups.append(ScratchPad("scratch", [
        DropDown("qalc", f"kitty --name scratchpad --config {expanduser('~/.config/kitty/kitty_dropdown.conf')}",
                 x=0.15, y=0.1, width=0.7, height=0.8, opacity=1,
                 on_focus_lost_hide=True),
        DropDown("term", f"kitty --name scratchpad --config {expanduser('~/.config/kitty/kitty.conf')}",
                 x=0.15, y=0.1, width=0.7, height=0.8, opacity=1,
                 on_focus_lost_hide=True),
        DropDown("arandr", "arandr",
                 x=0.15, y=0.1, width=0.7, height=0.8, opacity=1,
                 on_focus_lost_hide=True),
        ]))
    keys.extend([
        Key([], "XF86Favorites", lazy.group['scratch'].dropdown_toggle('qalc')),
        Key([], "XF86Messenger", lazy.group['scratch'].dropdown_toggle('term')),
        Key([], "XF86Display", lazy.group['scratch'].dropdown_toggle('arandr')),
        ])
    return (keys, groups)


def init_mouse() -> list[object]:
    """
    Initializes all mouse movements
    """
    return [
        Drag([MOD], "Button1", lazy.window.set_position_floating(),
             start=lazy.window.get_position()),
        Drag([MOD], "Button3", lazy.window.set_size_floating(),
             start=lazy.window.get_size()),
        Click([MOD], "Button2", lazy.window.bring_to_front())
    ]
