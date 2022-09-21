aucell_data_collection <- function(csv_file_path, gmt_file_path, argument) {
  # To setup the environment for AUCell, use the following command after installing the AUCell pacakage.
  library(AUCell,quietly = T)
  library(GSEABase,quietly = T)

  # For the inputs, the first one should be in matrix format.
  micro_array <- read.csv(csv_file_path, row = 1)
  micro_array <- as.matrix(micro_array)
  #reading the geneset data
  gene_dataset <-getGmt(gmt_file_path)

  # Builds the "rankings" for each cell: expression-based ranking for all the genes in each cell
  cells_rankings <- AUCell_buildRankings(micro_array, featureType = argument[['featureType']],
                                         plotStats = argument[['plotStats']],
                                         splitByBlocks = argument[['splitByBlocks']],
                                         BPPARAM = argument[['BPPARAM']],
                                         keepZeroesAsNA = argument[['keepZeroesAsNA']],
                                         verbose = argument[['verbose']],
                                         nCores = argument[['nCores']],
                                         mctype = argument[['mctype']])

  # The function AUCell_calcAUC calculates this score, and returns a matrix with an AUC score for each gene-set in each cell.
  cells_auc <- AUCell_calcAUC(gene_dataset, cells_rankings,
                              nCores = argument[['nCores_cal_auc']],
                              normAUC = argument[['normAUC']],
                              aucMaxRank = ceiling(argument[['aucMaxRank']] * nrow(cells_rankings)),
                              verbose = argument[['verbose_cal_auc']])

  # extracting the AUC score
  auc_data <- cells_auc@assays@data$AUC
  
  # it return three things 1. AUC score 2. row names and 3. column names
  result <- list(auc_data, row.names(cells_auc), colnames(cells_auc))
  return(result)

}
