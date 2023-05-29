## Creates spatial representation of most common bycicle docking sites in Chicago
## Data from Divvy Bikes, https://divvybikes.com/
## Data visualization technique adapted from https://rpubs.com/Dr_Gurpreet/spatial_data_visualisation_R

# Loading libraries
library(tidyverse); library(sf); library(sp)
library(RColorBrewer); library(raster); library(leaflet)
# Loading shape data
shp <- st_read("../static/shapefiles/shapefile_chicago_20230529/geo_export_7222b0ac-3863-42a7-8c7d-2cbd8122a6e4.shp")
# Loading image with divvy data
load("../static/tripdata.RData")
# Downscale data to get only stations and coordinates
data <- data %>% 
  dplyr::select(start_station_name, start_lat, start_lng)

# Get counts of how many trips have started at which station
trip_by_start_location <- data %>% 
  group_by(start_station_name) %>% 
  summarize(start_lat, start_lng, tot = n()) %>% 
  na.omit

# Get only first occurrences
trip_by_start_location <- trip_by_start_location[match(unique(trip_by_start_location$start_station_name), trip_by_start_location$start_station_name),]

# Convert data and adapt geometrically 
trip_by_start_location <- st_as_sf(trip_by_start_location, 
                                   coords = c("start_lng", "start_lat"), 
                                   crs = 4326)

# Custom color palette
custom_palette <- colorNumeric(wesanderson::wes_palette("Zissou1")[1:5], trip_by_start_location$tot, n = 5)
# Create base map for spatial data
basemap <- leaflet() %>% addProviderTiles("CartoDB.Positron")
basemap %>% addPolygons(data = shp,
                        color = "red",
                        fillOpacity = 0.1,
                        opacity = .3,
                        weight = 1,
                        popup = shp$name) %>% 
  addCircleMarkers(data = trip_by_start_location,
                   color = custom_palette(trip_by_start_location$tot),
                   radius = trip_by_start_location$tot/10000, 
                   fillOpacity = 1,
                   opacity = 1,
                   popup = trip_by_start_location$start_station_name)
# Viewer is used for visualization
# Fig saved as html

