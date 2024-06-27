# K-9-
Imperial team with IBM

Group Members:
- Krrish Jain
- William Ho
- Ryusei Kinosaki
- Chenglin Sun
- Boyan Zhang
- Qidong Zhou

## Introduction

The aim of this project was to build an AI companion robot pet for the elderly with the following features:

- Listen to voice commands to control the pet
- Control the movement of the pet
- Allow the pet to read the news
- Play music or podcasts requested by the user

These features help to encourage more positive behaviours for the user, through engaging physical and vocal interactions, as well as, providing companionship to help combat elderly loneliness.

### Project Specification

### Project Maangement and Meetings

### Testing processes

## Hardware

### Materials

### CAD Design

## Software

### Chatbot

### Movement

For the movement, the quarduped_new.py file contains 2 classes which are responsible for controlling the robot's movements. Using the adafruit_servokit library to control the servos, the approach we chose to use was to use inverse kinematics to calculate where to position each leg.

#### Motor Class

The motor class is used to help identify the corresponding pin location with the motor location.

#### Quadruped Class

The quardruped class is the main class to control the robot. 

- The class constructor __init__, initialises the object and instantiates the ServoKit and defines the initial lengths and angles for the leg. It also sends out a pulse width range for each servo motor.
- There are 2 functions to assist with controlling the movement, set_angle, and rad_to_degree. These functions help by setting the angle for the servo and converting radians to degrees, respectively.
- The calibrate function sets the pet to it's standing up position by getting those values from a dictionary, pos_dict.
- The sit function sets the pet to a sitting position by getting the standing up position from the dictionary, pos_dict, and adjusting the shoulder values by a constant value.
- The inverse_kinematics functions runs to get the desired angles, theta1 and theta2, based on the target x and y co-ordinates.
- The move function will use the angle that is calculated in the inverse_kinematics function to set the angle of the servos to the desired positions, as well as being able to adjust the direction of movement.
- THe pushups function moves the robot to a calibrated position, lowers the back legs and then proceeds to lower and extend the front legs.
- The steps function will call on the move function based on direction for a certain number of steps.

For the inverse kinematics:
1. First calculate distance, d, as the square root of x squared + y squared
2. Then, calculate theta2, which is pi take away the arccos of the length of upper leg squared + lower leg squared - d squared divided by 2 times the lower leg length times the upper leg length.
3. Then, get phi, by getting the arccos of the upper leg squared - lower leg squared + d squared divided by 2 times the upper leg length times d squared.
4. Finally, theta1 is the arctan2 of y, x - phi.

### Computer Vision

The computer vision code is in the bone_detector.py file. This code contains one class, the Follower class, and is used to detect a green bone, the colour values are set in the variables colorLower and colorHigher. The code uses the picamera2 library for the camera and cv2 for computer vision. The code will capture array from the camera and turn it into HSV colour space which creates a mask based on the desired color ranges, noise is then removed from the mask and a moments is created of the binary mask. A rectangle is then created around the desired object and will rotate the camera to center the object and turn the robot and move towards it.

## Setup

## Acknowledgements

## References
