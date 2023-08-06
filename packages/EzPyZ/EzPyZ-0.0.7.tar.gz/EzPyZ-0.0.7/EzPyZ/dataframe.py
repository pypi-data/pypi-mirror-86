"""
dataframe.py
~~~~~~~~~~~~
This module provides an ``EzPyZ`` class which will contain all functionality of this package.
"""

# Standard library.
from csv import DictWriter
from typing import Any, Dict, List, Union
# Related third-partly library.
import pandas as pd
# Internal classes/functions
from EzPyZ.column import Column

class DataFrame:
    """
    An ``EzPyZ`` object. An ``EzPyZ`` object will be used to utilize all other functionality in this
    package.

    If you would prefer to pass a ``pandas`` dataframe directly to the class:

    >>> import EzPyZ as ez
    >>> import pandas as pd
    >>> raw_data = {
    >>>     'height (cm)': [134, 168, 149, 201, 177],
    >>>     'weight (kg)': [32.2, 64.3, 59.9, 95.4, 104.2]
    >>> }
    >>> pandas_df = pd.DataFrame(raw_data)
    >>> df = ez.DataFrame(data=pandas_df)

    Or if you'd like to provide the data in a more raw format (similar to what would be passed to a
    ``pandas`` dataframe):

    >>> import EzPyZ as ez
    >>> raw_data = {
    >>>     'height (cm)': [134, 168, 149, 201, 177],
    >>>     'weight (kg)': [32.2, 64.3, 59.9, 95.4, 104.2]
    >>> }
    >>> df = ez.DataFrame(data=raw_data)

    Or if you'd like to provide the data directly from an Excel of CSV file:

    >>> import EzPyZ as ez
    >>> from EzPyZ.tools import read_file
    >>> df = ez.DataFrame(data=read_file("bmi_data.csv")) # A bmi_data.xlsx would also work here.
    """
    # ~~~~~ Special methods ~~~~~
    def __init__(
            self,
            data: Union[pd.DataFrame, Dict[str, List[Any]]],
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
        if type(data) not in (pd.DataFrame, dict):
            # ``data`` is of an invalid type.
            raise TypeError(
                "expected ``data`` to be of type Dict[str, List] or pandas.DataFrame, got "
                + type(data).__name__
            )
        elif type(columns) not in (list, type(None)):
            # ``columns`` is of an invalid type.
            raise TypeError(
                "expected ``columns`` to be of type List[str] or None, got "
                + type(data).__name__
            )

        # Check if ``data`` is a ``pandas`` dataframe, and handle it accordingly.
        if isinstance(data, pd.DataFrame):
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
            if columns is not None:
                # Use a subset of columns.
                # Ensure all items listed in ``columns`` are valid column titles
                # (i.e. they actually exist).
                for i in columns:
                    if i not in data:
                        # A column that doesn't exist was specified.
                        raise ValueError(i + " is not a valid column title.")
                data = {i: data[i] for i in columns}

        # Create dataframe using ``Column`` objects and ensure all columns are the same length.
        self.df = [Column(i, data[i]) for i in data]
        self.__correct_length()

        # Set attributes to class to contain column names.
        for i in self.df:
            setattr(self, i.title(), i)

        return
    def __str__(self) -> str:
        titles = self.get_titles()
        rows = [{title: title for title in titles}] + self.__generate_rows()
        spaces = " " * (len(str(self.df[0].length())) + 2)
        out_str = spaces
        for i in range(len(rows)):
            for val in rows[i]:
                out_str += "{:<15}".format(rows[i][val])
            out_str += "\n" + str(i) + spaces
        return out_str[1:-(len(spaces) + len(str(i)) + 1)]
    def __repr__(self) -> str:
        if len(self.df) >= 3:
            return "EzPyZ(df={})".format([str(i) for i in self.df])
        val_str = "["
        for i in self.df[:3]:
            val_str += str(i) + ", "
        val_str += "...]"
        return "EzPyZ(df={})".format(val_str)

    # ~~~~~ Public methods ~~~~~
    def get_titles(self) -> List[str]:
        """
        Returns a list of all column titles.

        :rtype: ``List[str]``
        """
        return [i.title() for i in self.df]
    def head(
        self,
        count: int = 5
    ) -> str:
        """
        Returns the first ``count`` rows of the dataframe.

        :param count:   The number of rows to return.
        :rtype:         ``str``
        """
        titles = self.get_titles()
        rows = [{title: title for title in titles}] + self.__generate_rows()[:count]
        spaces = " " * (len(str(self.df[0].length())) + 2)
        out_str = spaces
        for i in range(len(rows)):
            for val in rows[i]:
                out_str += "{:<15}".format(rows[i][val])
            out_str += "\n" + str(i) + spaces
        return out_str[1:-(len(spaces) + len(str(i)) + 1)]
    def write_csv(
            self,
            filename: str = "out.csv",
            header: bool = True
    ) -> None:
        """
        Writes the dataframe to a CSV file. If ``filename`` is left at default, the CSV will be
        generated in the local directory with the name "out.csv". If ``header`` is left at ``True``
        default, the first row in the CSV will be the column titles. If ``header`` is set to
        ``False``, the column titles will be omitted.

        :param filename:    (optional) The qualified name of the file to write to.
        :param header:      (optional) A ``bool`` specifying whether or not the column titles should
                            be written to the CSV.
        :rtype:             ``None``
        """
        with open(filename, "w") as out_csv:
            writer = DictWriter(out_csv, fieldnames=self.get_titles())
            if header:
                writer.writeheader()
            writer.writerows(self.__generate_rows())

    # ~~~~~ Private methods ~~~~~
    def __correct_length(self) -> None:
        """
        Set all columns to the same length of the longest column by appending ``None`` to the
        end of shorter columns.

        :rtype: ``None``
        """
        col_len = max([i.length() for i in self.df])
        for i in self.df:
            i.set_values(i.get_values() + ([None] * (i.length() - col_len)))
    def __generate_rows(self) -> List[Dict[str, Any]]:
        """
        Returns a list of dictionaries for values in the dataframe, where each dictionary in the
        list represents one row in the dataframe.

        :rtype: ``List[Dict[str, Any]]``
        """
        self.__correct_length()
        titles = self.get_titles()
        rows = []
        for i in range(self.df[0].length()):
            payload = {}
            for j in range(len(titles)):
                payload[titles[j]] = self.df[j].get_values()[i]
            rows.append(payload)
        return rows
