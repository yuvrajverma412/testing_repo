from __future__ import annotations
from typing import Union, List, Dict, Any, Optional
from pathlib import Path
import pandas as pd
import json

def loadJsonFromFile(data_file: Union[str, Path]) -> List[Dict[str, Any]]:

    '''
        Function to load json from file.

        Args:
        ------

        data_file: str|Path : JSON file containing data.

        Returns:
        ---------
        loaded data

    '''

    with open(data_file, 'r') as fid:
        data = json.load(fid)
    
    return data


def saveToCSV(df: pd.DataFrame, file_name:Union[str, Path], index:bool =False, **kwargs) -> None:

    """
    Accepts a dataframe and save it as CSV
    Args:
        df: pandas dataframe: dataframe which is to be saved
        file_name: str|Path : Filename of the csv file where dataframe has to be exported.
        index: bool=False : Stores indexes in the csv file if true.
    """

    df.to_csv(file_name, index=index)


def readCSV(file_name:Union[str, Path], 
            index_col:Optional[Union[int, str, List[int], List[str]]]=None, 
            header:Union[str, int, List[int]]='infer', 
            low_memory:bool=True,
            sep:str=',', **kwargs) -> pd.DataFrame:

    '''
        Function to read CSV file.

        Args:
            file_name: str|Path : Filename of the csv file where to load data frame.
            index_col: None|str|int|List of ints|List of strings=None : Column identification that should be treated as index of the dataframe.
            header: str|int|List of int=infer : Row identification that should be used as header of the dataframe.
            low_memory: bool=True : Whether to coerce all the values in a column to same datatype.
            sep: str=, : Delimiter of the file

    '''

    return pd.read_csv(file_name, index_col=index_col, header=header, low_memory=low_memory, sep=sep, **kwargs)
