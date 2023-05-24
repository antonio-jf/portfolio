library(tidyverse)
library(lubridate)
library(ggthemes)

# Load data from R image
load("../static/tripdata.RData")

data %>% 
  select(member_casual, started_at, started_at) %>% 
  mutate(month = month(started_at), year = year(started_at)) %>%
  group_by(month, year, member_casual) %>% 
  summarize(count = n()) %>% 
  mutate(date = my(paste(month, year))) %>% 
  ggplot(aes(x=date, count/1000, fill = member_casual)) +
  geom_bar(stat = 'identity', position = position_dodge(), color = "black") +
  theme_fivethirtyeight() +
  labs(title = "Trip count by user type",
       subtitle = "From April May 1st 2022 to April 30th 2023, amounts in thousands.",
       caption = "Data from divvybikes.com") + 
  guides(fill=guide_legend("User Type"))


