from collections import defaultdict, Counter
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


class HistDimensionError(Exception):
    pass


class BaseStatsDistributions:
    def __init__(self, series, **kwargs):
        self.series = series

        self._pd_series = False
        if isinstance(series, pd.Series):
            self._pd_series = True

        if self._pd_series:
            self.series_name = series.name
            self.column_name = self.series_name

    def __repr__(self):
        """Check if self.series is not too large.
        """
        return f"BaseStatsDistribution(series=[{self.series[0]},...,{self.series[-1]}])"

    def __len__(self):
        return len(tuple(self.series))

    def __contains__(self, value):
        return value in self.series

    def __eq__(self, other):
        return self.__hash__() == hash(other)

    def __hash__(self):
        return hash(self.series)

    @property
    def element_count(self):
        return len(self.series)


class PMF:
    def __init__(self, hist):
        self.hist = hist
        self.value_count_total = self._calculate_value_count()
        self.pmf = self._calculate_pmf()

    def __getitem__(self, value):
        return self.pmf.get(value, 0)

    def __len__(self):
        return len(self.pmf.keys())

    def __contains__(self, value):
        return value in self.pmf

    def __repr__(self):
        return f"PMF(hist={self.hist})"

    def iterkeys(self):
        return iter(self.pmf)

    def _calculate_value_count(self):
        return sum(self.hist.values())

    def _calculate_pmf(self):
        pmf = defaultdict(float)
        elements = self.value_count_total
        for key, value in self.hist.items():
            pmf[key] = value / elements

        return pmf

    @property
    def is_normalized(self):
        probability_sum = 0
        for values in self.pmf.values():
            probability_sum += round(values, 5)

        if round(probability_sum, 0) == 1.0:
            return True

        print(f"Not Normalized, probability sum: {probability_sum}")
        return False


class CDF:
    def __init__(self, hist):
        self.hist = hist
        self.sorted_key_value_pairs_hist = sorted(self.hist.items(), key=lambda x: x[0])
        self.value_count_total = self._calculate_value_count()
        self.cdf = self._calculate_cdf()
        self.sorted_key_value_pairs = sorted(self.cdf.items(), key=lambda x: x[0])

    def __getitem__(self, value):
        return self.cdf.get(value, 0)

    def __len__(self):
        return len(self.cdf.keys())

    def __contains__(self, value):
        return value in self.cdf

    def __repr__(self):
        return f"CDF(hist={self.hist})"

    def iterkeys(self):
        return iter(self.cdf)

    def _calculate_value_count(self):
        return sum(self.hist.values())

    def _calculate_cdf(self):

        cdf = defaultdict(float)
        count = 0
        for key, value in self.sorted_key_value_pairs_hist:
            count += value
            cdf[key] = count / self.value_count_total

        return cdf

    def probability(self, key):
        return self[key]

    def percentile_rank(self, key):
        return self[key] * 100.0

    def percentile(self, rank):
        return self.value(rank / 100)

    def value(self, probability):

        for key, value in self.sorted_key_value_pairs:
            if round(probability, 5) <= round(value, 5):
                return key

        raise KeyError(f"Could not find a value=='{probability}' in cdf.")

    @property
    def iqr(self):
        return self.value(0.75) - self.value(0.25)

    def quantile(self, steps):
        step_length = 1 / steps
        step = 0  # round(step_length, 2)
        quants = []
        while step < 1:
            quants.append((step, self.value(step)))
            step = round(step + step_length, 2)

        return tuple(quants)


class Hist(BaseStatsDistributions):
    """Provide a histogramm for a given series.
    """

    def __init__(self, series, **kwargs):
        """Create a new Hist instance.

        cut_nan=True, was removed, because np.nan's are treated as unique
        and not grouped. This results in many np.nan=1 entries.

        # TODO: 
            1. Hide series, kv_p, hist
            2. Add getters/setters to control access
            3. Add pmf dict, along with recalc, normalize methods
            4. Use kwargs as default, otherwise use inferred info (e.g., pd.series.name)
        """
        super().__init__(series.copy(), **kwargs)
        self.cut_nan = True  # cut_nan
        if self.cut_nan:
            try:
                self.series.dropna(inplace=True)
            except AttributeError:
                if np.nan in self.series:
                    self.series.remove(np.nan)
        self.histogramm = self._calculate_histogramm()

        self.key_value_pairs = sorted(self.histogramm.items(), key=lambda x: x[0])
        self.pmf = PMF(hist=self.histogramm)
        self.cdf = CDF(hist=self.histogramm)

    def __repr__(self):
        """Check if self.series is not too large.
        """
        return f"Hist(series=[{self.series[0]},...,{self.series[-1]}], cut_nan={self.cut_nan})"

    # def __getattr__(self, value):
    #     return (value, self.histogramm[value])

    def __len__(self):
        return len(self.histogramm.keys())

    def __contains__(self, value):
        return value in self.histogramm

    def __eq__(self, other):
        return self.histogramm == other.histogramm

    def __hash__(self):
        return hash(tuple(self.key_value_pairs))

    def iterkeys(self):
        return iter(self.histogramm)

    def __getitem__(self, value):
        return self.histogramm.get(value, 0)

    # def __get__(self, instance, owner):
    #     return self.histogramm

    def __iter__(self):
        for kv_pair in self.key_value_pairs:
            yield kv_pair

    def _calculate_histogramm(self):
        return Counter(self.series)
        # for element in self.series:
        #     self.histogramm[element] += 1

    @property
    def mode(self):
        max_key, max_value = max(self.key_value_pairs, key=lambda x: x[1])
        modals = [
            (key, value) for key, value in self.key_value_pairs if value == max_value
        ]
        # if len(modals) == 1:
        #     return modals[0]
        return modals

    @property
    def is_multimodal(self):
        modals = self.mode
        if len(modals) > 1:
            return True
        return False

    @property
    def mean(self):
        try:
            mean_value = 0
            value_sum = 0
            for key, value in self.key_value_pairs:
                mean_value += float(key) * value
                value_sum += value

            return mean_value / value_sum
        except ValueError:
            return None

    @property
    def median(self):
        sorted_series = sorted(self.series)
        series_length = len(sorted_series)
        if series_length % 2:
            return sorted_series[series_length // 2]
        else:
            return (
                sorted_series[series_length // 2]
                + sorted_series[series_length // 2 + 1]
            ) // 2

    @property
    def variance(self):
        mean = self.mean
        length = len(self.series)
        deviation_sum = 0

        for key, value in self.key_value_pairs:
            deviation_sum += np.square(mean - key) * value

        return deviation_sum / length

    @property
    def standard_deviation(self):
        return np.sqrt(self.variance)

    def outliers(self, n=5):
        sorted_key_values = sorted(self.key_value_pairs, key=lambda x: x[1])
        return sorted(sorted_key_values[:n], key=lambda x: float(x[0]))

    def first(self, n=5):
        sorted_key_values = sorted(self.key_value_pairs, key=lambda x: float(x[0]))
        return sorted_key_values[:n]

    def last(self, n=5):
        sorted_key_values = sorted(self.key_value_pairs, key=lambda x: float(x[0]))
        return sorted_key_values[-n:]

    def plot(self, dict_name, **options):
        """Plot the histogramm as a bar plot.

        Make sure to correctly handle multimodals.
        """
        if not dict_name:
            # Set the default here, because 'self' is not available in signature.
            dict_name = self.histogramm

        hist = plt.bar(dict_name.keys(), dict_name.values(), **options)

        return hist

    def cohens_d(self, other):
        if not isinstance(other, Hist):
            raise TypeError

        mean_diff = self.mean - other.mean
        self_length, other_length = len(self.series), len(other.series)

        if not self_length == other_length:
            pooled_variance = (
                self_length * self.variance + other_length * other.variance
            ) / (self_length + other_length)
        else:
            pooled_variance = (self.variance + other.variance) / 2

        d = mean_diff / np.sqrt(pooled_variance)
        return d

    def print_stats(self, round_by=3):
        if self.column_name:
            print(f"Column Name: \t {self.column_name}")
        print(f"Mean: \t\t {round(self.mean, round_by)}")
        print(f"Median: \t {round(self.median, round_by)}")
        print(f"Variance: \t {round(self.variance, round_by)}")
        print(f"Std Dev.: \t {round(self.standard_deviation, round_by)}")
        print(f"Outliers: \t {self.outliers()}")

    # def get_pmf(self, key):
    #     return self.pmf[key]


class BiasedHist(Hist):
    def __repr__(self):
        """Check if self.series is not too large.
        """
        return f"BiasedHist(series=[{self.series[0]},...,{self.series[-1]}], cut_nan={self.cut_nan})"

    def _calculate_histogramm(self):
        hist = defaultdict(int)
        normal_hist = Counter(self.series)

        for key, value in normal_hist.items():
            hist[key] = key * value

        return hist

    @property
    def elements_count(self):
        elements = 0
        for values in self.histogramm.values():
            elements += values

        return elements

