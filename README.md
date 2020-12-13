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

# Documentation
TimeGiver is an open-source, highly-customizable circadian lighting schedule generator with implementations in python and javascript built to serve as part of the backend for connected lighting systems.  The core of the system is the function TimeGiver() that takes arguments that describe a lighting rhythm and returns appropriate lighting parameters for the current or specified time under that rhythm.  The code has significant in-line documentation, so this text will focus on a conceptual understanding of the different arguments and return parameters.

## Arguments
TimeGiver accepts over 40 different arguments that describe different aspects of how a rhythm is generated, allowing for extensive customization.  However, changes in most of the arguments have a minor effect on the final rhythm and all of them come with default values that should be acceptable for most users.  As a result, the number of arguments you will want to expose as settings depends on your user base and how they value customizability versus simplicity.  There are several core arguments such as wake time and bed time that should be exposed as settings in nearly all applications, and I have listed them at the top and bolded them.  The arguments are the same across both implementations, though the syntax for passing them is different.  Some of the arguments serve for any use of TimeGiver and others only need to be worried about when using the sunlight simulator feature.  The arguments can also be divided into several different types: those that set key times, those that describe maximums and minimums that fence the rhythms in, those that describes lengths of change, and those that describe slopes of change.  The arguments will be grouped according to whether they are general-purpose or specific to the sunrise simulator and then according to their general category as above.

### General-Purpose Arguments for Key Times

#### Time
time is a simulated time variable that overrides real current time if it is set to greater than or equal to 1, and it is only intended to be used for testing purposes

#### Wake Time
wake_time is the time you intend to be awake and ready to start your day in minutes after midnight, and there should be at least 8 hours (480 minutes) of sleep time after bed_time and before wake_time

#### Bed Time
bed_time is the time you intend to be in bed with your head on the pillow in minutes after midnight

#### Wake Offset
wake_offset is how soon before your intended wake up time your lights should start rising and may need to be as high as 45 minutes for heavy sleepers or as low as 5 minutes for light sleepers

#### Bed Offset
bed_offset is how soon before your intended bed time your lights reach nightlight level and may need to be as high as an hour for hard sleepers or as low as 0 for easy sleepers.


### General-Purpose Arguments for Maximums and Minimums

#### Maximum Brightness
max_bright is the maximum brightness as a decimal that a light can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs

#### Minimum Brightness
min_bright is the minimum brightness a light should reach around bed time and should be just bright enough to allow you to function safely in a space

#### Maximum Correlated Color Temperature
max_CCT is the maximum color temperature in kelvins that a light should reach at midday and should generally correspond to the maximum the lighting system can attain, unless you find that white uncomfortably cool.

#### Minimum Correlated Color Temperature 
min_CCT is the minimum color temperature in kelvins that a light should reach at bedtime and should generally correspond to the minimum the lighting system can attain, unless you find that white uncomfortably warm.


### General-Purpose Arguments for Length

#### Sunrise Brightness Length
rise_length_bright is the length of the morning sunrise routine for brightness change and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise

#### Sunset Brightness Length
set_length_bright is the length of the evening sunset routine for brightness change and should usually be between 2 and 3 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime

#### Sunrise Correlated Color Temperature Length
rise_length_CCT is the length of the morning increase in color temperature in minutes.  The default value of 1 sets it to run for the entire first half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic morning change with a more restful midday. 

#### Sunset Correlated Color Temperature Length
set_length_CCT is the length of the evening decrease in color temperature in minutes.  The default value of 1 sets it to run for the entire second half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic evening change with a more restful midday.


### General-Purpose Arguments for Slope

#### Sunrise Brightness Slope
rise_slope_bright describes the slope at which brightness increases in the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Brightness Slope
set_slope_bright describes the slope at which brightness decreases in the evening. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Correlated Color Temperature Slope
rise_slope_CCT describes the slope at which color temperature increases in the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Correlated Color Temperature Slope
set_slope_CCT describes the slope at which color temperature decreases in the evening. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.


### Sunrise Simulator Specific Arguments for Maximums and Minimums

#### Maximum Blue-Yellow Scatter Distance
max_scatdist is the maximum difference between the central white point and the warm white point when using the blue-yellow feature. Higher numbers make for deeper blues and warmer whites, especially around midday, but a number too high can lead to errors, especially with low max_CCT, because color temperature is not defined below 1000K

#### Minimum Blue-Yellow Scatter Distance
min_scatdist is the minimum difference between the central white point and the warm white point when using the blue-yellow feature. Higher numbers make for deeper blues and warmer whites, especially around bedtime, but a number too high can lead to errors, especially with low min_CCT, because color temperature is not defined below 1000K

#### Maximum Blue-Yellow Angle Shift
max_scatangshift is the maximum angle in degrees by which the warm white is shifted up and the blue point is shifted down when using the blue-yellow feature during sunrise or sunset.  Higher numbers make for more yellow sunsets with dusky blue accents while lower numbers make for more pink sunsets with more aqua accents.

#### Minimum Blue-Yellow Angle Shift
min_scatangshift is the maximum angle in degrees by which the warm white is shifted up and the blue point is shifted down when using the blue-yellow feature during midday.  Higher numbers make for more yellow tinting with dusky blue accents around midday while lower numbers make for more neutral tinting during midday.  This should be 0 under most circumstances, unless you are simulating sunlight near a wildfire

#### Maximum Yellow Brightness
max_bright_yellow is the maximum brightness as a decimal that a yellow light using the blue-yellow feature can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs

#### Minimum Yellow Brightness
min_bright_yellow is the minimum brightness a yellow light using the blue yellow feature should reach around bed time and should be just bright enough to allow you to function safely in a space

#### Maximum Blue Brightness
max_bright_blue is the maximum brightness as a decimal that a blue light using the blue-yellow feature can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs

#### Minimum Blue Brightness
min_bright_blue is the minimum brightness a blue light using the blue yellow feature should reach around bed time and should be just bright enough to allow you to function safely in a space


### Sunrise Simulator Specific Arguments for Length

#### Sunrise Blue-Yellow Scatter Distance Length
rise_length_scatdist is the length in minutes of the morning increase in the distance between the white and warm white points when using the blue-yellow feature.  The default value of 1 sets it to run for the entire second half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic morning change with a more restful midday.

#### Sunset Blue-Yellow Scatter Distance Length
rise_length_scatdist is the length in minutes of the evening decrease in the distance between the white and warm white points when using the blue-yellow feature.  The default value of 1 sets it to run for the entire second half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic evening change with a more restful midday.

#### Sunrise Blue-Yellow Angle Shift Length
rise_length_scatangshift is the length in minutes of the morning increase in angle by which the warm white point is shifted upward and the blue point shifted downward during sunrise.  Higher numbers will make for long, sunrises followed by dramatic golden hours, while lower numbers will make for shorter, more forceful sunrises.

#### Sunset Blue-Yellow Angle Shift Length
set_length_scatangshift is the length in minutes of the morning increase in angle by which the warm white point is shifted upward and the blue point shifted downward during sunrise.  Higher numbers will make for long, sunsets preceeded by dramatic golden hours, while lower numbers will make for shorter, more forceful sunsets.

#### Sunrise Yellow Brightness Length
rise_length_bright_yellow is the length of the morning sunrise routine for brightness change in yellow lights when using the blue-yellow feature and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise.  This can be changed relative to set_length_bright_blue, making this one shorter than that to emphasize yellows in the golden hour or longer than that to emphasize blues at dawn.

#### Sunset Yellow Brightness Length
set_length_bright_yellow is the length of the evening sunset routine for brightness change in yellow lights when using the blue-yellow feature and should usually be between 2 and 3 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime.  This can be changed relative to set_length_bright_blue, making this one shorter than that to emphasize yellows in the golden hour or longer than that to emphasize blues at dusk.

#### Sunrise Blue Brightness Length
rise_length_bright_blue is the length of the morning sunrise routine for brightness change in blue lights when using the blue-yellow feature and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise.  This can be changed relative to set_length_bright_blue, making this one longer than that to emphasize yellows in the golden hour or shorter than that to emphasize blues at dawn.

#### Sunset Brightness Blue Length
set_length_bright_blue is the length of the evening sunset routine for brightness change in blue lights when using the blue-yellow feature and should usually be between 1 and 1.5 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime.  This can be changed relative to set_length_bright_yellow, making this one longer than that to emphasize yellows in the golden hour or shorter than that to emphasize blues at dusk.


### Sunrise Simulator Specific Arguments for Slope

#### Sunrise Blue-Yellow Scatter Distance Slope
rise_slope_scatdist describes the slope at which the distance between the central white and the warm white increases in the morning when using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Blue-Yellow Scatter Distance Slope
set_slope_scatdist describes the slope at which the distance between the central white and the warm white decreases in the evening when using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Blue-Yellow Angle Shift Slope
rise_slope_scatangshift describes the slope at which the angle by which the blue and warm white points are shifted while using the blue-yellow feature decreases over the course of the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Blue-Yellow Angle Shift Slope
set_slope_scatangshift describes the slope at which the angle by which the blue and warm white points are shifted while using the blue-yellow feature decreases over the course of the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Yellow Brightness Slope
rise_slope_bright_yellow describes the slope at which brightness of a yellow light increases in the morning while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Yellow Brightness Slope 
set_slope_bright_yellow describes the slope at which brightness of a yellow light decreases in the evening while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Blue Brightness Slope
rise_slope_bright_blue describes the slope at which brightness of a blue light increases in the morning while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Blue Brightness Slope
set_slope_bright_blue describes the slope at which brightness of a blue light decreases in the evening while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.