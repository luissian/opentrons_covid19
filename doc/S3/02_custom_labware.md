# OT-2 custom labware configuration guide.

## steps

1) Use [Opentrons Labware creator](https://labware.opentrons.com/create/) to create your custom labware configuration.

-   [Guide for measurements](https://support.opentrons.com/en/articles/3136504-creating-custom-labware-definitions): First you are going to make some measurements, using always if possible technical drawings from the manufacturer.

-   Fill all the measures in the web form. The well plate selection suits you for any custom labware you want to create, even if there are several elements involved. For example, an aluminum block + pcr plate + tube strips, as you don't have a selection for this you can treat it like a well plate, the height will be the total height from bottom of the aluminum block to the top of the tubes.

-   Once everything is filled we have to select a name for your labware and a pipette for testing and calibrating your configuration. You currently can't select GEN2 pipettes so you will need to twist that later in the testing code.

-   You will download two files: 1) json labware configuration file, 2) test protocol script.

-   **IMPORTANT:** This files have important fields: displayName, loadName and brand. This names have to be MEANINGFUL for your custom labware. The web form doesn't give you too much flexibility for the name so you need to change the displayName and loadName in your json and .py file. And the brand only in the json file.
    -   loadName: Only lower case letters, numbers, periods, and underscores may be used. Ej.
    -   DisplayName: meaningful!! No
    -   Brand: Example: covidWarriors.

-   You will also need to change the name for the pipette using GEN2, and the tiprack accordingly to the tips you have/need for that pipette.

2) Test and calibrate your custom labware:
-   Upload the test protocol to the Opentrons App.
-   The app is going to ask you several steps to calibrate your labware. First you need to make sure you don't have ANY labware in the deck, and the trash bin is REMOVED.
-   Do everything the app ask you to. Once finished you need to evaluate if the test was successful, you can do it using [this guide](https://opentrons-publications.s3.us-east-2.amazonaws.com/labwareDefinition_testGuide.pdf)
-   If you want to change something repeat measurements and change the json and py file, directly on the files or using the labware creator web and repeating the testing and calibration steps. Prior to re-calibrate you need to reset labware configuration (OT-2 APP > Robot > Factory reset > click labware calibration).

3) Once you are happy with your labware configuration files you need to save them properly. Suggestion:
-   Folder with displayName.
-   Inside the folder: testing python script, json file, photo of the custom labware.
-   Optional: inventory in excel with all the custom labware and its measurements.
