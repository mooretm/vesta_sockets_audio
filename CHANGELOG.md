# **Change Log**

---

## v1.1.0

Date: Mar 27, 2023

### Major Bug Fixes
1. Fixed bug where entering a level of 0 would be read as None. This resulted in normalizing instead of applying the level (if statement checking for level evaluated to None). The effect was a slow increase in level as the entered value approached 0, then a big jump at 0 (i.e., normalizing to full scale), then a return to a lower level above 0.
<br>
<br>

---

## v1.0.1

Date: Mar 17, 2023

### Minor Features
1. Cleaned up messages printed to console to be more legible.
<br>
<br>

---

## v1.0.0

Date: Mar 09, 2023

### Initial Release
1. An audio player with server for receiving instructions from the Vesta Over Sockets app. This is necessary because Vulcan requires Python 3.6 (32-bit), which does not work with the ASIO driver in the labs. 
<br>
<br>
