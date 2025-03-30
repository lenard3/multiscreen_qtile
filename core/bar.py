# Generates the single screen bar and
# changes it when 2 bars are required

# Python import
import os

# Qtile lib import
from libqtile import qtile, widget, bar  # type: ignore
from libqtile.utils import send_notification  # type: ignore
from libqtile.log_utils import logger  # type: ignore
from qtile_extras.widget.decorations import PowerLineDecoration, RectDecoration  # type: ignore
from qtile_extras import widget as extra_widget  # type: ignore

# Custom widgets
from core.custom_widgets import MicrophoneWidget, BatteryWithIcon, Brightness, VolumeWithIcon

# Helper functions
from core.helper import parse_window_name, get_clock_icon

home_dir = os.path.expanduser("~")
terminal = "kitty"


def init_catppuccin_mocha():
    """
    Set colors for the bar.
    Uses catppuccin mocha colorscheme
    """
    return [
            ["#f5e0dc", "#f5e0dc"],  # Rosewater 0
            ["#f2cdcd", "#f2cdcd"],  # Flamingo  1
            ["#f5c2e7", "#f5c2e7"],  # Pink      2
            ["#cba6f7", "#cba6f7"],  # Mauve     3
            ["#f38ba8", "#f38ba8"],  # Red       4
            ["#eba0ac", "#eba0ac"],  # Maroon    5
            ["#fab387", "#fab387"],  # Peach     6
            ["#f9e2af", "#f9e2af"],  # Yellow    7
            ["#a6e3a1", "#a6e3a1"],  # Green     8
            ["#94e2d5", "#94e2d5"],  # Teal      9
            ["#89dceb", "#89dceb"],  # Sky       10
            ["#74c7ec", "#74c7ec"],  # Sapphire  11
            ["#89b4fa", "#89b4fa"],  # Blue      12
            ["#b4befe", "#b4befe"],  # Lavender  13
            ["#cdd6f4", "#cdd6f4"],  # Text      14
            ["#bac2de", "#bac2de"],  # Subtext1  15
            ["#a6adc8", "#a6adc8"],  # Subtext0  16
            ["#9399b2", "#9399b2"],  # Overlay2  17
            ["#7f849c", "#7f849c"],  # Overlay1  18
            ["#6c7086", "#6c7086"],  # Overlay0  19
            ["#585b70", "#585b70"],  # Surface2  20
            ["#45475a", "#45475a"],  # Surface1  21
            ["#313244", "#313244"],  # Surface0  22
            ["#1e1e2e", "#1e1e2e"],  # Base      23
            ["#181825", "#181825"],  # Mantle    24
            ["#11111b", "#11111b"],  # Crust     25
            ]


colors = init_catppuccin_mocha()


def init_widgets_list() -> list:
    """
    Always initializes the bar for one monitor. When a second is needed this bar gets copied and manipulated
    """

    decoration_backwards = {
            "decorations": [
                PowerLineDecoration(path="back_slash"),
            ],
            "padding": 10,
            }
    decoration_forwards = {
            "decorations": [
                PowerLineDecoration(path="forward_slash"),
            ],
            "padding": 10,
            }

    widgets_list = [
            widget.Spacer(
                length=2,
                background=colors[23]
                ),

            # Start Left Side of the bar
            widget.Image(  # The arcolinux png
                         # This file may not exist for your system
                         filename="/usr/share/pixmaps/arcolinux.png",
                         background=colors[23],
                         margin=3,
                         mouse_callbacks={
                             # Left click opens the powermenu
                             'Button1': lambda: qtile.spawn("arcolinux-powermenu"),
                             # Right click opens config time
                             'Button3': lambda: qtile.spawn(f'{terminal} -e nvim {home_dir}/.config/qtile/config.py')
                             },
                         ),
            extra_widget.GroupBox(  # This is Desktop 1-9
                                  font="JetBrainsMono Nerd Font",
                                  fontsize=15,
                                  foreground=colors[4],
                                  background=colors[23],
                                  borderwidth=3,
                                  highlight_method="line",
                                  this_current_screen_border=colors[5],
                                  other_current_screen_border=colors[5],
                                  active=colors[4],
                                  inactive=colors[14],
                                  this_screen_border=colors[4],
                                  other_screen_border=colors[4],
                                  disable_drag=True,
                                  margin_y=4,
                                  margin_x=8,
                                  highlight_color=colors[23],
                                  **decoration_backwards
                            ),
            widget.Prompt(
                background=colors[22],
                foreground=colors[14],
                font="JetBrainsMono Nerd Font",
                ),
            # End of the left side of the bar

            widget.Spacer(
                    length=bar.STRETCH,
                    background=colors[22],
                    ),
            widget.TextBox(
                text=' ',
                foreground=colors[14],
                background=colors[22],
                font='JetBrainsMono Nerd Font',
            ),
            widget.WindowName(
                foreground=colors[14],
                background=colors[22],
                font='JetBrainsMono Nerd Font',
                width=bar.CALCULATED,
                empty_group_string='Desktop',
                max_chars=40,
                parse_text=parse_window_name,
            ),
            widget.Spacer(
                    length=bar.STRETCH,
                    background=colors[22],
                    ),

            # Start of the right side of the bar
            extra_widget.Systray(
                    background=colors[22],
                    **decoration_forwards,
                    ),
            widget.Wlan(
                    background=colors[23],
                    foreground=colors[14],
                    disconnected_message="No Wifi",
                    format="{essid}",
                    interface="wlan0",  # you may need to change the interface
                    ),
            widget.Spacer(
                    length=5,
                    background=colors[23]
                    ),
            MicrophoneWidget(
                    background=colors[23],
                    unmuted_foreground=colors[8],
                    muted_foreground=colors[4],
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    markup=True,
                    ),
            Brightness(
                    name="brightness",
                    background=colors[23],
                    foreground=colors[14],
                    ),
            BatteryWithIcon(
                    foreground=colors[14],
                    background=colors[23],
                    above_threshold_foreground=colors[8],
                    below_threshold_foreground=colors[4],
                    no_charge_foreground=colors[7],
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    markup=True,
                    ),
            VolumeWithIcon(
                    foreground=colors[14],
                    background=colors[23],
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    markup=True,
                    update_interval=1,
                    volume_icons=["󰝟", "", "", ""],
                    default_device="@DEFAULT_SINK@",
                    cmd_1=["pactl", "get-sink-volume"],
                    cmd_2=["pactl", "get-sink-mute"],
                    cmd_3=["pactl", "set-sink-mute"],
                    ),
            widget.TextBox(
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    text="",
                    foreground=colors[14],
                    background=colors[23]
                    ),
            widget.Clock(  # Shows the date in DMY-Format
                        format='%d-%b-%Y',
                        foreground=colors[14],
                        background=colors[23]
                        ),
            widget.GenPollText(
                    foreground=colors[14],
                    background=colors[23],
                    font="JetBrainsMono Nerd Font",
                    fontsize=15,
                    func=get_clock_icon,
                    update_interval=300,
                    ),
            widget.Clock(  # Clock in 24h Format
                        foreground=colors[14],
                        background=colors[23]
                        ),
            widget.Spacer(
                    length=5,
                    background=colors[23]
                    )
    ]
    return widgets_list


def init_widgets(monitorcount: int) -> tuple | list:
    """
    Generates two bars if necessary and manipulates them
    for the multimonitor setup
    When one screen is connected, one bar is generated
    """
    decoration_backwards = {
            "decorations": [
                PowerLineDecoration(path="back_slash"),
            ],
            "padding": 10,
            }
    decoration_forwards = {
            "decorations": [
                PowerLineDecoration(path="forward_slash"),
            ],
            "padding": 10,
            }

    if monitorcount == 1:
        return init_widgets_list()
    elif monitorcount == 2:
        # initialising two topbars
        # Copying will not work because some widgets need seperate inits
        bar1 = init_widgets_list()
        bar2 = init_widgets_list()

        # removing the standard groupbox from both bars
        bar1.pop(2)
        bar2.pop(2)

        # insert custom groupbox on first bar
        bar1.insert(2,
                    widget.GroupBox(  # This is Desktop 1-9
                                    font="JetBrainsMono Nerd Font",
                                    fontsize=15,
                                    foreground=colors[4],
                                    background=colors[23],
                                    borderwidth=3,
                                    highlight_method="line",
                                    this_current_screen_border=colors[4],
                                    other_current_screen_border=colors[4],
                                    active=colors[4],
                                    inactive=colors[14],
                                    this_screen_border=colors[4],
                                    other_screen_border=colors[4],
                                    disable_drag=True,
                                    margin_y=4,
                                    margin_x=8,
                                    highlight_color=colors[23],
                                    visible_groups=["1", "2", "3", "4"],
                                    ),
                    )
        # insert inidcator on which screen you are on first bar
        bar1.insert(3,
                    extra_widget.CurrentScreen(
                        background=colors[23],
                        active_color=colors[8],
                        inactive_color=colors[4],
                        active_text="",
                        font="JetBrainsMono Nerd Font",
                        fontsize=15,
                        inactive_text="",
                        **decoration_backwards,
                        )
                    )

        # insert custom groupbox on the second bar
        bar2.insert(2,
                    widget.GroupBox(  # This is Desktop 1-9
                                    font="JetBrainsMono Nerd Font",
                                    fontsize=15,
                                    foreground=colors[4],
                                    background=colors[23],
                                    borderwidth=3,
                                    highlight_method="line",
                                    this_current_screen_border=colors[4],
                                    other_current_screen_border=colors[4],
                                    active=colors[4],
                                    inactive=colors[14],
                                    this_screen_border=colors[4],
                                    other_screen_border=colors[4],
                                    disable_drag=True,
                                    margin_y=4,
                                    margin_x=8,
                                    highlight_color=colors[23],
                                    visible_groups=["5", "6", "7", "8", "9"],
                                    ),
                    )
        # insert inidcator on which screen you are on the second bar
        bar2.insert(3,
                    extra_widget.CurrentScreen(
                        background=colors[23],
                        active_color=colors[8],
                        inactive_color=colors[4],
                        active_text="",
                        font="JetBrainsMono Nerd Font",
                        fontsize=15,
                        inactive_text="",
                        **decoration_backwards,
                        )
                    )

        # Remove the spacer and replace it with the
        # decoratable widget
        bar2.pop(8)
        bar2.insert(8,
                    extra_widget.Spacer(
                        length=bar.STRETCH,
                        background=colors[22],
                        **decoration_forwards
                        ),
                    )
        # remove systray from second monitor
        # it would crash anyway
        bar2.pop(9)

        return bar1, bar2

    # Return one bar when one monitor is connected
    return init_widgets_list()
