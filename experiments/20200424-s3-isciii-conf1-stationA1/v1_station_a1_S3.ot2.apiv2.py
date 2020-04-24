from opentrons import protocol_api
from opentrons.drivers.rpi_drivers import gpio
import time
import math
import json
import os

# Metadata
metadata = {
    'protocolName': 'S3 Station C Version 1',
    'author': 'Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}

# Parameters to adapt the protocol
# Warning writing any Parameters below this line.
# It will be deleted if opentronsWeb is used.

NUM_SAMPLES = 96
BUFFER_LABWARE = 'opentrons plastic 30ml tubes'
DESTINATION_LABWARE = 'opentrons plastic 2ml tubes'
DEST_TUBE = '2ml tubes'
VOLUME_BUFFER = 300

# End Parameters to adapt the protocol

## global vars
robot = None
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

# Function definitions
def check_door():
    return gpio.read_window_switches()

def confirm_door_is_closed():
    #Check if door is opened
    if check_door() == False:
        #Set light color to red and pause
        gpio.set_button_light(1,0,0)
        robot.pause(f"Please, close the door")
        time.sleep(3)
        confirm_door_is_closed()
    else:
        #Set light color to green
        gpio.set_button_light(0,1,1)

def finish_run():
    #Set light color to blue
    gpio.set_button_light(0,0,1)


def retrieve_tip_info(pip,tipracks,file_path = '/data/A/tip_log.json'):
    global tip_log
    if not tip_log['count'] or pip not in tip_log['count']:
        if not robot.is_simulating():
            if os.path.isfile(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    if 'tips1000' in data:
                        tip_log['count'][pip] = data['tips1000']
                    elif 'tips300' in data:
                        tip_log['count'][pip] = data['tips300']
                    else:
                        tip_log['count'][pip] = 0
            else:
                tip_log['count'][pip] = 0
        else:
            tip_log['count'][pip] = 0

        if "8-Channel" in str(pip):
            tip_log['tips'][pip] =  [tip for rack in tipracks for tip in rack.rows()[0]]
        else:
            tip_log['tips'][pip] = [tip for rack in tipracks for tip in rack.wells()]

        tip_log['max'][pip] = len(tip_log['tips'][pip])

    return tip_log

## TODO MODIFY FOR NOT OVERRIDING tip_log.json
def save_tip_info(pip, file_path = '/data/A/tip_log.json'):
    if not robot.is_simulating():
        if "P1000" in str(pip):
            data = {'tips1000': tip_log['count'][pip]}
        elif "P300" in str(pip):
            data = {'tips300': tip_log['count'][pip]}

        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)

def pick_up(pip,tiprack):
    ## retrieve tip_log
    global tip_log
    if not tip_log:
        tip_log = {}
    tip_log = retrieve_tip_info(pip,tiprack)
    if tip_log['count'][pip] == tip_log['max'][pip]:
        robot.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
        pip.reset_tipracks()
        tip_log['count'][pip] = 0
    pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])
    tip_log['count'][pip] += 1

def transfer_buffer(bf_tube, dests, volume, pip,tiprack):
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
    pip.drop_tip(home_after=False)

# RUN PROTOCOL
def run(ctx: protocol_api.ProtocolContext):
    global robot
    robot = ctx
    # confirm door is close
    if not ctx.is_simulating():
        confirm_door_is_closed()

    # define tips
    tips1000 = [
        ctx.load_labware('opentrons_96_filtertiprack_1000ul', slot)
        for slot in ['3', '6']
    ]
    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '9')]

    # define pipettes
    p1000 = ctx.load_instrument('p1000_single_gen2', 'left', tip_racks=tips1000)
    p300 = ctx.load_instrument('p300_single_gen2', 'right', tip_racks=tips300)


    # check buffer labware type
    if BUFFER_LABWARE not in BUFFER_LW_DICT:
        raise Exception('Invalid BF_LABWARE. Must be one of the \
following:\nopentrons plastic 50ml tubes')

    # load mastermix labware
    buffer_rack = ctx.load_labware(
        BUFFER_LW_DICT[BUFFER_LABWARE], '10',
        BUFFER_LABWARE)

    # check mastermix tube labware type
    if DESTINATION_LABWARE not in DESTINATION_LW_DICT:
        raise Exception('Invalid DESTINATION_LABWARE. Must be one of the \
    following:\nopentrons plastic 2ml tubes')

    # load elution labware
    dest_racks = [
            ctx.load_labware(DESTINATION_LW_DICT[DESTINATION_LABWARE], slot,
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
        transfer_buffer(bf_tube, dests,VOLUME_BUFFER, p1000, tips1000)

    # track final used tip
    save_tip_info(p1000)

    finish_run()
