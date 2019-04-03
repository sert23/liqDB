BiocManager::install('seandavi/SRAdbV2')
library(SRAdbV2)
oidx = Omicidx$new()
query=paste(
  '(study.abstract:miRNAs OR study.abstract:miRNA OR study.abstract:microRNA OR study.abstract:microRNAs )',
  #'AND study.abstract:sequencing',
  'AND (study.abstract:human OR study.abstract:patient OR study.abstract:patients )',
  'AND (study.abstract:blood OR study.abstract:serum OR study.abstract:plasma OR study.abstract:saliva OR study.abstract:cerebrospinal OR study.abstract:urine OR study.abstract:milk OR study.abstract:seminal fluid OR study.abstract:bile)'
  #'AND (study.abstract:blood)'
  #'AND abstract:"blood"'
  )

#query='study.abstract:miRNAs'
z = oidx$search(q=query,entity='full',size=100L)
s = z$scroll()
s$count
res = s$collate(limit = 6000)

# SRPs<-res$study.study_accession
# articles<-unlist(res$study.xrefs)
# abstracts<-res$study.abstract

#Keep only human data
res<-subset(res,res$sample.organism == "Homo sapiens")
nsample<- table(factor(res$study.study_accession, levels=unique(res$study.study_accession)))
info<-res[c("study.study_accession","study.abstract","study.xrefs", "study.title","study.Received")]
initial_pub<-sapply(info$study.xrefs, function(x) if (class(x[["id"]]) == "character" ){return(unlist( x[["id"]],use.names=FALSE, recursive = TRUE )) }  else{ return(NA)} )

avector=c()
x=0
for(i in info$study.xrefs){
  x=x+1
  print(x)
  avector = c(avector,i[["id"]])
  print(i[["id"]][1])}

x<-as.vector(sapply(info$study.xrefs, function(x) as.vector(unlist(x[["id"]][1], use.names=FALSE, recursive = TRUE))))

info$pubmed<-unlist(sapply(info$study.xrefs, function(x) if (class(x[["id"]]) == "character" ){return(unlist( x[["id"]][1],use.names=FALSE, recursive = TRUE )) }  else{ return(NA)} ))

class(info$pubmed)
avector <- as.vector(info['pubmed'])
class(avector) 

info$pubmed<-as.vector(info$pubmed)
un_info<- info[!duplicated(info), ]
un_info$nsample<-nsample
un_info$study.xrefs<-NULL

ord_info<-un_info[order(-un_info$nsample),]

#write study info to file

write.table(ord_info,"liqdb_data.tsv" ,row.names = FALSE, col.names = TRUE, sep="\t")

template_link<-"http://trace.ncbi.nlm.nih.gov/Traces/sra/sra.cgi?save=efetch&db=sra&rettype=runinfo&term="

