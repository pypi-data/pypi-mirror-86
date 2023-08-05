from math import pow
import numpy as np


class TemperatureToRGBW:

    def color_temperature_to_rgb(self, color_temperature_kelvin: float):
        """
        Return an RGB color from a color temperature in Kelvin.
        see
        http://www.tannerhelland.com/4435/convert-temperature-rgb-algorithm-code/
        """
        # vibe check
        if color_temperature_kelvin < 1000:
            color_temperature_kelvin = 1000
        elif color_temperature_kelvin > 40000:
            color_temperature_kelvin = 40000

        tmp_internal = color_temperature_kelvin / 100.0

        red = self.get_red(tmp_internal)

        green = self.get_green(tmp_internal)

        blue = self.get_blue(tmp_internal)

        return red, green, blue

    def get_red(self, temperature: float) -> float:
        """Get the red component"""
        if temperature <= 66:
            return 255
        tmp_red = 329.698727446 * pow(temperature - 60, -0.1332047592)
        return self.bound(tmp_red)

    def get_green(self, temperature: float) -> float:
        """Get the green component"""
        if temperature <= 66:
            green = 99.4708025861 * np.log(temperature) - 161.1195681661
        else:
            green = 288.1221695283 * pow(temperature - 60, -0.0755148492)
        return self.bound(green)

    def get_blue(self, temperature: float) -> float:
        """Get the blue component"""
        if temperature >= 66:
            return 255
        if temperature <= 19:
            return 0
        blue = 138.5177312231 * np.log(temperature - 10) - 305.0447927307
        return self.bound(blue)

    def bound(self, color_component: float, minimum: float = 0, maximum: float = 255) -> float:
        """
        Bound the given color component value between the given min and max values.
        The minimum and maximum values will be included in the valid output.
        i.e. Given a color_component of 0 and a minimum of 10, the returned value
        will be 10.
        """
        color_component_out = max(color_component, minimum)
        return min(color_component_out, maximum)

    def match_max_scale(self, input_colors, output_colors):
        """Match the maximum value of the output to the input."""
        max_in = max(input_colors)
        max_out = max(output_colors)
        if max_out == 0:
            factor = 0.0
        else:
            factor = max_in / max_out
        return tuple(int(round(i * factor)) for i in output_colors)

    def color_rgb_to_rgbw(self, r, g, b):
        """Convert an rgb color to an rgbw representation."""
        # Calculate the white channel as the minimum of input rgb channels.
        # Subtract the white portion from the remaining rgb channels.
        w = min(r, g, b)
        rgbw = (r - w, g - w, b - w, w)

        # Match the output maximum value to the input. This ensures the full
        # channel range is used.
        return self.match_max_scale((r, g, b), rgbw)  # type: ignore

    def kelvin_to_rgbw(self, temperature: int) -> (int, int, int, int):
        r, g, b = self.color_temperature_to_rgb(temperature)
        return self.color_rgb_to_rgbw(r, g, b)
