"""
column.py
~~~~~~~~~
This module provides a ``Column`` class which will be used internally to provide certain
functionality.
"""

# Standard library.
from typing import Any, List

class Column:
    """
    A ``Column`` object. A ``Column`` object will make up ``EzPyZ`` dataframes in this module. This
    class is NOT intended for exernal use!
    """
    # ~~~~~ Special methods ~~~~~
    def __init__(
            self,
            title:  str,
            values: List[Any]
    ) -> None:
        """
        Initializes the ``Column`` object.

        :param title:   A string containing the title of the ``Column`` to be created.
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

        self.title = title
        self.values = values
        return
    def __str__(self) -> str:
        """
        Returns the ``Column`` as a string.
        """
        out_str = self.title + "\n"
        for i in self.values:
            out_str += i + "\n"
        return out_str
    def __repr__(self) -> str:
        """
        Returns basic ``Column`` information.
        """
        if len(self.values >= 5):
            return 'Column(title={}, values={})'.format(self.title, self.values)
        val_str = "["
        for i in self.values[:5]:
            val_str += str(i) + ", "
        val_str += "...]"
        return 'Column(title={}, values={})'.format(self.title, val_str)

    # ~~~~~ Public methods ~~~~~