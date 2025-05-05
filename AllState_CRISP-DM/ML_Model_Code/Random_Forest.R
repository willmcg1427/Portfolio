# Load in data
data <- read.csv("AllState_clean_data.csv")
set.seed(123)

# Grab only final purchase
data <- data[data$record_type == 1,]

# Select important fields
data <- data[,c(4,6,7,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27)]
data$car_value_number <- sapply(data$car_value_number, as.integer)
data$homeowner <- sapply(data$homeowner, as.factor)
data$married_couple <- sapply(data$married_couple, as.factor)
data$state <- sapply(data$state, as.factor)
data$C_previous <- sapply(data$C_previous, as.factor)

x <- c('A','B','C','D','E','F','G')
accuracyforest <- c()
library(randomForest)
library(dplyr)

for (i in x) {
  if (i == 'A') {
    data_new <- data[,1:14]
    data_new <- rename(data_new, y = A)
  }
  if (i == 'B') {
    data_new <- data[,c(1:13,15)]
    data_new <- rename(data_new, y = B)
  }
  if (i == 'C') {
    data_new <- data[,c(1:13,16)]
    data_new <- rename(data_new, y = C)
  }
  if (i == 'D') {
    data_new <- data[,c(1:13,17)]
    data_new <- rename(data_new, y = D)
  }
  if (i == 'E') {
    data_new <- data[,c(1:13,18)]
    data_new <- rename(data_new, y = E)
  }
  if (i == 'F') {
    data_new <- data[,c(1:13,19)]
    data_new <- rename(data_new, y = 'F')
  }
  if (i == 'G') {
    data_new <- data[,c(1:13,20)]
    data_new <- rename(data_new, y = G)
  }
  data_new$y <- sapply(data_new$y, as.factor)
  myForest <- randomForest(y ~ ., nodesize = 100, mtry = 3, ntree = 50, data = data_new)
  confusionforest <- myForest$confusion
  if (i == 'A' || i == 'D') {
    accuracyforest <- c(accuracyforest, sum(confusionforest[c(1,5,9)]) / sum(confusionforest[c(1,2,3,4,5,6,7,8,9)]))
  }
  if (i == 'B' || i == 'E') {
    accuracyforest <- c(accuracyforest, sum(confusionforest[c(1,4)]) / sum(confusionforest[1:4]))
  }
  if (i == 'C' || i == 'F' || i == 'G') {
    accuracyforest <- c(accuracyforest, sum(confusionforest[c(1,6,11,16)]) / sum(confusionforest[c(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16)]))
  }
}

