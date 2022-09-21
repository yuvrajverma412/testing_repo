import pandas as pd


class TcgaPreprocessing:

    def clinicalDatasetCleaner(clinical_ds):
        """
        Description:
            The first two rows of these dataset will contain the column name again and random CIDs.
            So they will be removed first. - Then rows which do not contain proper information for
            the column “treatment_best_response” will be removed. - Then rows which do not contain proper
            information for the column “pharmaceutical_therapy_drug_name” will be removed.
            clinical_ds -> clinical_dataset
        Args:
            clinical_ds -> The Cancer Genome Atlas (TCGA) clinical dataset contain treatment response,
            drug name, clinical trials drug, patient id and other information related to patients.
        Return:
            clinical_ds -> return a preprocessed clinical dataset.
        """

        # removing two rows which contains the column name again and cfi.
        clinical_ds.drop([0, 1], inplace=True)

        # Dropping rows which doesnot contain proper information for the column 'treatment best response'.
        clinical_ds.drop(
            clinical_ds[
                (clinical_ds['treatment_best_response'] == '[Not Applicable]') |
                (clinical_ds['treatment_best_response'] == '[Unknown]') |
                (clinical_ds['treatment_best_response'] == '[Not Available]') |
                (clinical_ds['treatment_best_response'] == '[discrepancy]')
                ].index,
            inplace=True)

        # Dropping rows which doesnot contain proper information for the column 'pharmaceutical_therapy_drug_name'.
        clinical_ds.drop(
            clinical_ds[
                (clinical_ds['pharmaceutical_therapy_drug_name'] == 'Chemo, NOS') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == 'Chemo, Multi-Agent, NOS') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == '[Not Available]') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == '[Unknown]') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == '[Not Available]') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == '[Not Applicable]') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == 'Poly E') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == 'Harmone, NOS') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == 'Mayo 425-20') |
                (clinical_ds['pharmaceutical_therapy_drug_name'] == 'recMAGE-A3')
                ].index,
            inplace=True)

        # resetting the index after preprocessing the clinical dataset
        clinical_ds.reset_index(drop=True, inplace=True)

        # Returning the cleaned dataset
        return clinical_ds


