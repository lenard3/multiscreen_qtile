from qtile_bonsai import Bonsai


def init_layout() -> list:
    """
    Creates list of all window layout
    Bonsai is in this case the only layout used
    """
    return [
            Bonsai(**{
                "window.margin": 0,
                "window.border_color": "#1e1e2e",
                "window.active.border_color": "#fab387",
                "tab_bar.tab.active.bg_color": "#fab387",
                "tab_bar.tab.active.fg_color": "#11111b",
                "tab_bar.tab.bg_color": "#6b4c39",
                "tab_bar.tab.fg_color": "#cdd6f4",
                "window.border_size": 2,
                "tab_bar.heigth": 20,
                "tab_bar.tab.width": "auto",
                "window.default_add_mode": "match_previous",
                }),
            ]
