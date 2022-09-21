# TGCA RNA DATA PREPROCESSING

 - First we have downloaded the TCGA clinical data and firehouse gene_data for every cancer types [Links for downloading firehouse Data](https://drive.google.com/file/d/1mPVt1iu6JyIjfIHxuiXps0FnN6eLahzr/view?usp=sharing)
 - Then we are using both the data in main.py for fetching RNA expression data
 - I have created the rnaPreProcessingFirehouse function in utils.py

## Algorithm to fetch rna expression data btwn clinical and firehouse data (Understanding  rnaPreProcessingFirehouse  function)

 - function is taking 2 dataframe as argument cl_data for clinical data and fr_data for firhouse data
 - In 1st step we are creating a empty dataframe to store the rna expression data
 - In 2nd step we are using 1st for loop to iterate through patient barcode and 2nd loop to iterate through firehouse data columns names
 - In 3rd step we are splitting up the column names into sub string to match the patient barcode length
 - In 4th step joining the first 3 substring to match with patient bracode format
 - In 5th step we are checking data only for tumour patient so we have put if condition to check if the sample code present in column value is <=9
 - In 6th step we are checking for scaled estimate column values as there are 3 clumns availabel with diff values
 - In 7th step we are checking if the patient barcode is matching with joined_barcode
 - Finally we are storing the rna values of each patient_barcode which matched and multiplied the values by 10**6
