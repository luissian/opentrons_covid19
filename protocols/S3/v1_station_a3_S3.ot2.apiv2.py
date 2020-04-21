from opentrons import protocol_api
from opentrons.drivers.rpi_drivers import gpio
import time
import math
import json
import os

# metadata
metadata = {
    'protocolName': 'S3 Station A Version 1',
    'author': 'Nick <protocols@opentrons.com>, Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.2'
}


# Parameters to adapt the protocol
NUM_SAMPLES = 96
BEADS_LABWARE = 'opentrons plastic 50 ml tubes'
PLATE_LABWARE = 'opentrons deep generic well plate'
VOLUME_BEADS = 400

## global vars
robot = None
tip_log = {}
tip_log['count'] = {}
tip_log['tips'] = {}
tip_log['max'] = {}

"""
NUM_SAMPLES is the number of samples, must be an integer number

BEADS_LABWARE must be one of the following:
    opentrons plastic 50 ml tubes

PLATE_LABWARE must be one of the following:
    opentrons deep generic well plate
    nest deep generic well plate
    vwr deep generic well plate
"""

BD_LW_DICT = {
    'opentrons plastic 50 ml tubes': 'opentrons_6_tuberack_falcon_50ml_conical'
}

PL_LW_DICT = {
    'opentrons deep generic well plate': 'usascientific_96_wellplate_2.4ml_deep',
    'nest deep generic well plate': 'usascientific_96_wellplate_2.4ml_deep',
    'vwr deep generic well plate': 'usascientific_96_wellplate_2.4ml_deep'
}

# Function definitions
def check_door():
    return gpio.read_window_switches()

def confirm_door_is_closed(ctx):
    #Check if door is opened
    if check_door() == False:
        #Set light color to red and pause
        gpio.set_button_light(1,0,0)
        ctx.pause(f"Please, close the door")
        time.sleep(3)
        confirm_door_is_closed(ctx)
    else:
        #Set light color to green
        gpio.set_button_light(0,1,0)

def finish_run():
    #Set light color to blue
    gpio.set_button_light(0,0,1)

def retrieve_tip_info(pip,tipracks,file_path = '/data/A/tip_log.json'):
    global tip_log
    if not tip_log or pip not in tip_log['count']:
        if not robot.is_simulating():
            if os.path.isfile(file_path):
                with open(file_path) as json_file:
                    data = json.load(json_file)
                    if 'tips1000' in data:
                        tip_log['count'][pip] = data['tips1000']
                    else:
                        tip_log['count'][pip] = 0
                    if 'tips300' in data:
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

def prepare_beads(bd_tube,eth_tubes,pip,tiprack):
    pick_up(pip,tiprack)
    # Mix beads
    pip.mix(10,300,bd_tube.bottom(2))
    # Dispense beads
    for e in eth_tubes:
        if not pip.hw_pipette['has_tip']:
            pick_up(pip,tiprack)
        pip.transfer(400, bd_tube.bottom(2),e.top(-20),new_tip='never')
        pip.mix(10,300,e.bottom(2))
        pip.drop_tip()

def transfer_beads(beads_tube, dests, volume, pip,tiprack):
    max_trans_per_asp = 2  # 1000/VOLUME_BUFFER = 3
    split_ind = [ind for ind in range(0, len(dests), max_trans_per_asp)]
    dest_sets = [dests[split_ind[i]:split_ind[i+1]]
             for i in range(len(split_ind)-1)] + [dests[split_ind[-1]:]]
    pick_up(pip,tiprack)
    for set in dest_sets:
        pip.aspirate(50, beads_tube.bottom(2))
        pip.distribute(volume, beads_tube.bottom(2), [d.bottom(10) for d in set],
                   air_gap=10, disposal_volume=0, new_tip='never')
        pip.blow_out(beads_tube.top(-20))
    pip.drop_tip()

# RUN PROTOCOL
def run(ctx: protocol_api.ProtocolContext):
    global robot
    robot = ctx

    # confirm door is closed
    if not ctx.is_simulating():
        confirm_door_is_closed(ctx)

    tips1000 = [ctx.load_labware('opentrons_96_filtertiprack_1000ul',
                                     slot, '1000µl tiprack')
                    for slot in ['3', '6', '9', '8']]

    # load pipette
    p1000 = ctx.load_instrument(
        'p1000_single_gen2', 'left', tip_racks=tips1000)

    # check source (elution) labware type
    if BEADS_LABWARE not in BD_LW_DICT:
        raise Exception('Invalid BF_LABWARE. Must be one of the \
following:\nopentrons plastic 50ml tubes')

    # load mastermix labware
    beads_rack = ctx.load_labware(
        BD_LW_DICT[BEADS_LABWARE], '7',
        BEADS_LABWARE)

    # check plate
    if PLATE_LABWARE not in PL_LW_DICT:
        raise Exception('Invalid PLATE_LABWARE. Must be one of the \
following:\nopentrons deep generic well plate\nnest deep generic well plate\nvwr deep generic well plate')

    # load pcr plate
    wells_plate = ctx.load_labware(PL_LW_DICT[PLATE_LABWARE], 10,
                    'sample elution well plate ')

    # prepare beads
    # One tube for each 24 samples
    num_tubes = math.ceil(NUM_SAMPLES/24)
    # How many wells for each tube
    num_wells = math.ceil(len(wells_plate.wells())/4)

    beads = beads_rack.wells()[0]
    ethanol = beads_rack.wells()[1:5][:num_tubes]

    prepare_beads(beads,ethanol,p1000,tips1000)

    # setup dests
    ethanol = beads_rack.wells()[1:5][:num_tubes]
    # Prepare destinations, a list of destination
    # compose of lists of 24, each 24 is for one tube until end of samples.
    # example: [[A1,B1,C1...G3,H3],[A4,B4..G4,H4],...]
    dest_sets = [
        [well
         for well in wells_plate.wells()
        ][:NUM_SAMPLES][i*num_wells:(i+1)*num_wells]
        for i in range(num_tubes)
        ]

    # transfer
    for bd_tube,dests in zip(ethanol,dest_sets):
        transfer_beads(bd_tube, dests,VOLUME_BEADS, p1000, tips1000)

    # track final used tip
    save_tip_info(p1000)

    finish_run()
