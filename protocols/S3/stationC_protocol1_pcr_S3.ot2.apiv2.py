from opentrons import protocol_api
from opentrons.types import Point
from opentrons.drivers.rpi_drivers import gpio
import time
import math
import os
import subprocess
import json

# Metadata
metadata = {
    'protocolName': 'S3 Station C Protocol 1 pcr Version 1',
    'author': 'Nick <protocols@opentrons.com>, Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.3'
}

# Parameters to adapt the protocol
# Warning writing any Parameters below this line.
# It will be deleted if opentronsWeb is used.

NUM_SAMPLES = 96
MM_LABWARE = 'opentrons aluminum block'
MMTUBE_LABWARE = '2ml tubes'
PCR_LABWARE = 'opentrons aluminum nest plate'
ELUTION_LABWARE = 'opentrons aluminum nest plate'
PREPARE_MASTERMIX = False
MM_TYPE = 'MM1'
TRANSFER_MASTERMIX = True
TRANSFER_SAMPLES = True

# End Parameters to adapt the protocol

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

MM_LABWARE must be one of the following:
    opentrons plastic block
    pentrons aluminum block
    covidwarriors aluminum block

MMTUBE_LABWARE must be one of the following:
    2ml tubes

PCR_LABWARE must be one of the following:
    opentrons aluminum biorad plate
    opentrons aluminum nest plate
    opentrons aluminum strip short
    covidwarriors aluminum biorad plate
    covidwarriors aluminum biorad strip short

ELUTION_LABWARE must be one of the following:
    opentrons plastic 2ml tubes
    opentrons plastic 1.5ml tubes
    opentrons aluminum 2ml tubes
    opentrons aluminum 1.5ml tubes
    covidwarriors aluminum 2ml tubes
    covidwarriors aluminum 1.5ml tubes
    opentrons aluminum biorad plate
    opentrons aluminum nest plate
    covidwarriors aluminum biorad plate
    opentrons aluminum strip alpha
    opentrons aluminum strip short
    covidwarriors aluminum biorad strip alpha
    covidwarriors aluminum biorad strip short

PREPARE_MASTERMIX: True or False

MM_TYPE must be one of the following:
    MM1
    MM2
    MM3

TRANSFER_MASTERMIX: True or False

TRANSFER_SAMPLES: True or False
"""

# Calculated variables
if MM_TYPE == 'MM3':
    VOLUME_MMIX = 15
else:
    VOLUME_MMIX = 20

# Constants
MM_LW_DICT = {
    'opentrons plastic block': 'opentrons_24_tuberack_generic_2ml_screwcap',
    'opentrons aluminum block': 'opentrons_24_aluminumblock_generic_2ml_screwcap',
    'covidwarriors aluminum block': 'covidwarriors_aluminumblock_24_screwcap_2000ul'
}

PCR_LW_DICT = {
    'opentrons aluminum biorad plate': 'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    'opentrons aluminum nest plate': 'opentrons_96_aluminumblock_nest_wellplate_100ul',
    'opentrons aluminum strip short': 'opentrons_aluminumblock_96_pcrstrips_100ul',
    'covidwarriors aluminum biorad plate': 'covidwarriors_aluminumblock_96_bioradwellplate_200ul',
    'covidwarriors aluminum biorad strip short': 'covidwarriors_aluminumblock_96_bioradwellplate_pcrstrips_100ul'
}

EL_LW_DICT = {
    # tubes
    'opentrons plastic 2ml tubes': 'opentrons_24_tuberack_generic_2ml_screwcap',
    'opentrons plastic 1.5ml tubes': 'opentrons_24_tuberack_nest_1.5ml_screwcap',
    'opentrons aluminum 2ml tubes': 'opentrons_24_aluminumblock_generic_2ml_screwcap',
    'opentrons aluminum 1.5ml tubes': 'opentrons_24_aluminumblock_nest_1.5ml_screwcap',
    'covidwarriors aluminum 2ml tubes': 'covidwarriors_aluminumblock_24_screwcap_2000ul',
    'covidwarriors aluminum 1.5ml tubes': 'covidwarriors_aluminumblock_24_screwcap_2000ul',
    # PCR plate
    'opentrons aluminum biorad plate': 'opentrons_96_aluminumblock_biorad_wellplate_200ul',
    'opentrons aluminum nest plate': 'opentrons_96_aluminumblock_nest_wellplate_100ul',
    'covidwarriors aluminum biorad plate': 'covidwarriors_aluminumblock_96_bioradwellplate_200ul',
    # Strips
    #'large strips': 'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
    #'short strips': 'opentrons_96_aluminumblock_generic_pcr_strip_200ul',
    'opentrons aluminum strip alpha': 'opentrons_aluminumblock_96_pcrstripsalpha_200ul',
    'opentrons aluminum strip short': 'opentrons_aluminumblock_96_pcrstrips_100ul',
    'covidwarriors aluminum biorad strip alpha': 'covidwarriors_aluminumblock_96_bioradwellplate_pcrstripsalpha_200ul',
    'covidwarriors aluminum biorad strip short': 'covidwarriors_aluminumblock_96_bioradwellplate_pcrstrips_100ul'
}

MMTUBE_LW_DICT = {
    # Radius of each possible tube
    '2ml tubes': 4
}

VOICE_FILES_DICT = {
    'start': './data/sounds/started_process.mp3',
    'finish': './data/sounds/finished_process.mp3',
    'close_door': './data/sounds/close_door.mp3',
    'replace_tipracks': './data/sounds/replace_tipracks.mp3',
    'empty_trash': './data/sounds/empty_trash.mp3'
}

# Function definitions
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

def finish_run():
    voice_notification('finish')
    #Set light color to blue
    gpio.set_button_light(0,0,1)

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

def retrieve_tip_info(pip,tipracks,file_path = '/data/C/tip_log.json'):
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

def save_tip_info(file_path = '/data/C/tip_log.json'):
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
    ## retrieve tip_log
    global tip_log
    if not tip_log:
        tip_log = {}
    tip_log = retrieve_tip_info(pip,tiprack)
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

def get_source_dest_coordinates(source_racks, pcr_plate):
    if 'strip' in ELUTION_LABWARE:
        sources = [
            tube
            for i, rack in enumerate(source_racks)
            for col in [
                rack.columns()[c] if i < 2 else rack.columns()[c+1]
                for c in [0, 5, 10]
            ]
            for tube in col
        ][:NUM_SAMPLES]
        dests = pcr_plate.wells()[:NUM_SAMPLES]
    elif 'plate' in ELUTION_LABWARE:
        sources = source_racks.wells()[:NUM_SAMPLES]
        dests = pcr_plate.wells()[:NUM_SAMPLES]
    else:
        sources = [
            tube
            for rack in source_racks for tube in rack.wells()][:NUM_SAMPLES]
        dests = [
            well
            for v_block in range(2)
            for h_block in range(2)
            for col in pcr_plate.columns()[6*v_block:6*(v_block+1)]
            for well in col[4*h_block:4*(h_block+1)]][:NUM_SAMPLES]
    return sources, dests

def get_mm_height(volume):
    # depending on the volume in tube, get mm fluid height
    height = volume // (3.14 * (MMTUBE_LW_DICT[MMTUBE_LABWARE] ** 2))
    height -= 18
    if height < 5:
        return 1
    else:
        return height

def homogenize_mm(mm_tube, pip, tiprack, times=5):
    # homogenize mastermix tube a given number of times
    pick_up(pip,tiprack)
    volume = VOLUME_MMIX * NUM_SAMPLES
    volume_height = get_mm_height(volume)
    #p300.mix(5, 200, mm_tube.bottom(5))
    for i in range(times):
        for j in range(5):
            # depending on the number of samples, start at a different height and move as it aspires
            if volume_height < 12:
                pip.aspirate(40, mm_tube.bottom(1))
            else:
                aspirate_height = volume_height-(3*j)
                pip.aspirate(40, mm_tube.bottom(aspirate_height))
        # empty pipete
        pip.dispense(200, mm_tube.bottom(volume_height))
    # blow out before dropping tip
    pip.blow_out(mm_tube.top(-2))
    # p300.drop_tip(home_after=False)

def prepare_mastermix(mm_rack, p300, p20,tiprack300,tiprack20):
    # setup mastermix coordinates
    """ mastermix component maps """
    mm1 = {
        tube: vol
        for tube, vol in zip(
            [well for col in mm_rack.columns()[2:5] for well in col][:10],
            [2.85, 12.5, 0.4, 1, 1, 0.25, 0.25, 0.5, 0.25, 1]
        )
    }
    mm2 = {
        tube: vol
        for tube, vol in zip(
            [mm_rack.wells_by_name()[well] for well in ['A3', 'C5', 'D5']],
            [10, 4, 1]
        )
    }
    mm3 = {
        tube: vol
        for tube, vol in zip(
            [mm_rack.wells_by_name()[well] for well in ['A6', 'B6']],
            [13, 2]
        )
    }
    mm_dict = {'MM1': mm1, 'MM2': mm2, 'MM3': mm3}

    # create mastermix
    mm_tube = mm_rack.wells()[0]
    for tube, vol in mm_dict[MM_TYPE].items():
        mm_vol = vol*(NUM_SAMPLES+5)
        disp_loc = mm_tube.top(-10)
        pip = p300 if mm_vol > 20 else p20
        tiprack = tiprack300 if mm_vol > 20 else tiprack20

        pick_up(pip,tiprack)
        #pip.transfer(mm_vol, tube.bottom(0.5), disp_loc, air_gap=2, touch_tip=True, new_tip='never')
        air_gap_vol = 5
        num_transfers = math.ceil(mm_vol/(200-air_gap_vol))
        for i in range(num_transfers):
            if i == 0:
                transfer_vol = mm_vol % (200-air_gap_vol)
            else:
                transfer_vol = (200-air_gap_vol)
            pip.transfer(transfer_vol, tube.bottom(0.5), disp_loc, air_gap=air_gap_vol, new_tip='never')
            pip.blow_out(disp_loc)
        pip.aspirate(5, mm_tube.top(2))
        drop(pip)

    # homogenize mastermix
    homogenize_mm(mm_tube, p300,tiprack300)

    return mm_tube

def transfer_mastermix(mm_tube, dests, p300, p20, tiprack300, tiprack20):
    max_trans_per_asp = 8  #230//(VOLUME_MMIX+5)
    split_ind = [ind for ind in range(0, NUM_SAMPLES, max_trans_per_asp)]
    dest_sets = [dests[split_ind[i]:split_ind[i+1]]
             for i in range(len(split_ind)-1)] + [dests[split_ind[-1]:]]
    pip = p300 if VOLUME_MMIX >= 20 else p20
    tiprack = tiprack300 if VOLUME_MMIX >= 20 else tiprack20
    if not pip.hw_pipette['has_tip']:
        pick_up(pip,tiprack)
    # get initial fluid height to avoid overflowing mm when aspiring
    mm_volume = VOLUME_MMIX * NUM_SAMPLES
    volume_height = get_mm_height(mm_volume)
    for set in dest_sets:
        # check height and if it is low enought, aim for the bottom
        if volume_height < 5:
            disp_loc = mm_tube.bottom(1)
        else:
            # reclaculate volume height
            mm_volume -= VOLUME_MMIX * max_trans_per_asp
            volume_height = get_mm_height(mm_volume)
            disp_loc = mm_tube.bottom(volume_height)
        pip.aspirate(4, disp_loc)
        pip.distribute(VOLUME_MMIX, disp_loc, [d.bottom(2) for d in set],
                   air_gap=1, disposal_volume=0, new_tip='never')
        pip.blow_out(disp_loc)
    drop(pip)

def transfer_samples(sources, dests, pip,tiprack):
    # height for aspiration has to be different depending if you ar useing tubes or wells
    if 'strip' in ELUTION_LABWARE or 'plate' in ELUTION_LABWARE:
        height = 1.5
    else:
        height = 1
    # transfer
    for s, d in zip(sources, dests):
        # Skip for negative control, position NUM_SAMPLES-2
        if s == sources[NUM_SAMPLES-2]:
            continue

        pick_up(pip,tiprack)
        pip.transfer(7, s.bottom(height), d.bottom(2), air_gap=2, new_tip='never')
        #p20.mix(1, 10, d.bottom(2))
        #p20.blow_out(d.top(-2))
        pip.aspirate(1, d.top(-2))
        drop(pip)

# RUN PROTOCOL
def run(ctx: protocol_api.ProtocolContext):
    global robot
    robot = ctx

    # confirm door is closed
    robot.comment(f"Please, close the door")
    confirm_door_is_closed()

    # Begin run
    voice_notification('start')

    # define tips
    tips20 = [
        robot.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['6', '9', '8', '7']
    ]
    tips300 = [robot.load_labware('opentrons_96_filtertiprack_200ul', '3')]

    # define pipettes
    p20 = robot.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300 = robot.load_instrument('p300_single_gen2', 'left', tip_racks=tips300)

    # tempdeck module
    tempdeck = robot.load_module('tempdeck', '10')
    tempdeck.set_temperature(4)

    # check mastermix labware type
    if MM_LABWARE not in MM_LW_DICT:
        raise Exception('Invalid MM_LABWARE. Must be one of the following:\n' + '\n'.join(list(MM_LW_DICT.keys())))


    # load mastermix labware
    mm_rack = robot.load_labware(
        MM_LW_DICT[MM_LABWARE], '11',
        MM_LABWARE)

    # check mastermix tube labware type
    if MMTUBE_LABWARE not in MMTUBE_LW_DICT:
        raise Exception('Invalid MMTUBE_LABWARE. Must be one of the following:\n' + '\n'.join(list(MMTUBE_LW_DICT.keys())))

    # This one is not loaded, it contains the raius of each tube to calculate volume height

    # check pcr plate
    if PCR_LABWARE not in PCR_LW_DICT:
        raise Exception('Invalid PCR_LABWARE. Must be one of the following:\n' + '\n'.join(list(PCR_LW_DICT.keys())))


    # load pcr plate
    pcr_plate = tempdeck.load_labware(
        PCR_LW_DICT[PCR_LABWARE], 'PCR plate')

    # check source (elution) labware type
    if ELUTION_LABWARE not in EL_LW_DICT:
        raise Exception('Invalid ELUTION_LABWARE. Must be one of the following:\n' + '\n'.join(list(EL_LW_DICT.keys())))


    # load elution labware
    if 'plate' in ELUTION_LABWARE:
        source_racks = robot.load_labware(
            EL_LW_DICT[ELUTION_LABWARE], '1',
            'RNA elution labware')
    else:
        source_racks = [
            robot.load_labware(EL_LW_DICT[ELUTION_LABWARE], slot,
                            'RNA elution labware ' + str(i+1))
            for i, slot in enumerate(['4', '1', '5', '2'])
    ]

    # setup sample sources and destinations
    sources, dests = get_source_dest_coordinates(source_racks, pcr_plate)

    # prepare mastermix
    if PREPARE_MASTERMIX:
        mm_tube = prepare_mastermix(mm_rack, p300, p20,tips300,tips20)
        if TRANSFER_MASTERMIX:
            p300.drop_tip(home_after=False)
    else:
        mm_tube = mm_rack.wells()[0]
        if TRANSFER_MASTERMIX:
            homogenize_mm(mm_tube, p300,tips300)

    # transfer mastermix
    if TRANSFER_MASTERMIX:
        transfer_mastermix(mm_tube, dests, p300, p20, tips300, tips20)
        if TRANSFER_SAMPLES:
            robot.pause(f"Please, check that all wells have received the right ammount of mastermix")

    # transfer samples to corresponding locations
    if TRANSFER_SAMPLES:
        transfer_samples(sources, dests, p20,tips20)
        # transfer negative control to position NUM_SAMPLES-2
        p20.transfer(7, mm_rack.wells()[4].bottom(1), dests[NUM_SAMPLES-2].bottom(2), air_gap=2, new_tip='always')

    finish_run()
