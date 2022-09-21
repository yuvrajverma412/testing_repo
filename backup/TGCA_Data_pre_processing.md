# TGCA Data pre processing
 - To download the TGCA dataset go to [GDC Data portal's repository](https://portal.gdc.cancer.gov/repository)
  - Apply the following filters:
              *Data category - clinical
              *Data type - clinical supplement
              *Data format - bcr biotab
              *Cases - TGCA
   - After applying this filter, pick files which have the word “drug” in it.
   - Download the manifest
   - To download the data using the manifest we need [gdc data transfer tool](https://gdc.cancer.gov/access-data/gdc-data-transfer-tool)
   - To know how to use the gdc data transfer tool, refer to this site [user's guide for gdc data transfer tool client](https://docs.gdc.cancer.gov/Data_Transfer_Tool/Users_Guide/Data_Download_and_Upload/).
    - After downloading the given, data using pandas dataframe the pre-processing is being done.
    - The first two rows of these dataset will contain the column name again and random CIDs. So they will be removed first.
    - Then rows which do not contain proper information for the column “Patient_drug_response” will be removed.
    - Then rows which do not contain proper information for the column “Patient_therapy_drug_name” will be removed.
