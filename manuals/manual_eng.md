## User manual for OT-2 covid19 ISCIII

This manual intents to instruct the OT-2 operator in the correct use of the protocols and configurations of the robots set up at ISCIII during the covid19 outbreak.

## Robots setup

The 8 robots are identical to each other, being the different pipettes and modules attached to each of them the reason they aregrouped in 3 different configurations:

- **A**: Robots **A1 and A2** have a 300µl pipette and a 1000µl pipette, with no module attached.
- **B**: Robots **B1, B2, B3 and B4** have an 8-channel 300µl  multipipette and a 1000µl pipette, with magnetic module attached.
- **C**: Robots **C1 and C2** have a 300µl pipette and a 20µl pipette, with a temperature module attached. These robots have no internal leds to avoid damaging photosensitive chemicals.

The robots are distributed in 2 different locations:

- **Extraction Room**: Located in Orientación Diagnóstica, here are robots **A1, A2, B1, B2, B3 and B4** in the same room with a PC to control them.

![extraction_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/extraction_room_setup.jpg?raw=true)

- **PCR prep Room**: Inside Virus Respiratorios we find robots **C1 y C2** paired with another PC for their control.

![pcrprep_room_setup.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/pcrprep_room_setup.jpg?raw=true)

## Powering on the robots

Before starting the robot, please make sure there are no tips attached to any pipette neither any object inside the hood that could get in the way od the arm and pipettes while they return home.

To power on the robot, press the power button located at the rear of the left lateral panel, just above where the power cable is plugged.

![robot_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/robot_power_button.jpg?raw=true)

The robot will produce some mechanical noises and it si possible the arem moves home several times. The front led button will blink blue during the startup process.

Once the noise is over and the arm stops moving, the front led will glow blue permanently signalling the robot is ready to take orders.

![robot_front_led.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/robot_front_led.jpg?raw=true)

Finally, for robot configurations **B** and **C** we will have to power on the magdeck and tempdeck, respectively. Press the power button at the rear of each module, next to wher its power cord is plugged. A white light will glow and once the module stops making noises it will be ready to use.

![tempdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/tempdeck_power_button.jpg?raw=true)
![magdeck_power_button.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/magdeck_power_button.jpg?raw=true)

**Note**: The unit **A2** has no blue led in the front button, so it will not show that the robot is booting up neither it is ready to be used. As a consecuence, we will need to check its status through the app as we will explain later.

**I push the power button but the robot/module does not responds**: Please check that the power cord is correctly plugged into the robot/module, that the power supply unit an the power cord are connected and finally that the power cord is plugged into a working electic outlet.

**It smells like something is burning or I see smoke**: Quickly power off the robot or module where the smoke comes from by pushing the power button at the rear of the left side panel. Check that electric plugs are correctly plugged matching the marks inside the male conector with the marks in the female one. If one of the pins has become black or everything was already correctly connected, do not power off the robot and contact support.

![power_connector_frontal_male.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/power_connector_frontal_male.jpg?raw=true)
![power_connector_frontal_female.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/power_connector_frontal_female.jpg?raw=true)

**I forgot to remove the tip from the pippete before powering on and ...**: Quickly power off the robot by pushing the power button at the rear of the left side panel. Once it has stopped, clean any liquid that can have been split and contact support to evaluate potential damage or discalibration caused by the colition.

**I forgot to remove the tip from the pippete before powering on but it has finished powering on without crashing into anything**: Carefully remove the tip from the pipette before executing any new orders. Once it is removed, you can continue operating the robot normally.

## Starting up Opentrons app

The PCs located in the romms of the robots have a common user logging which grants you all the programs needed to operate the robots. Log into the computer followingn the instrctions provided by your administrator or contact support.

Once you are logged in, look for the icon of Opentrons app and open it.

![opentrons_app_icon.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_icon.jpg?raw=true)

The app starts in developper mode, which provides some extra features we need for the correct execution of our protocols, but makes the interface a less user-friendly. Close the debug mode of the app and we are ready to go on.

Close any update mesagges, too. Each update needs to be tested before installing, as they will also update the robots and can modify their behaviour.

![close_debug_mode.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/close_debug_mode.jpg?raw=true)

The app interface is divided in 3 vertical sections:

![opentrons_app_mainwindow.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_mainwindow.jpg?raw=true)

- Left you have a menu to navigate between the windows robot, protocol, calibration and run.

![opentrons_app_leftmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_leftmenu.jpg?raw=true)

- In the middle panel we have the orders we can execute in the robot from the active window.

![opentrons_app_middlemenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_middlemenu.jpg?raw=true)

- To the right we have the largest panel, which shows information for the user and different configuration and interative options. As the previous panel, it contents depen on the active window.

![opentrons_app_rightmenu.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_rightmenu.jpg?raw=true)

## Connecting to a robot

Click on the first option displayed in the left menu inside the app: `Robot`. The list of available robots to connect to will be displayed in the middle panel. Click on any of them to see the robot info in the right panel, along with some configuration options. like the option to turn on/off the lights with the button `Lights`.

**Note**: Turning on the lights is a good practice to confirm the robot you are going to use. It also helps when seting up or removing the labware inside the hood before and after a run.

**Note**: Type **C** robots does not have lights.

![opentrons_app_mainrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_mainrobot.jpg?raw=true)

In order to operate a robot, we need to connect to it. You can do it either by activating the little slider button at the right of its name in the middle panel or by clicking on the `Connect``button in the right panel after selecting the robot in the middle one.

 ![opentrons_app_connecttorobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_connecttorobot.jpg?raw=true)

 A green banner at the top will confirm you are sucessfully connecte to a robot and its name.

  ![opentrons_app_connectedrobot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_connectedrobot.jpg?raw=true)

 **Note**: You can only be connected to one robot at the same time. All the robots will continue executing their given orders after disconnected, but any configuration done in a robot might get lost if disconnected before starting the run, so it is recommended that in case of disconnetion you start configurating your experiment again.

 **Note**: If you connect to a robot that is already running a protocol, it will be notified with a yellow banner at the top. While a protocol is running you can not execute new orders on the robot, only monitor the exetution and display robot info and configuration.

 **Note**: Although you can connect to all robots from the two PCs, it is highly remmended not to operate a robot which is not in your sight. You do not know what or who might be inside the hood. Always double check which orobot you are connecte to before giving an order.

## Loading a protocol

Click on the second option of the left menu: `Protocol`. In this window you can see which protocol is already loaded in the robot from the previous run in the right panel.

![opentrons_app_mainprotocol.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_mainprotocol.jpg?raw=true)

To load a new protocol, drag and drop the corresponding `.py` file in the middle panel or click on the button `Open` in the same panel and look for the desired file.

In the right panel we can check tne name of the loaded protocol, version, authors and API version required, followed by the pipettes and modules needed to be installed for the protocol, and finally a list of the labware to use.

**Note**: If the pipettes and modules of the robot do not match the reuirements (you will se a red cross next to their names where a black check should be), make sure you are connected to the right robot and loading the right file and try again.

**Note**: If the required module is not detected (empty circle where a black check should appear), check in the robot that the module is connecte to both power and the robot, and that the module is on.

**Note**: The labware names displayed by the app can be search in our inventary table to discover what they mean, or use our website.

**Note**: The robot may ask for less tips than than expected, but ignore it. Always put as many tip boxes as demanded for the protocol at maximum capacity. In case not all of them are spend, the robot will continue with the half-empied boxes in the next run. Once it run out of tips, the execution will stop and it will ask you to replace the empty tip boxes for new ones.

## Calibrating a protocol

The third option of the menu on the left, `Calibrate`, allows us to adjust the arm position and its movement inside the hood so the robot can do it preciselly and match the labware.

![opentrons_app_maincalibrate.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_app_maincalibrate.jpg?raw=true)

**Protocol calibration is only needed when:**
- it is the first time this protocol is being executed in this robot
- the labware options have been modified since previous executions of the protocol in this robot
- it has been observed that the robot arm fails to pick up tips, hits the labware when moving or is not able to reach the desired depth inside the tubes/wells.

**Note**: If after calibrate a protocol several times the arm and pipettes still hit the labware when moving inside the hood, perform a deck calibration. If the problem persists, get support.

**Protocol calbration is not needed when**:
- the same protocol prevously run in this robot is going to be run again.
- the only changes from previous execution in this robot are related to the number of samples.

The middle panel will show a list of the required labwared for running the protocol. In order to calibrate all the labware at onece, it is recommended to run the protocol for the maximum of samples and all the steps.

Calibration must be started with an ampty hood (but modules, as they have to remain and be plugged and turned on) and the pipettes without tips attached, and deck calibration has to have been previously executed.

Calibration will start with the pipettes. It will guide you step by step to remove the trash for the tips and attach a new tip to the pipettes, and the arm will move to touch the sensors usually coveretd by the trash in order to check the movement and poitioingn of the tips. Once both pipettes have been calibrated, carefully put back the trash in its place to cever the sensors.

![opentrons_calibration_metalpins.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_calibration_metalpins.jpg?raw=true)

**Note**: Sensors are tiny delicate metal pins. Be very careful when removing or setting the trash, or they could be damaged.

**Note**: In case one of the sensors gets damaged or the pipette start position is incorrect due to a bad deck calibration, the arm will move not-stop in a straight line and might cause serious damage. In case this happens, wuickly power off the robot by pushing the power button in the rear bottom of the left side panel.

**Note**: In case of collition or sensors not working, please contact support.

**Note**: If the procol needs only one pipette, the calibration process can go into a loop and ask several times to calibrate the same only pipette. In this case, once you have successfully calibrated the pipette and the button `Next pipette` shows up, do not click on it. Instead, click on the first tiprack option in the middel panel to move to the next step.

Once pipette calibration is complete and you start calibrating the first labware, the tipracks, the app will show a layout of how to set up modules (if they are required) and labware inside the hood. Follow the instructions to set up the labware as shown, but do not put liquids yet, only empty labware. Follow the instructions of the section `Colocar el labware en la cabina` in this manual to do it right. For the moment, we are only calibrating and liquids would become a hazard, potentially splitting and contaminating both labware and deck.

![opentrons_calibration_labwarelayout.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_calibration_labwarelayout.jpg?raw=true)

Now lets move to calibrate tipracks. The robot will move the corresponding pipette above the top-left tip of each tiprack,and using the contols in the app you must move the lower end of the pipette to the height of the top end of the tip and centered into it. When it is in the right position, it will try to attach the tip and if it achives it the tiprack will be calibrated. If it fails to do it, repeat the process until it is done correctly.

![opentrons_calibration_controls.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_calibration_controls.jpg?raw=true)

**Note**: The 1000µl pipette can shake several times when picking up a new tip. This behaviour does not depend on the robot but the app, and can be disabled inside the app in the window `Robot`, in the section `PIPETTES & MODULES` of the middle panel. Click on `SETTINGS` next to the pipette and there is a checkbox saying `shaking` that can be disabled.

**Note**: Multichannel pipettes can not be calibrated with only one tip, you have to use all the column and make sure that not only one is centered and at the right height, but also the average of them are in the correct position.

Finally the rest of the labware will be calibrated. The monocanal pipette on the right will keep a tip from tiprack calibration and will use it in this step. One by one, the pipette wil move to above the first well/tube of each labware and we will calibrate it using the controls in the app. The lower end of the tip must be at the same height as as the top edge of the well/tube and centered into it.

**Note**: The longer the tip is, the less precise the calibratin will be as there are more chances of the tip being bended or the pipette having picked up the tip lightly uncentered. Be particullary careful when calibrating with the 1000µl pipette.

**Note**: Multichannel pipettes can not be used to calibrate labware.

Once labware calibration is over, the pipette will return the tip and we are ready to run the protocol.

## Labware setup inside the hood

In order to set up the labware into the hood, follow the instructions provided by the aministrator for each protocol and also these guidelines:
- Make sure the robot is stopped.
- Always beging setting up the labware in the rear row (10 and 11), followed by the third row (7, 8 and 9), the middle one (4, 5 and 6) amd finally the front row (1, 2 and 3).
- If possible, put the tubes and boxes with their lid on, and open them only before starting the run.
- When building an Opentrons' rack, make sure the marked corner of the stand matches with the marked corner of the rack. That marked corner will go on the top-left of the deck slot.

![opentrons_labware_opentronsrack.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_labware_opentronsrack.jpg?raw=true)

- When putting a piece of labware in a deck slot, always put first the bottom-right corner into the metal hooks. Then the piece should easily fall into position.

![opentrons_labware_deckslot.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_labware_deckslot.jpg?raw=true)

- Make sure the tubes are in the right position in their racks.
- Set up all the tip boxes as if the protocol was going to be executed for the maximum number of samples and steps.

## Running a protocol

The last option of the left panel menu, `Run`, allow us to give the execution order to the robot and monitor its progress. In this window we can see a chronometer showing the execution time and the buttons `START`, `PAUSE`, `RESUME`, `CANCEL RUN` and `RESET RUN`, depending on the execution status:

- `START`:

This order starts the tun of the uploaded protocol. Make sure that the loaded protocol is the right one, that you are connected to the correct robot, that the labware is setup and without lids on, that reuired modules are on and pipettes with no tips attached before clicking on the button.

 ![opentrons_run_start.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_start.jpg?raw=true)

 - `PAUSE`:

 pause the run in progress. It can take a few seconds to pause, as it has to wait until the current order is completed before pausing.

 **Note**: In case the robot finds a recuperable execution error, like door is open, tips are over or trash is full, the execution will pause as if the button `PAUSE` was cliked on. This status is notified to the user both verbally and via text in the log. Once the problem is fixed, click on `RESUME` to resume the run.

 ![opentrons_run_pause.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_pause.jpg?raw=true)

 - `RESUME`:

 Resume execution after pausing.

 ![opentrons_run_pauserestart.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_pauserestart.jpg?raw=true)

- `CANCEL RUN`:

Abort run in progress. This order requires confirmation and all progress will be lost.

**Note**: After cancelling a run, the robot will erase all information about the run, so it is reommended to refill al tips before running anything again.

![opentrons_run_cancelrunconfirmation.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_cancelrunconfirmation.jpg?raw=true)

- `RESET RUN`:

Afeter finishing a run the robot will stop. The top baner colour and message will show if the run ended successfully (green), if it is paused (yellow) or got aborted or critical error (red). In order to run the same protocol again it is not needed to upload the same protocol file, but just click on this button and the robot will prepare everything for a new run using the same protocol file.

![opentrons_run_resetrun.jpg](https://github.com/BU-ISCIII/opentrons_covid19/blob/develop/img/opentrons_run_resetrun.jpg?raw=true)

A log of the process will be displayed at all times in the right panel of this window. While running, the log will scroll down and marking in blue the current step , in grey the already completed steps and in black the remaining ones.

**Note**: This log is generated during a simulation prior the actual run, so it can be slightly different from the reality of the run or display the steps at a different speed, so its information has to be taken carefully.

## Cleaning the robot
