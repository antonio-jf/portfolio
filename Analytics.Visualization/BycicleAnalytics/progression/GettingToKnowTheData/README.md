# Getting to know the data :card_file_box:

## How is the data structured?

| Column name              | Description                                                         | Possible values                                  |
|------------------------|------------------------|------------------------|
| `ride_id`                | Contains a unique id for every ride in the database                 | Unique string                                    |
| `rideable_type`          | Contains the type of bike utilized for a trip                       | `classic_type`, `docked_bike`, `electric_bike`   |
| `started_at`, `ended_at` | Contains the date at which the trip started and ended, respectively | Date type in ISO format                          |
| `start_station_name`     | Contains the name of the station where the trip started             | String representing the name                     |
| `start_station_id`       | ID of the trip's starting station                                   | Unique string for every station of variable size |
| `end_station_name`       | Contains the name of the station where the trip ended               | String representing the name                     |
| `end_station_id`         | ID of the trip's ending station                                     | Unique string for every station of variable size |
| `start_lat`              | Latitude coordinate from the station at which the trip started      | Coordinates in CRS                               |
| `start_lng`              | Longitude coordinate from the station at which the trip started     | Coordinates in CRS                               |
| `end_lat`                | Latitude coordinate from the station at which the trip ended        | Coordinates in CRS                               |
| `end_lng`                | Longitude coordinate from the station at which the trip ended       | Coordinates in CRS                               |
| `member_casual`          | Type of member that took the trip                                   | `casual`,`member`                                |

The raw data set contains more than 5.8 millions observations for trips from both members and casual users. Some of the basic visualizations contained in the first question do consider the full data set since it gives some useful insights. However, utilizing the full data set for the whole analysis is considered to be not optimal due to the demanding computational power required to process and plot the data; to address this and to 'descale' the data, 30,000 samples have been taken from the data set corresponding to every month for the period considered, and to prevent any concerns for the data not being representative, said samples have been taken at random.