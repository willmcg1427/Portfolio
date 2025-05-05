# Load in data
data <- read.csv("AllState_clean_data.csv")
set.seed(123)
library(dplyr)

# Grab only final purchase
data <- data[data$record_type == 1,]

# Select important fields
data <- data[,c(4,6,7,9,10,11,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27)]
data$car_value_number <- sapply(data$car_value_number, as.integer)
data$homeowner <- sapply(data$homeowner, as.factor)
data$married_couple <- sapply(data$married_couple, as.factor)
data$state <- sapply(data$state, as.factor)
data$C_previous <- sapply(data$C_previous, as.factor)


data[1:13] <- data[1:13] %>%
                  mutate_if(is.numeric, scale)

x <- c('B','E')
accuracylr <- c()

for (i in x) {
  if (i == 'B') {
    data_new <- data[,c(1:13,15)]
    data_new <- rename(data_new, y = B)
  }
  if (i == 'E') {
    data_new <- data[,c(1:13,18)]
    data_new <- rename(data_new, y = E)
  }
  data_new$y <- factor(data_new$y, levels = c("0","1"))
  # Partitioning are data, training and testing sets
  library(caret)
  partition <- createDataPartition(data_new$y, p = 0.7, list = FALSE)
  train <- data_new[partition,]
  test <- data_new[-partition,]
  # Logistic model
  m1 <- glm(y ~ ., family = binomial(link = "cauchit"), data = train)
  # Test 
  fitted.results <- predict(m1, test, type = 'response')
  fitted.results <- ifelse(fitted.results > 0.5, '1','0')
  accuracylr <- c(accuracylr, confusionMatrix(as.factor(fitted.results), as.factor(test$y))$overall[[1]])
}

