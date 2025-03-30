# Dynamic qtile

> [!IMPORTANT]
> This config uses [qtile-bonsai](https://github.com/aravinda0/qtile-bonsai) as the layout.
> This means you need to install it aswell or configure another layout before loading the config.


# Features of this configuration include

## (Semi)dynamic multiscreen qtile config
This qtile configuration can semi-dynamically switch between a single screen and multiscreen layout.
All you need to do is to configure your screens via arandr, xrandr, autorandr or what ever else you use and reload the config once.
This means the topbar, the keybinds and groups are changed according to the amount of monitors connected to the PC.
The config uses a small script at startup to determine the amount of screens connected.
Reloading the config can be done via an autorandr postswitch. So that no manual reload is required.

> [!NOTE]
> The config can currently only distinguish between 1 or 2 monitors. It uses the Xlib python library with the randr extension.

## Presentation mode
This config also comes with a small 'presentation mode'.
By default it uses [pympress](https://github.com/Cimbali/pympress) as a presenter.
It moves the content window to a hidden group on the second screen and puts it in fullscreen.
The script also disables any xset settings to prevent your PC from going to sleep.
The xset settings will be reset when 'turning off' the presentation mode.
Presentation mode can be turned on or off with `presentation_mode.sh [on|off]`.

> [!NOTE]
> The script can sometimes leave you on the wrong group, you have to sometimes switch to the presenter group yourself.

## Moving and resizing floating windows with the same keybinds as tiled windows
You can move and resize floating windows with your keyboard.
The functions determine if the window is floating or not and move the window or resize it.
Sounds like nothing special but i think its nice being able to move a settings window around when its floating.

## Restricting movement of floating windows to the configured screens
Floating windows, which can be moved with keybinds, are restricted to the configured screens.
When two screens are bordering each other you can move the window over this border, if no screen is bordering you cant.

---

# Requirements
This list may not be complete.
## Presentation mode
- pympress
- xset

## Qtile config
- qtile-bonsai
- xset
- xrandr
- autorandr
- feh
- picom
- dunst
- xfce4-power-manager
- udiskie
- polkit-gnome-authentication-agent-1
- nm-applet
- blueman-applet

---

> [!IMPORTANT]
> This repo only includes the qtile config files and the extra presentation mode script.
> No other files are provided. Maybe in the future.

> [!WARNING]
> Please try and understand whats happening in the config and the scripts that are provided in this repo.
> You should not just copy paste the files and run it.
