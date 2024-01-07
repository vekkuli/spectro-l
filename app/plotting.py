from typing import cast

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.axes import Axes
from matplotlib.cm import ScalarMappable
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.ticker import MaxNLocator


class SpectrumPlotter:
    """
    Display camera image and spectrum plot in real time.
    """

    def __init__(self, wavelengths: np.ndarray):
        self.wavelengths = wavelengths

        self.fig, (self.ax2, self.ax1) = plt.subplots(2, 1, figsize=(10, 12))
        plt.tight_layout(pad=1.3)
        self.ax1 = cast(Axes, self.ax1)
        (self.line,) = self.ax1.plot([], [], color="black")
        self.ax1.set_xlabel("Wavelength")
        self.ax1.set_xlim(self.wavelengths[0], self.wavelengths[-1])
        self.ax1.xaxis.set_major_locator(MaxNLocator(20))

        # Colorbar
        norm = Normalize(vmin=self.wavelengths[0], vmax=self.wavelengths[-1])
        colorlist = list(
            zip(
                norm(self.wavelengths),
                [self._wavelength_to_rgb(w) for w in self.wavelengths],
            )
        )
        spectralmap = LinearSegmentedColormap.from_list("spectrum", colorlist)
        x0, y0, w, h = self.ax1.get_position().bounds
        self.cax = self.fig.add_axes((x0, y0 + h, w, 0.02))
        self.cax.axis("off")
        self.sm = ScalarMappable(norm=norm, cmap=spectralmap)
        self.sm.set_array([])
        plt.colorbar(self.sm, cax=self.cax, orientation="horizontal")

        # Camera image plot
        self.ax2 = cast(Axes, self.ax2)
        self.ax2.axis("off")
        self.image = self.ax2.imshow(
            np.zeros((1920, 1080)),
            cmap="gray",
            aspect="auto",
            vmin=0,
            vmax=255,
        )

        plt.ion()
        plt.show()

    def update_plot(self, spectrum, image):
        self.line.set_data(self.wavelengths, spectrum)
        self.ax1.relim()
        self.ax1.autoscale_view(True, False, True)
        self.image.set_data(image)
        self.fig.canvas.draw()
        self.fig.canvas.flush_events()

    def close(self):
        plt.ioff()

    @staticmethod
    def _wavelength_to_rgb(wavelength, gamma=1.0):
        """
        See https://stackoverflow.com/questions/44959955/matplotlib-color-under-curve-based-on-spectral-color
        """
        wavelength = float(wavelength)
        A = 1.0
        wavelength = min(max(wavelength, 380.0), 750.0)
        if wavelength >= 380 and wavelength <= 440:
            attenuation = 0.3 + 0.7 * (wavelength - 380) / (440 - 380)
            R = ((-(wavelength - 440) / (440 - 380)) * attenuation) ** gamma
            G = 0.0
            B = (1.0 * attenuation) ** gamma
        elif wavelength >= 440 and wavelength <= 490:
            R = 0.0
            G = ((wavelength - 440) / (490 - 440)) ** gamma
            B = 1.0
        elif wavelength >= 490 and wavelength <= 510:
            R = 0.0
            G = 1.0
            B = (-(wavelength - 510) / (510 - 490)) ** gamma
        elif wavelength >= 510 and wavelength <= 580:
            R = ((wavelength - 510) / (580 - 510)) ** gamma
            G = 1.0
            B = 0.0
        elif wavelength >= 580 and wavelength <= 645:
            R = 1.0
            G = (-(wavelength - 645) / (645 - 580)) ** gamma
            B = 0.0
        elif wavelength >= 645 and wavelength <= 750:
            attenuation = 0.3 + 0.7 * (750 - wavelength) / (750 - 645)
            R = (1.0 * attenuation) ** gamma
            G = 0.0
            B = 0.0
        else:
            R = 0.0
            G = 0.0
            B = 0.0
        return (R, G, B, A)
