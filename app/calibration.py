import numpy as np

def get_wavelengths(calibration_coeffs: list[float], spectrum_size: int) -> np.ndarray:
    """
    Calculate the wavelengths for x axis values.
    Polynomial coefficients are ordered from highest to lowest degree (see polyval documentation).
    """
    return np.polyval(calibration_coeffs, np.arange(spectrum_size))
