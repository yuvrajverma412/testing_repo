def datasetcleaner(dataset):
    '''
      #This function cleans the dataset based on the information available on treatment_best_response and pharmaceutical_therapy_drug_name.
      #pharmaceutical_therapy_drug_name column should contain the name of the drug administred to the patient.
      #treatment_best_response column should contain the response of the patient to the administred drug.
      #In the first step, first two rows which contains the column name again and cfi id is removed.
      #In the second step, rows which doesnot contain proper information for the column treatment_best_response is removed.
      #In the third step, rows which doesnot contain proper information and rows which contain particular drug names for the column pharmaceutical_therapy_drug_name is removed.
      #This function returns the cleaned dataset.
    '''
    import pandas as pd
    #Remo dataset.drop([0,1],0,inplace = True)ving first two lines of the dataset containing column name information.

    #Dropping rows which doesnot contain proper information for the column 'treatment best response'.
    dataset.drop(
            dataset[
                    (dataset['treatment_best_response'] == '[Not Applicable]') |
                    (dataset['treatment_best_response'] == '[Unknown]') |
                    (dataset['treatment_best_response'] == '[Not Available]') |
                    (dataset['treatment_best_response'] == '[discrepancy]')
                ].index,
            inplace = True)

    #Dropping rows which doesnot contain proper information for the column 'pharmaceutical_therapy_drug_name'.
    dataset.drop(
            dataset[
                    (dataset['pharmaceutical_therapy_drug_name'] == 'Chemo, NOS') |
                    (dataset['pharmaceutical_therapy_drug_name'] == 'Chemo, Multi-Agent, NOS') |
                    (dataset['pharmaceutical_therapy_drug_name'] == '[Not Available]') |
                    (dataset['pharmaceutical_therapy_drug_name'] == '[Unknown]') | 
                    (dataset['pharmaceutical_therapy_drug_name'] == '[Not Available]') |
                    (dataset['pharmaceutical_therapy_drug_name'] == '[Not Applicable]') |
                    (dataset['pharmaceutical_therapy_drug_name'] == 'Poly E') |
                    (dataset['pharmaceutical_therapy_drug_name'] == 'Harmone, NOS') |
                    (dataset['pharmaceutical_therapy_drug_name'] == 'Mayo 425-20') |
                    (dataset['pharmaceutical_therapy_drug_name'] == 'recMAGE-A3')
                ].index,
            inplace = True)

    #Returning the cleaned dataset
    return(dataset)


########################
def rnaPreProcessingFirehouse(cl_data, fr_data):
    '''
      # Algorithm to fetch rna expression data btwn clinical and firehouse data

       * function is taking 2 dataframe as argument cl_data for clinical data and fr_data for firhouse data
       * In 1st step we are creating a empty dataframe to store the rna expression data
       * In 2nd step we are using 1st for loop to iterate through patient barcode and 2nd loop to iterate through firehouse data columns names
       * In 3rd step we are splitting up the column names into sub string to match the patient barcode length
       * In 4th step joining the first 3 substring to match with patient bracode format
       * In 5th step we are checking data only for tumour patient so we have put if condition to check if the sample code present in column value is <=9
       * IN 6th step we are checking for scaled estimate column values as there are 3 clumns availabel with diff values
       * In 7th step we are checking if the patient barcode is matching with joined_barcode
       * Finally we are storing the rna values of each patient_barcode which matched and multiplied the values by 10**6
    '''

    import pandas as pd

    data_cl_fr = pd.DataFrame()
    data_cl_fr['Hybridization REF'] = fr_data['Hybridization REF']

    for x in cl_data['bcr_patient_barcode']:
        for y in fr_data.columns:

            split_code = y.split('-')

            if len(split_code) >= 3:

                joined_barcode = '-'.join([split_code[0],split_code[1],split_code[2]])
                sample=""

                for c in split_code[3]:
                    if c.isdigit():
                       sample = sample + c

                if int(sample) <= 9:

                    if x == joined_barcode:

                        if fr_data[y].iloc[0] == 'scaled_estimate':

                            data_cl_fr[y] = pd.to_numeric(fr_data[y].iloc[1:], downcast = "float")*10**6

    ## removing first 30 rows to remove pseudo genes ?
    data_cl_fr.drop(index=data_cl_fr.index[:30], axis=0, inplace=True)
    ## splitting up the symbols and gene id and keeping ony symbols to use for scoring method
    data_cl_fr['Hybridization REF'] = data_cl_fr['Hybridization REF'].apply(lambda x: x.split('|')[0])

    return data_cl_fr
