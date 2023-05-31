library(tidyverse)
library(stringr)
library(viridis)
library(ggthemes)
# Load data into memory
load("../static/tripdata.RData")

# Select columns relevant for the analysis
data <- data %>%
  select(ride_id, rideable_type, started_at, start_station_name, member_casual)

# Plots bike usage by user type and bike type
data %>%
  group_by(rideable_type, member_casual) %>% 
  summarize(cnt = n()) %>%
  ungroup %>% 
  add_row(rideable_type = "docked_bike", member_casual = "member", cnt = 0) %>%
  mutate(rideable_type = str_replace(rideable_type, pattern = "classic_bike", "Classic")) %>% 
  mutate(rideable_type = str_replace(rideable_type, pattern = "docked_bike", "Docked")) %>% 
  mutate(rideable_type = str_replace(rideable_type, pattern = "electric_bike", "Electric")) %>% 
  ggplot(aes(x = rideable_type, y=cnt/1000, fill = member_casual)) + 
  geom_bar(stat = "identity", position = "dodge", color="black") +
  ylab("Amount of rides (in thousands)") +
  xlab("Bike type") +
  labs(title = "Amount of rides by bike and user type",
       subtitle = "From 05/2022 to 04/2023") +
  theme_fivethirtyeight() +
  scale_fill_viridis(discrete = TRUE, name = "User type", labels = c("Casual", "Member"))





