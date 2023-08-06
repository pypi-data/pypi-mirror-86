"""
read_files.py
~~~~~~~~~~~~~
This modules provides functions which aid in reading data from files.
"""

# Standard library.
from typing import Any, Dict, List, Union
# Related third-party library.
from pandas import DataFrame, read_excel, read_csv
from xlrd import open_workbook, XLRDError

def is_excel(
        filename: str
) -> bool:
    """
    Returns ``True`` if the file provided in ``filename`` is a valid Excel file, and ``False``
    otherwise.

    :param filename:    The qualified name of the file to be checked.
    :rtype:             ``bool``
    """
    try:
        open_workbook(filename)
        return True
    except XLRDError:
        return False
    except Exception as e:
        print(e)
        return False

def read_file(
        filename: str,
        return_pandas_df: bool = False
) -> Union[DataFrame, Dict[str, List[Any]]]:
    """
    Reads the provided Excel or CSV data file. Returns a pandas ``DataFrame`` object if
    ``return_pandas_df`` is ``True``, or a dictionary where the keys are column titles and the
    values are lists of associated values (in order) otherwise.
    
    :param filename:            The qualified path to the data file to read.
    :param return_pandas_df:    (optional) Defaults to ``False``. If ``True``, a pandas
                                ``DataFrame`` object will be returned. Otherwise, a dictionary where
                                the keys are column titles and the values are lists of associated
                                values (in order) will be returned.
    :rtype:                     ``Union[DataFrame, Dict[str, List[Any]]]``
    """
    # Reading file.
    if is_excel(filename):
        # File is an Excel file.
        df = read_excel(filename)
    else:
        # File is a CSV file.
        df = read_csv(filename)
    
    # Returning value based on whether ``return_pandas_df`` is ``True`` or ``False``
    if return_pandas_df:
        return df
    return {i: list(df[i]) for i in list(df.columns)}
