# Qtile lib imports
from libqtile.config import Screen
from libqtile import bar
from libqtile.utils import send_notification

# Config imports
from bar import init_widgets, init_widgets_list


def init_screen(amount_screens) -> list:
    """
    Configures the screens
    Either one or two
    param: amount_screens -> amount of monitors recognized by xrandr
    """
    topbar = init_widgets(amount_screens)
    if amount_screens == 1:
        screens = [Screen(top=bar.Bar(widgets=init_widgets_list(), size=30))]
        return screens
    elif amount_screens == 2:
        screens = [
            Screen(top=bar.Bar(widgets=topbar[0], size=30)),
            Screen(top=bar.Bar(widgets=topbar[1], size=30))
        ]
        return screens


def screenConfig(monitorcount):
    """
    Initializes everything that has to do with the screen
    Generates the topbar(s) and the screen objects
    param: monitorcount -> amount of monitors recognized by xrandr
    return: (screens, widgets_screen1)
    return: (screens, widgets_screen1, widgets_screen2)
    """
    if int(monitorcount) == 1:
        # When one Monitor is connected it creates the bar for one monitor
        send_notification("Screen config changed", f"Monitorcount: {str(monitorcount)}")
        screens = init_screen(monitorcount)
        widgets_screen1 = init_widgets(monitorcount)
        return screens, widgets_screen1

    else:
        # You can connect 2 Monitors at the moment
        # The two top bars created are a bit different from each other
        send_notification("Screen config changed", f"Monitorcount: {str(monitorcount)}")
        screens = init_screen(2)
        topbar = init_widgets(2)
        widgets_screen1 = topbar[0]
        widgets_screen2 = topbar[1]
        return screens, widgets_screen1, widgets_screen2
