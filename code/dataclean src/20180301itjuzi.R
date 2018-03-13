install.packages("openxlsx")
require(openxlsx)
itjz <- read.csv("InvestEvent_1.csv", stringsAsFactors = F)

# show all duplicated entries: 13990 out of 40088
#View(itjz[which(duplicated(itjz$company)),])

# step 0: ======================================================================
# processing financial history
itjz1 <- itjz[1,1:10]
itjz1[1,1:10] <- rep(0,10) # blank dataframe

for (i in 1:length(itjz[,1])) {
  fh <- gsub('"','',itjz[i,11])
  fh <- gsub("\\[","",fh)
  fh <- gsub("\\]","",fh)
  fh <- gsub("\\{","",fh)
  l <- strsplit(fh,"\\},") # string split into a list
  l <- l[[1]]  # successfully extract finan_hist into list
  
  if (length(l) == 0) next
  
  for (j in 1:length(l)) {
    newrow <- length(itjz1[,1])+1
    #copy company info
    itjz1[newrow,c(1,7:10)] <- itjz[i,c(1,7:10)]
    #round
    round <- gsub(".*round[:punct:]","",l[j])
    itjz1[newrow,2] <- gsub(",.*","",round)
    #time
    time<- gsub("time[:punct:]","",l[j])
    itjz1[newrow,6] <- gsub(",.*","",time)
    #money
    money <- gsub(".*money[:punct:]","",l[j])
    itjz1[newrow,3] <- gsub(",.*","",money)
    #investor
    itjz1[newrow,5] <- gsub(".*invests[:punct:]","",l[j])
    #itjz1[length(itjz1[,1])+1,1:10] <- itjz2[1,1:10] # new row
  }
  #进度条:每20行显示一次
  if (i %% 20 == 0) {print(paste0(i,"completed"))}
}
write.xlsx(itjz1,"itjz1.xlsx")

# step 1: ======================================================================
# first: remove duplicated in itjz1
loc <- which(duplicated(itjz1[,c(1:3,6)]) == F) #如果轮数，金额，以及时间均相同，可认为是完全重复的 
itjz2 <- itjz1[loc,]
itjz2 <- itjz2[-1,]

# combine itjz and itjz2
itjz3 <- rbind(itjz[,1:10], itjz2)
loc1 <- which(duplicated(itjz3[,c(1:3,6)]) == F)
itjz4 <- itjz3[loc1,]


# step 2: ======================================================================
# clean location variable, 水平有限，一行写不来，请多担待
geo <- gsub('"','',itjz4[,9]) 
geo <- gsub('\\[','',geo)
geo <- gsub('\\]','',geo)
itjz4[,12] <- sub(",.*","",geo) # state or province
itjz4[,13] <- sub(".*,","",geo) # city or area
write.xlsx(itjz4,"../../Desktop/201803_sorted_data.xlsx")

