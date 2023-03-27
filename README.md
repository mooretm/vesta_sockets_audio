# **Socket Audio Player**

- Written by: **Travis M. Moore**
- Latest version: **Version 1.1.0**
- Originally created: **February 28, 2023**
- Last edited: **March 27, 2023**
<br>
<br>

---

## Description
Audio player with server that accepts commands from "Vulcan Over Sockets" app. Necessary because Vulcan does not support a version of Python that works with ASIO. I know. 😒
<br>
<br>

---

## Getting Started

### Dependencies

- Windows 10 or greater (not compatible with Mac OS)

### Installing

- This is a compiled app; the executable file is stored on Starfile at: \\starfile\Public\Temp\MooreT\Custom Software
- Simply copy the executable file and paste to a location on the local machine
- Double click to start the app

### First Use
- Double-click to start the application for the first time.
- Go to **Tools-->Audio** Settings to enter a valid audio device ID.
- Go to **Server-->Start Server** to start the server.
<br>
<br>

---

## Audio Device
### Audio Device Selection
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

### Channel Routing
Channels are currently routed to speakers in order; the first channel of audio is routed to speaker 1, the second channel to speaker 2, etc. Currently the only way to control routing is to reorder the channels in the audio file. 
<br>
<br>

---

## Calibration
Navigate to **Tools-->Calibration** to open the calibration window (see image below).

<!-- <img src="./assets/images/calibration_window.png" alt="Calibration Window image" width="600"/> -->
<img src="calibration_window.png" alt="Calibration Window image" width="600"/>

### Calibration Stimulus Selection
There are two options when calibrating.

1. The Speech Task Controller contains its own white noise stimulus for general calibration. Select the "White Noise" button to use this stimulus.
2. The "Custom File" button allows for an existing calibration file to be loaded. For example, to present IEEE sentences, load in the IEEE calibration file. 

### Calibration Stimulus Playback
Clicking the PLAY button will present the calibration stimulus. You can set the level of the calibration stimulus using the "Level (dB)" text entry box. A level of -30 dB is relatively safe, and is the default value. Making the level more negative will decrease the presentation level. Making the level more positive will increase the presentation level. Be careful not to overdrive the speakers!
<br>
<br>

---

## Compiling from Source
```
pyinstaller --noconfirm --onefile --windowed --add-data "C:/Users/MooTra/Code/Python/vesta_sockets_audio/assets/cal_stim.wav;." --add-data "C:/Users/MooTra/Code/Python/vesta_sockets_audio/assets/README;README/"  "C:/Users/MooTra/Code/Python/vesta_sockets_audio/controller.py"
```
<br>
<br>

---

## Contact
Please use the contact information below to submit bug reports, feature requests and any other feedback. Thank you for using the Socket Audio Player!

- Travis M. Moore: travis_moore@starkey.com
