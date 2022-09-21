from __future__ import annotations
from ..abstract_class import RawDataProcessorEMC
from ..io import readCSV
import numpy as np
import pandas as pd
from typing import Union
from pathlib import Path
import glob
import os

class CCLE(RawDataProcessorEMC):

    def __init__(self, expression_data_folder_location:Union[str, Path],
                        processed_data_folder_location:Union[str, Path],
                        expression_file_identification_stub:str,
                        mutation_data_folder_location:Union[str, Path]) -> None:
        
        self.expr_data_folder = expression_data_folder_location if isinstance(expression_data_folder_location, Path)\
                                 else Path(expression_data_folder_location)
        self.processed_data_folder = processed_data_folder_location if isinstance(processed_data_folder_location, Path)\
                                else Path(processed_data_folder_location)
        self.expr_file_ident_stub = expression_file_identification_stub
        self.mut_data_folder = mutation_data_folder_location if isinstance(mutation_data_folder_location, Path)\
                                else Path(mutation_data_folder_location)

    
    def _readAndFixFile(self, exp_file: Union[str, Path]) -> pd.DataFrame:
        print('reading file:{}'.format(exp_file))
        data = readCSV(exp_file, sep='\t', low_memory=False, skiprows=1).dropna()
        #meta_info = data.iloc[:, np.where(data.iloc[0] == 'scaled_estimate')[0]]
        #print(meta_info)
        return data
    
    def processExpressionData(self) -> None:
        expression_file = os.path.join(self.expr_data_folder,self.expr_file_ident_stub)
        _data = self._readAndFixFile(expression_file)
        print('Saving file:{}'.format(self.expr_file_ident_stub))
        _data.to_csv(os.path.join(self.processed_data_folder,self.expr_file_ident_stub))

    def processMutationData(self) -> None:
        pass

    def processClinicalData(self) -> None:
        pass
    
    def processAllData(self) -> None:
        self.processExpressionData()
