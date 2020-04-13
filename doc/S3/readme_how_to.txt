Index guide: https://support.opentrons.com/en/collections/1559720-guide-for-getting-started-with-the-ot-2#6-calibrate-the-ot-2

1) Unboxing. https://support.opentrons.com/en/articles/2687501-get-started-unbox-the-ot-2

2) Unlock. https://slack-redir.net/link?url=https%3A%2F%2Fsupport.opentrons.com%2Fen%2Farticles%2F2687521-get-started-unlock-the-ot-2

3) Make inventory. See excel in this folder.

4) Attach pipettes. https://support.opentrons.com/en/articles/2067321-get-started-attach-pipettes
NOTE: p20 on the RIGHT, needed later for recalibration.

5) Renaming the robot 
This changes the hostname of the robots.
Run scripts in the folder rename_robots with the ot app. One for each robot.
Restart the OT from the OP app.

6) Assigning static IP address
IP static robots. Important in the script variable use IP/16 (mandatory indicate the mask, must be the same that in the mac computer)
Run scripts in the folder statics_ips with the ot app. One for each robot.
Restart the OT from the OP app.
Set the IP for the USB network in the Mac to manual IP 169.254.10.10 y mask 255.255.0.0

7) Backup calibration files
Run jupyter notebook in a browser.
<Robot IP>:48888

- Run in the terminal
## Save robot factory calibration files
cat /data/deck_calibration.json >  /var/lib/jupyter/notebooks/deck_calibration_factory.json

## Save robot factory settings
cat /data/robot_settings.json >  /var/lib/jupyter/notebooks/robot_settings_factory.json

- Save factory configuration files. Saved in \\galeon\CNM_testPCR

8) Mount offset changes
Run script normalize_mount_offset.py in the ot app en each robot. This script increases the clearance for the pipette travel to allow additional clearance as its moving to the tip probe in the future.
Restart OT from app.
Note: app and robot need to be updated first or an error is returned when uploading the protocol saying there are no steps in it.

9) Perform a deck calibration.
Do a deck calibration, using a pipette on the right mount - a P20S GEN2 is best.
https://support.opentrons.com/en/articles/2687620-get-started-calibrate-the-deck

10) Check calibration is correct.
Verify the robot's calibration
Upload the attached protocol
Do pipette and labware calibration as prompted.
Run the protocol move_to_crosses.py . Visually check that the tip hits all the crosses.

- Pipette misses crosses:
Pipette misses crosses during calibration check
The pipette tip should be within 1.5 mm of each cross. Additionally, any offset should be roughly consistent between crosses – 1.5 mm to the right of the first cross and 1.5 mm to the left of the second cross is unacceptable.
Upload the test protocol again, redo pipette and labware calibration, and run it again. See if the results improve.
If they do not improve, do a factory reset of pipette calibration through the app, and then do a new deck calibration.


- Pipette successfully hits all the crosses:
If the robot does hit all the crosses please back up the robot's verified calibration like we did with the other .json files
Save a robot's calibration
Open the OT-2's Jupyter notebook (robot_ip:48888 in a web browser).
Open a terminal (New > Terminal).
Enter: cp /data/deck_calibration.json /data/robot_settings.json /var/lib/jupyter/notebooks
Download deck_calibration.json and robot_settings.json from the Jupyter GUI to your computer and save them for each robot like we did for the initial factory calibration files


11) Dry protocol. This will include pipette and labware configurationn.
