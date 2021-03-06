library("heatmaply")

#miRNA_RPMadjLib <- read.delim("C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/studies/miRNA_RPMadjLib.txt", row.names=1, stringsAsFactors=FALSE)

args <- commandArgs(TRUE)
#load DE genes
#input_folder<- "/opt/liqDB/liqDB/gentelella/data_folder/queryData/JPCLAFL8UHJMRJLKEQSZ/queryOutput/de/Groups"
#input_folder<- "C:/Users/Ernesto/PycharmProjects/liqDB/gentelella/data_folder/queryData/JPCLAFL8UHJMRJLKEQSZ/queryOutput/de/Groups"
input_folder<- args[1]


DE_file <- paste(input_folder,"matrix_miRNA_RPMadjLib.txt", sep= "/")
DE_table <- read.delim(DE_file,  stringsAsFactors=FALSE, header = FALSE)
row_vector <- DE_table[,1]
gene_names<-unique(gsub("#.+", "", row_vector))

#load exp_mat
exp_file<- paste(input_folder,"matrix_sort_annot.txt", sep= "/")
#exp_file<- paste(gsub("\\/de\\/.+","",input_folder),"/miRNA_RPMadjLib.txt", sep="")
exp_mat <- read.delim(exp_file, row.names=1, stringsAsFactors=FALSE,  comment.char = "", header=TRUE)
exp_mat$sum<-NULL
x <- subset(exp_mat, rownames(exp_mat) %in% gene_names)
y<-sapply(x, as.character)
mm<-dim(x)
labels<-sapply(y,function(t) paste("RPM=",t,sep=""))
dim(labels)<-mm
log_trans <- log(x+1)
col_labs<-TRUE
if (dim(x)[2] > 50){
col_labs<-FALSE
}
Groups <-gsub(".+\\.", "", colnames(x))
side_col_df <- data.frame(Groups)


#heatmaply(head(log_trans,20), colors = RdYlGn,  file = "/home/eap/heatmaply_plot30.html")
heatmaply(head(log_trans,20), colors = c("Red", "Black", "Green"),
          file = paste(input_folder,"heatmap_euclidean.html",sep ="/"),
          fontsize_col=8, column_text_angle=60, key.title="log(RPM+1)", custom_hovertext = labels,
          col_side_colors = side_col_df ,showticklabels=c(TRUE,TRUE), hide_colorbar = FALSE)
          #col_side_colors = side_col_df ,showticklabels=c(col_labs,TRUE), hide_colorbar = FALSE)
          #ColSideColors = gsub(".+\\.", "", colnames(x)) )
          #\code{function(...) round(..., digits=3, )
          #label_format_fun



