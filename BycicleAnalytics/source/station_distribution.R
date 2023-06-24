library(tidyverse)
library(gridExtra)
library(ggthemes)
load("../static/sampled_tripdata.RData")

# Select only relevant data
aggregated <- sampled_data %>% 
  select(end_station_name, member_casual) %>%
  group_by(end_station_name, member_casual) %>%
  summarize(n = n()) %>% 
  ungroup() %>% 
  na.omit()

rm(sampled_data)

# Use for selecting top 15 for casual
aggregated_casual <- aggregated %>% 
  filter(member_casual == "casual") %>% 
  arrange(desc(n)) %>% 
  top_n(15)
# Use for selecting top 15 for member
aggregated_member <- aggregated %>% 
  filter(member_casual == "member") %>% 
  arrange(desc(n)) %>% 
  top_n(15)

# Merge again for 
rm(aggregated)

# Create lollipop plot for member trip count
member_plot <- aggregated_member %>% 
  #filter(member_casual == "member") %>%  
  mutate(end_station_name = reorder(end_station_name, n)) %>% 
  ggplot(aes(end_station_name, n)) + 
  geom_segment(aes(x=end_station_name, xend=end_station_name, y=0, yend=n)) +
  geom_point(size=2.5, color="#186e37") +
  ylim(0, 5000) +
  # Invert axis
  coord_flip() +
  theme_fivethirtyeight() +
  xlab("") +
  ylab("") +
  theme(
    panel.grid.major.y = element_blank(),
    panel.border = element_blank()
  ) +
  # Since this plot will go on top we'll add the plot title and subtitle here
  labs(title="Trip count comparison between popular destinations",
       subtitle="Member (top) vs Casual (bottom)") +
  theme(plot.title = element_text(hjust = 1, family = "Helvetica"),
        plot.subtitle = element_text(hjust=1))

# Create lollipop plot for casual trip count 
casual_plot <- aggregated_casual %>% 
  #filter(member_casual == "casual") %>%
  # Long names affect presentation
  mutate(end_station_name = str_replace(end_station_name, pattern = "DuSable Lake Shore", "DuSab LkSh.")) %>% 
  mutate(end_station_name = reorder(end_station_name, n)) %>% 
  ggplot(aes(end_station_name, n)) + 
  geom_segment(aes(x=end_station_name, xend=end_station_name, y=0, yend=n)) +
  geom_point(size=2.5, color="#186e37") +
  ylim(0,5000) +
  # Invert axis
  coord_flip() +
  theme_fivethirtyeight() +
  xlab("") +
  ylab("") +
  theme(
    panel.grid.major.y = element_blank(),
    panel.border = element_blank()
  ) +
  # Since this plot will go on the bottom we'll add the plot caption here
  labs(caption="Results from sampled data from Divvy Bikes")

# Creates a grid for both plots
grid.arrange(member_plot, casual_plot, nrow=2)
rm(list = ls())


