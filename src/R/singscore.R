singscore_data_collection <- function(csv_file_path, gmt_file_path, argument) {
  # To setup the environment for singscore, use the following command after installing the singscore and  GSEABase pacakage.
  library(singscore,quietly = T)
  library(GSEABase,quietly = T)
  
  gene_expression_data <- read.csv(csv_file_path, row = 1)
  gene_expression_data <- as.matrix(gene_expression_data)

  # To score samples, the gene expression or Rna_expression dataset first 
  # needs to be ranked using the rankGenes() function which returns a rank matrix
  
  rank_data <- rankGenes(gene_expression_data)
  gene_data_set <-getGmt(gmt_file_path)
  
  # knownDirection = FALSE then not provide down-regulated genes.
  if(argument[['knownDirection']] == FALSE){
    score_df <- simpleScore(rank_data, upSet = gene_data_set[[1]],
                           subSamples= argument[['subSamples']],
                           centerScore= argument[['centerScore']],
                           dispersionFun= argument[['dispersionFun']],
                           knownDirection= argument[['knownDirection']])
  }
  # know Direction = TRUE then may provide down-regulated genes and may not.
  else{
    if(argument[['downSet']] != FALSE){
      score_df <- simpleScore(rank_data, upSet = gene_data_set[[1]],
                             downSet = argument[['downSet']],
                             subSamples= argument[['subSamples']],
                             centerScore= argument[['centerScore']],
                             dispersionFun= argument[['dispersionFun']],
                             knownDirection= argument[['knownDirection']])
    }
    else{
      score_df <- simpleScore(rank_data, upSet = gene_data_set[[1]],
                             subSamples= argument[['subSamples']],
                             centerScore= argument[['centerScore']],
                             dispersionFun= argument[['dispersionFun']],
                             knownDirection= argument[['knownDirection']])
    }
  }
  
  
  # creating an empty matrix for total score of order 2982 r and 91 c
  total_score_mat <- matrix( nrow = length(names(gene_data_set)), ncol = length(row.names(score_df)) )
  # setting up the row names and column name
  rownames(total_score_mat) <- names(gene_data_set)
  colnames(total_score_mat) <- row.names(score_df)
  # creating a empty list to store the total_score_mat and total_dispersion_mat
  df = list()

  for (i in 1:length(gene_data_set)){
    # knownDirection = FALSE then not provide down-regulated genes.
    if(argument[['knownDirection']] == FALSE){
      # Now for each pathway we are calculating simple score using rank_data and geneset and storing the values in df.
      df[[i]] <- simpleScore(rank_data, upSet = gene_data_set[[i]],
                             subSamples= argument[['subSamples']],
                             centerScore= argument[["centerScore"]],
                             dispersionFun= argument[["dispersionFun"]],
                             knownDirection= argument[["knownDirection"]])
    }
    # know Direction = TRUE then may provide down-regulated genes and may not.
    else{
      if(argument[['downSet']] != FALSE){
        df[[i]] <- simpleScore(rank_data, upSet = gene_data_set[[i]],
                               downSet = argument[['downSet']],
                               subSamples= argument[['subSamples']],
                               centerScore= argument[["centerScore"]],
                               dispersionFun= argument[["dispersionFun"]],
                               knownDirection= argument[["knownDirection"]])
      }
      else{
        df[[i]] <- simpleScore(rank_data, upSet = gene_data_set[[i]],
                               subSamples= argument[['subSamples']],
                               centerScore= argument[["centerScore"]],
                               dispersionFun= argument[["dispersionFun"]],
                               knownDirection= argument[["knownDirection"]])
      }
    }
    if(nrow(df[[i]])==0){
      print(gene_data_set[i])
    }
    else{
      total_score_mat[i,] <- df[[i]][,1]
    }
    
  }

  # creating an empty matrix for total dispersion of order 2982 r and 91 c
  total_dispersion_mat <- matrix( nrow = length(names(gene_data_set)), ncol = length(row.names(score_df)) )
  rownames(total_dispersion_mat) <- names(gene_data_set)
  colnames(total_dispersion_mat) <- row.names(score_df)
  
  for (i in 1:length(gene_data_set)){
    
    if(nrow(df[[i]])==0){
      print(gene_data_set[i])
          }
    else{
      total_dispersion_mat[i,] <- df[[i]][,2]
    }
    
  }
  
  result = list(total_score_mat, total_dispersion_mat, row.names(total_dispersion_mat), colnames(total_dispersion_mat))
  return(result)
}


