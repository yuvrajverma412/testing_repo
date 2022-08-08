# Repo

**Operating System**

Windows 10

**Python Version**

Python 3.9.12

**Virtual Environment**

*Installing Virtual Environment*
```console
python -m pip install --user virtualenv
```
*Creating New Virtual Environment*
```console
python -m venv envname
```
*Activating Virtual Environment*
```console
source envname/bin/activate
```
*Installing Packages*
```console
python -m pip install -r requirements.txt
```

# Over View
r_2_python_conversion package is use to calculate GSVA, SingScore and AUCell. We can
calculate GSVA, SingScore and AUCell by passing the Micro Array and GeneSet data.
And it return Data Frame. To find GSVA Enrichment Score you use **gsva_score** function,
for singscore you use **singscore_score** function and for AUCell you use **aucell_score**
function. **singscore_score** function return two things (**total_score_df** and **total_dispersion_df**) Data Frame.

Gene set variation analysis (GSVA) is a particular type of gene set enrichment
method that works on single samples and enables pathway-centric analyses of 
molecular data by performing a conceptually simple but powerful change in the 
functional unit of analysis, from genes to gene sets.

SingScore implements a simple single-sample gene-set (gene-signature) scoring 
method which scores individual samples independently without relying on other 
samples in gene expression datasets.

AUCell allows to identify cells with active gene sets (e.g. signatures, gene 
modules...) in single-cell RNA-seq data. AUCell uses the "Area Under the Curve" 
(AUC) to calculate whether a critical subset of the input gene set is enriched 
within the expressed genes for each cell.

In this package, we using rpy2 library which help in to load the R script into python.
And inside python we can access all the functionality of the R script by using rp2.

## To import the function from R to python use below command
```console
r = robjects.r['function_name']
```

## To create the global Env. for R function use below command
```console
data_collection = robjects.globalenv['function_name_present_inside_r_script']

Example:
aucell_data_collection = robjects.globalenv['aucell_data_collection'] 
```

## store the argument of aucell_data_collection function in tuple 
```console
# tuple contain key and value -> key: argument name  and value: file_paths
args = (('csv_file_path', self.csv_file_path),
        ('gmt_file_path', self.gmt_file_path),
        ('lst', robjects.ListVector(dct)))
```
## pass the args variable in aucell_data_collection function to call the r function in python.
```console
matrix = aucell_data_collection.rcall(args)
```

## pass the R script path
```console
r_path = 'r_script_file_path'
```

## pass the csv and gmt path
```console
obj = r_2_python_conversion("csv_file_path", "gmt_file_path")
```

## choice the function which you want to run
```console
output = obj.aucell_score(**args)
```

# Getting Started

## importing r_2_python_conversion module by using below command

```console
from src.rtopy import r_2_python_conversion
```

## calling GSVA, SingScore and AUCell
```console
obj = r_2_python_conversion('micro_array_file_path', 'geneset_file_path')
gsva_output = obj.gsva_score()
aucell_output = obj.aucell_score()
singscore_output = obj.singscore()
```

# Arguments

## GSVA
```console
gsva_score(method: "ssgsea", 
            kcdf: "Gaussian", 
            abs_ranking: False,
            min_sz: 1,
            max_sz: float('inf'),
            parallel_sz: 100000000,
            max_diff: True,
            tau: {'tau_method':'ssgsea', 'gsva': 1, 'ssgsea': 0.25},
            ssgsea_norm: True,
            verbose: True)
```

## AUCell
```console
aucell_score(featureType: "genes",
                plotStats: True,
                splitByBlocks: False,
                BPPARAM: 'null',
                keepZeroesAsNA: False,
                verbose: True,
                nCores: 'null',
                mctype: 'null',
                nCores_cal_auc: 1,
                normAUC: True,
                aucMaxRank: 0.05,
                verbose_cal_auc: True)
```

## SingScore
```console
**if knownDirection = False set the downSet value False.**
singscore_score(downSet: False,
                subSamples: 'null',
                centerScore: True,
                dispersionFun: mad,
                knownDirection: True)
```

# Testing

## Test r_2_python_conversion module by using below command
```console
from src.rtopy import r_2_python_conversion

obj = r_2_python_conversion('./data/matrix_.csv', './data/c2.cp.v7.5.1.symbols.gmt')
gsva_output = obj.gsva_score()
# aucell_output = obj.aucell_score()
# singscore_output = obj.singscore()
print(gsva_output)
```

# Usage

## source function is use to load the whole R script inside the Python
```console
r = robjects.r
r['source'](r_file_path)
```

## Command to install BioPackage Installer
```console
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
```

## Command to install GSVA Library
```console
BiocManager::install("GSVA")
```

## Command to install SingScore Library
```console
BiocManager::install("singscore")
```

## Command to install AUCell Library
```console
BiocManager::install("AUCell")
```
