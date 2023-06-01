# Welcome to Bycicle analytics! :bike:
This is a project based on a case study from Google's Data Analytics Professional Certificate. It consists of analyzing monthly data from a company called Cyclistic, based on a real company called *Divvy*.

## Sections to this case study
1. Introduction
   - Context
   - How the data is being processed
   - Questions to be answered 
2. Getting to know the data
   - How is the data structured
   - Intuition behind querying for insights
   - Descriptive statistics
   

# Introduction
## Context
Cyclistic is a business that offers bike-sharing subscriptions to people in Chicago. The bikes can be unlocked from one station and
returned to any other station in the system anytime. Moreover, the company offers different types of membership alternatives that accomodate to users' preferences and needs, users that use single-trip and daily passes are referred to as 'casual' users, on the other hand, those who get annual memberships are referred to as 'members'. 

As you can already imagine, gathering usage data from this service is very important for the company and it's critical analysis plays a key role in decision-making and marketing.

According to finance analysts at Cyclistic, members are more profitable than casuals so the main goal of this case study is to analyze the way both of this consumer types behave in order to come up with useful insights that may help converting casual into members.

## How the data is being processed?
The language I'm using for this analysis is mostly `R`, and due to the nature of the language itself I've decided not to use a `SQL` database for querying over data and just do it all in plain `R`. 
The data used for this project has been downloaded directly from [Divvy's website](https://divvybikes.com/system-data) and hasn't been included in the files corresponding to this project due to storage constraints[^1]. However, any code used to load it, wrangle it, and overall manipulate it will be available in this repo.

## Questions to be answered 
1. How do annual members and casual riders use Cyclistic bikes differently?
2. Why would casual riders buy Cyclistic annual memberships?
3. How can Cyclistic use digital media to influence casual riders to become members?

# Getting to know the data
## How is the data structured?
| Column name | Description | Possible values |
| -- | -- | -- |
| `ride_id` | Contains a unique id for every ride in the database | Unique string |
| `rideable_type` | Contains the type of bike utilized for a trip | `classic_type`, `docked_bike`, `electric_bike` |
| `started_at`, `ended_at` | Contains the date at which the trip started and ended, respectively | Date type in ISO format |
| `start_station_name` | Contains the name of the station where the trip started | String representing the name |
| `start_station_id` | ID of the trip's starting station | Unique string for every station of variable size |
| `end_station_name` | Contains the name of the station where the trip ended | String representing the name |
| `end_station_id` | ID of the trip's ending station | Unique string for every station of variable size |
| `start_lat` | Latitude coordinate from the station at which the trip started | Coordinates in CRS |
| `start_lng` | Longitude coordinate from the station at which the trip started | Coordinates in CRS |
| `end_lat` | Latitude coordinate from the station at which the trip ended | Coordinates in CRS |
| `end_lng` | Longitude coordinate from the station at which the trip ended | Coordinates in CRS |
| `member_casual` | Type of member that took the trip|`casual`,`member`|

## Question solving
### 1. How do annual members and casual riders use Cyclistic bikes differently?
#### Intuition prior to querying
Before writing any code, one can notice that the first question being asked requires us to carry out descriptive statistics, which can be accompanied by visualizations to make inferences clearer.

#### Important distinctions
As the question states, one of the main takeaways one should aim to get from the data is the seggregation of the two types of users.


## Descriptive Statistics

[^1]: Although you shouldn't have any problems trying to reproduce the results achieved in this project, any critique and comment will be adressed as soon as possible to keep everything consistent.
