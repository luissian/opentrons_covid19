from opentrons import protocol_api
from opentrons.types import Point
from opentrons.drivers.rpi_drivers import gpio
import time
import math
import os
import subprocess
import json
from datetime import datetime


# metadata
metadata = {
    'protocolName': 'S3 Station A Protocol 3 lysates Version 1',
    'author': 'Nick <protocols@opentrons.com>, Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}


# Parameters to adapt the protocol
# Warning writing any Parameters below this line.
# It will be deleted if opentronsWeb is used.

NUM_SAMPLES = 96
LYSATE_LABWARE = 'opentrons plastic 2ml tubes'
PLATE_LABWARE = 'nest deep generic well plate'
VOLUME_LYSATE = 400
BEADS = False
LANGUAGE = 'esp'
RESET_TIPCOUNT = False

# End Parameters to adapt the protocol
ACTION = "StationA-protocol3-lysates"


## global vars
## initialize robot object
robot = None
# default var for drop tip switching
switch = True
# initialize tip_log dictionary
tip_log = {}
tip_log['count'] = {}
tip_log['tips'] = {}
tip_log['max'] = {}


# End Parameters to adapt the protocol

"""
NUM_SAMPLES is the number of samples, must be an integer number

LYSATE_LABWARE must be one of the following:
    opentrons plastic 2ml tubes

PLATE_LABWARE must be one of the following:
    opentrons deep generic well plate
    nest deep generic well plate
    vwr deep generic well plate
"""

LY_LW_DICT = {
    'opentrons plastic 2ml tubes': 'opentrons_24_tuberack_generic_2ml_screwcap'
}

PL_LW_DICT = {
    'opentrons deep generic well plate': 'usascientific_96_wellplate_2.4ml_deep',
    'nest deep generic well plate': 'nest_96_deepwellplate_2000ul',
    'vwr deep generic well plate': 'vwr_96_deepwellplate_2000ul'
}

LYSTUBE_LW_DICT = {
    # Radius of each possible tube
    '2ml tubes': 4
}

LANGUAGE_DICT = {
    'esp': 'esp',
    'eng': 'eng'
}

if LANGUAGE_DICT[LANGUAGE] == 'eng':
    VOICE_FILES_DICT = {
        'start': './data/sounds/started_process.mp3',
        'finish': './data/sounds/finished_process.mp3',
        'close_door': './data/sounds/close_door.mp3',
        'replace_tipracks': './data/sounds/replace_tipracks.mp3',
        'empty_trash': './data/sounds/empty_trash.mp3'
    }
elif LANGUAGE_DICT[LANGUAGE] == 'esp':
    VOICE_FILES_DICT = {
        'start': './data/sounds/started_process_esp.mp3',
        'finish': './data/sounds/finished_process_esp.mp3',
        'close_door': './data/sounds/close_door_esp.mp3',
        'replace_tipracks': './data/sounds/replace_tipracks_esp.mp3',
        'empty_trash': './data/sounds/empty_trash_esp.mp3'
    }

# Function definitions
def run_info(start, end):
    import requests
    info = {}


    # URL = "localhost:8001/api/robots/createUsage"

    '''
    hostname = subprocess.run(
        ['hostname'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).stdout.decode('utf-8').rstrip()

    info["RobotID"] = hostname
    '''
    info["RobotID"] = os.uname()[1]
    #info["RobotID"] = 'S3-A1'
    info["executedAction"] = ACTION
    info["ProtocolID"] = PROTOCOL_ID
    info["StartRunTime"] = start
    info["FinishRunTime"] = end
    info["parameters"] = parameters = {
        "NUM_SAMPLES" : NUM_SAMPLES,
        "LYSATE_LABWARE" : LYSATE_LABWARE,
        "PLATE_LABWARE" : PLATE_LABWARE,
        "VOLUME_LYSATE" : VOLUME_LYSATE,
        "BEADS" : BEADS,
        "LANGUAGE" : LANGUAGE,
        "RESET_TIPCOUNT" : RESET_TIPCOUNT
    }

    #data = json.dumps(info)
    #url = "http://localhost:8001/api/robots/createUsage"
    headers = {'Content-type': 'application/json'}
    url_https = 'https://' + URL
    url_http = 'http://' + URL
    try:
        r = requests.post(url_https, data=json.dumps(info), headers=headers)
    except:
        try:
            r = requests.post(url_http, data=json.dumps(info), headers=headers)
        except:
            print('No communication to server')
            # write information to log
            return
    if r.status_code > 201 :
        print('error formato  \n\n\n')
        # write info dictionary to log



def check_door():
    return gpio.read_window_switches()

def confirm_door_is_closed():
    if not robot.is_simulating():
        #Check if door is opened
        if check_door() == False:
            #Set light color to red and pause
            gpio.set_button_light(1,0,0)
            robot.pause()
            voice_notification('close_door')
            time.sleep(5)
            confirm_door_is_closed()
        else:
            #Set light color to green
            gpio.set_button_light(0,1,0)

def start_run():
    voice_notification('start')
    gpio.set_button_light(0,1,0)
    now = datetime.now()
    # dd/mm/YY H:M:S
    start_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return start_time

def finish_run():
    voice_notification('finish')
    #Set light color to blue
    gpio.set_button_light(0,0,1)
    now = datetime.now()
    # dd/mm/YY H:M:S
    finish_time = now.strftime("%Y/%m/%d %H:%M:%S")
    return finish_time

def voice_notification(action):
    if not robot.is_simulating():
        fname = VOICE_FILES_DICT[action]
        if os.path.isfile(fname) is True:
                subprocess.run(
                ['mpg123', fname],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
                )
        else:
            robot.comment(f"Sound file does not exist. Call the technician")

def reset_tipcount(file_path = '/data/A/tip_log.json'):
    if os.path.isfile(file_path):
        os.remove(file_path)

def retrieve_tip_info(pip,tipracks,file_path = '/data/A/tip_log.json'):
    global tip_log
    if not tip_log['count'] or pip not in tip_log['count']:
        tip_log['count'][pip] = 0
        if not robot.is_simulating():
            if os.path.isfile(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    if 'P1000' in str(pip):
                        tip_log['count'][pip] = data['tips1000']
                    elif 'P300' in str(pip):
                        tip_log['count'][pip] = data['tips300']
                    elif 'P20' in str(pip):
                        tip_log['count'][pip] = data['tips20']

        if "8-Channel" in str(pip):
            tip_log['tips'][pip] =  [tip for rack in tipracks for tip in rack.rows()[0]]
        else:
            tip_log['tips'][pip] = [tip for rack in tipracks for tip in rack.wells()]

        tip_log['max'][pip] = len(tip_log['tips'][pip])

    return tip_log

def save_tip_info(file_path = '/data/A/tip_log.json'):
    data = {}
    if not robot.is_simulating():
        if os.path.isfile(file_path):
            os.rename(file_path,file_path + ".bak")
        for pip in tip_log['count']:
            if "P1000" in str(pip):
                data['tips1000'] = tip_log['count'][pip]
            elif "P300" in str(pip):
                data['tips300'] = tip_log['count'][pip]
            elif "P20" in str(pip):
                data['tips20'] = tip_log['count'][pip]

        with open(file_path, 'a+') as outfile:
            json.dump(data, outfile)

def pick_up(pip,tiprack):
    if tip_log['count'][pip] == tip_log['max'][pip]:
        voice_notification('replace_tipracks')
        robot.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
        confirm_door_is_closed()
        pip.reset_tipracks()
        tip_log['count'][pip] = 0
    pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])
    tip_log['count'][pip] += 1

def drop(pip):
    global switch
    if "8-Channel" not in str(pip):
        side = 1 if switch else -1
        drop_loc = robot.loaded_labwares[12].wells()[0].top().move(Point(x=side*20))
        pip.drop_tip(drop_loc,home_after=False)
        switch = not switch
    else:
        drop_loc = robot.loaded_labwares[12].wells()[0].top().move(Point(x=20))
        pip.drop_tip(drop_loc,home_after=False)

def transfer_samples(sources, dests, pip, tiprack):
    # height for aspiration has to be different depending if you ar useing tubes or wells
    if 'strip' in LYSATE_LABWARE or 'plate' in LYSATE_LABWARE:
        height = 1.5
    else:
        height = 2
    # transfer
    for s, d in zip(sources, dests):
        pick_up(pip,tiprack)
        pip.transfer(VOLUME_LYSATE, s.bottom(height), d.bottom(15), air_gap=20, new_tip='never')
        if BEADS:
            pip.mix(3,400,d.bottom(4))
        #pip.blow_out(d.top(-2))
        pip.aspirate(50, d.top(-2))
        drop(pip)

# RUN PROTOCOL
def run(ctx: protocol_api.ProtocolContext):
    global robot
    robot = ctx

    # check if tipcount is being reset
    if RESET_TIPCOUNT:
        reset_tipcount()

    # confirm door is closed
    robot.comment(f"Please, close the door")
    confirm_door_is_closed()

    # Begin run
    start_time = start_run()

    tips1000 = [robot.load_labware('opentrons_96_filtertiprack_1000ul',
                                     3, '1000µl tiprack')]

    # load pipette
    p1000 = robot.load_instrument(
        'p1000_single_gen2', 'left', tip_racks=tips1000)

    ## retrieve tip_log
    retrieve_tip_info(p1000,tips1000)

    # check source (LYSATE) labware type
    if LYSATE_LABWARE not in LY_LW_DICT:
        raise Exception('Invalid LYSATE_LABWARE. Must be one of the \
following:\nopentrons plastic 2ml tubes')
    # load LYSATE labware
    if 'plate' in LYSATE_LABWARE:
        source_racks = robot.load_labware(
            LY_LW_DICT[LYSATE_LABWARE], '1',
            'RNA LYSATE labware')
    else:
        source_racks = [
            robot.load_labware(LY_LW_DICT[LYSATE_LABWARE], slot,
                            'sample LYSATE labware ' + str(i+1))
            for i, slot in enumerate(['4', '1', '5', '2'])
    ]

    # check plate
    if PLATE_LABWARE not in PL_LW_DICT:
        raise Exception('Invalid PLATE_LABWARE. Must be one of the \
following:\nopentrons deep generic well plate\nnest deep generic well plate\nvwr deep generic well plate')

    # load pcr plate
    wells_plate = robot.load_labware(PL_LW_DICT[PLATE_LABWARE], 10,
                    'sample LYSATE well plate ')

    # setup samples
    #sources, dests = get_source_dest_coordinates(LYSATE_LABWARE, source_racks, wells_plate)
    #sources = [tube for s in source_racks for tube in s.wells()][:NUM_SAMPLES]
    sources = []
    for i in range(0,24,4):
        for rack in source_racks[:2]:
            sources = sources + rack.wells()[i:i+4]

    for i in range(0,24,4):
        for rack in source_racks[2:5]:
            sources = sources + rack.wells()[i:i+4]

    sources = sources[:NUM_SAMPLES]
    dests = wells_plate.wells()[:NUM_SAMPLES]

    # transfer
    transfer_samples(sources, dests, p1000, tips1000)

    # track final used tip
    save_tip_info()

    finish_time = finish_run()
    '''
    par = {
        "NUM_SAMPLES" : NUM_SAMPLES,
        "LYSATE_LABWARE" : LYSATE_LABWARE,
        "PLATE_LABWARE" : PLATE_LABWARE,
        "VOLUME_LYSATE" : VOLUME_LYSATE,
        "BEADS" : BEADS,
        "LANGUAGE" : LANGUAGE,
        "RESET_TIPCOUNT" : RESET_TIPCOUNT
    }
    '''
    run_info(start_time, finish_time)
