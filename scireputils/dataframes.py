import pandas as pd


def dataframe_from_csv(csv_path: str, index_col=None, sep=r"\s*,\s*", **kwargs):
    """
    Creates Pandas dataframe from comma separated values file, allows # comments and
    blank lines.
    """

    separator = r"\s+" if sep == ' ' else sep
    return pd.read_csv(csv_path, sep=separator,
                       engine="python",
                       skip_blank_lines=True,
                       index_col=index_col,
                       comment="#",
                       **kwargs)
