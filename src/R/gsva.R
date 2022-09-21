gsva_data_collection <- function(csv_file_path, gmt_file_path, argument) {
  # To setup the environment for GSVA, use the following command after installing the GSVA pacakage.
  library(GSVA,quietly = T)
  library(GSEABase,quietly = T)
  # For the inputs, the first one should be in matrix format.
  micro_array <- read.csv(csv_file_path, row = 1)
  micro_array <- as.matrix(micro_array)

  #reading the geneset data
  gene_set = getGmt(gmt_file_path)
  
  #calculating gsva score for micro array data
  gsva_es_mat <- gsva(micro_array, gene_set, method = argument[['method']], kcdf = argument[['kcdf']],
                        abs.ranking = argument[['abs_ranking']], min.sz = argument[['min_sz']], max.sz = argument[['max_sz']],
                        parallel.sz = 1L, mx.diff = argument[['mx_diff']], 
                        tau = switch(argument[['tau']][['tau_method']], gsva = argument[['tau']][['gsva']], ssgsea = argument[['tau']][['ssgsea']], NA), 
                        ssgsea.norm = argument[['ssgsea_norm']],
                        verbose = argument[['verbose']])

  result <- list(gsva_es_mat, row.names(gsva_es_mat), colnames(gsva_es_mat))
  return(result)
  
}
