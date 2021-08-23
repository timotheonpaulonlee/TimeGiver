# TimeGiver
 TimeGiver is an open-source, highly-customizable circadian lighting rhythm generator that empowers connected lighting systems to support a healthy cycle of sleep and wakefulness.  It takes arguments such as wake time, bed time, and approximate location and returns an appropriate set of lighting parameters such as brightness and color temperature for your current moment and location.  Rhythms can be generated based on just a few parameters using appropriate defaults or customized extensively according to desired maximums, minimums, rates of change, and slope shapes.  TimeGiver also has a sky simulator that uses color lights positioned around a room to mimic the natural color of a clear sky as viewed from the center of a room, believably recreating everything from the crisp blues and pale yellows of noontime to the golden hues of late afternoon and mellow blues of dusk.  The project includes both javascript and python implementations, allowing TimeGiver to serve as part of the back-end of almost any connected lighting project.

## Illustrations
Check out our live demo for Philips Hue Lights at [TimeGiverDemo.com](http://timegiverdemo.com/) that demonstrates the power of TimeGiver's framework. 

The following gif shows a very simple light rhythm generated on the fly using TimeGiver applied to real smart lights from sunrise to sunset, and the graphs below show the brightness and color temperature over time according to that schedule.

![Animation of a simple daily rhythm created with TimeGiver](/images/illustrations/TimeGiverDemo20sec.gif)
![Graph showing brightness over the course of the day used in the schedule from the gif above](/images/illustrations/TimeGiverDemoBrightness.png)
![Graph showing color temperature over the course of the day used in the schedule from the gif above](/images/illustrations/TimeGiverDemoCCT.png)

This next gif shows a pair of light strips running a rhythm created using TimeGiver's sunlight simulator feature that produces a blue-yellow color gradient that mimics the changes in sunlight over the course of a sunny day.  The two colors always combine to form a perfect white, guaranteeing good color rendering all day long.  Note that the flashing and lines are visual artifacts created by the camera.
![Animation of a simple daily rhythm created with TimeGiver](/images/illustrations/KitchenTimeGiverDemo.gif)


## Attributions
TimeGiver is based on the research and development work of Timothy Lee, a 4th-year medical student at Mayo Clinic Alix School of Medicine going into academic psychiatry with strong interests in mood disorders, circadian rhythm disorders, and the importance of regular, restorative sleep to good mental health. Questions and comments can be directed to Timothy Lee on Github [@timotheonpaulonlee](https://github.com/timotheonpaulonlee) or [via LinkedIn](http://linkedin.com/in/timothy-paul-lee/).

# Documentation
TimeGiver is an open-source, highly-customizable circadian lighting schedule generator with implementations in python and javascript built to serve as part of the backend for connected lighting systems.  The core of the system is the function TimeGiver() that takes arguments that describe a lighting rhythm and returns appropriate lighting parameters for the current or specified time under that rhythm.  The code has significant in-line documentation, so this text will focus on a conceptual understanding of the different arguments and return parameters.

## Arguments
TimeGiver accepts over 40 different arguments that describe aspects of how a rhythm is generated, allowing for extensive customization.  However, changes in most of the arguments have a minor effect on the final rhythm and all of them come with default values that should be acceptable for most users.  As a result, the number of arguments you will want to expose as settings depends on your user base and how they value customizability versus simplicity.  There are several core arguments such as wake time and bed time that should be exposed as settings in nearly all applications, and I have bolded them.  The arguments are the same across both implementations, though the syntax for passing them is different.  Some of the arguments serve for any use of TimeGiver and others only matter when using the blue-yellow sunlight simulator feature.  The arguments can also be divided into several different types: those that set key times, those that describe maximums and minimums that fence the rhythms in, those that describes lengths of change, and those that describe slopes of change.  The arguments will be grouped according to whether they are general-purpose or specific to the sunrise simulator and then according to their general category as above.

### General-Purpose Arguments for Locations

#### Latitude
**lat is the approximate latitude of your location in decimal degrees (positive being north of the equator).**

#### Longitude
**long is the approximate longitude of your location in decimal degrees (positive being east of the prime meridian).**

#### Local Values
**localvalues determines whether TimeGiver bases final color values on your location or on your selected Wake Time and Bed Time.  You should activate this setting (set it to 1) in most cases if your schedule coincides with your local daylight hours to within several hours and only deactivate it if your schedule is very different from local daylight hours (for example if you are working night shifts).**

### General-Purpose Arguments for Times

#### Time
time is a simulated time variable that overrides real current time if it is defined.  It is only intended to be used for testing and validation purposes.

#### Wake Time
**wake_time is the time you intend to be awake and ready to start your day in minutes after midnight, and there should be at least 8 hours (480 minutes) of sleep time after bed_time and before wake_time.**

#### Bed Time
**bed_time is the time you intend to be in bed with your head on the pillow in minutes after midnight.**

#### Wake Offset
wake_offset is how soon before your intended wake up time your lights should start rising and may need to be as high as 45 minutes for heavy sleepers or as low as 5 minutes for light sleepers.  This variable is likely to confuse ordinary users and should probably be exposed through a binary questions such as "Are you a heavy sleeper?"

#### Bed Offset
bed_offset is how soon before your intended bed time your lights reach nightlight level and may need to be as high as an hour for hard sleepers or as low as 0 for easy sleepers.  This variable is likely to confuse ordinary users and should probably be exposed through a binary questions such as "Do you typically fall asleep easily?"

### General-Purpose Arguments for Maximums and Minimums

#### Maximum Brightness
**max_bright is the maximum brightness as a decimal that a light can take at midday and should be 1 under almost all circumstances except perhaps for overpowered lighting designs.**

#### Minimum Brightness
**min_bright is the minimum brightness a light should reach around bed time and should be just bright enough to allow you to function safely in a space.  Think of this as your nighttime snack, getting up to use the bathroom nightlight level.**

#### Maximum White Correlated Color Temperature
**max_whiteCCT is the maximum color temperature in kelvins that a white light should reach at midday and should generally correspond to the maximum the lighting system can attain with full brightness, unless you find that white uncomfortably cool.**

#### Minimum White Correlated Color Temperature 
**min_whiteCCT is the minimum color temperature in kelvins that a white light should reach in the early morning and at bedtime and should generally correspond to the minimum the lighting system can attain, unless you find that white uncomfortably warm.**


### General-Purpose Arguments for Length

#### Sunrise Brightness Length
rise_length_bright is the length of the morning sunrise routine for brightness change and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise and support a quick, painless transition to wakefulness.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total time between wakening and going to bed.

#### Sunset Brightness Length
set_length_bright is the length of the evening sunset routine for brightness change and should usually be between 2 and 3 hours to simulate the gradual decrease in brightness that happens around sunset and dusk and support a gradual transition to sleepiness at bedtime.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.

#### Sunrise White Correlated Color Temperature Length
rise_length_whiteCCT is the length of the morning increase in color temperature in minutes for white lights.  The default value sets it to run for the entire first half of the day, but values values less than half the day make for a more dramatic morning change with a more restful midday.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.

#### Sunset White Correlated Color Temperature Length
set_length_whiteCCT is the length of the evening decrease in color temperature in minutes for white lights.  The default value sets it to run for the entire second half of the day, but values values less than half the day make for a more dramatic evening change with a more restful midday.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.


### General-Purpose Arguments for Slope

#### Sunrise Brightness Slope
rise_slope_bright describes the slope at which brightness increases in the morning.  0 makes for a perfectly smooth change with a flat slope.  values approaching 100 make for a change that happens very quickly and then plateaus.  Intermediate positive numbers can be used to mimic exponential changes that happen during sunrise and sunset.  Negative numbers simulate a change that starts out gradually and accelerates over time.

#### Sunset Brightness Slope
set_slope_bright describes the slope at which brightness decreases in the evening. 0 makes for a perfectly smooth change with a flat slope.  values approaching 100 make for a change that happens very quickly and then plateaus.  Intermediate positive numbers can be used to mimic exponential changes that happen during sunrise and sunset.  Negative numbers simulate a change that starts out gradually and accelerates over time.

#### Sunrise White Correlated Color Temperature Slope
rise_slope_whiteCCT describes the slope at which the color temperature of white lights increases in the morning. 0 makes for a perfectly smooth change with a flat slope.  values approaching 100 make for a change that happens very quickly and then plateaus.  Intermediate positive numbers can be used to mimic exponential changes that happen during sunrise and sunset.  Negative numbers simulate a change that starts out gradually and accelerates over time.

#### Sunset White Correlated Color Temperature Slope
set_slope_whiteCCT describes the slope at which the color temperature of white lights decreases in the evening. 0 makes for a perfectly smooth change with a flat slope.  values approaching 100 make for a change that happens very quickly and then plateaus.  Intermediate positive numbers can be used to mimic exponential changes that happen during sunrise and sunset.  Negative numbers simulate a change that starts out gradually and accelerates over time.


### Sunrise Simulator Specific Arguments for Maximums and Minimums

#### Maximum Color Correlated Color Temperature
**max_colorCCT is the maximum color temperature in kelvins that the central white point in the sky simulator should reach at midday and should generally correspond to the maximum CCT of daylight in your area, unless you find that color uncomfortably cool.**

#### Minimum Color Correlated Color Temperature 
**min_colorCCT is the minimum color temperature in kelvins that the central white point in the sky simulator should reach in the early morning and at bedtime and should generally correspond to the minimum CCT of daylight in your area, unless you find that color uncomfortably warm.**

#### Maximum Sky Simulator Scatter Distance
**max_scatdist is the maximum difference between the central white point and the warm white point when using the sky simulator. Higher numbers make for deeper blues and warmer whites, especially around midday, but a number too high can reduce overall brightness and color rendering, especially with low max_whiteCCT, because color temperature is not defined below 1000K**

#### Minimum Sky Simulator Scatter Distance
**min_scatdist is the minimum difference between the central white point and the warm white point when using the sky simulator. Higher numbers make for deeper blues and warmer whites, especially around bedtime, but a number too high can impair color rendering, especially with low min_whiteCCT, because color temperature is not defined below 1000K**

#### Maximum Sky Simulator Angle Shift
**max_scatangshift is the maximum angle in degrees by which the warm white is shifted up toward yellow and the blue point is shifted down toward a more purple blue when using the sky simulator during sunrise or sunset.  Higher numbers make for more yellow sunsets with dusky blue accents while lower numbers make for more orange sunsets with more aqua accents.  Numbers too high can lead to very pink sunrises and sunsets with greenish accents.**

#### Minimum Sky Simulator Angle Shift
**min_scatangshift is the maximum angle in degrees by which the warm white is shifted up and the blue point is shifted down when using the sky simulator during midday.  Higher numbers make for more yellow tinting with dusky blue accents around midday while lower numbers make for more neutral tinting during midday.  This should be 0 under most circumstances, unless you are simulating sunlight near a wildfire**

#### Maximum Yellow Brightness
**max_bright_yellow is the maximum brightness as a decimal that a yellow light using the sky simulator can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs**

#### Minimum Yellow Brightness
**min_bright_yellow is the minimum brightness a yellow light using the blue yellow feature should reach around bed time and should be just bright enough to allow you to function safely in a space**

#### Maximum Blue Brightness
**max_bright_blue is the maximum brightness as a decimal that a blue light using the sky simulator can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs**

#### Minimum Blue Brightness
**min_bright_blue is the minimum brightness a blue light using the blue yellow feature should reach around bed time and should be just bright enough to allow you to function safely in a space**


### Sunrise Simulator Specific Arguments for Length

#### Sunrise Sky Simulator Scatter Distance Length
rise_length_scatdist is the length in minutes of the morning increase in the distance between the white and warm white points when using the sky simulator.  The default value of None or Null sets it to run for the entire second half of the day, but values less than half the day make for a more dramatic morning change with a more restful midday.  This argument can accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunset Sky Simulator Scatter Distance Length
rise_length_scatdist is the length in minutes of the evening decrease in the distance between the white and warm white points when using the sky simulator.  The default value of None or Null sets it to run for the entire second half of the day, but values less than half the day make for a more dramatic evening change with a more restful midday.  This argument can accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunrise Sky Simulator Angle Shift Length
rise_length_scatangshift is the length in minutes of the morning increase in angle by which the warm white point is shifted upward and the blue point shifted downward during sunrise.  Higher numbers will make for long, sunrises followed by dramatic golden hours, while lower numbers will make for shorter, more forceful sunrises.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunset Sky Simulator Angle Shift Length
set_length_scatangshift is the length in minutes of the morning increase in angle by which the warm white point is shifted upward and the blue point shifted downward during sunrise.  Higher numbers will make for long, sunsets preceeded by dramatic golden hours, while lower numbers will make for shorter, more forceful sunsets.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunrise Yellow Brightness Length
rise_length_bright_yellow is the length of the morning sunrise routine for brightness change in yellow lights when using the sky simulator and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise.  This can be changed relative to set_length_bright_blue, making this one shorter than that to emphasize yellows in the golden hour or longer than that to emphasize blues at dawn.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunset Yellow Brightness Length
set_length_bright_yellow is the length of the evening sunset routine for brightness change in yellow lights when using the sky simulator and should usually be between 2 and 3 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime.  This can be changed relative to set_length_bright_blue, making this one shorter than that to emphasize yellows in the golden hour or longer than that to emphasize blues at dusk.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunrise Blue Brightness Length
rise_length_bright_blue is the length of the morning sunrise routine for brightness change in blue lights when using the sky simulator and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise.  This can be changed relative to set_length_bright_blue, making this one longer than that to emphasize yellows in the golden hour or shorter than that to emphasize blues at dawn.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunset Brightness Blue Length
set_length_bright_blue is the length of the evening sunset routine for brightness change in blue lights when using the sky simulator and should usually be between 1 and 1.5 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime.  This can be changed relative to set_length_bright_yellow, making this one longer than that to emphasize yellows in the golden hour or shorter than that to emphasize blues at dusk.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.  It can also accept None or null, in which case it will be set to half of the day length.

#### Sunrise Color Correlated Color Temperature Length
rise_length_colorCCT is the length of the morning increase in color temperature in minutes for color lights.  The default value sets it to run for the entire first half of the day, but values values less than half the day make for a more dramatic morning change with a more restful midday.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.

#### Sunset Color Correlated Color Temperature Length
set_length_colorCCT is the length of the evening decrease in color temperature in minutes for color lights.  The default value sets it to run for the entire second half of the day, but values values less than half the day make for a more dramatic evening change with a more restful midday.  This argument can also accept fractions of half day length in a string with the form "0.5x", which would set the argument to 1/4th of the total day length.



### Sunrise Simulator Specific Arguments for Slope

#### Sunrise Sky Simulator Scatter Distance Slope
rise_slope_scatdist describes the slope at which the distance between the central white and the warm white increases in the morning when using the sky simulator. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Sky Simulator Scatter Distance Slope
set_slope_scatdist describes the slope at which the distance between the central white and the warm white decreases in the evening when using the sky simulator. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Sky Simulator Angle Shift Slope
rise_slope_scatangshift describes the slope at which the angle by which the blue and warm white points are shifted while using the sky simulator decreases over the course of the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Sky Simulator Angle Shift Slope
set_slope_scatangshift describes the slope at which the angle by which the blue and warm white points are shifted while using the sky simulator decreases over the course of the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Yellow Brightness Slope
rise_slope_bright_yellow describes the slope at which brightness of a yellow light increases in the morning while using the sky simulator. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Yellow Brightness Slope 
set_slope_bright_yellow describes the slope at which brightness of a yellow light decreases in the evening while using the sky simulator. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Blue Brightness Slope
rise_slope_bright_blue describes the slope at which brightness of a blue light increases in the morning while using the sky simulator. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunset Blue Brightness Slope
set_slope_bright_blue describes the slope at which brightness of a blue light decreases in the evening while using the sky simulator. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.

#### Sunrise Color Correlated Color Temperature Slope
rise_slope_colorCCT describes the slope at which the color temperature of color lights increases in the morning. 0 makes for a perfectly smooth change with a flat slope.  values approaching 100 make for a change that happens very quickly and then plateaus.  Intermediate positive numbers can be used to mimic exponential changes that happen during sunrise and sunset.  Negative numbers simulate a change that starts out gradually and accelerates over time.

#### Sunset Color Correlated Color Temperature Slope
set_slope_colorCCT describes the slope at which the color temperature of color lights decreases in the evening. 0 makes for a perfectly smooth change with a flat slope.  values approaching 100 make for a change that happens very quickly and then plateaus.  Intermediate positive numbers can be used to mimic exponential changes that happen during sunrise and sunset.  Negative numbers simulate a change that starts out gradually and accelerates over time.

## Returns
Now that you have reviewed the arguments TimeGiver accepts to build a schedule, it is important to understand how TimeGiver returns lighting parameters.  The implementation is different between the implementations, with parameters returned as a list in python and an object literal in javascript, but the variables should be identical across implementations.  There are 18 parameters returned in all instances.  Note that all variables are returned in every situation and it is your job to decide how to give your users choice over which set of parameters to implement.  The return variables are:
 1. bright_int_ret: Brightness for white lights as an integer out of 254.
 2. CCT_mired_int_ret: White light Color Temperature as an integer in Mired, which can be converted to Kelvin using the formula Kelvin = (1*10^6)/Mired.
 3. bright_yellow_int_ret: Brightness of yellow sky lights as an integer out of 254.
 4. bright_blue_int_ret: Brightness of blue sky lights as an integer out of 254.
 5. bright_comb_int_ret: Brightness of combined sky lights as an integer out of 254.
 6. white_x_ret: CIE 1931 x value of the plain white lights as a decimal, which can also be calculated from the white color temperature.
 7. white_y_ret: CIE 1931 y value of the plain white lights as a decimal, which can also be calculated from the white color temperature.
 8. yellow_shifted_x_ret: CIE 1931 x value of the yellow lights as a decimal.
 9. yellow_shifted_y_ret: CIE 1931 y value of the yellow lights as a decimal.
 10. blue_shifted_x_ret: CIE 1931 x value of the blue lights as a decimal.
 11. blue_shifted_y_ret: CIE 1931 y value of the blue lights as a decimal.
 12. comb_shifted_x_ret: CIE 1931 x value of the blue lights as a decimal.
 13. comb_shifted_y_ret: CIE 1931 y value of the combined sky lights as a decimal.
 14. sun_dist_ret: The angle in decimal degrees between a specified light and the sun in your present location, which always falls between 0 and 180 degrees.
 15. sun_altitude_ret: The smallest angle in decimal degrees between the horizon and the sun in your present location, which always falls between 90 and -90 degrees.
 16. sun_azimuth_ret: The compass angle in decimal degrees of the point on the horizon directly below the sun in your present location, where due north is 0 degrees, due east is 90 degrees, due south is 180 degrees, and due west is 270 degrees.
 17. sunrise_ret: The time in minutes after midnight at which the sun rose or will rise in your present location.
 18. sunset_ret: The time in minutes after midnight at which the sun set or will set in your present location.

## Usage
Now that you are familiar with TimeGiver's arguments and returns, the actual usage of the program is quite straightforward but differs slightly between implementations.

### Python Usage
1. Download the TimeGiver.py source file and place it in the root directory of the python program that is calling it.
2. Import the TimeGiver function into your python program as follows: 
```python 
from TimeGiver import TimeGiver
```
3. Set a variable such as lighting_parameters to assign to the list returned by the TimeGiver function passed with appropriate arguments with the following syntax, leaving all other arguments to be set to their default:
```python
lighting_parameters = TimeGiver (bed_time = "1260", wake_time = "360")
```
4. Optionally, parse out the items in the ordered list to make for easier usage elsewhere in your code:
```python
bright_int_ret = lighting_parameters[0]
CCT_mired_int_ret = lighting_parameters[1]
bright_yellow_int_ret = lighting_parameters[2]
bright_blue_int_ret = lighting_parameters[3]
white_x_ret = lighting_parameters[4]
white_y_ret = lighting_parameters[5]
yellow_x_shifted_ret = lighting_parameters[6]
yellow_y_shifted_ret = lighting_parameters[7]
blue_x_shifted_ret = lighting_parameters[8]
blue_y_shifted_ret = lighting_parameters[9]
```
5. Rerun steps 3 and 4 as often as needed to update lighting parameters as time passes.

### Javascript Usage
1. Download TimeGiver.js and place it somewhere in your project folder
2. Import TimeGiver.js into your HTML head as follows:
```javascript
<script type="text/javascript" src="TimeGiver.js"></script>
```
3. Set a variable such as lighting_parameters to assign to the object literal returned by the TimeGiver function passed with appropriate arguments with the following syntax, leaving all other arguments to be set to their default:
```javascript
let lighting_parameters = TimeGiver({wake_time: 360, bed_time: 1260})
```
4. Access the individual lighting parameters using the object.key syntax as in the example below:
```javascript
lighting_parameters.blue_x_shifted_ret
```
5. Rerun steps 3 and 4 as often as needed to update lighting parameters as time passes.