library(tidyverse)
library(gridExtra)
library(ggthemes)
library(gridExtra) # For stacking plots
load("../static/sampled_tripdata.RData")

# Select the top 30 destinations for bike trips
end_station_top_count <- sampled_data %>% 
  select(rideable_type, member_casual, end_station_id, end_station_name) %>% 
  group_by(end_station_id) %>% 
  summarize(n = n()) %>% 
  arrange(desc(n)) %>% 
  na.omit()
end_station_top_30 <- end_station_top_count[1:30,]

# Group the data by user type
end_station_count_by_member <- sampled_data %>% 
  select(rideable_type, member_casual, end_station_id, end_station_name) %>% 
  filter(end_station_id %in% end_station_top_30$end_station_id) %>% 
  group_by(end_station_id, member_casual) %>% 
  summarize(n = n())
  
# Empty vectors for the loop below
current = 1
stations <- c(1:30)
prop <- c(1:30)

# Iterates over the data and gets proportions of casual users for top destinations
for (i in seq(1,59,2)){
  prop[current] <- end_station_count_by_member[i,3]$n / 
    (end_station_count_by_member[i,3]$n + end_station_count_by_member[i+1,3]$n)
  stations[current] <- end_station_count_by_member[i,1]$end_station_id
  current = current + 1
}
# Joins tibbles, will be useful for plotting
proportions <- left_join(end_station_top_30, tibble(end_station_id = stations, prop), by="end_station_id")

# Plots amount of trips by user type in descendent order
trip_destination_plt <- end_station_count_by_member %>%
  left_join(end_station_top_30, by="end_station_id") %>%
  rename(n = n.y) %>% 
  arrange(desc(n)) %>% 
  ungroup() %>% 
  mutate(end_station_id = reorder(end_station_id, desc(n))) %>% 
  ggplot() +
  geom_point(aes(end_station_id, n.x, fill=member_casual), shape=21, size=3) +
  theme_fivethirtyeight() +
  theme(axis.text.x = element_text(angle = 90, vjust = 0.5, hjust=1)) # Rotates xticks

# Creates barplot of proportions for casual users vs members
proportions_plt <- proportions %>% 
  mutate(end_station_id = reorder(end_station_id, desc(n))) %>% 
  ggplot() +
  geom_bar(aes(end_station_id, prop), stat = "identity") +
  theme_fivethirtyeight(base_family = "sans") +
  theme(axis.ticks.x=element_blank(), axis.text.x = element_blank()) + # Removes xticks, since this plot will be on top 
  scale_y_continuous(limits = c(0,1), expand = c(0, 0)) + # Removes space between x-axis and plotted data
  labs(title="Popular trip destination comparison",
       subtitle="Proportion of casual users for the top 30 trip destinations (Above)\nAmount of trips by user type for the top 30 trip destinations (Below)")
  
grid.arrange(proportions_plt, trip_destination_plt) # Stacks both plots, with proportion plot on top
