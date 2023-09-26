### 1. How do annual members and casual riders use Cyclistic bikes differently?

You can take a look at a simple Public Tableau dashboard I created for this case study [here.](https://public.tableau.com/shared/79CRF8BM5?:display_count=n&:origin=viz_share_link)

#### Intuition prior to querying

Before writing any code, one can notice that the first question being asked requires us to carry out descriptive statistics, which can be accompanied by visualizations to make inferences clearer.

#### Important distinctions

As the question states, one of the main takeaways one should aim to get from the data is to understand how bike usage behavior diverts when comparing casual users with members.

A first approach to this is visualizing just how trip counts differ between both types of users. The following graph allows us to see that over the last year, members had more trips every single month than casual users.

![Trip count plot.](figs/plots/trip_count.png)

The gap between trip counts every month seems to be shorter during warm months, *i.e.* spring and winter months, with the spread between trips in July 2022 being as close as around 1%. The graph also allows us to see a very clear stationary pattern in the data; the combined trip count shows an increasing trend from january through july and then decreases back down from august onward.

This is consistent with trip duration over the same period, we see from the following two plots how durations change during winter and autumn. Notice the dashed line across the plot, representing a duration of 1 minute for reference.

![Trip count plot.](figs/plots/bike_trip_durations_warm.png)

![Trip count plot.](figs/plots/bike_trip_durations_cold.png)

This is obvious considering that bikes are not very popular to use during cold months in contrast with warmer ones.

The plots also let us see something worth noting: **casual users tend to have longer trips than members** regardless of the time of the year and the biggest outliers come from casual users as well.

A density plot─shown below─of the duration by bike type also lets us see that casual users have a bigger proportion of long trips than members.

![Trip count density plot](figs/plots/bycicle_duration_density.png)

Also remarkable is the fact that, as could be deducted from the plot, members have no trips involving docked-type bikes; a different perspective lets us appreciate this fact more clearly.

![Bike usage by bike type](figs/plots/bike_usage.png)

Note that so far these plots allow us to see that in general members have more trips regardless of the time of the year and the type of bike ─ aside from the docked-type. A quick query shows that the actual proportion for casual users is 40.25%.

#### How much do popular stations matter for casual users in contrast to members?

For this section a final approach to understanding how user behavior differs regarding stations with a high-traffic volume will be analyzed. In concrete, we want to see just how much the top trip destinations─in this case the top 10─for each group affect the group's trip distribution.

A few considerations prior to coding are the following:

1.  End station data will be taken into account for the analysis.

2.  A proportion will be taken into account due to, as mentioned before, members have more trips than casual users so it makes sense to not use just the count.

3.  For the rest of this first section a sampled data set will be used for convenience.

The following is a simple spatial plot of the trip count by station, using the whole data set.

![Spatial bike trip distribution](figs/plots/dock_traffic_count.png)

##### Analizing popular trip destination

In this last section a couple of insights will be reviewed, namely *proportion of casual users in popular destinations* as well as *overall trip count for popular destinations*, both of these will further improve our perspective on both groups.

As shown previously, there is an expectation for stations in the downtown area to be the most visited, so names for popular stations will also be shown in order to inform the *hypothetical* marketing team of potentially strategic zones.

The plot down below allows us to see a couple of the insights we're looking for in this section. For starters, when it comes to overall trip count there is a clear outlier for one of the stations and it happens to be also the most visited station in the dataset. Further analysis reveals that the station with the outlier is located near a very turistically significant spot of the city, namely the *Navy Pier*.

![Popular trip destinations insights](figs/plots/popular_destinations.png)

#### Final remarks

This section allowed us to see some key insights that either provided or reinforced some of the intuition on user group behavior that we could have gotten from this dataset. Having visualizations also made clear some statistics or patterns that would've been hard to grasp at first by only looking at static data. From this section we can conclude the following:

-   Casual users have, on average, trips with a higher duration than members.

-   Members have a bigger proportion of trip year round, regardless of the season.

-   Members do not use docked bikes.

-   Members are almost split down the middle when it comes to using classic or electric bikes.

-   Casual users, as expected, commonly use the service to go to touristic spots.
