# The main objective of this analysis is to create a Generalized Linear Model 
# based on a logistic regression model in order to classify, based on a series 
# of predictors, which direction is the market going on a given day.

# The data used for this analysis as well as the methodology can be found in
# James G., Witten D., Hastie T. & Tibshirani R. (2021)  An Introduction to 
# Statistical Learning with Applications in R. Springer. Second Edition. 
# ISBN: 978-1-0716-1420-4 

library(ISLR2)

# Load data used for the analysis
data("Smarket")
attach(Smarket)

# Get a correlation matrix for the data, except the last column
cor(Smarket[,-9])

# First attempt at a logistic regression model
# Fit a model with lag variables and the volume
glm.fit <- glm(Direction ~ Lag1 + Lag2 + Lag3 + Lag4 + Lag5 + Volume, 
               data = Smarket, 
               family = "binomial") # Prediction can only take on two values
# Inspect the p-values for the model
summary(glm.fit)
# No p-values statistically significant for this particular model 

# Measure the overall training accuracy
glm.probs <- predict(glm.fit, type = 'response') # 'response' to get the actual calculated values

glm.pred <- rep('Down', length(Smarket[,1])) # Create vector of size [1250,] with all values 'Down'
glm.pred[glm.probs > .5] <- 'Up' # Substitute all values where 'Up' was predicted
rm(glm.probs)
# To find out which value is assigned for the ranges [0, 0.5) and (0.5, 1] 
# the contrasts() function was employed on the 'Direction' predictor

# Get training accuracy
mean(glm.pred == Direction) # Around 52.16%, marginally better than guessing

# Create training and test vectors to use for bootstrap
l <- length(Smarket[,1])
training = 1:(l - l/5)
testing = (l - l/5 + 1):l
# Training on 4/5 of the data
training.set <- Smarket[training,]
# Test on 1/5 of the data
testing.set <- Smarket[testing,]; rm(l)

# Train a new model with training set
glm.fit <- glm(
  Direction ~ Volume + Lag1 + Lag2,
  data = training.set,
  family = "binomial"
)
summary(glm.fit)

# Measure the overall training accuracy
glm.probs <- predict(glm.fit, testing.set, type = 'response') # 'response' to get the actual calculated values

glm.pred <- rep('Down', length(testing))
glm.pred[glm.probs > .5] <- 'Up' # Substitute all values where 'Up' was predicted
rm(glm.probs)

# Get test accuracy
mean(glm.pred == Direction[1:length(testing)]) # Around 51.2%, marginally worse than the previous






