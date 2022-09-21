bed_to_vcf_converter <- function(bed_file_path, vcf_file_path, argument) {
  
  library(bedr)
  x <- read.table(bed_file_path,sep = "")
  bed2vcf(x, vcf_file_path, zero.based = TRUE, header = NULL, fasta = NULL)

}
