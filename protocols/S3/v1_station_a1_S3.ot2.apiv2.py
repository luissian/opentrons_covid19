from opentrons import protocol_api
from opentrons.drivers.rpi_drivers import gpio
import time
import math

# Metadata
metadata = {
    'protocolName': 'S3 Station C Version 1',
    'author': 'Nick <protocols@opentrons.com>, Sara <smonzon@isciii.es>, Miguel <mjuliam@isciii.es>',
    'source': 'Custom Protocol Request',
    'apiLevel': '2.1'
}

# Parameters to adapt the protocol
NUM_SAMPLES = 96
BUFFER_LABWARE = 'opentrons plastic 50 ml tubes'
DESTINATION_LABWARE = 'opentrons plastic 2ml tubes'
DEST_TUBE = '2ml tubes'

"""
NUM_SAMPLES is the number of samples, must be an integer number

BUFFER_LABWARE must be one of the following:
    opentrons plastic 50 ml tubes

DESTINATION_LABWARE must be one of the following:
    opentrons plastic 2ml tubes

DEST_TUBE
    2m tubes
"""


# Constants
BUFFER_LW_DICT = {
    'opentrons plastic 50 ml tubes': 'opentrons_6_tuberack_falcon_50ml_conical'
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


def retrieve_tip_info(file_path):
    tip_log = {}

    if tip_log and not ctx.is_simulating():
        if os.path.isfile(file_path):
            with open(file_path) as json_file:
                data = json.load(json_file)
                if 'tips1000' in data:
                    tip_log['count'] = {p1000: data['tips1000']}
                else:
                    tip_log['count'] = {p1000: 0}
    else:
        tip_log['count'] = {p1000: 0}

    tip_log['tips'] = {
        p1000: [tip for rack in tipracks1000 for tip in rack.wells()]}
    tip_log['max'] = {p1000: len(tip_log['tips'][p1000])}

    return tip_log

def save_tip_info(file_path):
    if not ctx.is_simulating():
        data = {'tips1000': tip_log['count'][p1000]}
        with open(file_path, 'w') as outfile:
            json.dump(data, outfile)


def pick_up(pip):
    nonlocal tip_log
    if tip_log['count'][pip] == tip_log['max'][pip]:
        ctx.pause('Replace ' + str(pip.max_volume) + 'µl tipracks before \
resuming.')
        pip.reset_tipracks()
        tip_log['count'][pip] = 0
    tip_log['count'][pip] += 1
    pip.pick_up_tip(tip_log['tips'][pip][tip_log['count'][pip]])

def transfer_buffer(mm_tube, dests, VOLUME_BUFFER, p1000):
    pip.pick_up()
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
    pip.drop_tip()

def transfer_samples(ELUTION_LABWARE, sources, dests, p20):
    # height for aspiration has to be different depending if you ar useing tubes or wells
    if 'strip' in ELUTION_LABWARE or 'plate' in ELUTION_LABWARE:
        height = 1.5
    else:
        height = 1
    # transfer
    for s, d in zip(sources, dests):
        p20.pick_up_tip()
        p20.transfer(7, s.bottom(height), d.bottom(2), air_gap=2, new_tip='never')
        #p20.mix(1, 10, d.bottom(2))
        #p20.blow_out(d.top(-2))
        p20.aspirate(1, d.top(-2))
        p20.drop_tip()

# RUN PROTOCOL
def run(ctx: protocol_api.ProtocolContext):

    # confirm door is closed
    if not ctx.is_simulating():
        confirm_door_is_closed(ctx)

    # define tips
    tips20 = [
        ctx.load_labware('opentrons_96_filtertiprack_20ul', slot)
        for slot in ['6', '9', '8', '7']
    ]
    tips300 = [ctx.load_labware('opentrons_96_filtertiprack_200ul', '3')]

    # define pipettes
    p20 = ctx.load_instrument('p20_single_gen2', 'right', tip_racks=tips20)
    p300 = ctx.load_instrument('p300_single_gen2', 'left', tip_racks=tips300)

    # tempdeck module
    tempdeck = ctx.load_module('tempdeck', '10')
    tempdeck.set_temperature(4)

    # check mastermix labware type
    if MM_LABWARE not in MM_LW_DICT:
        raise Exception('Invalid MM_LABWARE. Must be one of the \
following:\nopentrons plastic block\nopentrons aluminum block\ncovidwarriors aluminum block')

    # load mastermix labware
    mm_rack = ctx.load_labware(
        MM_LW_DICT[MM_LABWARE], '11',
        MM_LABWARE)

    # check mastermix tube labware type
    if MMTUBE_LABWARE not in MMTUBE_LW_DICT:
        raise Exception('Invalid MMTUBE_LABWARE. Must be one of the \
    following:\no2ml tubes')

    # This one is not loaded, it contains the raius of each tube to calculate volume height

    # check pcr plate
    if PCR_LABWARE not in PCR_LW_DICT:
        raise Exception('Invalid PCR_LABWARE. Must be one of the \
following:\nopentrons aluminum biorad plate\nopentrons aluminum nest plate\nopentrons aluminum strip short\ncovidwarriors aluminum biorad plate\ncovidwarriors aluminum biorad strip short')

    # load pcr plate
    pcr_plate = tempdeck.load_labware(
        PCR_LW_DICT[PCR_LABWARE], 'PCR plate')

    # check source (elution) labware type
    if ELUTION_LABWARE not in EL_LW_DICT:
        raise Exception('Invalid ELUTION_LABWARE. Must be one of the \
following:\nopentrons plastic 2ml tubes\nopentrons plastic 1.5ml tubes\nopentrons aluminum 2ml tubes\nopentrons aluminum 1.5ml tubes\ncovidwarriors aluminum 2ml tubes\ncovidwarriors aluminum 1.5ml tubes\nopentrons aluminum biorad plate\nopentrons aluminum nest plate\ncovidwarriors aluminum biorad plate\nopentrons aluminum strip alpha\nopentrons aluminum strip short\ncovidwarriors aluminum biorad strip alpha\ncovidwarriors aluminum biorad strip short')

    # load elution labware
    if 'plate' in ELUTION_LABWARE:
        source_racks = ctx.load_labware(
            EL_LW_DICT[ELUTION_LABWARE], '1',
            'RNA elution labware')
    else:
        source_racks = [
            ctx.load_labware(EL_LW_DICT[ELUTION_LABWARE], slot,
                            'RNA elution labware ' + str(i+1))
            for i, slot in enumerate(['4', '1', '5', '2'])
    ]

    # setup sample sources and destinations
    sources, dests = get_source_dest_coordinates(ELUTION_LABWARE, source_racks, pcr_plate)

    # prepare mastermix
    if PREPARE_MASTERMIX:
        mm_tube = prepare_mastermix(MM_TYPE, mm_rack, p300, p20)
    else:
        mm_tube = mm_rack.wells()[0]
        if TRANSFER_MASTERMIX:
            homogenize_mm(mm_tube, p300)

    # transfer mastermix
    if TRANSFER_MASTERMIX:
        transfer_mastermix(mm_tube, dests, VOLUME_MMIX, p300, p20)

    # transfer samples to corresponding locations
    if TRANSFER_SAMPLES:
        transfer_samples(ELUTION_LABWARE, sources, dests, p20)

    finish_run()
