library("heatmaply")

#miRNA_RPMadjLib <- read.delim("C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/studies/miRNA_RPMadjLib.txt", row.names=1, stringsAsFactors=FALSE)

args <- commandArgs(TRUE)
#load DE genes
#input_folder<- "/opt/liqDB/liqDB/gentelella/data_folder/queryData/JPCLAFL8UHJMRJLKEQSZ/queryOutput/de/Groups"
#input_folder<- "C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/queryData/JPCLAFL8UHJMRJLKEQSZ/queryOutput/de/Groups"
input_folder<- args[1]
print("hey")

DE_file <- paste(input_folder,"matrix_miRNA_RPMadjLib.txt", sep= "/")
DE_table <- read.delim(DE_file,  stringsAsFactors=FALSE, header = FALSE)

DE_table <- DE_table[order(-DE_table$FC),]
DE_table <- head(DE_table,20)
row_vector <- DE_table[,1]
gene_names<-unique(gsub("#.+", "", row_vector))

#load exp_mat
exp_file<- paste(gsub("\\/de\\/.+","",input_folder),"/miRNA_RPMadjLib_sort.txt", sep="")

exp_mat <- read.delim(exp_file, row.names=1, stringsAsFactors=FALSE)
exp_mat$sum <- NULL
x <- subset(exp_mat, rownames(exp_mat) %in% gene_names)
log_trans <- log(x+1)

print("you")

#heatmaply(head(log_trans,20), colors = RdYlGn,  file = "/home/eap/heatmaply_plot30.html")
heatmaply(head(log_trans,20), colors = c("Red", "Black", "Green"),
file = paste(input_folder,"heatmap_euclidean.html",sep ="/"), fontsize_col=8, column_text_angle=60, key.title="log(RPM+1)")








