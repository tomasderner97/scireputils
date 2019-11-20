def _parse_column_property(cp):
    if isinstance(cp, str):
        cp = cp.split()

    col_name = cp[0]
    if len(cp) >= 2:
        quantity_name = cp[1]
    else:
        quantity_name = col_name
    if len(cp) >= 3:
        unit = cp[2]
    else:
        unit = ""
    if len(cp) >= 4:
        float_format = cp[3]
    else:
        float_format = None

    return col_name, quantity_name, unit, float_format


def _make_column_strings_equal_length(quantity_name, unit, str_data):
    """
    finds lenght of the longest string in column and fills others to that length,
    quantity and unit aligned left and data right
    """

    len_of_longest = len(max(str_data + [quantity_name, unit], key=len))

    right_adjust = f"{{:>{len_of_longest}}}".format
    right_adjusted = [right_adjust(s) for s in str_data]
    left_adjust = f"{{:<{len_of_longest}}}".format
    quantity_name = left_adjust(quantity_name)
    unit = left_adjust(unit)

    return [quantity_name, unit] + right_adjusted


def _make_formater_from_s_col_format_string(format_string):
    fmt = format_string

    if "e" in format_string:
        fmt = format_string.split("e")[0] + "e"
    else:
        fmt += "f"

    return f"{{:{fmt}}}".format
