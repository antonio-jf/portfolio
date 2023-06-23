library(tidyverse)
library(ggthemes)
library(lubridate)
library(viridis)
# Load data into memory
load("../static/tripdata.RData")
# How many samples are being taken from each month
SAMPLES <- 25000

# Select columns relevant for the analysis
data <- data %>%
  select(ride_id, rideable_type, started_at, ended_at, member_casual)

# Sample from warm months to descale data
warm_months <- c(3, 4, 5, 6, 7, 8)
WarmData <- tibble()

for(mnth in warm_months){
  y <- data %>% filter(month(started_at) == mnth)
  l <- length(y$ride_id)
  samples <- sample(c(1:l), SAMPLES)
  WarmData <- rbind(WarmData, y[samples,])
}

# Sample from cold months to descale
cold_months <- c(1, 2, 9, 10, 11, 12)
ColdData <- tibble()

for(mnth in cold_months){
  y <- data %>% filter(month(started_at) == mnth)
  l <- length(y$ride_id)
  samples <- sample(c(1:l), SAMPLES)
  ColdData <- rbind(ColdData, y[samples,])
}

# Unload data to save memory
rm(data)

# Get duration of individual trips during spring and summer
WarmDurations <- WarmData %>%
  # Add duration column
  mutate(duration = as.numeric(ended_at - started_at), start_m = month(started_at), start_y = year(started_at)) %>%
  select(rideable_type, member_casual, start_m, start_y, duration) %>%
  # Group results by user type, bike type, and the month at which the trip started
  group_by(start_m, start_y, rideable_type, member_casual) %>%
  mutate(full_date = lubridate::my(paste(start_m, start_y))) %>%
  mutate(duration = duration/600) %>%
  ungroup

# Plot durations as boxplots for visualization 
WarmDurations %>%
  ggplot(aes(factor(full_date), duration, fill = member_casual)) +
  geom_boxplot(position = "dodge2") +
  # Transform y axis for ease of visualization
  scale_y_continuous(trans="log2") +
  geom_hline(yintercept = 1, linetype = "dashed") +
  theme_classic() +
  scale_fill_manual(values=c("#999999", "#E69F00", "#56B4E9")) +
  ylab("Duration in minutes (log2 transformed)") +
  xlab("") + 
  labs(title="Trip durations by user type",
        subtitle="Data from Spring and Summer months, period 05/2022 - 04/2023") +
  guides(fill=guide_legend("User Type")) +
  # Rotate x axis' ticks
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

# Get duration of individual trips during spring and summer
ColdDurations <- ColdData %>%
  # Add duration column
  mutate(duration = as.numeric(ended_at - started_at), start_m = month(started_at), start_y = year(started_at)) %>%
  select(rideable_type, member_casual, start_m, start_y, duration) %>%
  # Group results by user type, bike type, and the month at which the trip started
  group_by(start_m, start_y, rideable_type, member_casual) %>%
  mutate(full_date = lubridate::my(paste(start_m, start_y))) %>%
  mutate(duration = duration/600) %>%
  ungroup

# Plot durations as boxplots for visualization
ColdDurations %>%
  ggplot(aes(factor(full_date), duration, fill = member_casual)) +
  geom_boxplot(position = "dodge2") +
  scale_y_continuous(trans="log2") +
  geom_hline(yintercept = 1, linetype = "dashed") +
  theme_classic() +
  scale_fill_manual(values=c("#AA77FF", "#56B4E9")) +
  ylab("Duration in minutes (log2 transformed)") +
  xlab("") + 
  labs(title="Trip durations by user type",
       subtitle="Data from Fall and Winter months, period 05/2022 - 04/2023") +
  guides(fill=guide_legend("User Type")) +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1))

# Clean variables
rm(list = ls())

# Load sampled data
load("../static/sampled_tripdata.RData")

# 
sampled_data %>%
  select(rideable_type, started_at, ended_at, member_casual) %>% 
  mutate(duration = as.numeric(ended_at - started_at)/600) %>%
  mutate(rideable_type = factor(rideable_type)) %>% 
  mutate(rideable_type = str_replace(rideable_type, "classic_bike", "Classic")) %>%
  mutate(rideable_type = str_replace(rideable_type, "docked_bike", "Docked")) %>%
  mutate(rideable_type = str_replace(rideable_type, "electric_bike", "Electric")) %>%
  ggplot(aes(duration, ..count.., fill=member_casual)) +
  geom_density(alpha = .5) +
  scale_x_continuous(trans = "log2", breaks=c(.5)) +
  facet_grid(.~rideable_type) +
  guides(fill=guide_legend("User Type")) +
  ylab("") +
  xlab("Duration in minutes (log2 transformed)")
  
  
rm(list = ls())
