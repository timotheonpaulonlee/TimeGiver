#This sample script uses TimeGiver to generate schedules for lights in 3 different rooms with slightly different parameters, 1 of them with the blue-yellow feature and 2 without it.
#It uses the phue Philips Hue Python SDK available at https://github.com/studioimaginaire/phue and python's APScheduler package
#The scheduler sets the lights up to change every 3 seconds, but only when they are on, and an override feature is included to ensure that control panels can be used to override scheduled brightness levels when more light is needed urgently.
from phue import Bridge #imports phue Hue Python SDK
b = Bridge('10.0.0.64') #LAN IP Address for Hue bridge
b.connect() #deals with user authorization, requiring button press on first run

##APScheduler and Time Imports
from datetime import datetime 
import os 
from apscheduler.schedulers.blocking import BlockingScheduler

def kitchenlightchanger():
    from TimeGiver import TimeGiver 
    lighting_parameters = TimeGiver (bed_time = "1260", wake_time = "360", max_CCT = "7500", min_CCT = "4000")
    bright_int = lighting_parameters[0]
    CCT_mired_int = lighting_parameters[1]
    bright_yellow_int = lighting_parameters[2]
    bright_blue_int = lighting_parameters[3]
    white_x_flt = lighting_parameters[4]
    white_y_flt = lighting_parameters[5]
    yellow_x_shifted_flt = lighting_parameters[6]
    yellow_y_shifted_flt = lighting_parameters[7]
    blue_x_shifted_flt = lighting_parameters[8]
    blue_y_shifted_flt = lighting_parameters[9]
    #print (lighting_parameters[0])

    lights = ["None"]
    lights_yellow = ["Kitchen White"]
    lights_blue =["Kitchen Blue"] 
    blue_yellow_active = "true"
    override_1 = b.get_sensor (137, "state")
    overridebutton_1 = str (override_1["buttonevent"])
    override_2 = b.get_sensor (51, "state")
    overridebutton_2 = str (override_2["buttonevent"])
    trans_time = int (40)

    if "100" not in overridebutton_1 and "400" not in overridebutton_1:
        print ("Override Activated")

    elif "100" not in overridebutton_2 and "400" not in overridebutton_2:
        print ("Override Activated")

    elif "true" in blue_yellow_active:
        b.set_light(lights_yellow, 'bri', bright_yellow_int, transitiontime=trans_time) #applies brightness based on time of day
        b.set_light(lights_blue, 'bri', bright_blue_int, transitiontime=trans_time)
        b.set_light(lights_yellow, 'xy', value=[yellow_x_shifted_flt, yellow_y_shifted_flt], transitiontime=trans_time)
        b.set_light(lights_blue, 'xy', value=[blue_x_shifted_flt, blue_y_shifted_flt], transitiontime=trans_time)
        #print ("blue-yellow activated")

    else: 
        b.set_light(lights, 'bri', bright_int, transitiontime=trans_time) #applies brightness based on time of day
        b.set_light(lights, 'ct', CCT_mired_int, transitiontime=trans_time)
        #print ("Lights Changed")

def bathroomlightchanger():
    from TimeGiver import TimeGiver 
    lighting_parameters = TimeGiver (bed_time = "1260", wake_time = "360", max_CCT = "6000", min_CCT = "2700")
    bright_int = lighting_parameters[0]
    CCT_mired_int = lighting_parameters[1]
    bright_yellow_int = lighting_parameters[2]
    bright_blue_int = lighting_parameters[3]
    yellow_x_shifted_flt = lighting_parameters[4]
    yellow_y_shifted_flt = lighting_parameters[5]
    blue_x_shifted_flt = lighting_parameters[6]
    blue_y_shifted_flt = lighting_parameters[7]
    #print (lighting_parameters[0])

    lights = ["Bathroom Left", "Bathroom Middle", "Bathroom Right"]
    blue_yellow_active = "false"
    lights_yellow = ["None"]
    lights_blue =["None"] 
    override_1 = b.get_sensor (150, "state")
    overridebutton_1 = str (override_1["buttonevent"])
    trans_time = int (40)

    if "100" not in overridebutton_1 and "400" not in overridebutton_1:
        print ("Override Activated")

    elif "true" in blue_yellow_active:
        b.set_light(lights_yellow, 'bri', bright_yellow_int, transitiontime=trans_time) #applies brightness based on time of day
        b.set_light(lights_blue, 'bri', bright_blue_int, transitiontime=trans_time)
        b.set_light(lights_yellow, 'xy', value=[yellow_x_shifted_flt, yellow_y_shifted_flt], transitiontime=trans_time)
        b.set_light(lights_blue, 'xy', value=[blue_x_shifted_flt, blue_y_shifted_flt], transitiontime=trans_time)
        #print ("blue-yellow activated")

    else: 
        b.set_light(lights, 'bri', bright_int, transitiontime=trans_time) #applies brightness based on time of day
        b.set_light(lights, 'ct', CCT_mired_int, transitiontime=trans_time)
        #print ("Lights Changed")


def dawncasterlightchanger():
    from TimeGiver import TimeGiver 
    lighting_parameters = TimeGiver (bed_time = "1260", wake_time = "360", max_CCT = "6000", min_CCT = "2700")
    bright_int = lighting_parameters[0]
    CCT_mired_int = lighting_parameters[1]
    bright_yellow_int = lighting_parameters[2]
    bright_blue_int = lighting_parameters[3]
    yellow_x_shifted_flt = lighting_parameters[4]
    yellow_y_shifted_flt = lighting_parameters[5]
    blue_x_shifted_flt = lighting_parameters[6]
    blue_y_shifted_flt = lighting_parameters[7]
    #print (lighting_parameters[0])

    lights = ["Dawncaster"]
    lights_yellow = ["None"]
    lights_blue =["None"] 
    blue_yellow_active = "false"
    override_1 = b.get_sensor (142, "state")
    overridebutton_1 = str (override_1["buttonevent"])
    trans_time = int (200)

    if "100" not in overridebutton_1 and "400" not in overridebutton_1:
        print ("Override Activated")

    elif "true" in blue_yellow_active:
        b.set_light(lights_yellow, 'bri', bright_yellow_int, transitiontime=trans_time) #applies brightness based on time of day
        b.set_light(lights_blue, 'bri', bright_blue_int, transitiontime=trans_time)
        b.set_light(lights_yellow, 'xy', value=[yellow_x_shifted_flt, yellow_y_shifted_flt], transitiontime=trans_time)
        b.set_light(lights_blue, 'xy', value=[blue_x_shifted_flt, blue_y_shifted_flt], transitiontime=trans_time)
        #print ("blue-yellow activated")

    else: 
        b.set_light(lights, 'bri', bright_int, transitiontime=trans_time) #applies brightness based on time of day
        b.set_light(lights, 'ct', CCT_mired_int, transitiontime=trans_time)
        #print ("Lights Changed")

def tick():
    kitchenlightchanger()
    dawncasterlightchanger()
    bathroomlightchanger()

##APScheduler 
if __name__ == '__main__':
    scheduler = BlockingScheduler()
    scheduler.add_executor('processpool')
    scheduler.add_job(tick, 'interval', seconds=3) #Time interval between process running
    print('Press Ctrl+{0} to exit'.format('Break' if os.name == 'nt' else 'C'))

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass