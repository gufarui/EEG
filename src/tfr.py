from __future__ import annotations

import numpy as np
import mne


def tfr_multitaper_epochs(
    epochs: mne.Epochs,
    fmin: float = 2.0,
    fmax: float = 50.0,
    n_freqs: int = 20,
    tbw: float = 4.0,
) -> mne.time_frequency.EpochsTFR:
    freqs = np.logspace(np.log10(fmin), np.log10(fmax), n_freqs)
    n_cycles = freqs / 2.0
    power = mne.time_frequency.tfr_multitaper(
        epochs, freqs=freqs, n_cycles=n_cycles, time_bandwidth=tbw, return_itc=False, decim=2
    )
    return power

