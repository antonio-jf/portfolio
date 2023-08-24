# The main objective of this analysis is to create a Generalized Linear Model 
# based on a linear discriminant analysis in order to classify, based on a series 
# of predictors, which direction is the market going on a given day.

# The data used for this analysis as well as the methodology can be found in
# James G., Witten D., Hastie T. & Tibshirani R. (2021)  An Introduction to 
# Statistical Learning with Applications in R. Springer. Second Edition. 
# ISBN: 978-1-0716-1420-4 

library(ISLR2)
library(MASS)

# Load data used for the analysis
data("Smarket")
attach(Smarket)

l <- length(Smarket[,1])
training = 1:(l - l/5)
testing = (l - l/5 + 1):l

# Train on 4/5 of the data
training.set <- Smarket[training,]
# Test on 1/5 of the data
testing.set <- Smarket[testing,]; rm(l)

# Train a Linear Discriminant Analysis using MASS library's lda()
lda.fit <- lda(
  Direction ~ Lag1 + Lag2,
  training.set
)

# Coefficients
lda.fit$scaling

# Test the accuracy of a linear approach
lda.pred <- predict(lda.fit, testing.set)
table(lda.pred$class, testing.set$Direction)
mean(lda.pred$class == testing.set$Direction) # 57.6% overall accuracy

