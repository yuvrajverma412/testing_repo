from src import getConfig, PrimaryNameMappper, loadJsonFromFile
from registry_processor import registryTCGA

def runExample(config:object) -> None:

    mapper_json = loadJsonFromFile(config['JSON']['JSON_MAPPER_FILE'])[0]

    ccle_table_path = config['CCLE']['CELL_LINE_NAME_MAPPER_FILE']
    ccle_mapper = PrimaryNameMappper(ccle_table_path)
    ccle_mapper_json = mapper_json['celllines']
    ccle_target_column = ccle_mapper_json['target_column']
    ccle_mapped_column = ccle_mapper_json['mapped_column']

    ans1 = ccle_mapper.correctCellLineNames('ACH-000708', ccle_target_column, ccle_mapped_column)
    print(ans1)

    gene_names_table_path = config['CCLE']['GENE_NAME_MAPPER_FILE']
    gene_mapper = PrimaryNameMappper(gene_names_table_path)
    gene_mapper_json = mapper_json['genes']
    gene_target_column = gene_mapper_json['target_column']

    ans2 = gene_mapper.correctGeneNames('agpat3', 'HGNC ID', gene_target_column)
    print(ans2)


if __name__ == '__main__':
    config = getConfig(config_file='config.ini')
    #print(config)

    #runExample(config)
    registryTCGA(config, None)
