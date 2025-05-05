# Load in data and set seed
data <- read.csv("Phish_Training_Dataset.csv")
set.seed(123)
library(randomForest)

col_names <- names(data)
data[,col_names] <- lapply(data[,col_names] , factor)

# neg_cor <- c("Favicon",'Iframe','Redirect',
# 'double_slash_redirecting','Abnormal_URL','Shortining_Service',
# 'Domain_registeration_length')
# data[,neg_cor] <- NULL

myForest <- randomForest(Result ~ ., mtry = 10, ntree = 100, data = data)

confusionforest <- myForest$confusion
accuracyforest <- sum(confusionforest[c(1,4)]) / sum(confusionforest[1:4])
f1forest <- confusionforest[1] / 
  (confusionforest[1] + (1/2)*(confusionforest[2]+confusionforest[3]))

confusionforest
accuracyforest
f1forest

varImpPlot(myForest, n.var = min(15,nrow(myForest$importance)))





