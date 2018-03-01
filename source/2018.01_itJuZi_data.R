require(openxlsx)
itjz <- read.xlsx("../../Desktop/work/2018.01_L_project/vc_info_20171215.xlsx")

# show all duplicated entries
#View(itjz[which(duplicated(itjz$company)),])

# step 0: ======================================================================
# get a brief view of the data
round_label <- levels(factor(itjz$round)) # vector of all 20 rounds labels

require(stringr)
# find observations with max num of investor
which(str_count(itjz$invests,",") == max(str_count(itjz$invests,","))) #mobike & SenseTime, 15 investor in one round

# step 1: ======================================================================
# create a company list with duplicated entries removed
itjz1 <- itjz[which(!duplicated(itjz$company)),]
itjz2 <- itjz1[,c(1,7:8)] # keep company info only
# clean location variable, 水平有限，一行写不来，请多担待
loc <- gsub('"','',itjz1[,9]) 
loc <- gsub('\\[','',loc)
loc <- gsub('\\]','',loc)
itjz2[,4] <- sub(",.*","",loc) # state or province
itjz2[,5] <- sub(".*,","",loc) # city or area
itjz2[,6] <- itjz1[,10] # company descriptions

# add 20 round labels as variables, each with time money investor and percentage
for (i in 7:86) {itjz2[,i] <- "NA"}
name <- read.xlsx("../../Desktop/variable_name.xlsx", colNames = F)
colnames(itjz2) <- name[,1]
itjz3 <- itjz2

# step 2: ======================================================================
# add info for each round to companies
# reorder round labels,之前排序干的傻事，现在又得修...
new_roundLabels <- 1:20
new_roundLabels[c(2,1,4,3,6,5,8,7,9:14,17,15,18,19,20,16)] <- round_label[c(1:20)]

# convert existing info, except financial history, into new table
for (i in 1:length(itjz$company)) {
  m <- which(itjz2[,1] == itjz[i,1]) # which company
  n <- which(new_roundLabels == itjz[i,2]) # which round
  itjz2[m,((n-1)*4+7):((n-1)*4+10)] <- itjz[i,c(6,3:5)]
  if (i %% 20 == 0) {print(paste0(i,"completed"))}
}

# step 3: ======================================================================
# processing financial history
for (i in 1:length(itjz$company)) {
  fh <- gsub('"','',itjz$finan_history[i])
  fh <- gsub("\\[","",fh)
  fh <- gsub("\\]","",fh)
  fh <- gsub("\\{","",fh)
  l <- strsplit(fh,"\\},") # string split into a list
  l <- l[[1]]
  m <- which(itjz3[,1] == itjz[i,1]) # which company
  # successfully extract finan_hist into list
  for (j in 1:length(l)) {
    #round
    round1 <- gsub(".*round[:punct:]","",l[1])
    round2 <- gsub(",.*","",round1)
    #time
    time1 <- gsub("time[:punct:]","",l[1])
    time2 <- gsub(",.*","",time1)
    #money
    money1 <- gsub(".*money[:punct:]","",l[1])
    money2 <- gsub(",.*","",money1)
    #investor
    invest2 <- gsub(".*invests[:punct:]","",l[1])
    n <- which(new_roundLabels == round2) # which round
    # if(itjz3[m,(n-1)*4+7] != "NA") {print(paste0("error at ",m," & ",n))} # warning if there are repeated information on same round
    itjz3[m,c((n-1)*4+7,(n-1)*4+8,(n-1)*4+10)] <- c(time2,money2,invest2)
  }
  if (i %% 20 == 0) {print(paste0(i,"completed"))}
}

# step 3: ======================================================================
# merge itjz2 and itjz3 and return repeated locations
for (i in 1:length(itjz2$company)) {
  q <- which(itjz2[i,7:86] != "NA")
  w <- which(itjz3[i,7:86] != "NA")
  e <- w[which(!(w %in% q))] # e is the location of itjz3 which not found in itjz2
  if (length(e) != 0) {itjz2[i,e+6] <- itjz3[i,e+6]} # +6 because it starts at 7
}

write.xlsx(itjz2,"../../Desktop/sorted_data.xlsx")