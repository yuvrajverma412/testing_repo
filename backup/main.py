import pandas as pd
import numpy as np
# importing rnaProcessing function from utils file
from utils import rnaPreProcessingFirehouse 
# importing datasetcleaner function from utils file 
from utils import datasetcleaner

if __name__ == "__main__":
    
    # while entering the clinical data path in console pls ensure that you don't include "" 
    cl_path = str(input("Enter the path or location of clinical data and pls don't include "": "))
    # while entering the firehouse data path in console pls ensure that you don't include ""
    fr_path = str(input("Enter the path or location of firehouse data and pls don't include "": "))

    # reading clinical patient metadata
    data_CL = pd.read_table(cl_path)
    # applying the datasetcleaner function to clean clinical dataset based on the treatment_response and drug_name
    data_CL = datasetcleaner(data_CL)

    # reading firehouse data 
    data_fr = pd.read_table(fr_path, low_memory= False)

    #calling rnaProcessing func for correlation btwn clinical and firehouse data
    # this variable stores the rna processed data which we can save as csv file
    ACC_cl_fr = rnaPreProcessingFirehouse(data_CL,data_fr)   

    print(ACC_cl_fr)

