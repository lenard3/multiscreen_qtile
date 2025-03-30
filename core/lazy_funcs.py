# This file contains all lazy functions and funcs used by lazy functions

import subprocess
from libqtile.lazy import lazy  # type: ignore

from os.path import expanduser


def _check_window_move(qtile, change_x: int, change_y: int) -> tuple[int, int]:
    """
    Checks and adjusts the movement of a floating window to ensure it stays within screen boundaries
    or moves into adjacent screens if they exist.

    @param qtile: The qtile manager instance.
    @param change_x (int): The intended horizontal movement.
    @param change_y (int): The intended vertical movement.

    @return (int, int): Adjusted changes for x and y movement.
    """
    window = qtile.current_window
    if not window or not window.floating:
        return change_x, change_y

    # Get window's current position and dimensions
    win_x, win_y = window.x, window.y
    win_width, win_height = window.width, window.height

    # Find the screen where the window is currently located
    current_window_screen = qtile.current_screen

    screen_x, screen_y = current_window_screen.x, current_window_screen.y
    screen_width, screen_height = current_window_screen.width, current_window_screen.height

    # Calculate the new intended position of the window
    new_x = win_x + change_x
    new_y = win_y + change_y

    # Check for adjacent screens
    has_left = any(screen.x + screen.width == screen_x for screen in qtile.screens if screen != current_window_screen)
    has_right = any(screen.x == screen_x + screen_width for screen in qtile.screens if screen != current_window_screen)
    has_top = any(screen.y + screen.height == screen_y for screen in qtile.screens if screen != current_window_screen)
    has_bottom = any(screen.y == screen_y + screen_height for screen in qtile.screens if screen != current_window_screen)

    # Check horizontal boundaries
    if new_x < screen_x and not has_left:
        # Restrict to left edge
        change_x = screen_x - win_x
    elif new_x + win_width > screen_x + screen_width and not has_right:
        # Restrict to right edge
        change_x = (screen_x + screen_width) - (win_x + win_width)

    # Check vertical boundaries
    if new_y < screen_y and not has_top:
        # Restrict to top edge
        change_y = screen_y - win_y
    elif new_y + win_height > screen_y + screen_height and not has_bottom:
        # Restrict to botton edge
        change_y = (screen_y + screen_height) - (win_y + win_height)

    return change_x, change_y


@lazy.function
def update_brightness(qtile):
    widget = qtile.widgets_map["brightness"]
    widget.update(widget.poll())


@lazy.function
def call_rofi_rbw(qtile) -> None:
    """
    Opens the rofi-rbw extension when the database is unlocked
    When its not unlocked, sends notification, because otherwise it leaves qtile
    in a non responsive state

    param: qtile -> necessary for lazy.function but not used

    return: None
    """

    subprocess.run([expanduser("~/.scripts/rofi_bw.sh")])


@lazy.function
def resize_window(qtile, direction: str, amount: int) -> None:
    """
    Resizes the window depending on the state of it (floating or tiled)
    param: qtile -> standard stuff
    param: direction -> which direction the window is resized. Up and left make floating smaller
    param: amount -> How much the window is resized
    return: None
    """
    x: int = 0
    y: int = 0

    window = qtile.current_window
    layout = qtile.current_layout

    if window.floating:
        match direction:
            case "left":
                window.resize_floating(amount * -1, y)
            case "right":
                window.resize_floating(amount, y)
            case "up":
                window.resize_floating(x, amount * -1)
            case "down":
                window.resize_floating(x, amount)
            case _:
                return

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

        x, y = _check_window_move(qtile, x, y)

        window.move_floating(x, y)

    elif direction in ["left", "right", "up", "down"]:
        layout.swap(direction)

    elif direction in ["previous", "next"]:
        layout.swap_tabs(direction)


@lazy.function
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


@lazy.function
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
