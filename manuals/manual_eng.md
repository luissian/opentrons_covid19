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

The PCs located in the romms of the robots have a common user logging which grants you all the programs needed to operate the robots. Log into the computer followingn the instrctions provided by your administrator or contact support.

Once you are logged in, look for the icon of Opentrons app and open it.

![opentrons_app_icon.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_icon.jpg?raw=true)

The app starts in developper mode, which provides some extra features we need for the correct execution of our protocols, but makes the interface a less user-friendly. Close the debug mode of the app and we are ready to go on.

![close_debug_mode.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/close_debug_mode.jpg?raw=true)

The app interface is divided in 3 vertical sections:

![opentrons_app_mainwindow.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_mainwindow.jpg?raw=true)

- Left you have a menu to navigate between the windows robot, protocol, calibration and run.

![opentrons_app_leftmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_leftmenu.jpg?raw=true)

- In the middle panel we have the orders we can execute in the robot from the active window.

![opentrons_app_middlemenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_middlemenu.jpg?raw=true)

- To the right we have the largest panel, which shows information for the user and different configuration and interative options. As the previous panel, it contents depen on the active window.

![opentrons_app_rightmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_rightmenu.jpg?raw=true)

## Connecting to a robot

Click on the first option displayed in the left menu inside the app: `Robot`. The list of available robots to connect to will be displayed in the middle panel. Click on any of them to see the robot info in the right panel, along with some configuration options. like the option to turn on/off the lights with the button `Lights`.

**Note**: Turning on the lights is a good practice to confirm the robot you are going to use. It also helps when seting up or removing the labware inside the hood before and after a run.

**Note**: Type **C** robots does not have lights.

![opentrons_app_mainrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_mainrobot.jpg?raw=true)

In order to operate a robot, we need to connect to it. You can do it either by activating the little slider button at the right of its name in the middle panel or by clicking on the `Connect``button in the right panel after selecting the robot in the middle one.

 ![opentrons_app_connectedrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_connectedrobot.jpg?raw=true)

 A green banner at the top will confirm you are sucessfully connecte to a robot and its name.

 **Note**: You can only be connected to one robot at the same time. All the robots will continue executing their given orders after disconnected, but any configuration done in a robot might get lost if disconnected before starting the run, so it is recommended that in case of disconnetion you start configurating your experiment again.

 **Note**: If you connect to a robot that is already running a protocol, it will be notified with a yellow banner at the top. While a protocol is running you can not execute new orders on the robot, only monitor the exetution and display robot info and configuration.

 **Note**: Although you can connect to all robots from the two PCs, it is highly remmended not to operate a robot which is not in your sight. You do not know what or who might be inside the hood. Always double check which orobot you are connecte to before giving an order.

## Loading a protocol

Click on the second option of the left menu: `Protocol`. In this window you can see which protocol is already loaded in the robot from the previous run in the right panel.

![opentrons_app_mainprotocol.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/master/img/opentrons_app_mainprotocol.jpg?raw=true)

To load a new protocol, drag and drop the corresponding `.py` file in the middle panel or click on the button `Open` in the same panel and look for the desired file.

In the right panel we can check tne name of the loaded protocol, version, authors and API version required, followed by the pipettes and modules needed to be installed for the protocol, and finally a list of the labware to use.

**Note**: If the pipettes and modules of the robot do not match the reuirements (you will se a red cross next to their names where a black check should be), make sure you are connected to the right robot and loading the right file and try again.

**Note**: If the required module is not detected (empty circle where a black check should appear), check in the robot that the module is connecte to both power and the robot, and that the module is on.

**Note**: The labware names displayed by the app can be search in our inventary table to discover what they mean, or use our website.

**Note**: The robot may ask for less tips than than expected, but ignore it. Always put as many tip boxes as demanded for the protocol at maximum capacity. In case not all of them are spend, the robot will continue with the half-empied boxes in the next run. Once it run out of tips, the execution will stop and it will ask you to replace the empty tip boxes for new ones.

## Calibrating a protocol

## Running a protocol
