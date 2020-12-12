# TimeGiver
 TimeGiver is an open-source, highly-customizable circadian lighting rhythm generator that empowers connected lighting systems to support a healthy cycle of sleep and wakefulness.  It takes arguments such as wake time and sunset length and returns an appropriate set of lighting parameters such as brightness and color temperature for the current moment.  Rhythms can be generated based on just a few parameters using appropriate defaults or customized extensively according to desired maximums, minimums, rates of change, and slope shapes.  TimeGiver also includes a sunlight simulator that mimics the natural blue-yellow color gradient of sunlight, producing a unique combination of colors for every time of day that recreates everything from the crisp blue noontime to the golden hues of late afternoon and mellow blues of dusk, all without compromising color rendering.  The project includes both python and javascript implementations, allowing TimeGiver to serve as part of the back-end of almost any connected lighting project.

## Illustrations
This gif shows a very simple light rhythm generated on the fly using TimeGiver applied to real smart lights from sunrise to sunset, and the graphs below show the brightness and color temperature over time according to that schedule.

![Animation of a simple daily rhythm created with TimeGiver](/images/illustrations/TimeGiverDemo20sec.gif)
![Graph showing brightness over the course of the day used in the schedule from the gif above](/images/illustrations/TimeGiverDemoBrightness.png)
![Graph showing color temperature over the course of the day used in the schedule from the gif above](/images/illustrations/TimeGiverDemoCCT.png)

This next gif shows a pair of light strips running a rhythm created using TimeGiver's sunlight simulator feature that produces a blue-yellow color gradient that mimics the changes in sunlight over the course of a sunny day.  The two colors always combine to form a perfect white, guaranteeing good color rendering all day long.  Note that the flashing and lines are visual artifacts created by the camera.
![Animation of a simple daily rhythm created with TimeGiver](/images/illustrations/KitchenTimeGiverDemo.gif)


## Attributions
TimeGiver is based on the research and development work of Timothy Lee, a 3rd-year medical student at Mayo Clinic Alix School of Medicine with strong interests in circadian rhythm disorders and the importance of regular, restorative sleep to good mental health.  Questions and comments can be directed to Timothy Lee, @timotheonpaulonlee on Github or linkedin.com/in/timothy-paul-lee/.