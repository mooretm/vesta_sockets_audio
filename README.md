# **Socket Audio Player**

Audio player with server that accepts commands from "Vulcan Over Sockets" app. Necessary because Vulcan does not support a version of Python that works with ASIO. I know. 😒

- Written by: **Travis M. Moore**
- Originally created: **October 28, 2022**
- Latest version: **Version 0.0.0**
- Last edited: **March 01, 2023**
<br>
<br>

---

## Description
- The Vesta project was developed to provide a user-friendly interface to read/write hearing aid parameters that is also appropriate for data collection purposes. 

- This particular version of Vesta was created to force snapshots for Dynamic Edge Mode, as well as allow self-paced participant-led data collection. 

- Test conditions should be provided as a matrix in .csv format.

- Session data are output in .csv format. This avoids data entry errors (e.g., transferring 
paper scores into a spreadsheet), as well as provides a common format for storing
scores (e.g., for use with automated data entry scripts). 
<br>
<br>

---

## Getting Started

### Dependencies

- Windows 10 or greater (not compatible with Mac OS)
- Python 3.6, 32-bit (must be this version)

### Installing

- This is a compiled app; the executable file is stored on Starfile at: \\starfile\Public\Temp\MooreT\Custom Software
- Simply copy the executable file and paste to a location on the local machine
- Double click to start the app

### First Use
- Double-click to start the application for the first time.
- Go to **File-->Session** to provide file paths to stimulus files, as 
well as enter session information 
- Go to **Tools-->Audio** Settings to enter a valid audio device ID.
- Go to **Tools-->Calibration** to calibrate using a sound level meter.
- Click the START button on the main screen to begin.
<br>
<br>

---

## Session Details
The Speech Task Controller requires several pieces of session information. Navigate to **File-->Session** to open the Session window (see image below).

<!-- <img src="./assets/images/session_info_window.png" alt="Session Info Window image" width="600"/> -->
<img src="session_info_window.png" alt="Session Info Window image" width="600"/>

### Session Information
The first section of the Session window asks for the following information:

- Subject: The participant ID number. Can be alphanumeric. 
- Condition: A custom name for the current condition. Use underscores to add additional descriptors. For example: `quiet_highpass_unaided`.
- List(s): Specify the list you would like to present from the speech test/corpus. Enter additional list numbers separated by spaces to present multiple lists. For example: `1 2 5`. Lists do not have to be in sequential order. 
- Level (dB): Enter the desired presentation level, using up to one decimal place For example: `65.5`.

### Stimulus Directories
Provide the Speech Task Controller with the file paths to your stimuli. 

- Click the BROWSE button in the "Audio File Directory" section and navigate to the folder containing your audio files.
- Click the BROWSE button in the "Sentence File Directory" section and navigate to the folder containing your .csv file of sentence text.
<br>
<br>

---

## Stimulus Requirements

### Matrix File
Vesta requires a matrix file containing all unique experiment conditions. 

<img src="sentence_list.png" alt="Sentence List image" width="600"/>

### Audio Files

- All audio files must be in .wav format. 
- Vesta **does not** support 24-bit audio files.
- There should be a single instance of each .wav file. 
- Audio file names must match those list in the matrix file.
<br>
<br>

---

## Audio Device Selection and Channel Routing
### Choose an Audio Device
The Audio Settings window will display a list of available audio devices in 
tabular format (see image below). Navigate to **Tools-->Audio Settings** to open the Audio Settings window.

1. Use the "name" column to find the desired audio device (often 
the Hammerfall ASIO device in the clinical research labs). 
2. Ensure that the number of channels out in the "chans_out" column is not 0, 
and is sufficient for the desired number of audio channels/speakers. For example, to present audio from speaker 5, there must be at least 5 channels in the "chans_out" column.
3. After you have identified the appropriate audio device, enter its ID number 
from the "device_id" column into the "Audio Device ID" text entry box. 
4. Finally, click the SUBMIT button to save your selections. 

<img src="audio_settings_window.png" alt="Audio Settings Window image" width="600"/>

### Choose a Speaker
Because this version of Vesta expects 8-channel ambisonic .wav files, there is no need to specify speaker routing. Vesta will simply assign each channel to a speaker based on its position in the .wav file. For example, the first audio channel in the .wav file will be assigned to speaker 1, the second audio channel to speaker 2, etc. <br>
NOTE: The speaker number refers to the channel assigned to a speaker by the soundcard. Check the speaker routing to identify its number.
<br>
<br>

---

## Calibration
Before actual use in an experiment, the Speech Task Controller must be calibrated using a sound level meter (SLM). Use the menu to navigate to **Tools-->Calibration** to open the calibration window (see image below).

<!-- <img src="./assets/images/calibration_window.png" alt="Calibration Window image" width="600"/> -->
<img src="calibration_window.png" alt="Calibration Window image" width="600"/>

### Choose Calibration Stimulus
There are two options when calibrating.

1. The Speech Task Controller contains its own white noise stimulus for general calibration. Select the "White Noise" button to use this stimulus.
2. The "Custom File" button allows for an existing calibration file to be loaded. For example, to present IEEE sentences, load in the IEEE calibration file. 

### Play Calibration Stimulus
Clicking the PLAY button will present the calibration stimulus. You can set the level of the calibration stimulus using the "Raw Level (dB FS)" text entry box. A level of -30 dB FS is relatively safe, and is the default value. Making the Raw Level more negative will decrease the presentation level. Making the Raw Level more positive will increase the presentation level. It is not recommended to make this level more positive to avoid damaging the speakers. 

### Sound Level Meter
After you have loaded a calibration file and set up the SLM, press the PLAY button (Note: Make sure you have the SLM set to the proper speed and weighting [e.g., slow, dBA]). Enter the value from the SLM into the "SLM Reading (dB)" text entry box. Click the SUBMIT button to save the SLM value. 
<br>
<br>

---

## Data Output
Session data are written after each response as a new line in the data .csv file. This file serves as a record of the session and can be used to calculate scores for later analysis. The file appears in the same directory as the Vesta app, with a naming convention of: `subject_condition_year_month_day_time.csv`. This ensures previous records are not overridden, even if you need to repeat the same condition on the same day. 

The data .csv file stores the following information on each trial: 

- trial: a counter starting at 1 and increasing with each presentation
- subject: taken from the Session window
- condition: taken from the Session window
- scaling_factor: the factor used to scale the audio level (taken from the matrix file)
- raw_lvl: hard-coded starting level in dB FS
- slm_cal_val: the SLM value entered in the Calibration window
- slm_offset: calculated as `SLM Calibration Value - Raw Level`
- new_db_lvl: calculated on each trial using values in the "Step (dB)" text entry boxes on the main screen
- new_raw_lvl: calculated as `new_db_lvl - slm_offset`
- snapshot_A: the snapshot assigned to the "A" button for a given trial
- snapshot_B: the snapshot assigned to the "A" button for a given trial
- expected_response: the snapshot that should match a given audio stimulus for a given trial (provided in the matrix file)
- Outcome: a `1` or `0` based on whether the RIGHT or WRONG button was clicked, respectively

<br>
<br>

---

## Compiling from Source
```
pyinstaller --noconfirm --onefile --windowed --add-data "C:/Users/MooTra/Code/Python/vesta/assets/cal_stim.wav;." --add-data "C:/Users/MooTra/Code/Python/vesta/assets/README;README/"  "C:/Users/MooTra/Code/Python/vesta/controller.py"
```
<br>
<br>

---

## Contact
Please use the contact information below to submit bug reports, feature requests and any other feedback. Thank you for using Vesta!

- Travis M. Moore: travis_moore@starkey.com
