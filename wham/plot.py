"""
Plot WHAM free energy barrier, probability, and position histograms.
"""
import matplotlib.pyplot as plt
from scipy.stats import norm
import numpy as np


def plot_energy_barrier(position, free_energy, probability, hist_min, hist_max, title='', save=None):
    """
    Plot WHAM results free energy barrier and Probability.
    """
    fig = plt.figure(figsize=(10, 3), dpi=200)

    ax = fig.add_subplot(1, 2, 1)
    ax.plot(position, free_energy, '-o', c='xkcd:crimson', lw=2, markersize=6)
    ax.set_xlabel('Position')
    ax.set_ylabel('Free energy (kcal / mol)')
    ylims = list(ax.get_ylim())
    ax.plot([hist_min, hist_min], ylims, 'k--')
    ax.plot([hist_max, hist_max], ylims, 'k--')

    ax = fig.add_subplot(1, 2, 2)
    ax.plot(position, probability, '-o', c='xkcd:crimson', lw=2, markersize=6)
    ax.set_xlabel('Position')
    ax.set_ylabel('Probability')
    ylims = list(ax.get_ylim())
    ax.plot([hist_min, hist_min], ylims, 'k--')
    ax.plot([hist_max, hist_max], ylims, 'k--')
    plt.suptitle(title, y=0.95)
    if save is not None:
        plt.savefig(save, transparent=True, bbox_inches='tight', dpi=300)
        plt.close()


def plot_histogram(data, bins=50, color='xkcd:crimson', linestyle='k', alpha=0.25, lw=1.5,
                   xlabel='', ylabel='Frequency', title='', show_points=True):
    """
    Plot position histogram.
    """
    (mu, sigma) = norm.fit(data)
    # the histogram of the data
    n, bins, patches = plt.hist(data, bins, density=1, facecolor=color, alpha=alpha)
    # add a 'best fit' line
    y = norm.pdf(bins, mu, sigma)
    plt.plot(bins, y, linestyle, linewidth=lw)
    if show_points:
        plt.plot([data[0], mu], [max(y), max(y)], 'k-')
        plt.scatter(data[0], max(y), c='k', s=20)
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
