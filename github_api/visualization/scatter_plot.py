from functools import lru_cache

import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

from ..utils import log


class ScatterPlot:

    DEFAULT_MIN_SIZES = 40
    DEFAULT_SIZES_FACTOR = 0.1

    def __init__(self, args, df):
        self.args = args
        self.df = df
        self.delta = self.max_changes - self.min_changes
        self._set_changes_bins()

    def _set_changes_bins(self):
        step = int(self.delta / self.bins_num)
        bins = range(self.min_changes, self.max_changes, step)
        arr = np.array(bins)
        indexes = arr.searchsorted(self.df['changes'], side='right') - 1
        self.df['changes_bins'] = [arr[i] for i in indexes]
        log.debug(f"changes_bins:\n{self.df['changes_bins']}")

    @property
    @lru_cache(1)
    def bins_num(self):
        # TODO: consider later
        if self.delta < 100:
            return 8
        elif self.delta < 2000:
            return 16
        elif self.delta < 5000:
            return 32
        else:
            return 64

    @property
    @lru_cache(1)
    def min_changes(self):
        return self.df['changes'].min()

    @property
    @lru_cache(1)
    def max_changes(self):
        return self.df['changes'].max()

    @property
    @lru_cache(1)
    def sizes(self):
        sizes = [(i, (i * self.DEFAULT_SIZES_FACTOR) + self.DEFAULT_MIN_SIZES)
                 for i in self.df['changes_bins']]
        log.debug(f'sizes: {sizes}')
        return dict(sizes)

    def show(self):
        with sns.axes_style(self.args.style):
            sns.relplot(
                alpha=.7,
                col='labels_',
                col_wrap=2,
                data=self.df,
                height=5,
                hue='labels_',
                kind='scatter',
                legend='full',
                palette='muted',
                size='changes_bins',
                sizes=self.sizes,
                x='elapsed_days',
                y='elapsed_days_of_first_comment')
            plt.show()


def create_changes_and_elapsed_days(args, df):
    sp = ScatterPlot(args, df)
    sp.show()
    plt.show()