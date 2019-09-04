# DJI Tello Face Track

This is a ComputerVision/Control algorithm which forces a DJI Tello drone to center the camera according to your face position. if the camera don't detect any face then turn around until detect anyone.

# Dependencies 
<br>
This algorithm is based on: 
<br>
djitellopy ver 1.5 by https://github.com/damiafuentes
<br>
selfie-drone by https://github.com/the-beast-code
<br> opencv-python 
<br> 

# Install

```
pip install djitellopy
```

```
git clone https://github.com/Jacobprojects/Tello-FaceTrack.git
```
```
cd Tello-FaceTrack
```
```
pip install -r requirements.txt
```

# Usage 

```
python face.py
```

### Notes 
You need to be careful with the place where you are flying.
<br>
Im working to fix some bugs.
