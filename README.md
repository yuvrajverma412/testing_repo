# rtopy


# Description
rtopy package is use to calculate GSVA, SingScore and AUCell. We can
calculate GSVA, SingScore and AUCell by passing the Micro Array and GeneSet data.
And it return Data Frame. To find GSVA Enrichment Score you use **gsvaScore** function,
for singscore you use **singScore** function and for AUCell you use **aucellScore**
function. **singScore** function return two things (**total_score_df** and **total_dispersion_df**) Data Frame.

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
        ('argument', robjects.ListVector(default_arg)))
```
## pass the args variable in aucell_data_collection function to call the r function in python.
```console
matrix = aucell_data_collection.rcall(args)
```

## pass the R script path
```console
r_path = 'r_script_file_path'
```

## pass the micro array file path in csv format and gene set data path in gmt format
```console
obj = RtoPy("mirco_array", "gene_set")
```

## choice the function which you want to run
```console
output = obj.aucellScore(**args)
```

# Setup

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
# command for windows

envname\Scripts\activate

# command for Linux

source envname/bin/activate
```
*Installing Packages*
```console
python -m pip install -r requirements.txt
```

**Command to install BioPackage Installer**
```console
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
```

**Command to install GSVA Library**
```console
BiocManager::install("GSVA")
```

**Command to install SingScore Library**
```console
BiocManager::install("singscore")
```

**Command to install AUCell Library**
```console
BiocManager::install("AUCell")
```

## importing rtopy module by using below command

```console
from src.rtopy import RtoPy
```

## calling GSVA, SingScore and AUCell
```console
obj = RtoPy('micro_array_file_path.csv', 'geneset_file_path.gmt')
gsva_output = obj.gsvaScore()
aucell_output = obj.aucellScore()
singscore_output = obj.singScore()
```



# Testing

## Test rtopy module by using below command
```console
test.py
```
If it show 'Tested_ok' then rtopy module running prefectly. Otherwise, it show 'Test Fail'


# Usage

## GSVA
```console
gsvaScore(method: "ssgsea", 
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
aucellScore(featureType: "genes",
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
singScore(downSet: False,
                subSamples: 'null',
                centerScore: True,
                dispersionFun: mad,
                knownDirection: True)
```

# Platform Tested

**Windows**
