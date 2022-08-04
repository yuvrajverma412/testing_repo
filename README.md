# testing_repo

## Install Libraries 
```console
pip install rpy2
pip install numpy
pip install pandas
```

## Import Libararies
```console
import rpy2.robjects.packages as rpackages
import rpy2.robjects as robjects
import pandas as pd
import numpy as np
```

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
## tuple contain key and value -> key: argument name  and value: file_paths
```console
args = (('csv_file_path', self.csv_file_path),
        ('gmt_file_path', self.gmt_file_path),
        ('lst', robjects.ListVector(dct)))
```
# pass the args variable in aucell_data_collection function to call the r function in python.
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
output = obj.aucell_score(r_path)
```



