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

### Project Manangement and Meetings

### Testing processes

## Hardware
### Components
The robodog consists of the following components:

* 11x MG995 Servo Motor
* 1x 6V, 5.5A Buck Voltage Converter
* 1x 6V to 5V/8A Buck Voltage Converter
* 1x 11.1V 3500mAh 3S1C Lithium Ion Battery
* 1x Adafruit Mini USB Microphone
* 1x MikroElektronika 2x20W Audio Amplifier
* 1x Raspberry Pi 4B (8GB RAM)
* 1x 16A Rocker Switch
* 1x OLED 128x64 Pixels
* 1x 300mm RPi Camera Ribbon
* 1x Raspberry Pi Camera
* 4x 8 Ω 1 W Speaker
* 4x Squash Balls
* PLA Filament
* PETG Filament
  
### CAD Design
The IBM K-9 bot's body is divided into 3 parts: the chassis, the legs and the head, where each of them were designed for the sake of practicality, manoeuverability and compactness.
Unless otherwise specified, the material used are PLA filament, which were 3D printed for the sake of rapid prototyping and bespoke modifications.

<h2>Legs</h2>
The mechanism of the legs is controlled by two servos, each controlling the shoulder (upper half of the leg) and the elbow (lower half of the leg).
The torque of the shoulder is controlled directly via the servo, whose circular attachment is slotted into the shoulder and fastened with a screw.
The torque of the elbow is transfered via the links which are attached between the servo and the elbow.
Finally, the feet of the chassis is a squash ball cut into half. The advantage of the squash ball is the higher friction surface and elasticity, preventing the K-9 from slipping while walking towards the user.

The mechanism works consistently, however, collisions and wear could loosen the joints, hence improvemets is possible with the use of ball bearings and adjusting the cad so the bearings would slot into them.

<h2>Head</h2>
The head works as a housing for the audio amplifier, speaker and the camera which could not be put into the circuit within the chassis. The design was made to be as compact as possible so that the weight would not affect the walking control. Moreover, it was made with the same design approach as the legs, where it can be easily put on the servo's circular bit.

<h2>Chassis</h2>
The chassis itself was made mainly to house the circuitry, while also holding switches and the OLED display. Instead of making one large chassis, it was divided into parts so that only one small part had to be printed in case of any problems. The central body of the chassis was made by PETG filament whose flexibility allowed for the components to be assembled easier.

### Circuitry
The circuit that controls the robodog is shown in the block diagram below.

![K9 Block](https://github.com/ydclzby/K-9/assets/105930789/0293a27a-12aa-443a-b428-09d847a4ecbd)


## Software

### Chatbot

The chatbot implementation leverages IBM Watson Assistant, speech recognition, and various other APIs to provide interactive functionalities. This section details the important classes and aspects involved in the chatbot implementation.

#### SysState Class

The `SysState` class is central to managing the state of the system and coordinating interactions between the various components and APIs.

##### Initialization

- **`__init__(self, history_fp)`**
  - Initializes system state variables.
  - Sets up the IBM Watson Assistant API.
  - Configures the Picamera and servos for movement.
  - Instantiates a `Quadruped` object for controlling the robot.

##### Methods

- **chatbot_thread()**
  - Initializes the IBM Watson Assistant using the provided API key and service URL.
  - Manages a session with the Assistant, sending user commands and processing responses.
  - Adjusts the system mode based on the Assistant's responses.

- **audio_thread()**
  - Listens for audio commands using a microphone.
  - Converts speech to text using the `speech_recognition` library.
  - Sets the recognized text as a command for processing.

- **mode_thread()**
  - Executes actions based on the current mode, such as reading text, playing podcasts, fetching news, playing songs, and controlling the robot's movements.

#### IBM Watson Assistant Integration

The IBM Watson Assistant is used to interpret user commands and provide responses. 

##### Methods

- **chatbot_thread()**
  - **authenticator = IAMAuthenticator(api_key)**
    - Authenticates using the IBM Cloud API key.
  - **assistant = AssistantV2(version='2024-05-03', authenticator=authenticator)**
    - Initializes the Assistant with the specified version and authenticator.
  - **assistant.set_service_url(service_url)**
    - Sets the service URL for the Assistant.
  - **response = assistant.create_session(assistant_id=assistant_id).get_result()**
    - Creates a session with the Assistant.
  - **response = assistant.message(assistant_id=assistant_id, session_id=session_id, input=message_input).get_result()**
    - Sends user commands to the Assistant and processes the response.

#### Speech Recognition Integration

The `speech_recognition` library is used to capture and interpret audio commands from the user.

##### Methods

- **audio_thread()**
  - **recognizer = sr.Recognizer()**
    - Initializes the recognizer.
  - **mic = sr.Microphone()**
    - Sets up the microphone.
  - **audio = recognizer.listen(source, timeout=5.0, phrase_time_limit=3.0)**
    - Listens for audio input with a timeout and phrase time limit.
  - **recognized_text = recognizer.recognize_google(audio)**
    - Converts the captured audio to text using Google’s speech recognition API.

#### Additional APIs and Functionalities

##### News API

The News API fetches the latest news articles on a given topic.

- **get_news(topic)**
  - **params = {'api-key': news_api_key, 'q': topic, 'page-size': 1, 'order-by': 'relevance'}**
    - Sets the parameters for the news search.
  - **response = requests.get(news_endpoint, params=params)**
    - Sends a request to the News API to fetch articles.

##### iTunes API

The iTunes API is used to search for and play podcasts.

- **first_podcast(topic)**
  - **params = {'term': topic, 'media': 'podcast', 'limit': 1}**
    - Sets the parameters for the podcast search.
  - **response = requests.get(itunes_search_url, params=params)**
    - Sends a request to the iTunes API to search for podcasts.

##### Jamendo API

The Jamendo API fetches songs based on a given topic.

- **get_song(topic)**
  - **params = {'client_id': CLIENT_ID, 'format': 'json', 'limit': 1, 'tags': topic, 'order': 'popularity_total_desc'}**
    - Sets the parameters for the song search. This implementation fetches the most popular song under a user-specified genre (topic).
  - **response = requests.get(api_url, params=params)**
    - Sends a request to the Jamendo API to search for songs.

#### Thread Management

The chatbot employs threading to manage different tasks concurrently.

- **threading.Thread(target=ibm_Chatbot.chatbot_thread).start()**
  - Starts the chatbot thread to handle interactions with IBM Watson Assistant.
- **threading.Thread(target=ibm_Chatbot.audio_thread).start()**
  - Starts the audio thread to capture and process audio commands.
- **threading.Thread(target=ibm_Chatbot.mode_thread).start()**
  - Starts the mode thread to execute actions based on the system mode.

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
