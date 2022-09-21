from __future__ import annotations
from ..abstract_class import RawDataProcessorEMC
from ..io import readCSV, saveToCSV
import numpy as np
import pandas as pd
from typing import Union, Any, Dict
from pathlib import Path
import glob
import tqdm

class TCGA(RawDataProcessorEMC):
    
    def __init__(self, expression_data_folder_location:Union[str, Path],
                        expression_file_identification_stub:str,

                        mutation_data_folder_location:Union[str, Path],
                        mutation_file_identification_stub:str,
                        
                        clinical_data_folder_location:Union[str, Path],

                        mut_output_loc_indiv:Union[str, Path],
                        **kwargs: Dict[str, Any]) -> None:
        
        '''
        
            This class has been written with the assumption that the build of mutation data is GRCh38.

            Args:
            ------

            expression_data_folder_location: str|Path : Folder containing all files having expression data. 
                                                        These files are downloaded from firehose and are stored
                                                        seperatly on the basis of cancer type.
            expression_file_identification_stub: str : Identifer for the firehose files that have expression with
                                                       with required normalization.
            mutation_data_folder_location: str|Path: Folder containing all files having mutation data for every patient.
                                                     These files are downloaded from GDC.
            mutation_file_identification_stub: str : Identifier for GDC mutation files.
            clinical_data_folder_location: str|Path : Folder having files for clinical data. These files are downloaded
                                                      from GDC. These files are stored seperatly on the basis of
                                                      cancer-type.
            mut_output_loc_indiv: str|Path : Output location for mutation data. This file name will be used to store
                                             mutation data for all patients. No clinical information will be considered here.
            
            **kwargs: dict :

                'mut_header' : dict[str, str] : A dictionary containing mapping of header for mutation data.


            @TODO:
                Add output for common data: Clinical + DNA
                Add header for expression data :
                ---
        '''

        self.expr_data_folder = expression_data_folder_location if isinstance(expression_data_folder_location, Path)\
                                 else Path(expression_data_folder_location)
        self.expr_file_ident_stub = expression_file_identification_stub

        self.mut_data_folder = mutation_data_folder_location if isinstance(mutation_data_folder_location, Path)\
                                else Path(mutation_data_folder_location)
        self.mut_file_ident_stub = mutation_file_identification_stub

        self.clin_data_folder = clinical_data_folder_location if isinstance(clinical_data_folder_location, Path)\
                                else Path(clinical_data_folder_location)
        
        self.mut_header_map = kwargs['mut_header'] if 'mut_header' in kwargs else None

        #Output segment
        self.mut_output_loc_indiv = mut_output_loc_indiv if isinstance(mut_output_loc_indiv, Path)\
                                    else Path(mut_output_loc_indiv)

    def _readAndFixExprFile(self, exp_file: Union[str, Path]) -> pd.DataFrame:
        
        #print(exp_file)
        data = readCSV(exp_file, sep='\t', low_memory=False, skiprows=1).dropna()#.set_index('Unnamed: 0')
        return data
        #print(data)
        #meta_info = data.iloc[:, np.where(data.iloc[0] == 'scaled_estimate')[0]]
        #print(meta_info)

    def _fixTcgaId(self, rna_dataset):
        rna_expression_df = pd.DataFrame()
        rna_expression_df['Hybridization REF'] = rna_dataset['Hybridization REF']

        patient_id = []
        for rna_data_col_name in rna_dataset.columns:
            split_col_name = rna_data_col_name.split('-')
            
            if len(split_col_name) >= 3:
                joined_barcode = '-'.join([split_col_name[0], split_col_name[1], split_col_name[2]])

                sample_id = ""
                for barcode_sample_id in split_col_name[3]:
                    if barcode_sample_id.isdigit():
                        sample_id += barcode_sample_id

                if len(sample_id) <= 9:
                    if rna_dataset[rna_data_col_name].iloc[0] == 'scaled_estimate':
                        patient_id.append(joined_barcode)
                        rna_expression_df[rna_data_col_name] = pd.to_numeric(
                            rna_dataset[rna_data_col_name].iloc[1:], downcast="float") * 10 ** 6

        patient_id.insert(0, 'Hybridization REF')
        line = pd.DataFrame([patient_id], columns=rna_expression_df.columns)
        rna_expression_df = pd.concat([rna_expression_df[:0], line, rna_expression_df[0:]], ignore_index=True)
        rna_expression_df.drop(index=rna_expression_df.index[1:31], inplace=True)
        

        col_names = [col_name for col_name in rna_expression_df.columns] 
        pivot = col_names[1][:12]
        index = 2
        select_col = [col_names[0]]
        while(index < len(col_names)):
            if pivot == col_names[index][:12]:
                col_names.pop(index)

            else:
                pivot = col_names[index][:12]
                index += 1

        rna_expression_df = rna_expression_df[col_names]
        rna_expression_df.reset_index(drop=True, inplace=True)

        return rna_expression_df

    def _geneNameProcessing(self, gene_name: str): # processing the gene name for expression data
        pass

    def _readAndFixMutFile(self, mut_file: Union[str, Path]) -> pd.DataFrame:

        '''
            This function reads mutation file `maf` and selects required columns and fixes them.

            Args:
            ------
             mut_file: str|Path : Path to the mutation data file in mutation annotation format.

            Output:
            --------
             returns processed data.

        '''

        data = readCSV(mut_file, sep='\t', low_memory=False, comment='#').dropna(axis=1)
        if self.mut_header_map is not None:

            sampled_data = data[list(self.mut_header_map.keys())]
            sampled_data = sampled_data.rename(self.mut_header_map, axis=1)

            return sampled_data
        
        return data

    def _fixGeneNames(self, gene_name:str) -> str:
        return gene_name

    def processExpressionData(self) -> None:
        
        expression_files = glob.iglob(str(self.expr_data_folder/f'*/*{self.expr_file_ident_stub}*.gz'))
        
        exp_data = []

        print("Processing expression files")
        for exp_file in expression_files:
            _data = self._readAndFixExprFile(exp_file)
            _rna_exp_df = self._fixTcgaId(_data)

            exp_data.append(_rna_exp_df)

        exp_df = pd.concat(exp_data, axis=0).reset_index(drop=True)
        print("Saving processed expression file")
        saveToCSV(exp_df, self.expr_data_folder, index=False)

        # singscore or aucell preprocessing needs to be included in this function.
        
    def processMutationData(self) -> None:

        '''

            Function to process mutation data.

        '''
        
        mutation_file = glob.glob(str(self.mut_data_folder/f'*/*{self.mut_file_ident_stub}*.maf.gz'))

        mut_data = []

        print('Processing mutation files')
        for i in tqdm.tqdm(range(len(mutation_file))):
            mut_file = mutation_file[i]
            _data = self._readAndFixMutFile(mut_file)
            _data['gene'] = _data['gene'].apply(self._fixGeneNames)

            mut_data.append(_data)
        
        mut_df = pd.concat(mut_data, axis=0).reset_index(drop=True)
        print('Saving processed mutation file')
        saveToCSV(mut_df, self.mut_output_loc_indiv, index=False)

    def processClinicalData(self) -> None:
        pass

    def processAllData(self) -> None:

        '''
            Wrapper function to all TCGA processing scripts.
        '''
        
        self.processExpressionData()
        # self.processMutationData()
