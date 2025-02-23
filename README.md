# EYEfollow
Steven Caro and Gian Favero, 2023

![Screenshot](images/Logo.png)

EYEfollow is a novel diagnostic device that combines an interactive user experience with cutting-edge eye tracking technology to deliver easy, fast, and accurate eye assessments.

EYEfollow is currently under development at the University of Windsor in a partnership between the Human Systems Lab (supervised by Dr. Bala Balasingam) and Dr. Moussa, a leading optometrist in the Windsor-Essex region.

## Getting Started
### Gazepoint GP3 Software
1) Find the Gazepoint software at this Dropbox [link](https://www.dropbox.com/s/7wtdwbvmq8ws1ud/Gazepoint_5.1.0.exe?dl=0) 
2) Download and then use the wizard to install the accompanying Gazepoint applications (Analysis, Control, etc)
3) Locate and open Gazepoint Control and Gazepoint Analysis
4) In Gazepoint Analysis, make a new project and hit the calibrate button
5) Wait for calibration to finish, then exit Gazepoint Analysis and return to Gazepoint Control
6) Ensure that the calibration sequence occurs when the calibrate button is pressed.
7) Press "P" to enable Gain Sweep (will be indicated in the status bar at the bottom of the window)

### Running the Code
This project requires Python 3.9.

1) Clone the repository
2) Install the required packages by running `pip install -r requirements.txt` in your environment
3) Launch the GUI by running `application.py`

### Data Collection
Gazepoint Control should automatically open alongside the GUI, and should become the active window once the `Start` button is pressed. It is recommended to use this window to calibrate the Gazepoint GP3 prior to entering the participant's name and starting the test(s).

Once the test(s) are complete, the collected eye data is outputted as a .xlsx file within a newly created `Test Results` directory located on the Desktop. 

### Distribution
The EYEfollow application can be distributed as a .bat file which included in this repository.

For ease of use, create a shortcut to the EYEfollow.bat file on your desktop or location of choice. Simply double-clicking EYEfollow.bat should first update the code (via git commands), then launch the EYEfollow application. 

