
# OT-2 installation summary guide

## Index guide from opentrons.

-   [Index guide](https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2#6-calibrate-the-ot-2)

## Steps

1) [Unboxing](https://support.opentrons.com/en/articles/2687501-get-started-unbox-the-ot-2)

2) [Unlock](https://slack-redir.net/link?url=https%3A%2F%2Fsupport.opentrons.com%2Fen%2Farticles%2F2687521-get-started-unlock-the-ot-2)

3) **Make inventory:** This is an example of the info you should collect. IDs mean serial numbers for the robot, pipettes and modules.

| Location | Configuration | Robots | ID | static IP      | Host Name    | Macbook Air MAC | Right pipette | RP ID | Left pipette | LP ID | Module 1 type | Module 1 ID |
|----------|---------------|--------|----|----------------|--------------|-----------------|---------------|-------|--------------|-------|---------------|-------------|
|          | B             | S3\-B1 |    | 169\.254\.2\.1 | Hod04\-mac06 |                 | pM300         |       | p1000        |       | Magnetic      |             |
|          | B             | S3\-B2 |    | 169\.254\.2\.2 | Hos04\-mac08 |                 | pM300         |       | p1000        |       | Magnetic      |             |
|          | C             | S3\-C1 |    | 169\.254\.3\.1 | Hos04\-mac07 |                 | p20           |       | p300         |       | Temperature   |             |
|          | C             | S3\-C2 |    | 169\.254\.3\.2 | Hos04\-mac01 |                 | p20           |       | p300         |       | Temperature   |             |
|          | A             | S3\-A1 |    | 169\.254\.1\.1 | Hos04\-mac04 |                 | p300          |       | p1000        |       |               |             |
|          | B             | S3\-B3 |    | 169\.254\.2\.3 | Hos04\-mac05 |                 | pM300         |       | p1000        |       | Magnetic      |             |
|          | A             | S3\-A2 |    | 169\.254\.1\.2 | Hos04\-mac03 |                 | p300          |       | p1000        |       |               |             |
|          | B             | S3\-B4 |    | 169\.254\.2\.4 | Hos04\-mac02 |                 | pM300         |       | p1000        |       | Magnetic      |             |

4) [Attach pipettes](https://support.opentrons.com/en/articles/2067321-get-started-attach-pipettes)
> **NOTE:** p20 on the RIGHT, needed later for recalibration.

5) **Renaming the robot**: This changes the hostname of the robots. Run scripts in the folder rename_robots with the ot app. One for each robot. Restart the OT from the OP app.

6) **Assigning static IP address to the robots:** Important in the script variable use IP/16 (mandatory indicate the mask, must be the same that in the mac computer).

    -   Run scripts in the folder statics_ips with the ot app. One for each robot.
    -   Restart the OT from the OP app.
    -   Set the IP for the USB network in the Mac to manual IP 169.254.10.10 y mask 255.255.0.0 (this makes the connection faster as it don't need to wait for dhcp resolution).

7) **Configure Robots wifi:** this will allow you to control several robots using only one computer and wireless.
Set wifi ISCIII-IoT wifi:
```Bash
$ cd /var/lib/NetworkManager/system-connections
$ vi ISCIII-IoT

## Add this lines
[connection]
id=ISCIII-IoT
uuid=75f43d24-f0a9-42fb-b228-4c9c631ccfed
type=wifi
interface-name=wlan0
permissions=

[wifi]
cloned-mac-address=permanent
mac-address-blacklist=
mac-address-randomization=1
mode=infrastructure
ssid=ISCIII-IoT

[wifi-security]
key-mgmt=wpa-psk
psk=EPxjsboD7QZ4I1yPS3ls

[ipv4]
address1=172.17.70.<IP>/24
dns=8.8.8.8;8.8.4.4;
dns-search=
method=manual

[ipv6]
addr-gen-mode=stable-privacy
dns-search=
method=auto
```

Where <IP> = code of the robot in two digits format, being the first digit the letter of the robot and the second one its number, I.e. C1 is 31 and A2 is 12.

7) Backup calibration files Run jupyter notebook in a browser.

`http://<robotIP>:48888`

-   Run in the terminal

```Bash
  ## Save robot factory calibration files
  cat /data/deck_calibration.json > /var/lib/jupyter/notebooks/deck_calibration_factory.json
  ## Save robot factory settings
  cat /data/robot_settings.json > /var/lib/jupyter/notebooks/robot_settings_factory.json
```

-   Save factory configuration files. Saved in `\galeon\CNM_testPCR`

8) **Mount offset changes**
-   Run script normalize_mount_offset.py in the ot app en each robot. This script increases the clearance for the pipette travel to allow additional clearance as its moving to the tip probe in the future.
-   Restart OT from app.
    > **Note:** app and robot need to be updated first or an error is returned when uploading the protocol saying there are no steps in it.

9) [**Perform deck calibration**]( https://support.opentrons.com/en/articles/2687620-get-started-calibrate-the-deck): Use a pipette on the right mount - a P20S GEN2 is best.

10) **Check if calibration is correct:** Verify the robot's calibration Upload the attached protocol Do pipette and labware calibration as prompted. Run the protocol move_to_crosses.py . Visually check that the tip hits all the crosses.

-   *Pipette misses crosses:* Pipette misses crosses during calibration check The pipette tip should be within 1.5 mm of each cross. Additionally, any offset should be roughly consistent between crosses – 1.5 mm to the right of the first cross and 1.5 mm to the left of the second cross is unacceptable. Upload the test protocol again, redo pipette and labware calibration, and run it again. See if the results improve. If they do not improve, do a factory reset of pipette calibration through the app, and then do a new deck calibration.

-   *Pipette successfully hits all the crosses:* If the robot does hit all the crosses please back up the robot's verified calibration like we did with the other .json files save a robot's calibration.
    -   Open the OT-2's Jupyter notebook (robot_ip:48888 in a web browser).
    -   Open a terminal (New > Terminal).
    -   Enter:
    ```Bash
    cp /data/deck_calibration.json /data/robot_settings.json /var/lib/jupyter/notebooks
    ```
    -   Download deck_calibration.json and robot_settings.json from the Jupyter GUI to your computer and save them for each robot like we did for the initial factory calibration files

11) **Dry protocol.** This will include pipette and labware configurationn. And will be explained in other doc.

## Extra calibration steps

Some settings and pipete behaivours can only be set on the opentrons application and not the protocol script, so make sure they are activated in the Opentrons app of the computer you are using before launching a protocol. Examples of these are:

-   By default P1000 pipete shakes several times when picking up a new tip. It is suppose to be for shaking off adjacent tips that may attach to the pipete.
    
-   In order to attach or use an 8-channel pipette gen 2, you have to enable Developer Tools inside the app ("More" -> "Enable Developer Tools"). Then Developer Tools wile appear an you can enable multi-channel pipetes gen2 can be enabled by its option ("More" -> "__DEV__ Enable Multi GEN 2"). Now you can select multi-channel piptes gen 2 when attaching a new pipette.

## When do you need to calibrate

-   *Deck calibration* is when you move the pipette tip to the crosses etched on the deck. You need to do deck calibration: As part of setting the OT-2 up for the first time with one pipette. Once or twice per year, for maintenance. Or, if you're troubleshooting calibration issues.

-   *Pipette calibration* is prompted by the Opentrons App each time a protocol is uploaded at time of writing, but you do not need to complete pipette calibration each time a protocol is uploaded. Pipette calibration only needs to be redone if:
    -   The pipette has not yet been previously calibrated
    -   The pipette has been unmounted and remounted since the last time it was used in a protocol
    -   The pipette is being used with different tips from those used in its previous run
    -   The deck has been calibrated since the last run If none of the above circumstances are true, you can skip to labware calibration by clicking your tipracks in the calibration screen, or skip to the run by clicking the "Run" tab of the app.

-   *Labware calibration* is prompted after pipette calibration has been completed.
    -   In all cases, you must complete labware calibration if you have completed pipette calibration.
    -   However, if you skip pipette calibration, you may still need to complete labware calibration. Labware calibration needs to be completed if:
        -   Pipette calibration has been completed
        -   If there is any labware on the deck being used for the first time
        -   If you are troubleshooting calibration issues
