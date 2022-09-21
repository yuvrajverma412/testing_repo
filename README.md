# data-cleaning

## Gene list download
HUGO (https://www.genenames.org/download/custom/)

## Format Conversion
#### h19 to h38 

**Usage**
```console
python main.py format -f hg19 -i <path_to_input_bed_file> -o <path_to_output_bed_file>

#Example
python main.py format -f hg19 -i /gntrprtr/DataRepo/software-data/liftover/old.bed -o /gntrprtr/DataRepo/software-data/liftover/new_h19.bed
```
#### h38 to h19
```console
python main.py format -f hg38 -i <path_to_input_bed_file> -o <path_to_output_bed_file>

# Example
python main.py format -f hg38 -i /gntrprtr/DataRepo/software-data/liftover/old.bed -o /gntrprtr/DataRepo/software-data/liftover/new_h38.bed
```

#### VCF to BED
```console
python main.py format -f vcf -i <path_to_input_vcf_file> -o <path_to_output_bed_file>

# Example
python main.py format -f vcf -i /gntrprtr/sajil/mylab/reference_vcf2bed_foo.vcf -o /gntrprtr/sajil/mylab/out.bed
```
**Tested on**
```console
MAC 10.14.6
```
