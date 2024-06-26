#!/usr/bin/python3

import cv2
from adafruit_servokit import ServoKit
from picamera2 import Picamera2
from time import sleep


class Follower:
  colorLower = (57, 100, 100)
  colorUpper = (77, 255, 255)

  HEAD_SERVO = 0
  tiltAngle = 90

  def __init__(self):
    self.picam2 = Picamera2()
    self.picam2.configure(self.picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
    self.picam2.start()
    self.kit = ServoKit(channels=16)
    self.kit.servo[0].set_pulse_width_range(500,2500)
    self.set_servo_angle(90)
    self.tiltAngle = 90
    self.cv_switch = True

  def set_servo_angle(self,degrees):
    self.kit.servo[0].angle = degrees

  def move_servo(self,x,y):
    if (x < 240):
      self.tiltAngle += 3
      if self.tiltAngle > 140:
        self.tiltAngle = 140
        #print("move left")
      self.set_servo_angle (self.tiltAngle)
      sleep(0.02)
    if (x > 400):
      self.tiltAngle -= 3
      if self.tiltAngle < 40:
          self.tiltAngle = 40
          #print("move right")
      self.set_servo_angle (self.tiltAngle)
      sleep(0.02)
      

  def start_follow(self):
    
    while True:
      tmp = self.cv_switch
      
      im = self.picam2.capture_array()
      hsv = cv2.cvtColor(im, cv2.COLOR_BGR2HSV)

      mask = cv2.inRange(hsv, self.colorLower, self.colorUpper)
      mask = cv2.erode(mask, None, iterations=2)
      mask = cv2.dilate(mask, None, iterations=2)

      M = cv2.moments(mask)

      centre_x = -1
      centre_y = -1

      if M["m00"] > 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        x, y, w, h = cv2.boundingRect(mask)
        cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 2)
        centre_x = x + w/2
        centre_y = y + y/2
        #print("(x,y) = ({0},{1})".format(centre_x,centre_y))
      else:
        centre_x = -1
        centre_y = -1

      if (centre_x != -1 and centre_y != -1):
        self.move_servo(centre_x, centre_y)

      #cv2.imshow("Frame", im)
      key = cv2.waitKey(1) & 0xFF
      if key == ord("q"):
        break
      
      if tmp == False:
        break
      
      


    cv2.destroyAllWindows()
    
  def change_switch(self, outer):
    self.cv_switch = outer
    

    


if __name__ == '__main__':
  print("starting")
  f = Follower()
  f.start_follow()


