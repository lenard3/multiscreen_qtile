from Xlib import display
from Xlib.ext import randr
from os.path import basename
from datetime import datetime


def are_monitors_offset() -> bool:
    """
    Checks if monitors found by xrandr are offset from each other

    @param: None

    @return: bool: If monitors have offset True, else False
    """

    d = display.Display()
    root = d.screen().root

    resources = randr.get_screen_resources(root)
    outputs = resources.outputs

    monitors: list = []

    # Gets the x and y coordinates for each monitor and appends them into a list with dict
    for output in outputs:
        output_info = randr.get_output_info(root, output, resources.config_timestamp)

        if output_info.crtc:
            crtc_info = randr.get_crtc_info(root, output_info.crtc, resources.config_timestamp)
            if crtc_info:
                monitors.append({
                    "x": crtc_info.x,
                    "y": crtc_info.y,
                    })

    # No offset possible at this time if more than two or one monitor is connected
    if len(monitors) != 2:
        d.close()
        return False

    # If at least one of the x and y are not the same, monitors have offset
    if monitors[0]["x"] != monitors[1]["x"] or monitors[0]["y"] != monitors[1]["y"]:
        d.close()
        return True

    d.close()
    return False


def connected_monitors() -> int:
    """
    Returns the amount of the connected monitors

    @param: None

    @return: resources.outputs (int): The amount of monitors connected
    """
    d = display.Display()
    root = d.screen().root

    resources = randr.get_monitors(root)

    d.close()

    return resources.outputs


def parse_window_name(text) -> str:
    """
    Some names of Windows are long (firefox, vscode, discord)
    This shortens the names to not take up that much space

    @param: text (str): The text shown in the topbar

    @return: text (str): Possibly newly changed and shortened text
    """
    target_names = [
        "Mozilla Firefox",
        "Visual Studio Code",
        "Discord",
        "Zotero",
    ]
    try:
        if text == "org.pwmt.zathura":
            return "Zathura"

        if "org.pwmt.zathura" in text:
            path, app = text.split(" ", 1)
            filename = basename(path)
            app_name = app.split(".")[-1].capitalize()
            text = f"{app_name} {filename}"

        # "e" is aliased to nvim in zshrc
        if text == "e":
            return "nvim"
        if text.startswith("e "):
            return text.replace("e ", "nvim ", 1)
        # Check for the target name in text and return short version when found
        return next(filter(lambda name: name in text, target_names), text)
    except TypeError:
        return text


def layout_title_provider(index, active_pane, tab) -> str:
    """
    Title generation callback for bonsai layout. Passes the name to window name parser

    @param: index (int): index of the given window
    @param: active_pane: the pane currently in focus
    @param: tab: unused but necessary

    @return: (str) "<index>: <windowname>
    """
    return f"{index+1}: {parse_window_name(active_pane.window.name)}"


def get_clock_icon() -> str:
    """
    Callback from the GenPollText widget used as a text clock icon.
    Gimmick for having the correct nerd font clock for the correct time.

    @param: None

    @return: str: Nerd Font Icon corresponding to the current time
    """
    time = datetime.now().hour
    clock_icons = ["", "", "", "", "", "", "", "", "", "", "", ""]
    return clock_icons[time % 12]
