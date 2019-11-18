import numpy as np


def repeated_measurement_mean_and_error(values):
    """
    Calculates the mean and mean error of multiple measurements of one quantity.

    Parameters
    ----------
    values : sequence
        multiple values of one quantity from repeated measurement

    Returns
    -------
    mean : float
        mean of the values
    mean_error : float
        error of the mean, eg. std (ddof=1) of values divided by sqrt of number of values
    """
    array = np.array(values)
    mean = array.mean()
    single_value_error = array.std(ddof=1)
    mean_error = single_value_error / np.sqrt(len(array))

    return mean, mean_error
