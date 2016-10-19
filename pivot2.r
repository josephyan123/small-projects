#!/usr/bin/env Rscript
args = commandArgs(trailingOnly=TRUE)
# test if there is at least one argument: if not, return an error
if (length(args)==0) {
  stop("At least one argument must be supplied (input_file.csv).n", call.=FALSE)
} else if (length(args)==1) {
  # default values
  args[2] = "OCR"; args[3]="output_file.csv"; args[4] = "Time"; args[5] = "Group"
} else if (length(args)==2) {
  # default values
  args[3]="output_file.csv"; args[4] = "Time"; args[5] = "Group"
} else if (length(args)==3) {
  # default values
  args[4] = "Time"; args[5] = "Group"
}


input_file = args[1]
val = args[2]
output_file = args[3]
unique_row_index = args[4]
ununique_col_index = args[5]


sh1 = read.csv(input_file)
d = NULL
y = unique(sh1[unique_row_index])
for (i in 1:length(t(y))) {
    val1 = y[i,]
    sh2 = sh1[sh1[unique_row_index]==val1, c(ununique_col_index, val)]
    sh3 = t(sh2)
    colnames(sh3) = sh3[1,]
    sh3 = sh3[-1,]
    sh3[unique_row_index]=val1
    d = rbind(d, sh3)
}
rownames(d) = d[, ncol(d)]
d1 = d[, -ncol(d)]
write.csv(d1, file=output_file)

