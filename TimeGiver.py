import math
import datetime 

##CCT to XY Transformer - Converts CCT values stored as integers in kelvin into CIE 1931 Color Diagram X and Y coordinates specifying the location of that color temperature in that master color space.
x_transform_dict = {"0": "0"}
x_transform_file = open ("x_transform_dict.txt", "r")
for x in x_transform_file:
    x_transform_line = x
    x_value = x_transform_line [0:6]
    CCT_value = x_transform_line [7:-1]
    x_transform_dict.update({CCT_value: x_value})

y_transform_dict = {"0": "0"}
y_transform_file = open ("y_transform_dict.txt", "r")
for x in y_transform_file:
    y_transform_line = x
    y_value = y_transform_line [0:6]
    CCT_value = y_transform_line [7:-1]
    y_transform_dict.update({CCT_value: y_value})

def TimeGiver ( #TimeGiver is the main function of the script that takes arguments about rhythm parameters using key-value syntax with defaults as shown below and returns a list of 8 items describing how the lights should look at that moment according to that schedule.
    max_bright = float (1), #max_bright is the maximum brightness as a decimal that a light can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs
    min_bright = float (0.05), #min_bright is the minimum brightness a light should reach around bed time and should be just bright enough to allow you to function safely in a space
    max_CCT = float (6500), #max_CCT is the maximum color temperature in kelvins that a light should reach at midday and should generally correspond to the maximum the lighting system can attain, unless you find that white uncomfortably cool.
    min_CCT = float (2700), #min_CCT is the minimum color temperature in kelvins that a light should reach at bedtime and should generally correspond to the minimum the lighting system can attain, unless you find that white uncomfortably warm.
    max_scatdist = float (3000), #max_scatdist is the maximum difference between the central white point and the warm white point when using the blue-yellow feature. Higher numbers make for deeper blues and warmer whites, especially around midday, but a number too high can lead to errors, especially with low max_CCT, because color temperature is not defined below 1000K
    min_scatdist = float (2000), #min_scatdist is the minimum difference between the central white point and the warm white point when using the blue-yellow feature. Higher numbers make for deeper blues and warmer whites, especially around bedtime, but a number too high can lead to errors, especially with low min_CCT, because color temperature is not defined below 1000K
    max_scatangshift = float (15), #max_scatangshift is the maximum angle in degrees by which the warm white is shifted up and the blue point is shifted down when using the blue-yellow feature during sunrise or sunset.  Higher numbers make for more yellow sunsets with dusky blue accents while lower numbers make for more pink sunsets with more aqua accents.
    min_scatangshift = float (0), #min_scatangshift is the maximum angle in degrees by which the warm white is shifted up and the blue point is shifted down when using the blue-yellow feature during midday.  Higher numbers make for more yellow tinting with dusky blue accents around midday while lower numbers make for more neutral tinting during midday.  This should be 0 under most circumstances, unless you are simulating sunlight near a wildfire
    max_bright_yellow = float (1), #max_bright_yellow is the maximum brightness as a decimal that a yellow light using the blue-yellow feature can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs
    min_bright_yellow = float (0.05), #min_bright_yellow is the minimum brightness a yellow light using the blue yellow feature should reach around bed time and should be just bright enough to allow you to function safely in a space
    max_bright_blue = float (1), #max_bright_blue is the maximum brightness as a decimal that a blue light using the blue-yellow feature can take at midday and should be 1 under almost all circumstances except for overpowered lighting designs
    min_bright_blue = float (0.05), #min_bright_blue is the minimum brightness a blue light using the blue yellow feature should reach around bed time and should be just bright enough to allow you to function safely in a space
    rise_slope_bright = float (0), #rise_slope_bright describes the slope at which brightness increases in the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    set_slope_bright = float (0), #set_slope_bright describes the slope at which brightness decreases in the evening. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    rise_slope_CCT = float (0), #rise_slope_CCT describes the slope at which color temperature increases in the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    set_slope_CCT = float (0), #set_slope_CCT describes the slope at which color temperature decreases in the evening. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    rise_slope_scatdist = float (0), #rise_slope_scatdist describes the slope at which the distance between the central white and the warm white increases in the morning when using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    set_slope_scatdist = float (0), #set_slope_scatdist describes the slope at which the distance between the central white and the warm white decreases in the evening when using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    rise_slope_scatangshift = float (0), #rise_slope_scatangshift describes the slope at which the angle by which the blue and warm white points are shifted while using the blue-yellow feature decreases over the course of the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    set_slope_scatangshift = float (0), #set_slope_scatangshift describes the slope at which the angle by which the blue and warm white points are shifted while using the blue-yellow feature decreases over the course of the morning. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    rise_slope_bright_yellow = float (0), #rise_slope_bright_yellow describes the slope at which brightness of a yellow light increases in the morning while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    set_slope_bright_yellow = float (0), #set_slope_bright_yellow describes the slope at which brightness of a yellow light decreases in the evening while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    rise_slope_bright_blue = float (0), # rise_slope_bright_blue describes the slope at which brightness of a blue light increases in the morning while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    set_slope_bright_blue = float (0), #set_slope_bright_blue describes the slope at which brightness of a blue light decreases in the evening while using the blue-yellow feature. 0 makes for a perfectly smooth change with a flat slope and 100 makes for a change that happens very quickly and then plateaus, while numbers inbetween can be used to mimic exponential changes that happen during sunrise and sunset.
    time = float (0), #time is a simulated time variable that overrides real current time if it is set to greater than or equal to 1, and it is only intended to be used for testing purposes
    wake_time = float (420), #wake_time is the time you intend to be awake and ready to start your day in minutes after midnight, and there should be at least 8 hours (480 minutes) of sleep time after bed_time and before wake_time
    bed_time = float (1320), #bed_time is the time you intend to be in bed with your head on the pillow in minutes after midnight
    wake_offset = float (30), #wake_offset is how soon before your intended wake up time your lights should start rising and may need to be as high as 45 minutes for heavy sleepers or as low as 5 minutes for light sleepers
    bed_offset = float (30), #bed_offset is how soon before your intended bed time your lights reach nightlight level and may need to be as high as an hour for hard sleepers or as low as 0 for easy sleepers.
    rise_length_bright = float (45), #rise_length_bright is the length of the morning sunrise routine for brightness change and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise
    set_length_bright = float (180), #set_length_bright is the length of the evening sunset routine for brightness change and should usually be between 2 and 3 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime
    rise_length_CCT = float (1), #rise_length_CCT is the length of the morning increase in color temperature in minutes.  The default value of 1 sets it to run for the entire first half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic morning change with a more restful midday. 
    set_length_CCT = float (1), #set_length_CCT is the length of the evening decrease in color temperature in minutes.  The default value of 1 sets it to run for the entire second half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic evening change with a more restful midday.
    rise_length_scatdist = float (1), #rise_length_scatdist is the length in minutes of the morning increase in the distance between the white and warm white points when using the blue-yellow feature.  The default value of 1 sets it to run for the entire second half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic morning change with a more restful midday.
    set_length_scatdist = float (1), #rise_length_scatdist is the length in minutes of the evening decrease in the distance between the white and warm white points when using the blue-yellow feature.  The default value of 1 sets it to run for the entire second half of the day, but values greater than 2 will be honored, and values less than half the day make for a more dramatic evening change with a more restful midday.
    rise_length_scatangshift = float (240), #rise_length_scatangshift is the length in minutes of the morning increase in angle by which the warm white point is shifted upward and the blue point shifted downward during sunrise.  Higher numbers will make for long, sunrises followed by dramatic golden hours, while lower numbers will make for shorter, more forceful sunrises.
    set_length_scatangshift = float (240), #set_length_scatangshift is the length in minutes of the morning increase in angle by which the warm white point is shifted upward and the blue point shifted downward during sunrise.  Higher numbers will make for long, sunsets preceeded by dramatic golden hours, while lower numbers will make for shorter, more forceful sunsets.
    rise_length_bright_yellow = float (30), #rise_length_bright_yellow is the length of the morning sunrise routine for brightness change in yellow lights when using the blue-yellow feature and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise.  This can be changed relative to set_length_bright_blue, making this one shorter than that to emphasize yellows in the golden hour or longer than that to emphasize blues at dawn.
    set_length_bright_yellow = float (90), #set_length_bright_yellow is the length of the evening sunset routine for brightness change in yellow lights when using the blue-yellow feature and should usually be between 2 and 3 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime.  This can be changed relative to set_length_bright_blue, making this one shorter than that to emphasize yellows in the golden hour or longer than that to emphasize blues at dusk.
    rise_length_bright_blue = float (60), #rise_length_bright_blue is the length of the morning sunrise routine for brightness change in blue lights when using the blue-yellow feature and should usually be between 30 minutes and 1 hour to simulate the fast increase in brightness that happens around sunrise.  This can be changed relative to set_length_bright_blue, making this one longer than that to emphasize yellows in the golden hour or shorter than that to emphasize blues at dawn.
    set_length_bright_blue = float (180), #set_length_bright_blue is the length of the evening sunset routine for brightness change in blue lights when using the blue-yellow feature and should usually be between 1 and 1.5 hours to simulate the gradual decrease in brightness that happens around sunset and dusk, supporting a gradual transition to sleepiness at bedtime.  This can be changed relative to set_length_bright_yellow, making this one longer than that to emphasize yellows in the golden hour or shorter than that to emphasize blues at dusk.
 ):

    if time > 1: #This conditional statement allows users to pass a simulated time variable that will override the real current time for all times greater than or equal to 1
        hm = float (time) 
    else: 
        now = datetime.datetime.now() #sets the variable now equal to the current date and time
        hh = int (now.strftime("%H")) #sets the variable hh equal to the number of hours that have passed since the day started.
        hh_sixty = (hh * 60) #sets the variable hh_sixty equal to the number of minutes in the day at the time of the last hour change.
        mm = float ((now.strftime("%M"))) #sets the variable mm equal to the number of minutes since the last hour
        hm = float (hh_sixty + mm) #sets the variable hm equal to the total number of minutes that have passed since the day began.

    if float (float (wake_time) - float (wake_offset) - float (bed_time) + float (bed_offset)) > 0 and float (float (wake_time) - float (wake_offset) - float (hm)) > 0: #This conditional statement allows for proper handling of the edge case in which wake_time is greater than bed_time, i.e. when the user is going to bed after midnight.
        hm = float (float (hm) + float (1440))
        bed_time = float (float (bed_time) + float (1440))
        print ("if wake time greater than bed time")

    elif float (float (wake_time) - float (wake_offset) - float (bed_time) + float (bed_offset)) > 0:
        bed_time = float (float (bed_time) + float (1440))
        print ("else wake time greater than bed time")

    
    max_bright_flt = float (max_bright) #maximum brightness as a decimal
    min_bright_flt = float (min_bright) #minimum brightness as a decimal
    max_CCT_flt = float (max_CCT) #maximum color temperature in kelvins
    min_CCT_flt = float (min_CCT) #minimum color temperature in kelvins
    max_scatdist_flt = float (max_scatdist) #maximum scattering distance in kelvins
    min_scatdist_flt = float (min_scatdist) #minimum scattering distance in kelivins
    max_scatangshift_flt = float (max_scatangshift) #maximum scattering angle shift in degrees
    min_scatangshift_flt = float (min_scatangshift) #minimum scattering angle shift in degrees
    max_bright_yellow_flt = float (max_bright_yellow) #maximum yellow brightness as a decimal
    min_bright_yellow_flt = float (min_bright_yellow) #minimum yellow brightness as a decimal
    max_bright_blue_flt = float (max_bright_blue) #maximum yellow brightness as a decimal
    min_bright_blue_flt = float (min_bright_blue) #minimum yellow brightness as a decimal

    rise_slope_bright_flt = float (rise_slope_bright) #slope at which brightness increases in the morning out of 100
    set_slope_bright_flt = float (set_slope_bright) #slope at which brightness decreases in the evening out of 100
    rise_slope_CCT_flt = float (rise_slope_CCT) #slope at which color temperature increases in the morning out of 100
    set_slope_CCT_flt = float (set_slope_CCT) #slope at which color temperature decreases in the evening out of 100
    rise_slope_scatdist_flt = float (rise_slope_scatdist) #slope at which scattering distance increases in the morning out of 100
    set_slope_scatdist_flt = float (set_slope_scatdist) #slope at which scattering distance decreases in the evening out of 100
    rise_slope_scatangshift_flt = float (rise_slope_scatangshift) #slope at which scattering angle shift decrease in the morning out of 100
    set_slope_scatangshift_flt = float (set_slope_scatangshift) #slope at which scattering angle shift increases in the evening out of 100
    rise_slope_bright_yellow_flt = float (rise_slope_bright_yellow) #slope at which yellow brightness increases in the morning out of 100
    set_slope_bright_yellow_flt = float (set_slope_bright_yellow) #slope at which yellow brightness decreases in the evening out of 100
    rise_slope_bright_blue_flt = float (rise_slope_bright_blue) #slope at which blue brightness increases in the morning out of 100
    set_slope_bright_blue_flt = float (set_slope_bright_blue) #slope at which blue brightness decreases in the evening out of 100

    wake_time_flt = float (wake_time) #wake time in minutes
    bed_time_flt = float (bed_time) #bed time in minutes
    wake_offset_flt = float (wake_offset) #offset in minutes before wake time at which light starts to increase
    bed_offset_flt = float (bed_offset) #offset in minutes before bed time at which light reaches minimum

    day_length = float ((bed_time_flt - bed_offset_flt) - (wake_time_flt - wake_offset_flt)) #time between wake time and bed time in minutes
    half_day_length = float (day_length/2) #half of time between wake time and bed time in minutes

    rise_length_bright_flt = float (rise_length_bright) #length of brightness wake routine in minutes
    set_length_bright_flt = float (set_length_bright) #length of brightness bed routine in minutes

    #This next set of conditional statements allows these variables to default to half of day length, whatever that is, since that tends to work well for these variables
    if rise_length_CCT < 2:
        rise_length_CCT_flt = float (half_day_length)
    else:
        rise_length_CCT_flt = float (rise_length_CCT)
    
    if set_length_CCT < 2:
        set_length_CCT_flt = float (half_day_length)
    else:
        set_length_CCT_flt = float (set_length_CCT)

    if rise_length_scatdist < 2:
        rise_length_scatdist_flt = float (half_day_length)
    else:
        rise_length_scatdist_flt = float (rise_length_scatdist)

    if set_length_scatdist < 2:
        set_length_scatdist_flt = float (half_day_length)
    else:
        set_length_scatdist_flt = float (set_length_scatdist)

    rise_length_scatangshift_flt = float (rise_length_scatangshift) #length of scattering angle shift wake routine in minutes
    set_length_scatangshift_flt = float (set_length_scatangshift) #length of scattering angle shift bed routine in minutes
    rise_length_bright_yellow_flt = float (rise_length_bright_yellow) #length of yellow brightness wake routine in minutes
    set_length_bright_yellow_flt = float (set_length_bright_yellow) #length of yellow brightness bed routine in minutes
    rise_length_bright_blue_flt = float (rise_length_bright_blue) #length of blue brightness wake routine in minutes
    set_length_bright_blue_flt = float (set_length_bright_blue) #length of blue brightness bed routine in minutes

    #This part consists of intermediate variables that are only defined to make the final math formulas easier to read and change if needed
    rise_slope_bright_exp1 = float ((rise_slope_bright_flt - 100))
    rise_slope_bright_exp2 = float (rise_slope_bright_exp1/-100) #slope exponent for brightness
    rise_slope_CCT_exp1 = float ((rise_slope_CCT_flt - 100))
    rise_slope_CCT_exp2 = float (rise_slope_CCT_exp1/-100) #slope exponent for color temperature
    rise_slope_scatdist_exp1 = float ((rise_slope_scatdist_flt - 100))
    rise_slope_scatdist_exp2 = float (rise_slope_scatdist_exp1/-100) #slope exponent for scattering distance
    rise_slope_scatangshift_exp1 = float ((rise_slope_scatangshift_flt - 100))
    rise_slope_scatangshift_exp2 = float (rise_slope_scatangshift_exp1/-100) #slope exponent for scattering angle shift
    rise_slope_bright_yellow_exp1 = float ((rise_slope_bright_yellow_flt - 100))
    rise_slope_bright_yellow_exp2 = float (rise_slope_bright_yellow_exp1/-100) #slope exponent for yellow brightness
    rise_slope_bright_blue_exp1 = float ((rise_slope_bright_blue_flt - 100))
    rise_slope_bright_blue_exp2 = float (rise_slope_bright_blue_exp1/-100) #slope exponent for blue brightness

    set_slope_bright_exp1 = float ((set_slope_bright_flt - 100))
    set_slope_bright_exp2 = float (set_slope_bright_exp1/-100) #slope exponent for brightness
    set_slope_CCT_exp1 = float ((set_slope_CCT_flt - 100))
    set_slope_CCT_exp2 = float (set_slope_CCT_exp1/-100) #slope exponent for color temperature
    set_slope_scatdist_exp1 = float ((set_slope_scatdist_flt - 100))   
    set_slope_scatdist_exp2 = float (set_slope_scatdist_exp1/-100) #slope exponent for scattering distance
    set_slope_scatangshift_exp1 = float ((set_slope_scatangshift_flt - 100))
    set_slope_scatangshift_exp2 = float (set_slope_scatangshift_exp1/-100) #slope exponent for scattering angle shift
    set_slope_bright_yellow_exp1 = float ((set_slope_bright_yellow_flt - 100))
    set_slope_bright_yellow_exp2 = float (set_slope_bright_yellow_exp1/-100) #slope exponent for yellow brightness
    set_slope_bright_blue_exp1 = float ((set_slope_bright_blue_flt - 100))
    set_slope_bright_blue_exp2 = float (set_slope_bright_blue_exp1/-100) #slope exponent for blue brightness

    #These are the final formulas that define the lighting parameters during periods of change
    rise_bright = float ((((hm - wake_time_flt + wake_offset_flt)/rise_length_bright_flt) ** (rise_slope_bright_exp2)) * (max_bright_flt - min_bright_flt) + min_bright_flt) #brightness as a decimal during wake routine
    rise_CCT = float ((((hm - wake_time_flt + wake_offset_flt)/rise_length_CCT_flt) ** (rise_slope_CCT_exp2)) * (max_CCT_flt - min_CCT_flt) + min_CCT_flt) #color temperature in kelvin during wake routine
    set_bright = float ((((bed_time_flt - bed_offset_flt - hm)/set_length_bright_flt) ** (set_slope_bright_exp2)) * (max_bright_flt - min_bright_flt) + min_bright_flt) #brightness as a decimal during bed routine
    set_CCT = float ((((bed_time_flt - bed_offset_flt - hm)/set_length_CCT_flt) ** (set_slope_CCT_exp2)) * (max_CCT_flt - min_CCT_flt) + min_CCT_flt) #color temperature in kelvin during bed routine
    rise_scatdist = float ((((hm - wake_time_flt + wake_offset_flt)/rise_length_scatdist_flt) ** (rise_slope_scatdist_exp2)) * (max_scatdist_flt - min_scatdist_flt) + min_scatdist_flt) #scattering distance in kelvin during wake routine
    set_scatdist = float ((((bed_time_flt - bed_offset_flt - hm)/set_length_scatdist_flt) ** (set_slope_scatdist_exp2)) * (max_scatdist_flt - min_scatdist_flt) + min_scatdist_flt) #scattering distance in kelvin during bed routine
    rise_scatangshift = float (-1 * ((((hm - wake_time_flt + wake_offset_flt)/rise_length_scatangshift_flt) ** (rise_slope_scatangshift_exp2)) * (max_scatangshift_flt - min_scatangshift_flt) + min_scatangshift_flt) + max_scatangshift_flt) #scattering angle shift in degrees during wake routine
    set_scatangshift = float (-1 * ((((bed_time_flt - bed_offset_flt - hm)/set_length_scatangshift_flt) ** (set_slope_scatangshift_exp2)) * (max_scatangshift_flt - min_scatangshift_flt) + min_scatangshift_flt) + max_scatangshift_flt) #scattering angle shift in degrees during bed routine
    rise_bright_yellow = float ((((hm - wake_time_flt + wake_offset_flt)/rise_length_bright_yellow_flt) ** (rise_slope_bright_yellow_exp2)) * (max_bright_yellow_flt - min_bright_yellow_flt) + min_bright_yellow_flt) #brightness as a decimal during wake routine
    set_bright_yellow = float ((((bed_time_flt - bed_offset_flt - hm)/set_length_bright_yellow_flt) ** (set_slope_bright_yellow_exp2)) * (max_bright_yellow_flt - min_bright_yellow_flt) + min_bright_yellow_flt) #brightness as a decimal during bed routine
    rise_bright_blue = float ((((hm - wake_time_flt + wake_offset_flt)/rise_length_bright_blue_flt) ** (rise_slope_bright_blue_exp2)) * (max_bright_blue_flt - min_bright_blue_flt) + min_bright_blue_flt) #brightness as a decimal during wake routine
    set_bright_blue = float ((((bed_time_flt - bed_offset_flt - hm)/set_length_bright_blue_flt) ** (set_slope_bright_blue_exp2)) * (max_bright_blue_flt - min_bright_blue_flt) + min_bright_blue_flt) #brightness as a decimal during bed routine

    #This section takes the outputs from the formulas above and the arguments and converts it into the form and data type needed for the final output
    max_bright_int = int (max_bright_flt * 254) #Brightness values in decimal are multiplied by 254 for use in control systems that specify brightness values using 1 byte of data, a widely used industry standard.
    rise_bright_int = int (rise_bright * 254)
    set_bright_int = int (set_bright * 254)
    min_bright_int = int (min_bright_flt *254)

    max_CCT_int = int (max_CCT_flt)
    rise_CCT_int = int (rise_CCT)
    set_CCT_int = int (set_CCT)
    min_CCT_int = int (min_CCT_flt)

    max_scatdist_int = int (max_scatdist_flt)
    rise_scatdist_int = int (rise_scatdist)
    set_scatdist_int = int (set_scatdist)
    min_scatdist_int = int (min_scatdist_flt)

    max_bright_yellow_int = int (max_bright_yellow_flt * 254)
    rise_bright_yellow_int = int (rise_bright_yellow * 254)
    set_bright_yellow_int = int (set_bright_yellow * 254)
    min_bright_yellow_int = int (min_bright_yellow_flt *254)

    max_bright_blue_int = int (max_bright_blue_flt * 254)
    rise_bright_blue_int = int (rise_bright_blue * 254)
    set_bright_blue_int = int (set_bright_blue * 254)
    min_bright_blue_int = int (min_bright_blue_flt *254)

    #This next part consists of most of the logic that determines whether to output the maximum, current setting value, minimum, or current rising value for each final output based on the time of day.

    #Setting bright_int to appropriate value based on day segment
    if not float (hm - wake_time_flt + wake_offset_flt) > 0:
        bright_int = min_bright_int
        #print ('Time is before wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and not float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_flt) > 0:
        bright_int = rise_bright_int
        #print ('Time is during wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt + set_length_bright_flt) > 0:
        bright_int = max_bright_int
        #print ('Time is after wake up and before bed')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_bright_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt) > 0:
        bright_int = set_bright_int
        #print ('Time is during bed time')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_bright_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt) > 0:
        bright_int = min_bright_int
        #print ('Time is after bed')

    #Setting CCT_int to appropriate value based on day segment
    if not float (hm - wake_time_flt + wake_offset_flt) > 0:
        CCT_int = min_CCT_int
        #print ('Time is before wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and not float (hm - wake_time_flt + wake_offset_flt - rise_length_CCT_flt) > 0:
        CCT_int = rise_CCT_int
        #print ('Time is during wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_CCT_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt + set_length_CCT_flt) > 0:
        CCT_int = max_CCT_int
        #print ('Time is after wake up and before bed')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_CCT_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_CCT_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt) > 0:
        CCT_int = set_CCT_int
        #print ('Time is during bed time')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_CCT_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_CCT_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt) > 0:
        CCT_int = min_CCT_int
        #print ('Time is after bed')

    #Setting scatdist_int to appropriate value based on day segment
    if not float (hm - wake_time_flt + wake_offset_flt) > 0:
        scatdist_int = min_scatdist_int
        #print ('Time is before wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and not float (hm - wake_time_flt + wake_offset_flt - rise_length_scatdist_flt) > 0:
        scatdist_int = rise_scatdist_int
        #print ('Time is during wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_scatdist_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt + set_length_scatdist_flt) > 0:
        scatdist_int = max_scatdist_int
        #print ('Time is after wake up and before bed')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_scatdist_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_scatdist_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt) > 0:
        scatdist_int = set_scatdist_int
        #print ('Time is during bed time')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_scatdist_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_scatdist_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt) > 0:
        scatdist_int = min_scatdist_int
        #print ('Time is after bed')

    #Setting scatangshift_flt to appropriate value based on day segment
    if not float (hm - wake_time_flt + wake_offset_flt) > 0:
        scatangshift_flt = float (max_scatangshift_flt)
        #print ('Time is before wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and not float (hm - wake_time_flt + wake_offset_flt - rise_length_scatangshift_flt) > 0:
        scatangshift_flt = float (rise_scatangshift)
        #print ('Time is during wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_scatangshift_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt + set_length_scatangshift_flt) > 0:
        scatangshift_flt = float (min_scatangshift_flt)
        #print ('Time is after wake up and before bed')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_scatangshift_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_scatangshift_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt) > 0:
        scatangshift_flt = float (set_scatangshift)
        #print ('Time is during bed time')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_scatangshift_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_scatangshift_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt) > 0:
        scatangshift_flt = float (max_scatangshift_flt)
        #print ('Time is after bed')

    #This next bit takes the color temperature supplied above and figures out the appropriate blue and yellow values for use in the sunlight simulator
    #In a nutshell, this part finds the xy values for the main white color temperature and a somewhat warmer color temperature and then finds a blue point exactly opposite on the other side of the central white point from the warmer white point.
    #Lastly, the warm white point is shifted up to make it more yellow and the blue point shifted down to make it more blue by an angle that increases at sunrise and sunset
    white_CCT_str = str (CCT_int)
    yellow_CCT_str = str (CCT_int - scatdist_int)

    if int (white_CCT_str) > 1000: #These conditional statements ensure that the value for the lowest possible number is given rather than an error if the color temperature is too low, since the conversion module only defines color temperatures down to 1000K (pretty much the lowest temperature that produces any visible light)
        white_x_flt = float (x_transform_dict.get(white_CCT_str))
        white_y_flt = float (y_transform_dict.get(white_CCT_str))
    else:
        white_x_flt = float (x_transform_dict.get("1001"))
        white_y_flt = float (y_transform_dict.get("1001"))

    if int (yellow_CCT_str) > 1000:
        yellow_x_flt = float (x_transform_dict.get(yellow_CCT_str))
        yellow_y_flt = float (y_transform_dict.get(yellow_CCT_str))
    else:
        yellow_x_flt = float (x_transform_dict.get("1001"))
        yellow_y_flt = float (y_transform_dict.get("1001"))

    blue_x_flt = float (white_x_flt - (yellow_x_flt - white_x_flt))
    blue_y_flt = float (white_y_flt - (yellow_y_flt - white_y_flt))

    scatdist_x_flt = float (yellow_x_flt - white_x_flt)
    scatdist_y_flt = float (yellow_y_flt - white_y_flt)
    origang_deg_flt = float (math.degrees(math.atan(scatdist_y_flt/scatdist_x_flt)))

    yellow_x_shifted_flt = ((math.sqrt((scatdist_x_flt ** 2) + (scatdist_y_flt ** 2))) * (math.cos(math.radians(origang_deg_flt + scatangshift_flt)))) + (white_x_flt)
    yellow_y_shifted_flt = ((math.sqrt((scatdist_x_flt ** 2) + (scatdist_y_flt ** 2))) * (math.sin(math.radians(origang_deg_flt + scatangshift_flt)))) + (white_y_flt)

    blue_x_shifted_flt = float (white_x_flt - (yellow_x_shifted_flt - white_x_flt))
    blue_y_shifted_flt = float (white_y_flt - (yellow_y_shifted_flt - white_y_flt))
    
    CCT_mired_int = int (1000000*(1/CCT_int))

    #This next part consists of more of the logic that determines whether to output the maximum, current setting value, minimum, or current rising value for each final output based on the time of day.
    
    #Setting bright_yellow_int to appropriate value based on day segment
    if not float (hm - wake_time_flt + wake_offset_flt) > 0:
        bright_yellow_int = min_bright_yellow_int
        #print ('Time is before wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and not float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_yellow_flt) > 0:
        bright_yellow_int = rise_bright_yellow_int
        #print ('Time is during wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_yellow_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt + set_length_bright_yellow_flt) > 0:
        bright_yellow_int = max_bright_yellow_int
        #print ('Time is after wake up and before bed')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_yellow_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_bright_yellow_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt) > 0:
        bright_yellow_int = set_bright_yellow_int
        #print ('Time is during bed time')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_yellow_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_bright_yellow_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt) > 0:
        bright_yellow_int = min_bright_yellow_int
        #print ('Time is after bed')

    #Setting bright_blue_int to appropriate value based on day segment
    if not float (hm - wake_time_flt + wake_offset_flt) > 0:
        bright_blue_int = min_bright_blue_int
        #print ('Time is before wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and not float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_blue_flt) > 0:
        bright_blue_int = rise_bright_blue_int
        #print ('Time is during wake up')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_blue_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt + set_length_bright_blue_flt) > 0:
        bright_blue_int = max_bright_blue_int
        #print ('Time is after wake up and before bed')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_blue_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_bright_blue_flt) > 0 and not float (hm - bed_time_flt + bed_offset_flt) > 0:
        bright_blue_int = set_bright_blue_int
        #print ('Time is during bed time')

    elif float (hm - wake_time_flt + wake_offset_flt) > 0 and float (hm - wake_time_flt + wake_offset_flt - rise_length_bright_blue_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt + set_length_bright_blue_flt) > 0 and float (hm - bed_time_flt + bed_offset_flt) > 0:
        bright_blue_int = min_bright_blue_int
        #print ('Time is after bed')

    #Here is the final return command for the function that returns a list of the lighting parameters in the stated order
    return [bright_int, CCT_mired_int, bright_yellow_int, bright_blue_int, yellow_x_shifted_flt, yellow_y_shifted_flt, blue_x_shifted_flt, blue_y_shifted_flt]

TimeGiver()