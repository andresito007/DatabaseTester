import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy import signal

def Main():
    dataframe = pd.read_csv("0_001.csv")
    pos = dataframe["Position"]
    vel = dataframe["Velocity"]
    tor = dataframe["Torque"]
    cur = dataframe["Current"]

    x, y = pos, cur

    corr = signal.correlate(x, y)
    lags = signal.correlation_lags(len(x), len(y))

    corr /= np.max(corr)
    max_i = np.argmax(corr)
    max_y = corr[max_i]
    max_x = lags[max_i]
    

    fig, (ax_orig, ax_noise, ax_corr) = plt.subplots(3, 1, figsize=(4.8, 4.8))
    ax_orig.plot(x)
    ax_orig.set_title('Position')
    ax_orig.set_xlabel('Sample Number')
    ax_orig.grid(True)
    ax_noise.plot(y)
    ax_noise.set_title('Velocity')
    ax_noise.set_xlabel('Sample Number')
    ax_noise.grid(True)
    ax_corr.plot(lags, corr)
    ax_corr.plot(max_x, max_y, 'ro')
    ax_corr.annotate("({},{})".format(max_x, max_y), xy=[max_x, max_y])
    ax_corr.set_title('Cross-correlated signal')
    ax_corr.set_xlabel('Lag')
    ax_corr.grid(True)
    ax_orig.margins(0, 0.1)
    ax_noise.margins(0, 0.1)
    ax_corr.margins(0, 0.1)
    fig.tight_layout()

    plt.show()

    return None 
    

Main()