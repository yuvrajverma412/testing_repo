import json
import numpy as np
import pandas as pd
import rpy2.robjects as robjects
import rpy2.robjects.packages as rpackages


with open('params.json','r') as f:
    Params = json.load(f)

class RtoPy:

    def __init__(self, csv_file_path, gmt_file_path):
        self.csv_file_path = csv_file_path
        self.gmt_file_path = gmt_file_path
        self.aucell_params = Params['HYPER_PARAMS_AUCELL']
        self.singscore_params = Params['HYPER_PARAMS_SINGSCORE']
        self.gsva_params = Params['HYPER_PARAMS_GSVA']

    # r script file paths
    __gsva_r_code = './rcodes/gsva.R'
    __aucell_r_code = './rcodes/aucell.R'
    __singscore_r_code = './rcodes/singscore.R'

    
    def aucellScore(self, **args_list):
        """
        Args:
            featureType -> Name for the rows (e.g. "genes")
            plotStats -> Plot the expression boxplots/histograms? (True / False)
            splitByBlocks -> Whether to split the matrix by blocks in the ranking calculation
            Allows using multiple cores. (Default: False). Required for using sparse matrices
            BPPARAM -> Set to use multiple cores. Only used if 'splitByBlocks=True'
            keepZeroesAsNA -> Convert zeroes to NA
            verbose -> Should the function show progress messages? (True / False)
            nCores -> Number of cores to use for computation
            nCores_cal_auc -> Number of cores to use for computation
            normAUC -> Wether to normalize the maximum possible AUC to 1 (Default: True)
            aucMaxRank -> Threshold to calculate the AUC
            verbose_cal_auc -> Should the function show progress messages? (True / False)
        
        Return:
            aucell_score_df -> returns a data frame with an AUC score for each gene-set in each cell
            aucell_params -> Hyperparameters used for the AUCell
        """
        print('\nComputing AUCell Scores')

        # Defining the R script and loading the instance in Python
        r = robjects.r
        r['source'](self.__aucell_r_code)  

        # Creating the global environment and importing the aucell_data_collection\
        # function from r script in globalenv.
        aucell_data_collection = robjects.globalenv['aucell_data_collection']
        as_null = robjects.r['as.null']

        # Change the default value when user input the argument value
        for key, value in args_list.items():
            # Replacing the 'null' string with as_null() function
            if self.aucell_params[key] == 'as.null':
                self.aucell_params[key] = as_null()
            else:
                self.aucell_params[key] = value

        # Storing the argument of aucell_data_collection function in tuple
        # Tuple contain key and value -> key: argument name  and value: file_paths
        args = (('csv_file_path', self.csv_file_path),\
            ('gmt_file_path', self.gmt_file_path),\
            ('argument', robjects.ListVector(self.aucell_params)))

        # Pass the args variable in aucell_data_collection function
        # AuCell_data_collection returns three things 
        # 1. aucell_score_mat, 
        # 2. rownames and 
        # 3. colnames
        aucell_matrixs = aucell_data_collection.rcall(args)

        # Extracting aucell_score_mat and converting into numpy array
        aucell_score_mat = np.array(aucell_matrixs[0])

        # Extracting row names
        rownames = aucell_matrixs[1]

        # Extracting column names
        colnames = aucell_matrixs[2]
        
        # Creating a dataframe that contain aucell_score_mat
        aucell_score_df = pd.DataFrame(aucell_score_mat, columns=list(colnames))

        # Creating a new column of row names
        aucell_score_df['X'] = list(rownames)

        # Set row names column as index
        aucell_score_df.set_index('X', inplace=True)

        return aucell_score_df, self.aucell_params


    def singScore(self, **args_list):
        """
        Args:
            downSet	-> A GeneSet object or character vector of gene IDs of down-regulated gene set
                 or False where only a single gene set is provided
            subSamples -> A vector of sample labels/indices that will be used to subset the rankData matrix
            centerScore -> A Boolean, specifying whether scores should be centered around 0 (Default: True)
            dispersionFun -> A dispersion function with default being mad
            knownDirection -> A boolean, determining whether the gene set should be considered to be directional or not. 
            
            Return: 
                    total_score_df -> format Data Frame
                    total_dispersion_df -> format Data Frame
                    singscore_params -> Hyperparameters used for Singscore
        """
        print('\nComputing Signscore Scores')

        # Defining the R script and loading the instance in Python
        r = robjects.r
        r['source'](self.__singscore_r_code)

        # Creating the global environment and import the singscore_data_collection function from r script in globalenv.
        singscore_data_collection = robjects.globalenv['singscore_data_collection']
        
        mad = robjects.r['mad']
        as_null = robjects.r['as.null']  
 
        self.singscore_params['subSamples'] = as_null() 
        self.singscore_params['dispersionFun'] = mad

        # Store the argument of singscore_data_collection function in tuple
        # Tuple contain key and value -> key: argument name  and value: file_paths
        args = (('csv_file_path', self.csv_file_path),
                ('gmt_file_path', self.gmt_file_path),
                ('argument', robjects.ListVector(self.singscore_params)))
        
        # Singscore_data_collection returns four things 
        # 1. total_score_mat, 
        # 2. total_dispersion_mat, 
        # 3. rownames and 
        # 4. colnames
        total_score_mat, total_dispersion_mat, rownames, colnames = singscore_data_collection.rcall(args)
        
        # Converting into numpy arrays
        total_score_mat = np.array(total_score_mat)
        total_dispersion_mat = np.array(total_dispersion_mat)
        
        # Creating data frame for total_score
        total_score_df = pd.DataFrame(total_score_mat, columns=list(colnames))
        total_score_df['X'] = list(rownames)
        total_score_df.set_index('X', inplace=True)

        # Creating data frame for total_dispersion
        total_dispersion_df = pd.DataFrame(total_dispersion_mat, columns=list(colnames))

        # Creating a new column of row names
        total_dispersion_df['X'] = list(rownames)

        # Set the row names as index
        total_dispersion_df.set_index('X', inplace=True)

        return total_score_df, total_dispersion_df, self.singscore_params


    def gsvaScore(self, **args_list):
        """
        Args:
        method -> Method to employ in the estimation of gene-set enrichment scores per sample. 
            - gsva (Default)
            - ssgsea
            - zscore
            - plage
        abs_ranking -> Flag to determine whether genes should be ranked according to their sign 
            - True/False
        min_sz -> Minimum size of the resulting gene sets 
        max_sz -> Maximum size of the resulting gene sets
        parallel_sz -> Number of processors to use when doing the calculations in parallel
        max_diff -> Two approaches to calculate the enrichment statistic
            - mx_diff=True/False
        tau -> Exponent defining the weight of the tail in the random walk 
        ssgsea_norm -> Logical, set to True (default) with method="ssgsea" 
        verbose -> Gives information about each calculation step (Default: False)
        
        Return:
            gsva_es_df -> returns gene set enrichment scores data frame for each sample and gene set
            gsva_params -> Hyperparameters used for GSVA
        """
        
        print('\nComputing GSVA Scores')

        # Defining the R script and loading the instance in Python
        r = robjects.r
        r['source'](self.__gsva_r_code)

        # Creating the global environment and import the aucell_data_collection function from r script in globalenv.
        gsva_data_collection = robjects.globalenv['gsva_data_collection']
    
        as_null = robjects.r['as.null']
        
        # Change the default argument value when user give the arguments
        for key, value in args_list.items():
            # replacing the 'null' string with as_null() function
            if self.gsva_params[key] == 'as.null':
                self.gsva_params[key] = as_null()
            else:
                self.gsva_params[key] = value
        self.gsva_params['tau'] = robjects.ListVector(self.gsva_params['tau'])

        args = (('csv_file_path', self.csv_file_path),\
            ('gmt_file_path', self.gmt_file_path),\
            ('argument', robjects.ListVector(self.gsva_params)))

        # Gsva_data_collection returns four things 
        # 1. gsva_enrichment_score, 
        # 2. rownames and 
        # 3. colnames
        gsva_es_mat = gsva_data_collection.rcall(args)

        # Extracting gsva_enrichment_score and converting into numpy array
        gsva_enrichment_score = np.array(gsva_es_mat[0])

        # Extracting row names
        rownames = gsva_es_mat[1]

        # Extracting column names
        colnames = gsva_es_mat[2]
        
        # Creating data frame for gsva_enrichment_score
        gsva_es_df = pd.DataFrame(gsva_enrichment_score, columns=list(colnames))

        # Creating a new column of row names
        gsva_es_df['X'] = list(rownames)

        # Set the row names as index
        gsva_es_df.set_index('X', inplace=True)

        return gsva_es_df, self.gsva_params

class FormatConverter:

    def __init__(self, infile, outfile):
        self.input_file_path = infile
        self.fasta_input_file_path = Params['HYPER_PARAMS_BED2VCF']['fasta_file']
        self.output_file_path = outfile
        self.bed_2_vcf_params = Params['HYPER_PARAMS_BED2VCF']

    __bed2vcf_r_code = './rcodes/bed2VCF.R'

    def convertBed2VCF(self, **args_list):
        print('\nConverting Bed File to VCF')

        # Defining the R script and loading the instance in Python
        r = robjects.r
        r['source'](self.__bed2vcf_r_code)
        bed_to_vcf_converter = robjects.globalenv['bed_to_vcf_converter']
        args = (('bed_file_path', self.input_file_path),\
            ('fasta', self.fasta_input_file_path),\
            ('vcf_file_path', self.output_file_path),\
            ('argument', robjects.ListVector(self.bed_2_vcf_params)))

        bed_to_vcf_converter.rcall(args)
        # All the interface to call R code from python here.
