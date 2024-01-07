from acquisition import Acquisition
from calibration import get_wavelengths
from plotting import SpectrumPlotter

# Region of interest (x, y, width, height)
roi = (
    0,
    438,
    1920,
    30,
)

# Calibration coefficients for the spectrometer used in this example.
calibration_coeffs = [
    361.175805,
    0.25881296,
    2.843242e-5,
    -9.2885e-9,
]

acquisition = Acquisition(roi)
acquisition.set_exposure(-2)

wavelengths = get_wavelengths(calibration_coeffs[::-1], roi[2])

plot = SpectrumPlotter(wavelengths)

try:
    while True:
        frame = acquisition.capture_frame()
        if frame is None:
            break

        spectrum = acquisition.get_spectrum(frame)
        plot.update_plot(spectrum, frame)

finally:
    acquisition.close()
    plot.close()
