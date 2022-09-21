import subprocess
from os import path
from pathlib import Path

def convertFileFormat(config:object, argument_parser:object) -> None:

    liftover_mappers_folder = Path(config['LIFTOVER']['LIFTOVER_MAPPER_FILES_PATH'])
    liftover_h19_h38_mapper_file = Path(config['LIFTOVER']['LIFTOVER_H19_H38_MAPPER'])
    liftover_h38_h19_mapper_file = Path(config['LIFTOVER']['LIFTOVER_H38_H19_MAPPER'])

    for f in argument_parser.formats:
        infile = argument_parser.input_file
        outfile = argument_parser.output_file
        h19_path = path.join(liftover_mappers_folder,liftover_h38_h19_mapper_file)
        h38_path = path.join(liftover_mappers_folder,liftover_h19_h38_mapper_file)

        if f == 'hg19' and infile and outfile:
            subprocess.run(['liftOver',\
                    infile,\
                    h19_path,\
                    outfile,\
                    '_unMapped.'.join(outfile.split('.'))])
        
        elif f == 'hg38' and infile and outfile:
            subprocess.run(['liftOver',\
                    infile,\
                    h38_path,\
                    outfile,\
                    '_unMapped.'.join(outfile.split('.'))])

        elif f =='vcf' and infile and outfile:
            subprocess.Popen('convert2bed -i vcf <'+infile+'> '+outfile, shell=True)
                    
        else:
            print('No valid output format given')
                
