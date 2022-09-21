from __future__ import annotations
from typing import Union, List
from pathlib import Path
import pandas as pd
from .io import saveToCSV, readCSV

def buildCellLineNamesTable(sample_info_file:Union[str, Path], 
                            output_file_name:Union[str, Path],
                            *,
                            selected_fields_cell_line:List[str],
                            target_column:str,
                            base_column:str,
                            mapped_column:str) -> None:
    
    '''
        Function to build cell line tables that creates map that can be used to fix names.

        Arguments:
        ------------
        sample_info_file: str|Path : File containing all information regarding cell lines.
        output_file_name: str|Path : File where to the output file.
    '''
    

    cell_line_df = pd.DataFrame()
    cell_line_table = readCSV(sample_info_file)

    cell_line_table = cell_line_table[selected_fields_cell_line]
    cell_line_df[target_column] = cell_line_table[base_column]

    synonyms = cell_line_table.drop([base_column],axis=1)

    cell_line_df[mapped_column] = synonyms[synonyms.columns].agg(lambda x: '|'\
        .join(x[~x.isnull()].values), axis=1)
    cell_line_df = cell_line_df.apply(lambda x: x.astype(str).str.lower())
    
    saveToCSV(cell_line_df, output_file_name)


def buildGeneNamesTable(gene_list_file:Union[str, Path], 
                        output_file_name:Union[str, Path], 
                        *, 
                        selected_fields_genes:List[str]) -> None:
    
    '''
        Function to build gene name table that creates map that can be used to fix names.

        Arguments:
        -----------
        gene_list_file: str|Path : File containing all information regarding gene names.
        output_file_name: str|Path : File where to the output file.
    '''

    gene_names_table = readCSV(gene_list_file, sep='\t')

    gene_names_table = gene_names_table[selected_fields_genes]
    gene_names_table = gene_names_table.fillna('')
    gene_names_table = gene_names_table.apply(lambda x: x.astype('string').str.lower())

    if 'Alias symbols' in selected_fields_genes:
        gene_names_table['Alias symbols'] =  gene_names_table['Alias symbols'].apply(lambda x: '|'.join(x.split(',')))
    if 'Alias names' in selected_fields_genes:
        gene_names_table['Alias names'] =  gene_names_table['Alias names'].apply(lambda x: '|'.join(x.split(',')))
    
    saveToCSV(gene_names_table, output_file_name)
    
