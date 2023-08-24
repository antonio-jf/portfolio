library(tidyverse)
library(readr)
library(lubridate)

# Load data into memory
pathmay <- "202205-divvy-tripdata.csv"
data_may <- read_csv(pathmay)
rm(pathmay)

pathjun <- "202206-divvy-tripdata.csv"
data_jun <- read_csv(pathjun)
rm(pathjun)

pathjul <- "202207-divvy-tripdata.csv"
data_jul <- read_csv(pathjul)
rm(pathjul)

pathaug <- "202208-divvy-tripdata.csv"
data_aug <- read_csv(pathaug)
rm(pathaug)

pathsep <- "202209-divvy-publictripdata.csv"
data_sep <- read_csv(pathsep)
rm(pathsep)

pathoct <- "202210-divvy-tripdata.csv"
data_oct <- read_csv(pathoct)
rm(pathoct)

pathnov <- "202211-divvy-tripdata.csv"
data_nov <- read_csv(pathnov)
rm(pathnov)

pathdec <- "202212-divvy-tripdata.csv"
data_dec <- read_csv(pathdec)
rm(pathdec)

pathjan <- "202301-divvy-tripdata.csv"
data_jan <- read_csv(pathjan)
rm(pathjan)

pathfeb <- "202302-divvy-tripdata.csv"
data_feb <- read_csv(pathfeb)
rm(pathfeb)

pathmar <- "202303-divvy-tripdata.csv"
data_mar <- read_csv(pathmar)
rm(pathmar)

pathapr <- "202304-divvy-tripdata.csv"
data_apr <- read_csv(pathapr)
rm(pathapr)

data <- rbind(data_may, data_jun, data_jul, data_aug, data_sep, data_oct, data_nov, data_dec, data_jan, data_feb, data_mar, data_apr)
rm(list = c(data_may, data_jun, data_jul, data_aug, data_sep, data_oct, 
            data_nov, data_dec, data_jan, data_feb, data_mar, data_apr))

save.image("../../static/tripdata.RData")

SAMPLES <- 25000
months <- c(1:12)
sampled_data <- tibble()

for(mnth in months){
  y <- data %>% 
    filter(month(started_at) == mnth)
  l <- length(y$ride_id)
  samples <- sample(c(1:l), SAMPLES)
  sampled_data <- rbind(sampled_data, y[samples,])
}

# Clear all variables and save image
rm(data)
save.image("../../static/sampled_tripdata.RData")
rm(sampled_data)
rm(list = ls())


