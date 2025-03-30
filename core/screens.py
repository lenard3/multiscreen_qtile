# Qtile lib imports
from libqtile.config import Screen  # type: ignore
from libqtile import bar  # type: ignore
from libqtile.utils import send_notification  # type: ignore

# Config imports
from core.bar import init_widgets, init_widgets_list


def init_screen(monitorcount: int) -> list[Screen]:
    """
    Configures the screens
    Either one or two
    param: monitorcount -> amount of monitors recognized by xrandr
    """

    send_notification("Screen config changed", f"Monitorcount: {str(monitorcount)}")

    if monitorcount == 1:
        screens = [Screen(top=bar.Bar(widgets=init_widgets_list(),
                                      size=30,
                                      ))]
    elif monitorcount == 2:
        topbar = init_widgets(monitorcount)

        screens = [
            Screen(top=bar.Bar(widgets=topbar[0],
                               size=30,
                               )),
            Screen(top=bar.Bar(widgets=topbar[1],
                               size=30,
                               ))
        ]

    return screens
