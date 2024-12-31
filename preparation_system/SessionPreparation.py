import numpy as np
from typing import Union
from scipy.integrate import simps
from mne.time_frequency import psd_array_multitaper

class SessionPreparation:
    def __init__(self, configuration):
        self.configuration = configuration

    def correct_missing_samples(self, raw_session: dict, placeholder: Union[int, str, None]) -> dict:
        """
        corrects the missing samples with an interpolation function
        :param raw_session: raw session
        :param placeholder: missing value to replace
        :return: False if records are missing, the raw session otherwise (as dict)
        """

        # Find indices of null values in the list
        null_indices = [i for i, value in enumerate(raw_session['eeg']) if value is placeholder]

        # Create an array of indices for the non-null values
        other_indices = [i for i in range(len(raw_session['eeg'])) if i not in null_indices]

        # Perform linear interpolation for each null value and update the list in place
        for null_index in null_indices:
            # Use numpy.interp for linear interpolation
            interpolated_value = np.interp(null_index, other_indices, [raw_session['eeg'][i] for i in other_indices])

            # Update the value in the original data list
            raw_session['eeg'][null_index] = interpolated_value
        return raw_session

    def correct_outliers(self, raw_session: dict) -> dict:
        """
        corrects outliers using the value_range.
        :param raw_session: raw_session
        :return: the corrected Raw session
        """

        min_value, max_value = self.value_range

        # bound between min and max
        raw_session['eeg'] = [min(max(value, min_value), max_value) for value in raw_session['eeg']]
        return raw_session

    def extract_feature(self, time_series: list, sf: float, band: list, relative=False) -> float:
        """Compute the average power of the signal x in a specific frequency band.
        Requires MNE-Python >= 0.14.
        """
        band = np.asarray(band)
        low, high = band
        psd, frequencies = psd_array_multitaper(time_series, sf, adaptive=True, normalization='full', verbose=0)

        # Frequency resolution
        freq_res = frequencies[1] - frequencies[0]

        # Find index of band in frequency vector
        idx_band = np.logical_and(frequencies >= low, frequencies <= high)

        # Integral approximation of the spectrum using parabola (Simpson's rule)
        bp = simps(psd[idx_band], dx=freq_res)
        if relative:
            bp /= simps(psd, dx=freq_res)

        return bp

    def create_prepared_session(self, raw_session: dict) -> dict:
            prepared_session = {
                "uuid": raw_session["uuid"],
                "label": raw_session["label"],
            }

            time_series = np.array(raw_session['eeg'])

            for band in self.bandwidths:
                prepared_session[band] = self.extract_feature(time_series, self.sf, self.bandwidths[band])

            prepared_session["activity"] = raw_session["activity"]
            prepared_session["genre"] = raw_session["genre"]

            return prepared_session
