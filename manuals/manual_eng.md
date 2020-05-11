## User manual for OT-2 covid19 ISCIII

This manual intents to instruct the OT-2 operator in the correct use of the protocols and configurations of the robots set up at ISCIII during the covid19 outbreak.

## Robots setup

The 8 robots are identical to each other, being the different pipettes and modules attached to each of them the reason they aregrouped in 3 different configurations:

- **A**: Robots **A1 and A2** have a 300µl pipette and a 1000µl pipette, with no module attached.
- **B**: Robots **B1, B2, B3 and B4** have an 8-channel 300µl  multipipette and a 1000µl pipette, with magnetic module attached.
- **C**: Robots **C1 and C2** have a 300µl pipette and a 20µl pipette, with a temperature module attached. These robots have no internal leds to avoid damaging photosensitive chemicals.

The robots are distributed in 2 different locations:

- **Extraction Room**: Located in Orientación Diagnóstica, here are robots **A1, A2, B1, B2, B3 and B4** in the same room with a PC to control them.

![extraction_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/extraction_room_setup.jpg?raw=true)

- **PCR prep Room**: Inside Virus Respiratorios we find robots **C1 y C2** paired with another PC for their control.

![pcrprep_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/pcrprep_room_setup.jpg?raw=true)

## Powering on the robots

Before starting the robot, please make sure there are no tips attached to any pipette neither any object inside the hood that could get in the way od the arm and pipettes while they return home.

To power on the robot, press the power button located at the rear of the left lateral panel, just above where the power cable is plugged.

![robot_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/robot_power_button.jpg?raw=true)

The robot will produce some mechanical noises and it si possible the arem moves home several times. The front led button will blink blue during the startup process.

Once the noise is over and the arm stops moving, the front led will glow blue permanently signalling the robot is ready to take orders.

![robot_front_led.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/robot_front_led.jpg?raw=true)

Finally, for robot configurations **B** and **C** we will have to power on the magdeck and tempdeck, respectively. Press the power button at the rear of each module, next to wher its power cord is plugged. A white light will glow and once the module stops making noises it will be ready to use.

![tempdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/tempdeck_power_button.jpg?raw=true)
![magdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/magdeck_power_button.jpg?raw=true)

**Note**: The unit **A2** has no blue led in the front button, so it will not show that the robot is booting up neither it is ready to be used. As a consecuence, we will need to check its status through the app as we will explain later.

**I push the power button but the robot/module does not responds**: Please check that the power cord is correctly plugged into the robot/module, that the power supply unit an the power cord are connected and finally that the power cord is plugged into a working electic outlet.

**It smells like something is burning or I see smoke**: Quickly power off the robot or module where the smoke comes from by pushing the power button at the rear of the left side panel. Check that electric plugs are correctly plugged matching the marks inside the male conector with the marks in the female one. If one of the pins has become black or everything was already correctly connected, do not power off the robot and contact support.

![power_connector_frontal_male.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/power_connector_frontal_male.jpg?raw=true)
![power_connector_frontal_female.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/power_connector_frontal_female.jpg?raw=true)

**I forgot to remove the tip from the pippete before powering on and ...**: Quickly power off the robot by pushing the power button at the rear of the left side panel. Once it has stopped, clean any liquid that can have been split and contact support to evaluate potential damage or discalibration caused by the colition.

**I forgot to remove the tip from the pippete before powering on but it has finished powering on without crashing into anything**: Carefully remove the tip from the pipette before executing any new orders. Once it is removed, you can continue operating the robot normally.

## Starting up Opentrons app

## Connecting to a robot

## Loading a protocol

## Calibrating a protocol

## Running a protocol
