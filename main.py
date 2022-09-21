from __future__ import annotations
import numpy as np
from src import createArgumentParser, getConfig, PrimaryNameMappper,\
     buildCellLineNamesTable, buildGeneNamesTable, loadJsonFromFile
import sys
from pathlib import Path
from registry_processor import registryTCGA, registryCCLE
from format_converter import convertFileFormat

def cellLineFileBuilder(config:object) -> None:

    cell_mapper_json = loadJsonFromFile(config['JSON']['JSON_MAPPER_FILE'])[0]['celllines']

    sample_info_file = Path(config['CCLE']['RAW_SAMPLE_FILE'])
    output_path = Path(config['COMMON']['CELL_LINE_NAME_MAPPER_FILE'])
    selected_fields_cell_line = cell_mapper_json['required_columns']
    target_column = cell_mapper_json['target_column']
    base_column = cell_mapper_json['base_column']
    mapped_column = cell_mapper_json['mapped_column']

    buildCellLineNamesTable(sample_info_file=sample_info_file,
                            output_file_name=output_path,
                            selected_fields_cell_line=selected_fields_cell_line,
                            target_column=target_column,
                            base_column=base_column,
                            mapped_column=mapped_column)


def genenamesBuilder(config:object) -> None:    
    gene_mapper_json = loadJsonFromFile(config['JSON']['JSON_MAPPER_FILE'])[0]['genes']

    gene_list_file = Path(config['COMMON']['GENE_MASTER'])
    output_path = Path(config['COMMON']['GENE_NAME_MAPPER_FILE'])

    required_columns = gene_mapper_json['required_columns']

    buildGeneNamesTable(gene_list_file=gene_list_file,
                        output_file_name=output_path,
                        selected_fields_genes=required_columns)


if __name__ == '__main__':
    
    config = getConfig()
    
    command = ''
    if len(sys.argv) > 1:
        command = sys.argv[1]

    argument_parser = createArgumentParser(default_config_file=config['JSON']['JSON_DEFAULT_CONFIGS'], global_config=config)

    if command == 'preprocess':
        if argument_parser.preprocess_genename:
            genenamesBuilder(config)
            sys.exit(0)

        if argument_parser.preprocess_cellline:
            cellLineFileBuilder(config)
            sys.exit(0)

        if argument_parser.datasets is not None:
            for dataset in argument_parser.datasets:
                eval(f'registry{dataset}')(config, argument_parser)
            sys.exit(0)
    
    elif command =='format':
        if argument_parser.formats is not None:
            eval(f'convertFileFormat')(config, argument_parser)
            sys.exit(0)

