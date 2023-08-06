"""
column.py
~~~~~~~~~
This module provides an ``EzPyZ.Column`` class which will be used internally to provide certain
functionality.
"""

# Standard library.
from math import isnan
import statistics as st
from typing import Any, List

class Column:
    """
    A ``Column`` object. A ``Column`` object will make up ``EzPyZ`` dataframes in this module. This
    class is NOT intended for exernal use!
    """
    # ~~~~~ Special methods ~~~~~
    def __init__(
            self,
            title: str,
            values: List[Any]
    ) -> None:
        """
        Initializes the ``Column`` object.

        :param title:   A string containing the title of the column.
        :param values:  A list containing the values in the column, in order.
        :rtype:         ``None``
        """
        # Validating input.
        if type(title) is not str:
            # ``title`` is of an invalid type.
            raise TypeError(
                "expected ``title`` to be of type str, got "
                + type(title).__name__
            )
        elif type(values) is not list:
            # ``values`` is of an invalid type.
            raise TypeError(
                "expected ``values`` to be of type List[Any], got "
                + type(values).__name__
            )

        self.col_title = title
        self.values = values
        return
    def __repr__(self) -> str:
        """
        Returns basic ``Column`` information.

        :rtype: ``str``
        """
        if len(self.values) >= 5:
            return 'Column(title={}, values={})'.format(self.col_title, self.values)
        val_str = "["
        for i in self.values[:5]:
            val_str += str(i) + ", "
        val_str += "...]"
        return 'Column(title={}, values={})'.format(self.col_title, val_str)
    def __str__(self) -> str:
        """
        Returns the ``Column`` as a string.

        :rtype: ``str``
        """
        out_str = self.col_title + "\n"
        for i in self.values:
            out_str += str(i) + "\n"
        return out_str[:-1]

    # ~~~~~ Public methods ~~~~~
    def get_values(self) -> List[Any]:
        """
        Returns ``self.values``.

        :rtype: ``List[Any]``
        """
        return self.values
    def length(self) -> int:
        """
        Returns the length of ``self.values``.

        :rtype: ``int``
        """
        return len(self.values)
    def mean(self) -> float:
        """
        Returns the mean of ``self.values``.

        :rtype: ``float``
        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.mean(vals)
    def median(self) -> int:
        """
        Returns the median of ``self.values``.

        :rtype: ``float``
        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.median(self.values)
    def mode(self) -> float:
        """
        Returns the mode of ``self.values``.

        :rtype: ``float``
        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.mode(self.values)
    def stdev(self) -> float:
        """
        Returns the standard deviation of ``self.values``.

        :rtype: ``float``
        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.stdev(vals)
    def set_values(
            self,
            values: List[Any]
    ) -> None:
        """
        Sets ``self.values``.

        :param values:  A list containing the values in the column, in order.
        :rtype:         ``None``
        """
        if type(values) is not list:
            # ``values`` is of an invalid type.
            raise TypeError(
                "expected ``values`` to be of type List[Any], got "
                + type(values).__name__
            )
        self.values = values
    def title(self) -> str:
        """
        Returns ``self.col_title``

        :rtype: ``str``
        """
        return self.col_title
    def variance(self) -> float:
        """
        Returns the variance of ``self.values``.

        :rtype: ``float``
        """
        vals = []
        for i in self.values:
            if type(i) not in (int, float, type(None)):
                raise TypeError("expected values in column "
                                + self.title() +
                                " to be str, float, or NoneType, got "
                                + type(i).__name__
                )
            elif type(i) is not None and not isnan(i):
                vals.append(i)
        return st.variance(vals)