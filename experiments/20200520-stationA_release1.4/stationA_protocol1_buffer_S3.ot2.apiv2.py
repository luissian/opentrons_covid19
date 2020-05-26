from opentrons import protocol_api
from opentrons.types import Point
from opentrons.drivers.rpi_drivers import gpio
import time
import math
import os
import subprocess
import json
from datetime import datetime


# Metadata
metadata = {
    'protocolName': 'S3 Station A Protocol 1 buffer Version 1',
    'author': 'Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}

# Parameters to adapt the protocol
# Warning writing any Parameters below this line.
# It will be deleted if opentronsWeb is used.

NUM_SAMPLES = 16
BUFFER_LABWARE = 'opentrons plastic 30ml tubes'
DESTINATION_LABWARE = 'opentrons plastic 2ml tubes'
DEST_TUBE = '2ml tubes'
VOLUME_BUFFER = 300
LANGUAGE = 'esp'
RESET_TIPCOUNT = False

# End Parameters to adapt the protocol
ACTION = "StationA-protocol1-buffer"
PROTOCOL_ID = "0000-AA"

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

"""
NUM_SAMPLES is the number of samples, must be an integer number

BUFFER_LABWARE must be one of the following:
    opentrons plastic 50ml tubes
    opentrons plastic 30ml tubes

DESTINATION_LABWARE must be one of the following:
    opentrons plastic 2ml tubes

DEST_TUBE
    2m tubes
"""


# Constants
BUFFER_LW_DICT = {
    'opentrons plastic 50ml tubes': 'opentrons_6_tuberack_falcon_50ml_conical',
    'opentrons plastic 30ml tubes': 'opentrons_6_tuberack_generic_30ml_conical'
}

DESTINATION_LW_DICT = {
    'opentrons plastic 2ml tubes': 'opentrons_24_tuberack_generic_2ml_screwcap',
}

DESTUBE_LW_DICT = {
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
def run_info(start, end, parameters = dict()):
    info = {}
    hostname = subprocess.run(
        ['hostname'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    ).stdout.decode('utf-8')

    info["RobotID"] = hostname
    info["executedAction"] = ACTION
    info["ProtocolID"] = PROTOCOL_ID
    info["StartRunTime"] = start
    info["FinishRunTime"] = end
    info["parameters"] = parameters
    # write json to file. This is going to be an api post.
    #with open('run.json', 'w') as fp:
        #json.dump(info, fp,indent=4)


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

def transfer_buffer(bf_tube, dests, pip,tiprack):
    max_trans_per_asp = 3  # 1000/VOLUME_BUFFER = 3
    split_ind = [ind for ind in range(0, len(dests), max_trans_per_asp)]
    dest_sets = [dests[split_ind[i]:split_ind[i+1]]
             for i in range(len(split_ind)-1)] + [dests[split_ind[-1]:]]
    pick_up(pip,tiprack)
    pip.mix(3, 800, bf_tube.bottom(2))
    for set in dest_sets:
        pip.aspirate(50, bf_tube.bottom(2))
        pip.distribute(VOLUME_BUFFER, bf_tube.bottom(2), [d.bottom(10) for d in set],
                   air_gap=3, disposal_volume=0, new_tip='never')
        pip.dispense(50,bf_tube.top(-20))
    drop(pip)

# RUN PROTOCOL
def run(ctx: protocol_api.ProtocolContext):
    global robot
    robot = ctx

    # check if tipcount is being reset
    if RESET_TIPCOUNT:
        reset_tipcount()

    # confirm door is close
    robot.comment(f"Please, close the door")
    confirm_door_is_closed()

    # Begin run
    start_time = start_run()

    # define tips
    tips1000 = [robot.load_labware('opentrons_96_filtertiprack_1000ul',
                                     3, '1000µl tiprack')]

    # define pipettes
    p1000 = robot.load_instrument('p1000_single_gen2', 'left', tip_racks=tips1000)

    # Retrieve tip log
    retrieve_tip_info(p1000,tips1000)
    # check buffer labware type
    if BUFFER_LABWARE not in BUFFER_LW_DICT:
        raise Exception('Invalid BF_LABWARE. Must be one of the \
following:\nopentrons plastic 50ml tubes')

    # load mastermix labware
    buffer_rack = robot.load_labware(
        BUFFER_LW_DICT[BUFFER_LABWARE], '10',
        BUFFER_LABWARE)

    # check mastermix tube labware type
    if DESTINATION_LABWARE not in DESTINATION_LW_DICT:
        raise Exception('Invalid DESTINATION_LABWARE. Must be one of the \
    following:\nopentrons plastic 2ml tubes')

    # load elution labware
    dest_racks = [
            robot.load_labware(DESTINATION_LW_DICT[DESTINATION_LABWARE], slot,
                            'Destination tubes labware ' + str(i+1))
            for i, slot in enumerate(['4', '1', '5', '2'])
    ]

    # setup sample sources and destinations
    bf_tubes = buffer_rack.wells()[:4]
    number_racks = math.ceil(NUM_SAMPLES/len(dest_racks[0].wells()))

    # dest_sets is a list of lists. Each list is the destination well for each rack
    # example: [[tube1,tube2,...tube24](first rack),[tube1,tube2(second rack),...]
    dest_sets = [
        [tube
         for rack in dest_racks
         for tube in rack.wells()
        ][:NUM_SAMPLES][i*len(dest_racks[0].wells()):(i+1)*len(dest_racks[0].wells())]
        for i in range(number_racks)
        ]

    # transfer buffer to tubes
    for bf_tube,dests in zip(bf_tubes,dest_sets):
        transfer_buffer(bf_tube, dests, p1000, tips1000)

    # track final used tip
    save_tip_info()

    finish_time = finish_run()

    par = {
        "NUM_SAMPLES" : NUM_SAMPLES,
        "BUFFER_LABWARE" : BUFFER_LABWARE,
        "DESTINATION_LABWARE" : DESTINATION_LABWARE,
        "DEST_TUBE" : DEST_TUBE,
        "VOLUME_BUFFER" : VOLUME_BUFFER,
        "LANGUAGE" : LANGUAGE,
        "RESET_TIPCOUNT" : RESET_TIPCOUNT
    }

    run_info(start_time, finish_time, par)
