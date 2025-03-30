# Python imports
import subprocess

# Qtile lib imports
from libqtile.widget.base import ThreadPoolText  # type: ignore
from libqtile.log_utils import logger  # type: ignore


class MicrophoneWidget(ThreadPoolText):
    """
    Will give you the status of the microphone. When pressed it will toggle the
    microphone.

    Get the default device with "pactl list sinks short", then take the number
    in the first col. You can also use indicator-sound-switcher and leave the
    device at the default source and switch the source through the switcher.

    @param: update_interval -> Update time in seconds
    @param: muted_foreground -> Color when microphone is muted
    @param: unmuted_foreground -> Color when microphone is unmuted
    @param: default_device -> Uses default mic used by pactl
    @param: cmd_1 -> Command to get the status of the microphone
    @param: cmd_2 -> Command to get the volume of the microphone
    @param: cmd_3 -> Command to toggle the microphone on or off
    """

    def __init__(self,
                 update_interval=1,
                 muted_foreground=["ff0000", "ff0000"],
                 unmuted_foreground=["00ff00", "00ff00"],
                 default_device="@DEFAULT_SOURCE@",
                 cmd_1=["pactl", "get-source-mute"],
                 cmd_2=["pactl", "get-source-volume"],
                 cmd_3=["pactl", "set-source-mute", "toggle"],
                 **config):

        super().__init__("initializing widget", **config)
        self.update_interval = update_interval
        self.muted_foreground = muted_foreground
        self.unmuted_foreground = unmuted_foreground
        self.default_device = default_device

        self.get_mute = cmd_1 + [self.default_device]
        self.get_vol = cmd_2 + [self.default_device]
        self.set_tog = cmd_3[:2] + [self.default_device] + cmd_3[2:]

    def get_mic_status(self) -> str:
        try:
            status = subprocess.run(self.get_mute,
                                    capture_output=True,
                                    text=True)

            level = subprocess.run(self.get_vol,
                                   capture_output=True,
                                   text=True)

            percent = list(filter(None, level.stdout.split("/")[1].split(" ")))

            if "yes" in status.stdout:
                return "<span size='13000' rise='2000'>󰍭</span> <span size='10000' rise='4500'>Mut</span>"
            elif "no" in status.stdout:
                return f"<span size='13000' rise='2000'>󰍬</span> <span size='10000' rise='4500'>{percent[0]}</span>"
            return "󱦉 "

        except Exception as e:
            return f"Error {e}"

    def poll(self):
        status = self.get_mic_status()
        if "󰍭" in status:
            self.foreground = self.muted_foreground
        elif "󰍬" in status:
            self.foreground = self.unmuted_foreground
        else:
            self.foreground = self.muted_foreground
        return status

    def toggle_mic(self):
        try:
            subprocess.run(self.set_tog,
                           capture_output=True,
                           text=True)
        except Exception as e:
            return f"Error {e}"

    def button_press(self, x, y, button):
        if button == 1:
            self.toggle_mic()
            self.update(self.poll())


class BatteryWithIcon(ThreadPoolText):
    """
    Generates a battery icon depending on the percentage the battery is on and
    if its charging, discharging or not charging.

    @param: update_interval -> update time in seconds
    @param: battery_threshold -> at what battery percentage icon color changes
    @param: above_threshold_foreground -> color above the threshold
    @param: below_threshold_foreground -> color below the threshold
    @param: discharge_icons -> icons used when battery is discharging
    @param: charge_icons -> icons used when battery is charging
    @param: no_charge_icon -> icon used when battery is not charging
    """

    def __init__(self,
                 update_interval=60,
                 battery_threshold=30,
                 above_threshold_foreground=["#00ff00", "#00ff00"],
                 below_threshold_foreground=["#ff0000", "#ff0000"],
                 no_charge_foreground=["#ffff00", "ffff00"],
                 discharge_icons=["󱃍", "󰁺", "󰁻", "󰁼", "󰁽", "󰁾", "󰁿", "󰂀", "󰂁", "󰂂", "󰁹"],
                 charge_icons=["󰢜", "󰢜", "󰂆", "󰂇", "󰂈", "󰢝", "󰂉", "󰢞", "󰂊", "󰂋", "󰂅"],
                 no_charge_icon="󱞜",
                 **config):

        super().__init__("initializing widget", **config)
        self.update_interval = update_interval
        self.battery_threshold = battery_threshold
        self.above_threshold_foreground = above_threshold_foreground
        self.below_threshold_foreground = below_threshold_foreground
        self.no_charge_foreground = no_charge_foreground
        self.discharge_icons = discharge_icons
        self.charge_icons = charge_icons
        self.no_charge_icon = no_charge_icon

    def get_bat_status(self):
        try:
            with open("/sys/class/power_supply/BAT0/capacity", "r") as cap:
                capacity = cap.read().strip()

            return int(capacity)
        except ValueError:
            print("capacity cannot be converted to int")
            return 0
        except Exception as e:
            print(f"Error {e}")
            return 0

    def get_charging_status(self) -> int:
        try:
            with open("/sys/class/power_supply/BAT0/status", "r") as charg:
                charging = charg.read().lower().strip()

            if charging == "charging" or charging == "full":
                return 0
            elif charging == "discharging":
                return 1
            elif charging == "not charging":
                return 2
            else:
                return 1

        except Exception as e:
            logger.warning(f"Error {e}")
            return -1

    def set_color(self, capacity, status) -> None:
        if status == 2:
            self.foreground = self.no_charge_foreground
            return
        if capacity >= self.battery_threshold:
            self.foreground = self.above_threshold_foreground
        elif capacity < self.battery_threshold:
            self.foreground = self.below_threshold_foreground
        else:
            self.foreground = self.below_threshold_foreground

    def poll(self):
        capacity: int = self.get_bat_status()
        status = self.get_charging_status()
        self.set_color(capacity, status)
        thresholds = [10, 20, 30, 40, 50, 60, 70, 80, 90, 95, 100]

        if status == -1:
            return "Err"
        elif status == 0:
            for i, threshold in enumerate(thresholds):
                if capacity <= threshold:
                    return f"<span size='13000' rise='3000'>{self.charge_icons[i]}</span> <span size='10000' rise='4500'>{capacity}%</span>"
        elif status == 1:
            for i, threshold in enumerate(thresholds):
                if capacity <= threshold:
                    return f"<span size='13000' rise='3000'>{self.discharge_icons[i]}</span> <span size='10000' rise='4500'>{capacity}%</span>"
        elif status == 2:
            return f"<span size='13000' rise='3000'>{self.no_charge_icon}</span> <span size='10000' rise='4500'>{capacity}%</span>"


class Brightness(ThreadPoolText):
    def __init__(self,
                 update_interval=1,
                 brightness_icons=["󰃞", "󰃟", "󰃠"],
                 backlight_name="amdgpu_bl1",
                 **config):

        super().__init__("initializing widget", **config)
        self.update_interval = update_interval
        self.brightness_icons = brightness_icons
        self.backlight_name = backlight_name

        with open(f"/sys/class/backlight/{self.backlight_name}/max_brightness", "r") as max_brightness:
            self.max_brightness = int(max_brightness.read())

    def get_brightness(self):
        with open(f"/sys/class/backlight/{self.backlight_name}/brightness", "r") as bright:
            brightness = round(int(bright.read()) / self.max_brightness * 100)

        if brightness <= 33:
            return f"<span size='13000' rise='3000'>{self.brightness_icons[0]}</span> <span size='10000' rise='5500'>{brightness}%</span>"
        elif brightness <= 66:
            return f"<span size='13000' rise='3000'>{self.brightness_icons[1]}</span> <span size='10000' rise='5500'>{brightness}%</span>"
        else:
            return f"<span size='13000' rise='3000'>{self.brightness_icons[2]}</span> <span size='10000' rise='5500'>{brightness}%</span>"

    def poll(self):
        return self.get_brightness()


class VolumeWithIcon(ThreadPoolText):
    def __init__(self,
                 update_interval=1,
                 volume_icons=["󰝟", "", "", ""],
                 default_device="@DEFAULT_SINK@",
                 cmd_1=["pactl", "get-sink-volume"],
                 cmd_2=["pactl", "get-sink-mute"],
                 cmd_3=["pactl", "set-sink-mute"],
                 **config):

        super().__init__("initializing widget", **config)
        self.update_interval = update_interval
        self.volume_icons = volume_icons
        self.default_device = default_device
        self.cmd_1 = cmd_1
        self.cmd_2 = cmd_2
        self.cmd_3 = cmd_3
        self.cmd_1.append(self.default_device)
        self.cmd_2.append(self.default_device)
        self.cmd_3.append(self.default_device)

    def get_volume(self):
        cmd = list(filter(None, subprocess.run(self.cmd_1,
                             capture_output=True,
                             text=True).stdout.split(" ")))
        mute = subprocess.run(self.cmd_2,
                              capture_output=True,
                              text=True)
        volume = int(cmd[4].strip("%"))

        if "yes" in mute.stdout:
            return f"<span size='13000' rise='2000'>{self.volume_icons[0]}</span> <span size='10000' rise='4000'>Mut</span>"
        if volume <= 33:
            return f"<span size='13000' rise='2000'>{self.volume_icons[1]}</span> <span size='10000' rise='4000'>{volume}%</span>"
        elif volume <= 66:
            return f"<span size='13000' rise='2000'>{self.volume_icons[2]}</span> <span size='10000' rise='4000'>{volume}%</span>"
        elif volume >= 66:
            return f"<span size='13000' rise='2000'>{self.volume_icons[3]}</span> <span size='10000' rise='4000'> {volume}%</span>"

        return f"<span size='13000' rise='2000'>{self.volume_icons[0]}</span> <span size='10000' rise='4000'>?%</span>"

    def set_mute(self):
        try:
            subprocess.run(self.cmd_3)
        except Exception as e:
            print(f"Error: {e}")

    def poll(self):
        return self.get_volume()

    def button_press(self, x, y, button):
        if button == 1:
            self.set_mute()
            self.update(self.poll())
