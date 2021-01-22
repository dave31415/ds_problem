import numpy as np
from bokeh.plotting import figure, show


def add_hist_plot(x, plot, n_bins=100, x_range=None, normalize=False, norm=1.0, **kwargs):
    if x_range is None:
        x_range = [min(x), max(x)]

    hist, edges = np.histogram(x, bins=n_bins, range=x_range)
    dx = edges[1] - edges[0]
    if normalize:
        hist = hist / (dx*hist.sum())

    hist = hist/norm

    plot.quad(top=hist, bottom=0, left=edges[:-1], right=edges[1:], alpha=0.5, **kwargs)


def hist_plot(x, n_bins=100, x_range=None, normalize=False, **kwargs):
    plot = figure(**kwargs)
    add_hist_plot(x, plot, n_bins=n_bins, x_range=x_range, normalize=normalize, **kwargs)
    show(plot)
    return plot
