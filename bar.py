# Generates the single screen bar and
# changes it when 2 bars are required

# Python import
import os

# Qtile lib import
from libqtile import qtile, widget, bar

home_dir = os.path.expanduser("~")
terminal = "kitty"


def get_backlight_status() -> str:
    """
    Reads the brightness of the laptop monitor and
    returns the correct icon for the bar
    Is called regularly by the GenPollText widget
    """
    with open("/sys/class/backlight/amdgpu_bl1/brightness", "r") as f:
        current_brightness = int(f.read())
    with open("/sys/class/backlight/amdgpu_bl1/max_brightness", "r") as f:
        max_brightness = int(f.read())

    brightness_percent = (current_brightness / max_brightness) * 100

    if brightness_percent <= 30:
        return "󰃞"
    elif brightness_percent <= 70:
        return "󰃟"
    else:
        return "󰃠"


def init_colors() -> list:
    """
    Sets all the colors used in the topbar
    """
    return [["#3D3250", "#3D3250"],  # color 0
            ["#353446", "#353446"],  # color 1
            ["#C4C7C5", "#C4C7C5"],  # color 2
            ["#B07190", "#B07190"],  # color 3
            ["#BFBAAC", "#BFBAAC"],  # color 4
            ["#3466C2", "#3466C2"],  # color 5
            ["#E0B742", "#E0B742"],  # color 6
            ["#D56F6E", "#D56F6E"],  # color 7
            ["#68CB79", "#68CB79"]]  # color 8


colors = init_colors()


def init_widgets_list() -> list:
    """
    Initializes the bar for one monitor
    """
    widgets_list = [
            widget.Spacer(
                length=2,
                background=colors[1]
                ),

            # Start Left Side of the bar
            widget.Image(  # The arcolinux png
                         # This file may not exist for your system
                         filename="/usr/share/pixmaps/arcolinux.png",
                         background=colors[1],
                         margin=3,
                         mouse_callbacks={
                             # Left click opens the powermenu
                             'Button1': lambda: qtile.spawn("arcolinux-powermenu"),
                             # Right click opens config time
                             'Button3': lambda: qtile.spawn(f'{terminal} -e nvim {home_dir}/.config/qtile/config.py')
                             }
                         ),
            widget.GroupBox(  # This is Desktop 1-9
                            font="JetBrainsMono Nerd Font",
                            fontsize=15,
                            foreground=colors[2],
                            background=colors[1],
                            borderwidth=6,
                            highlight_method="text",
                            this_current_screen_border=colors[5],
                            active=colors[3],
                            inactive=colors[4],
                            this_screen_border=colors[4],
                            other_current_screen_border=colors[5],
                            other_screen_border=colors[4],
                            disable_drag=True,
                            margin_y=3,
                            margin_x=8,
                            highlight_color=colors[5],
                            ),
            widget.Image(
                filename="~/.config/qtile/Assets/1.png"
                ),
            widget.AGroupBox(
                background=colors[1],
                foreground=colors[2],
                font="JetBrainsMono Nerd Font",
                fontsize=15,
                borderwidth=0,
                ),
            widget.Prompt(
                background=colors[1],
                foreground=colors[2],
                font="JetBrainsMono Nerd Font",
                ),
            # End of the left side of the bar

            widget.Spacer(
                    length=bar.STRETCH,
                    background=colors[1]
                    ),

            # Start of the Center bar
            widget.Image(
                    filename="~/.config/qtile/Assets/1.png"
                    ),
            widget.Pomodoro(
                    background=colors[1],
                    foreground=colors[2],
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    prefix_inactive="P"
                    ),
            widget.TextBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    text="",
                    foreground=colors[6],
                    background=colors[1]
                    ),
            widget.CPU(
                    format="{load_percent}%",
                    foreground=colors[2],
                    background=colors[1],
                    update_interval=2,
                    mouse_callbacks={
                        'Button1': lambda: qtile.spawn(f"{terminal} -e btop")
                        }
                    ),
            widget.ThermalSensor(
                    background=colors[1],
                    foreground=colors[5],
                    # you may need to find the correct sensor tag
                    # use 'sensors' in the terminal
                    tag_sensor="CPU",
                    format=" {temp:.0f}{unit}",
                    threshold=70.0
                    ),
            widget.TextBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    text="﬙",
                    foreground=colors[5],
                    background=colors[1]
                    ),
            widget.Memory(
                    format="{MemUsed:.0f}{mm}",
                    foreground=colors[2],
                    background=colors[1],
                    update_interval=2,
                    mouse_callbacks={
                        'Button1': lambda: qtile.spawn(f"{terminal} -e btop")
                        }
                    ),
            widget.Image(
                    filename="~/.config/qtile/Assets/2.png"
                    ),
            # End of the center bar

            # Start of the Right Side of the bar
            widget.Spacer(
                    length=bar.STRETCH,
                    background=colors[1]
                    ),
            widget.Systray(
                    background=colors[1]
                    ),
            widget.Image(
                    filename="~/.config/qtile/Assets/2.png"
                    ),
            widget.Wlan(
                    background=colors[1],
                    foreground=colors[2],
                    disconnected_message="No Wifi",
                    format="{essid}",
                    interface="wlan0",  # you may need to change the interface
                    ),
            widget.Spacer(
                    length=5,
                    background=colors[1]
                    ),
            widget.GenPollText(
                    name="brightness",
                    background=colors[1],
                    foreground="#B99BCE",
                    fontsize=15,
                    func=get_backlight_status,
                    update_interval=5,
                    ),
            widget.Backlight(
                    background=colors[1],
                    foreground=colors[2],
                    backlight_name="amdgpu_bl1",
                    step=5,
                    ),
            widget.BatteryIcon(
                    background=colors[1],
                    theme_path="~/.config/qtile/Assets/Battery/"
                    ),
            widget.Battery(
                    foreground=colors[2],
                    background=colors[1],
                    format="{percent:2.0%}"
                    ),
            widget.Volume(
                    foreground=colors[2],
                    background=colors[1],
                    theme_path="~/.config/qtile/Assets/Volume/",
                    ),
            widget.Spacer(
                    length=-12,
                    background=colors[1]
                    ),
            widget.Volume(
                    background=colors[1],
                    foreground=colors[2],
                    mouse_callbacks={
                        'Button1': lambda: qtile.spawn(f"{home_dir}/.scripts/rofi-sound-picker")
                        },

                    ),

            widget.TextBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    text="",
                    foreground=colors[2],
                    background=colors[1]
                    ),
            widget.Clock(  # Shows the date in DMY-Format
                        format='%d-%b-%Y',
                        foreground=colors[2],
                        background=colors[1]
                        ),
            widget.Clock(  # Clock in 24h Format
                        foreground=colors[2],
                        background=colors[1]
                        ),
            widget.Spacer(
                    length=5,
                    background=colors[1]
                    )
    ]
    return widgets_list


def init_widgets(amount_screen: int) -> tuple:
    """
    Generates two bars if necessary and manipulates them
    for the multimonitor setup
    When one screen is connected, one bar is generated
    """
    if amount_screen == 2:
        # initialising two topbars
        bar1 = init_widgets_list()
        bar2 = init_widgets_list()

        # removing the standard groupbox from both bars
        bar1.pop(2)
        bar2.pop(2)

        # insert custom groupbox
        bar1.insert(2,
                    widget.GroupBox(  # This is Desktop 1-4
                                    font="JetBrainsMono Nerd Font",
                                    fontsize=15,
                                    foreground=colors[2],
                                    background=colors[1],
                                    borderwidth=6,
                                    highlight_method="text",
                                    this_current_screen_border=colors[5],
                                    active=colors[3],
                                    inactive=colors[4],
                                    this_screen_border=colors[4],
                                    other_current_screen_border=colors[5],
                                    other_screen_border=colors[4],
                                    disable_drag=True,
                                    margin_y=3,
                                    margin_x=8,
                                    highlight_color=colors[5],
                                    visible_groups=["1", "2", "3", "4"]
                                    )
                    )
        # insert inidcator on which screen you are
        bar1.insert(14,
                    widget.CurrentScreen(
                        background=colors[1],
                        active_text="  ",
                        font="JetBrainsMono Nerd Font",
                        fontsize=15,
                        inactive_text="  "
                        )
                    )

        # insert custom groupbox
        bar2.insert(2,
                    widget.GroupBox(  # This is Desktop 5-9
                                    font="JetBrainsMono Nerd Font",
                                    fontsize=15,
                                    foreground=colors[2],
                                    background=colors[1],
                                    borderwidth=6,
                                    highlight_method="text",
                                    this_current_screen_border=colors[5],
                                    active=colors[3],
                                    inactive=colors[4],
                                    this_screen_border=colors[4],
                                    other_current_screen_border=colors[5],
                                    other_screen_border=colors[4],
                                    disable_drag=True,
                                    margin_y=3,
                                    margin_x=8,
                                    highlight_color=colors[5],
                                    visible_groups=["5", "6", "7", "8", "9"]
                                    )
                    )
        # insert inidcator on which screen you are
        bar2.insert(14,
                    widget.CurrentScreen(
                        background=colors[1],
                        active_text="  ",
                        font="JetBrainsMono Nerd Font",
                        fontsize=15,
                        inactive_text="  "
                        )
                    )
        # remove systray from second monitor
        # it would crash anyway
        bar2.pop(17)

        return (bar1, bar2)
    return (init_widgets_list())
