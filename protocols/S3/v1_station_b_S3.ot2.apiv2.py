from opentrons.types import Point
from opentrons.drivers.rpi_drivers import gpio
from opentrons import protocol_api
import os
import json
import math
import time

# metadata
metadata = {
    'protocolName': 'S3 Station B Version 2',
    'author': 'Nick <protocols@opentrons.com> Sara <smonzon@isciii.es> Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.0'
}

"""
REAGENT SETUP:
- slot 7 12-channel reservoir:
    - elution buffer: channel 1
    - magnetic beads: channel 2
    - bead buffer: channels 3-5
    - wash 1: channels 6-7
    - wash 2: channels 8-9
    - wash 3: channels 10-11
- slot 11 single-channel reservoir:
    - empty reservoir for liquid waste (supernatant removals)
"""

# Parameters to adapt the protocol
NUM_SAMPLES = 48
REAGENT_LABWARE = 'nest 12 reservoir plate'
MAGPLATE_LABWARE = 'nest deep well plate'
WASTE_LABWARE = 'nest 1 reservoir plate'
ELUTION_LABWARE = 'opentrons aluminum biorad plate'
TIP_TRACK = True

## global vars
robot = None
tip_log = {}
tip_log['count'] = {}
tip_log['tips'] = {}
tip_log['max'] = {}

"""
NUM_SAMPLES is the number of samples, must be an integer number

REAGENT_LABWARE must be one of the following:
    nest 12 reservoir plate

MAGPLATE_LABWARE must be one of the following:
    nest deep well plate

WASTE labware
    nest 1 reservoir plate
ELUTION_LABWARE
    opentrons aluminum biorad plate
"""


# Constants
REAGENT_LW_DICT = {
    'nest 12 reservoir plate': 'nest_12_reservoir_15ml'
}

MAGPLATE_LW_DICT = {
    'nest deep well plate': 'usascientific_96_wellplate_2.4ml_deep'
}

WASTE_LW_DICT = {
    # Radius of each possible tube
    'nest 1 reservoir plate': 'nest_1_reservoir_195ml'
}

ELUTION_LW_DICT = {
    'opentrons aluminum biorad plate': 'opentrons_96_aluminumblock_nest_wellplate_100ul'
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


def retrieve_tip_info(pip,tipracks,file_path = '/data/B/tip_log.json'):
    ## TODO if tip_log already have data, append instead of statement.
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

        if pip in '':
            tip_log['tips'][pip] = [tip for rack in tipracks for tip in rack.wells()]
            tip_log['max'][pip] = len(tip_log['tips'][pip])
        else:


    return tip_log

def save_tip_info(pip, file_path = '/data/B/tip_log.json'):
    if not robot.is_simulating():
        data = {'tips1000': tip_log['count'][pip]}
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
    tip_log['count'][pip] += 1
    pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])

def run(ctx: protocol_api.ProtocolContext):
    global robot
    robot = ctx

    # confirm door is close
    if not ctx.is_simulating():
        confirm_door_is_closed()

    # load labware and modules
    ## ELUTION LABWARE
    #tempdeck = ctx.load_module('tempdeck', '1')
    if ELUTION_LABWARE not in ELUTION_LW_DICT:
        raise Exception('Invalid ELUTION_LABWARE. Must be one of the \
    following:\nopentrons aluminum biorad plate')

    elution_plate = ctx.load_labware(
        ELUTION_LW_DICT[ELUTION_LABWARE], '1',
        'elution plate')

    ## MAGNETIC PLATE LABWARE
    magdeck = ctx.load_module('magdeck', '10')
    magdeck.disengage()

    if MAGPLATE_LABWARE not in MAGPLATE_LW_DICT:
        raise Exception('Invalid MAGPLATE_LABWARE. Must be one of the \
    following:\nnest deep well plate')

    magplate = magdeck.load_labware(MAGPLATE_LW_DICT[MAGPLATE_LABWARE])

    ## WASTE LABWARE
    if WASTE_LABWARE not in WASTE_LW_DICT:
        raise Exception('Invalid WASTE_LABWARE. Must be one of the \
    following:\nnest 1 reservoir plate')

    waste = ctx.load_labware(
        WASTE_LW_DICT[WASTE_LABWARE], '11', 'waste reservoir').wells()[0].top()

    ## REAGENT RESERVOIR
    if REAGENT_LABWARE not in REAGENT_LW_DICT:
        raise Exception('Invalid REAGENT_LABWARE. Must be one of the \
    following:\nnest 12 reservoir plate')

    reagent_res = ctx.load_labware(
        REAGENT_LW_DICT[REAGENT_LABWARE], '7', 'reagent reservoir')

    ## TIPS
    # using standard tip definition despite actually using filter tips
    # so that the tips can accommodate ~220µl per transfer for efficiency
    tips300 = [
        ctx.load_labware(
            'opentrons_96_tiprack_300ul', slot, '200µl filter tiprack')
        for slot in ['2', '3', '5', '6', '9']
    ]
    tips1000 = [
        ctx.load_labware('opentrons_96_filtertiprack_1000ul', slot,
                         '1000µl filter tiprack')
        for slot in ['8', '4']
    ]

    # reagents and samples
    num_cols = math.ceil(NUM_SAMPLES/8)
    mag_samples_m = magplate.rows()[0][:num_cols]
    mag_samples_s = magplate.wells()[:NUM_SAMPLES]
    elution_samples_m = elution_plate.rows()[0][:num_cols]

    elution_buffer = reagent_res.wells()[0]
    beads = reagent_res.wells()[1]
    bead_buffer = reagent_res.wells()[2:5]
    wash_sets = [reagent_res.wells()[i:i+2] for i in [5, 7, 9]]

    # pipettes
    m300 = ctx.load_instrument('p300_multi_gen2', 'right', tip_racks=tips300)
    p1000 = ctx.load_instrument('p1000_single_gen2', 'left',
                                tip_racks=tips1000)
    m300.flow_rate.aspirate = 150
    m300.flow_rate.dispense = 300
    m300.flow_rate.blow_out = 300
    p1000.flow_rate.aspirate = 100
    p1000.flow_rate.dispense = 1000
    p1000.flow_rate.blow_out = 1000

    # mix beads and add to buffer
    bead_dests = bead_buffer[:math.ceil(num_cols/4)]
    pick_up(m300,tips300)
    m300.mix(5, 200, beads)
    m300.transfer(200, beads, bead_dests, new_tip='never', air_gap=20)

    # premix, transfer, and mix magnetic beads with sample
    for d in bead_dests:
        for _ in range(5):
            m300.aspirate(200, d.bottom(3))
            m300.dispense(200, d.bottom(20))

    for i, m in enumerate(mag_samples_m):
        if not m300.hw_pipette['has_tip']:
            pick_up(m300,tips300)
        m300.transfer(400, bead_buffer[i//4], m.bottom(5), new_tip='never', air_gap=20)
        m300.mix(5, 200, m.bottom(5))
        m300.blow_out(m.top(-2))
        m300.drop_tip()

    # incubate off and on magnet
    ctx.delay(minutes=5, msg='Incubating off magnet for 5 minutes.')
    magdeck.engage()
    ctx.delay(minutes=5, msg='Incubating on magnet for 5 minutes.')

    # remove supernatant with P1000
    for i, m in enumerate(mag_samples_s):
        side = -1 if (i % 8) % 2 == 0 else 1
        loc = m.bottom(5).move(Point(x=side*2))
        pick_up(p1000,tips1000)
        p1000.move_to(m.center())
        p1000.transfer(900, loc, waste, air_gap=100, new_tip='never')
        p1000.blow_out(waste)
        p1000.drop_tip()

    # 3x washes
    for wash_set in wash_sets:
        for i, m in enumerate(mag_samples_m):
            # transfer and mix wash with beads
            magdeck.disengage()
            wash_chan = wash_set[i//6]
            side = 1 if i % 2 == 0 else -1
            disp_loc = m.bottom(5).move(Point(x=side*2))
            asp_loc = m.bottom(5).move(Point(x=-1*side*2))
            pick_up(m300,tips300)
            m300.transfer(
                200, wash_chan, m.center(), new_tip='never', air_gap=20)
            m300.mix(5, 175, disp_loc)
            m300.move_to(m.top(-20))

            magdeck.engage()
            ctx.delay(seconds=20, msg='Incubating on magnet for 20 seconds.')

            # remove supernatant
            m300.transfer(200, asp_loc, waste, new_tip='never', air_gap=20)
            m300.drop_tip()

    ctx.delay(minutes=5, msg='Airdrying for 5 minutes.')

    # elute samples
    for i, (m, e) in enumerate(zip(mag_samples_m, elution_samples_m)):
        # tranfser and mix elution buffer with beads
        magdeck.disengage()
        side = 1 if i % 2 == 0 else -1
        disp_loc = m.bottom(5).move(Point(x=side*2))
        asp_loc = m.bottom(5).move(Point(x=-1*side*2))
        pick_up(m300,tips300)
        m300.transfer(
            50, elution_buffer, m.center(), new_tip='never', air_gap=20)
        m300.mix(5, 40, disp_loc)
        m300.move_to(m.top(-20))

        magdeck.engage()
        ctx.delay(seconds=30, msg='Incubating on magnet for 30 seconds.')

        # transfer elution to new plate
        m300.transfer(50, asp_loc, e, new_tip='never', air_gap=20)
        m300.blow_out(e.top(-2))
        m300.drop_tip()

    # track final used tip
    save_tip_info(p1000)
    save_tip_info(m300)

    finish_run()
