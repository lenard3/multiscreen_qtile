# This file contains all keymaps and builds them according
# to the amount of monitors connected

# Qtile lib imports
from libqtile.lazy import lazy
from libqtile.config import Click, Drag, EzKey, KeyChord, Group, Key, Match, Screen, ScratchPad, DropDown

# Python imports
from os.path import expanduser

# default variables
MOD = "mod4"  # Super key (Windows Key)
TERMINAL = "kitty"
ROFI_RUN = "rofi -show drun"


@lazy.function
def resize_window(qtile, direction: str, amount: int) -> None:
    """
    Resizes the window depending on the state of it (floating or tiled)
    param: qtile -> standard stuff
    param: direction -> which direction the window is resized. Up and left make floating smaller
    param: amount -> How much the window is resized
    return: None
    """
    x = 0
    y = 0
    window = qtile.current_window
    layout = qtile.current_layout

    if window.floating:
        match direction:
            case "left":
                x = -100
            case "right":
                x = 100
            case "up":
                y = -100
            case "down":
                y = 100

        window.resize_floating(x, y)

    elif direction in ["left", "right", "up", "down"]:
        layout.resize(direction, amount)


@lazy.function
def move_window(qtile, direction: str) -> None:
    """
    Move the window depending on the state of it (floating or tiled)
    Floating windows are actually moved around. Tiled ones are swapped with the neighbour
    param: qtile -> standard stuff
    param: direction -> which direction the window is moved
    return: None
    """
    x = 0
    y = 0
    window = qtile.current_window
    layout = qtile.current_layout

    if window.floating:
        match direction:
            case "left":
                x = -100
            case "right":
                x = 100
            case "up":
                y = -100
            case "down":
                y = 100

        window.move_floating(x, y)

    elif direction in ["left", "right", "up", "down"]:
        layout.swap(direction)

    elif direction in ["previous", "next"]:
        layout.swap_tabs(direction)


def keymaps():
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
        EzKey("M-d", lazy.layout.prev_tab()),
        EzKey("M-f", lazy.layout.next_tab()),

        # Resize operations for tiled and floating windows
        EzKey("M-C-h", resize_window("left", 100)),
        EzKey("M-C-l", resize_window("right", 100)),
        EzKey("M-C-k", resize_window("up", 100)),
        EzKey("M-C-j", resize_window("down", 100)),

        # Swap windows/tabs with neighbors or move floating windows around
        EzKey("M-S-h", move_window("left")),
        EzKey("M-S-l", move_window("right")),
        EzKey("M-S-k", move_window("up")),
        EzKey("M-S-j", move_window("down")),
        EzKey("M-S-d", move_window("previous")),
        EzKey("M-S-f", move_window("next")),

        # Move to specific tab at the nearest tab level
        # Only works for up to 9 tabs
        EzKey("C-1", lazy.layout.focus_nth_tab(1, level=-1)),
        EzKey("C-2", lazy.layout.focus_nth_tab(2, level=-1)),
        EzKey("C-3", lazy.layout.focus_nth_tab(3, level=-1)),
        EzKey("C-4", lazy.layout.focus_nth_tab(4, level=-1)),
        EzKey("C-5", lazy.layout.focus_nth_tab(5, level=-1)),
        EzKey("C-6", lazy.layout.focus_nth_tab(6, level=-1)),
        EzKey("C-7", lazy.layout.focus_nth_tab(7, level=-1)),
        EzKey("C-8", lazy.layout.focus_nth_tab(8, level=-1)),
        EzKey("C-9", lazy.layout.focus_nth_tab(9, level=-1)),

        EzKey("M-o", lazy.layout.select_container_outer()),
        EzKey("M-i", lazy.layout.select_container_inner()),

        # Same as the TERMINAL "spawning" just with the application launcher
        # The opened application spawns the same way
        EzKey("A-v", lazy.layout.spawn_split(ROFI_RUN, "x")),
        EzKey("A-c", lazy.layout.spawn_split(ROFI_RUN, "y")),
        EzKey("A-<Space>", lazy.layout.spawn_tab(ROFI_RUN)),
        EzKey("A-S-<Space>", lazy.layout.spawn_tab(ROFI_RUN, new_level=True)),

        # Second "level" of the keyboard
        # Press MOD+w to enter it
        KeyChord(
            [MOD],
            "w",
            [
                # Toggle branch-selection MODe to split/tab over containers of
                # multiple windows. Manipulate using
                # select_branch_out()/select_branch_in()
                EzKey("C-v", lazy.layout.toggle_container_select_MODe()),

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
        Key([MOD], "q", lazy.window.kill(), desc="Kill focused window"),

        # EzKey("M-S-r", lazy.restart(), desc="Restart qtile"),
        # EzKey("M-S-q", lazy.shutdown(), desc="Shutqtile"),
        Key([MOD, "shift"], "r", lazy.restart(), desc="Restart Qtile"),
        Key([MOD, "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile"),

        # CUSTOM KEYBINDINGS

        # starts the powermenu to restart, shutdown, etc.
        Key([MOD], "x",
            lazy.spawn("arcolinux-powermenu"),
            desc="Starts the powermenu"
            ),

        # dmenu. app launcher, run commands, search files,
        # connect to past ssh connections and switch windows
        EzKey("A-d", lazy.spawn("rofi -show run")),
        EzKey("A-s", lazy.spawn("rofi -show ssh")),
        EzKey("A-w", lazy.spawn("rofi -show window")),
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
        Key([], "XF86Display", lazy.spawn("arandr")),
        Key([], "XF86MonBrightnessUp", lazy.spawn("brightnessctl set +5%")),
        Key([], "XF86MonBrightnessDown", lazy.spawn("brightnessctl set 5%-")),

        # lock and settings
        EzKey("M-A-l", lazy.spawn("xset s activate")),

        # Screenshot Keys
        Key([], "Print", lazy.spawn("flameshot gui"), desc="Opens Flameshot"),

        Key([MOD], "period", lazy.next_screen(),
            desc="Moves Focus to next monitor"),

    ]


def goToGroup(qtile, name: str) -> None:
    """
    This function is called everytime you want to change a group
    The behaviour changes wether one or two monitors are connected
    param: name -> name of the group
    """
    if len(qtile.screens) == 1:
        qtile.groups_map[name].toscreen()
        return

    # Switches Screen focus to the one where the Group is you want to switch to
    # Every Group stays on the defined screen
    # 1-4 on screen 0 (Laptop)
    # 5-9 on screen 1 (secondary screen)
    if name in "1234":
        qtile.focus_screen(0)
        qtile.groups_map[name].toscreen()
    else:
        qtile.focus_screen(1)
        qtile.groups_map[name].toscreen()


def goToGroupAndMoveWindow(qtile, name: str) -> None:
    """
    This function is called everytime you want to move a window to a different group
    The behaviour is the same for one or two monitors
    With two, it also changes the screen to the correct one
    param: name of the group
    """
    if len(qtile.screens) == 1:
        qtile.current_window.togroup(name, switch_group=True)
        return

    # When you want to move a window to another screen this block does that
    # Every Group stays on the defined screen
    # The window will be moved and the focuse changed to the screen
    # & group you moved the window to
    # 1-4 on screen 0 (Laptop)
    # 5-9 on screen 1 (secondary screen)
    if name in "1234":
        qtile.current_window.togroup(name, switch_group=False)
        qtile.focus_screen(0)
        qtile.groups_map[name].toscreen()
    else:
        qtile.current_window.togroup(name, switch_group=False)
        qtile.focus_screen(1)
        qtile.groups_map[name].toscreen()


def init_keys(monitorcount) -> tuple:
    """
    Generates the keymaps and appends the switch group and go to group functions
    param: monitorcount: The amount of monitors connected
    return: keys: all keybindings
    return: groups: all generated groups/scratchpads
    """

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
        # Scratchpads are currently not working when more than one monitor is connected
        groups.append(ScratchPad("scratch", [
            DropDown("qalc", "qalculate-gtk",
                     x=0.15, y=0.1, width=0.7, height=0.8, opacity=1,
                     on_focus_lost_hide=True),
            DropDown("term", f"kitty -c {expanduser('~/.config/kitty/kitty_dropdown.conf')}",
                     x=0.15, y=0.1, width=0.7, height=0.8, opacity=1,
                     on_focus_lost_hide=True),
            ]))
        keys.extend([
            Key([], "XF86Favorites", lazy.group['scratch'].dropdown_toggle('qalc')),
            Key([], "XF86Messenger", lazy.group['scratch'].dropdown_toggle('term')),
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
                            lazy.function(goToGroup, i.name),
                            desc="Switch to group {}".format(i.name)))

            keys.append(Key([MOD, "shift"],
                            i.name,
                            lazy.function(goToGroupAndMoveWindow, i.name),
                            desc="Move & switch window to group{}".format(i.name)))
    return (keys, groups)


def init_mouse() -> list:
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
