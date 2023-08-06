"""
dataframe.py
~~~~~~~~~~~~
This module provides an ``EzPyZ.DataFrame`` class which will contain all functionality of this package.
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
    A ``DataFrame`` object will be used to utilize all other functionality in this package.

    If you would prefer to pass a ``pandas`` dataframe directly to the class:

    code:: python3

        >>> import EzPyZ as ez
        >>> import pandas as pd
        >>> raw_data = {
        >>>     'height_cm': [134, 168, 149, 201, 177, 168],
        >>>     'weight_kg': [32.2, 64.3, 59.9, 95.4, 104.2, 63.1]
        >>> }
        >>> pandas_df = pd.DataFrame(raw_data)
        >>> df = ez.DataFrame(data=pandas_df)

    Or if you'd like to provide the data in a more raw format (similar to what would be passed to a
    ``pandas`` dataframe):

    code:: python3

        >>> import EzPyZ as ez
        >>> raw_data = {
        >>>     'height_cm': [134, 168, 149, 201, 177, 168],
        >>>     'weight_kg': [32.2, 64.3, 59.9, 95.4, 104.2, 63.1]
        >>> }
        >>> df = ez.DataFrame(data=raw_data)

    Or if you'd like to provide the data directly from an Excel of CSV file:

    code:: python3

        >>> import EzPyZ as ez
        >>> from EzPyZ.tools import read_file
        >>> df = ez.DataFrame(data=read_file("bmi_data.csv")) # A bmi_data.xlsx would also work here.

    """
    # ~~~~~ Special methods ~~~~~
    def __init__(self, data, columns=None):
        """
        Constructs a :class:`DataFrame <DataFrame>` object.

        :param data:    Either a pandas DataFrame object, or a dictionary where the keys are column
                        titles and the values are lists of associated values (in order).
        :type data:     ``Union[pd.DataFrame, Dict[str, List[Any]]]``
        :param columns: (optional) A list of strings containing the titles of columns to be included
                        in the dataframe. All others will be excluded. If this option is left blank
                        or set to ``None``, then all columns will be included.
        :type columns:  ``List[str]``
        :return:        A new ``EzPyZ.DataFrame`` object.
        :rtype:         ``EzPyZ.DataFrame`
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
    def __str__(self):
        """
        Returns the ``DataFrame`` as a string.

        :return:    A print-friendly string representing the ``DataFrame`` object.
        :rtype:     ``str``

        code:: python3

            >>> import EzPyZ as ez
            >>> data = ez.tools.read_file("bmi_data.csv") A bmi_data.xlsx would also work here.
            >>> df = ez.DataFrame(data=data)
            >>> print(df)
            height_cm      weight_kg
            0   134            32.2
            1   168            64.3
            2   149            59.9
            3   201            95.4
            4   177            104.2
            5   168            63.1

        """
        titles = self.get_titles()
        rows = [{title: title for title in titles}] + self.__generate_rows()
        spaces = " " * (len(str(self.df[0].length())) + 2)
        out_str = spaces
        for i in range(len(rows)):
            for val in rows[i]:
                out_str += "{:<15}".format(rows[i][val])
            out_str += "\n" + str(i) + spaces
        return out_str[1:-(len(spaces) + len(str(len(rows) - 1)) + 1)]
    def __repr__(self):
        """
        Returns basic ``DataFrame`` information.

        :return:    Basic ``DataFrame`` information for debugging.
        :rtype:     ``str``

        code:: python3

            >>> import EzPyZ as ez
            >>> data = ez.tools.read_file("bmi_data.csv") A bmi_data.xlsx would also work here.
            >>> df = ez.DataFrame(data=data)
            >>> print(repr(df))
            DataFrame(df=Column(title=height_cm, values=[134, 168, 149, 201, 177, ...]),
                      Column(title=weight_kg, values=[32.2, 64.3, 59.9, 95.4, 104.2, ...]))

        """
        if self.length_columns() <= 3:
            return "DataFrame(df={})".format(",".join([repr(i) for i in self.df]))
        val_str = "["
        for i in self.df[:3]:
            val_str += str(i).rstrip('\n') + ", "
        val_str += "...]"
        return "EzPyZ(df={})".format(val_str)

    # ~~~~~ Public methods ~~~~~
    def get_columns(self):
        """
        Returns columns as a list.

        :return:    Columns as a list.
        :rtype:     ``List[EzPyZ.Column]``
        """
        return self.df
    def get_titles(self):
        """
        Returns a list of all column titles.

        :return:    A list of all column titles.
        :rtype:     ``List[str]``

        code:: python3

            >>> import EzPyZ as ez
            >>> data = ez.tools.read_file("bmi_data.csv") A bmi_data.xlsx would also work here.
            >>> df = ez.DataFrame(data=data)
            >>> print(df.get_titles())
            ['height_cm', 'weight_kg']

        """
        return [i.title() for i in self.df]
    def head(self, count=5):
        """
        Returns the first ``count`` rows of the dataframe.

        :param count:   (optional) The number of rows to return. Defaults to ``5``.
        :type count:    ``int``
        :return:        The first ``count`` rows of the dataframe.
        :rtype:         ``str``

        code:: python3

            >>> import EzPyZ as ez
            >>> data = ez.tools.read_file("bmi_data.csv") A bmi_data.xlsx would also work here.
            >>> df = ez.DataFrame(data=data)
            >>> print(df.head())
            height_cm      weight_kg
            0   134            32.2
            1   168            64.3
            2   149            59.9
            3   201            95.4
            4   177            104.2
            5   168            63.1

        """
        titles = self.get_titles()
        rows = [{title: title for title in titles}] + self.__generate_rows()[:count]
        spaces = " " * (len(str(self.df[0].length())) + 2)
        out_str = spaces
        for i in range(len(rows)):
            for val in rows[i]:
                out_str += "{:<15}".format(rows[i][val])
            out_str += "\n" + str(i) + spaces
        return out_str[1:-(len(spaces) + len(str(len(rows) - 1)) + 1)]
    def length_columns(self):
        """
        Returns the number of columns in the ``DataFrame``.

        :return:    Number of columns.
        :rtype:     ``int``

        code:: python3

            >>> import EzPyZ as ez
            >>> data = ez.tools.read_file("bmi_data.csv") A bmi_data.xlsx would also work here.
            >>> df = ez.DataFrame(data=data)
            >>> print(df.length_columns())
            2

        """
        return len(self.df)
    def length_rows(self):
        """
        Returns the number of rows in the ``DataFrame``.

        :return:    Number of rows.
        :rtype:     ``int``

        code:: python3

            >>> import EzPyZ as ez
            >>> data = ez.tools.read_file("bmi_data.csv") A bmi_data.xlsx would also work here.
            >>> df = ez.DataFrame(data=data)
            >>> print(df.length_columns())
            6

        """
        if self.length_columns() == 0:
            return 0
        return self.df[0].length()
    def write_csv(self, filename="out.csv", header=True):
        """
        Writes the dataframe to a CSV file.

        :param filename:    (optional) The qualified name of the file to write to. Defaults to
                            ``out.csv``.
        :type filename:     ``str``
        :param header:      (optional) Boolean. Specifies whether or not the column titles should
                            be written to the CSV. Defaults to ``True``.
        :type header:       ``bool``
        :return:            Nothing.
        :rtype:             ``NoneType``

        code:: python3

            >>> import EzPyZ as ez
            >>> raw_data = {
            >>>     'height (cm)': [134, 168, 149, 201, 177, 168],
            >>>     'weight (kg)': [32.2, 64.3, 59.9, 95.4, 104.2, 63.1]
            >>> }
            >>> df = ez.DataFrame(data=raw_data)
            >>> df.write_csv("bmi_data.csv")

        """
        with open(filename, "w") as out_csv:
            writer = DictWriter(out_csv, fieldnames=self.get_titles())
            if header:
                writer.writeheader()
            writer.writerows(self.__generate_rows())

    # ~~~~~ Private methods ~~~~~
    def __correct_length(self):
        """
        Set all columns to the same length of the longest column by appending ``None`` to the
        end of shorter columns.

        :return:    Nothing.
        :rtype:     ``None``
        """
        col_len = max([i.length() for i in self.df])
        for i in self.df:
            i.set_values(i.get_values() + ([None] * (i.length() - col_len)))
    def __generate_rows(self):
        """
        Returns a list of dictionaries for values in the dataframe, where each dictionary in the
        list represents one row in the dataframe.

        :return:    List of dictionaries where each dictionary represents one row in the dataframe.
        :rtype:     ``List[Dict[str, Any]]``
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
