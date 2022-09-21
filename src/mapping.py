from __future__ import annotations
from typing import Union, Tuple
from pathlib import Path
import pandas as pd
from .io import readCSV

class PrimaryNameMappper:

    def __init__(self, mapping_file_path:Union[str, Path]) -> None:

        self.cell_table = readCSV(mapping_file_path)
    
    def correctCellLineNames(self, keyword:str, primary_name:str, *args) -> Tuple[str, int]:

        """
        Accepts a potential cell line name and returns its primary name
        and number of matches from the cell line names table
        Args:
            keyword: name of the cell line to be searched
        Returns:
            primary_name: primary name/s of matched cell line/s
            hits : number of matches in the cell line names table
        """

        keyword = keyword.lower()
        self.cell_table['names'] = self.cell_table[primary_name] + '|' + self.cell_table[args[0]]
        ans = self.cell_table[self.cell_table['names'].str.contains(keyword, na=False)]
        if ans.shape[0]==1:
            name = ans[primary_name].values[0]
            hits = 1
        elif ans.shape[0]==0:
            name=''
            hits = 0
        elif ans.shape[0]>1:
            hits = ans.shape[0]
            name = ans[primary_name].values
        return name,hits


    def correctGeneNames(self,keyword:str, primary_name:str, *args) -> Tuple[str, int]:

        """
        Accepts a potential gene name and returns its primary name
        and number of matches from the gene names table
        Args:
            keyword: name of the gene to be searched
        Returns:
            primary_name: primary name of the gene
            hits : number of matches in the the gene names table
        """
        
        name, hits = self.correctCellLineNames(keyword, primary_name, *args)
        return name,hits
