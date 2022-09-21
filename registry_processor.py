from __future__ import annotations
from src import TCGA
from src import CCLE
from src import loadJsonFromFile
from pathlib import Path


def registryTCGA(config:object, argument_parser:object) -> None:

    expr_data_folder = Path(config['TCGA']['RAW_EXPRESSION_TCGA_LOCATION'])

    mut_data_folder = Path(config['TCGA']['RAW_MUTATION_TCGA_LOCATION'])
    clin_data_folder = Path(config['TCGA']['RAW_CLINICAL_TCGA_LOCATION'])
    expr_file_ident_stub = config['TCGA']['FIREHOSE_DATA_FILE_IDENTIFICATION_STUB']
    mut_file_ident_stub = config['TCGA']['GDC_MUT_DATA_FILE_IDENTIFICATION_STUB']

    feature_name_map = loadJsonFromFile(config['JSON']['JSON_FEATURE_NAME_FIX'])[0]['TCGA_MUT']

    mut_output_file_loc_indiv = config['TCGA']['PROCESSED_TCGA_MUTATION_FILE_LOCATION_INDIV']

    tcga = TCGA(expression_data_folder_location=expr_data_folder,
                expression_file_identification_stub=expr_file_ident_stub,

                mutation_data_folder_location=mut_data_folder,
                mutation_file_identification_stub=mut_file_ident_stub,
                
                clinical_data_folder_location=clin_data_folder,
                
                mut_output_loc_indiv=mut_output_file_loc_indiv,
                
                mut_header=feature_name_map,)
    
    tcga.processAllData()


def registryCCLE(config:object, argument_parser:object) -> None:

    expr_data_folder = Path(config['CCLE']['RAW_CCLE_DATA_PATH'])
    processed_data_folder = Path(config['CCLE']['PROCESSED_CCLE_DATA_PATH'])
    mut_data_folder = Path(config['CCLE']['RAW_CCLE_DATA_PATH'])
    expr_file_ident_stub = config['CCLE']['RAW_CCLE_EXPRESSION_FILE']
  
    ccle = CCLE(expression_data_folder_location=expr_data_folder,
                processed_data_folder_location=processed_data_folder,
                expression_file_identification_stub=expr_file_ident_stub,
                mutation_data_folder_location=mut_data_folder)
    
    ccle.processAllData()
