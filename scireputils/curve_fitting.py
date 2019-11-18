import warnings

from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
import numpy as np


class FitCurve:
    """
    Class representing function fitted to some data. Objects are callable.
    Arguments are the same as for scipy.optimize.curve_fit.

    Parameters
    ----------
    f: callable
        Function to fit parameters to.
        Has to have format f(x, param1, param2, ...)
    xdata: M-length sequence
        X values of data points.
    ydata: M-length sequence
        Y values of data points.
    p0: None, scalar or N-length sequence
        Initial guess for the parameters.
    sigma: None or M-length sequence
        Determines the uncertainty of ydata.
    """

    def __init__(self, f, xdata, ydata, *args, **kwargs):
        params, cov = curve_fit(f, xdata, ydata, *args, **kwargs)
        errors = [np.sqrt(cov[i, i]) for i in range(len(cov))]

        if len(np.where(cov == np.inf)[0]) > 0:
            raise ValueError(
                "Fit unsuccessful, provide better initial parameters (p0)")

        self.params = params
        self.errors = errors
        self.xdata = np.array(xdata)
        self.ydata = np.array(ydata)
        self.f = lambda x: f(x, *params)

    def __call__(self, x):
        return self.f(x)

    def curve(self, start=None, end=None, res=100, overrun=0):
        """
        Calculates the curve of the fit, used as line of theoretical function.

        Parameters
        ----------
        start: float, optional
            The lowest x value. If none, lowest of original x data is used.
        end: float, optional
            The highest x value. If none, highest of original x data is used.
        resolution: int
            Number of points used in between start and end(inclusive).
        overrun: float, (float, float)
            fraction of x interval to add before start and after end.
            If tuple, the values are used for start and end separately.
        """
        if start is None:
            start = self.xdata.min()
        if end is None:
            end = self.xdata.max()

        interval_length = end - start

        try:
            start -= overrun[0] * interval_length
            end += overrun[1] * interval_length
        except TypeError:
            start -= overrun * interval_length
            end += overrun * interval_length

        xes = np.linspace(start, end, res)
        ys = self(xes)

        return xes, ys


class Spline(UnivariateSpline):
    """
    Thin wrapper around the scipy's UnivariateSpline. Original data is saved in xdata, ydata.
    Curve function was added. Objects are callable.
    If passed x array is not strictly increasing, raises a warning and monotonizes
    the data automaticaly.

    Parameters
    ----------
    x: Sequence like
        x data
    y: Sequence like
        y data
    and other params of UnivariateSpline.
    """

    def __init__(self, x, y, *args, **kwargs):
        try:
            super().__init__(self, x, y, *args, **kwargs)
        except ValueError as e:
            if str(e) == "x must be strictly increasing":
                warnings.warn("Spline: ValueError catched, monotonizing!")

                mono_x, mono_y = self._monotonize(x, y)
                super().__init__(
                    self, mono_x, mono_y, *args, **kwargs
                )
            else:
                raise e

        self.xdata = np.array(x)
        self.ydata = np.array(y)

    def curve(self, start=None, end=None, resolution=100, overrun=0):
        """
        Calculates the curve of the spline, used as line of theoretical function
        or a lead for an eye.

        Parameters
        ----------
        start: float, optional
            The lowest x value. If none, lowest of original x data is used.
        end: float, optional
            The highest x value. If none, highest of original x data is used.
        resolution: int
            Number of points used in between start and end(inclusive).
        overrun: float, (float, float)
            fraction of x interval to add before start and after end. If tuple,
            the values are used for start and end separately.
        """
        if start is None:
            start = self.xdata.min()
        if end is None:
            end = self.xdata.max()

        interval_length = end - start

        try:
            start -= overrun[0] * interval_length
            end += overrun[1] * interval_length
        except TypeError:
            start -= overrun * interval_length
            end += overrun * interval_length

        xes = np.linspace(start, end, resolution)
        ys = self(xes)

        return xes, ys

    def _monotonize(self, xdata, ydata):
        """
        Helper function to make passed x and y value array strictly increasing.
        New in 0.1.2

        Parameters:
        -----------
        xdata: sequence
            X points
        ydata: sequence
            Y points

        Returns:
        --------
        new_x: numpy.ndarray
            monotonized X points
        new_y: numpy.ndarray
            monotonized Y points
        """
        highest = xdata[0] - 1
        new_x = []
        new_y = []

        for x, y in zip(xdata, ydata):
            if x > highest:
                new_x.append(x)
                new_y.append(y)
                highest = x

        return np.array(new_x), np.array(new_y)
