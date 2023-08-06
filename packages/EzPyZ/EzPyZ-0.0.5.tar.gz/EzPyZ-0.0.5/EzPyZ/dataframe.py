"""
dataframe.py
~~~~~~~~~~~~
This module provides an ``EzPyZ`` class which will contain all functionality of this package.
"""

# Standard library.
from typing import Any, Dict, List, Union
# Related third-partly library.
from pandas import DataFrame
# Internal classes/functions
from EzPyZ.column import Column

class EzPyZ:
    """
    An ``EzPyZ`` object. An ``EzPyZ`` object will be used to utilize all other functionality in this
    package.

    If you would prefer to pass a ``pandas`` dataframe directly to the class:

    >>> import EzPyZ
    >>> import pandas as pd
    >>> raw_data = {
    >>>     'height (cm)': [134, 168, 149, 201, 177],
    >>>     'weight (kg)': [32.2, 64.3, 59.9, 95.4, 104.2]
    >>> }
    >>> pandas_df = pd.DataFrame(raw_data)
    >>> df = EzPyz(data=pandas_df)

    Or if you'd like to provide the data in a more raw format (similar to what would be passed to a
    ``pandas`` dataframe):

    >>> import EzPyZ
    >>> raw_data = {
    >>>     'height (cm)': [134, 168, 149, 201, 177],
    >>>     'weight (kg)': [32.2, 64.3, 59.9, 95.4, 104.2]
    >>> }
    >>> df = EzPyZ(data=raw_data)

    Or if you'd like to provide the data directly from an Excel of CSV file:

    >>> import EzPyZ
    >>> from EzPyZ.tools import read_file
    >>> df = EzPyZ(data=read_file("bmi_data.csv")) # A bmi_data.xlsx would also work here.
    """
    # ~~~~~ Special methods ~~~~~
    def __init__(
            self,
            data: Union[DataFrame, Dict[str, List[Any]]],
            columns: List[str] = None
    ) -> None:
        """
        Initializes the ``EzPyZ`` object.

        :param data:    Either a pandas DataFrame object, or a dictionary where the keys are column
                        titles and the values are lists of associated values (in order).
        :param columns: (optional) A list of strings containing the titles of columns to be included
                        in the dataframe. All others will be excluded. If this option is left blank
                        or set to ``None``, then all columns will be included.
        :rtype:         ``None``
        """
        # Validating input.
        if type(data) not in (DataFrame, dict):
            # ``data`` is of an invalid type.
            raise TypeError(
                "expected ``data`` to be of type Dict[str, List] or pandas.DataFrame, got "
                + type(data).__name__
            )
        elif type(columns) not in (list, None):
            # ``columns`` is of an invalid type.
            raise TypeError(
                "expected ``columns`` to be of type List[str], got "
                + type(data).__name__
            )

        # Check if ``data`` is a ``pandas`` dataframe, and handle it accordingly.
        if isinstance(data, DataFrame):
            # ``data`` is a ``pandas`` dataframe.
            if columns is None:
                # Use all columns.
                data = {i: list(data[i]) for i in list(data.columns)}
            else:
                # Use a subset of the columns.
                # Ensure all items listed in ``columns`` are valid column titles
                # (i.e. they actually exist).
                for i in columns:
                    if i not in list(data.columns):
                        # A column that doesn't exist was specified.
                        raise ValueError(i + " is not a valid column title.")
                data = {i: list(data[i]) for i in columns}
        else:
            # ``data`` is NOT a ``pandas`` dataframe.
            if columns is None:
                # Use all columns.
                data = data
            else:
                # Use a subset of columns.
                # Ensure all items listed in ``columns`` are valid column titles
                # (i.e. they actually exist).
                for i in columns:
                    if i not in data:
                        # A column that doesn't exist was specified.
                        raise ValueError(i + " is not a valid column title.")
                data = {i: data[i] for i in columns}

        # Create dataframe using ``Column`` objects.
        self.df = [Column(i, data[i]) for i in data]
        return
    def __str__(self) -> str:
        pass
    def __repr__(self) -> str:
        if len(self.df) >= 3:
            return "EzPyZ(df={})".format([str(i) for i in self.df])
        val_str = "["
        for i in self.df[:3]:
            val_str += str(i) + ", "
        val_str += "...]"
        return "EzPyZ(df={})".format(val_str)

    # ~~~~~ Public methods ~~~~~
