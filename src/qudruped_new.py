from adafruit_servokit import ServoKit
from enum import IntEnum
import math
import bezier
import numpy as np
from time import sleep


#from measurements
#FR:
# shoulder angle: 138
# elbow angle: 75
class Motor(IntEnum):
    # identifies the corresponding pin location with the motor location
    FR_SHOULDER = 4
    FR_ELBOW = 2
    FR_HIP = 9
    FL_SHOULDER = 3
    FL_ELBOW = 1
    FL_HIP = 10
    BR_SHOULDER = 6
    BR_ELBOW = 8
    BL_SHOULDER = 5
    BL_ELBOW = 7

class Quadruped:

    #    pos_dict = {Motor.FR_SHOULDER: 87, Motor.FR_ELBOW: 58, Motor.FR_HIP:95, Motor.FL_SHOULDER: 90, Motor.FL_ELBOW:94, Motor.FL_HIP:75, Motor.BR_SHOULDER:73, Motor.BR_ELBOW:62, Motor.BL_SHOULDER:86, Motor.BL_ELBOW:90}
#    pos_dict = {Motor.FR_SHOULDER: 70, Motor.FR_ELBOW: 47, Motor.FR_HIP:90, Motor.FL_SHOULDER: 106, Motor.FL_ELBOW:96, Motor.FL_HIP:83, Motor.BR_SHOULDER:63, Motor.BR_ELBOW:65, Motor.BL_SHOULDER:100, Motor.BL_ELBOW:84}
    pos_dict = {Motor.FR_SHOULDER: 65, Motor.FR_ELBOW: 62, Motor.FR_HIP:90, Motor.FL_SHOULDER: 106, Motor.FL_ELBOW:81, Motor.FL_HIP:83, Motor.BR_SHOULDER:60, Motor.BR_ELBOW:80, Motor.BL_SHOULDER:100, Motor.BL_ELBOW:69}
    shoulder_ang_measured = 138
    elbow_ang_measured = 75

    L1 = 10  # Upper leg length in cm
    L2 = 10.5  # Lower leg length in cm
    def __init__(self):
        self.kit = ServoKit(channels=16)
        self.upper_leg_length = 10
        self.lower_leg_length = 10.5
        for i in range(10):
            self.kit.servo[i].set_pulse_width_range(500,2500)
            sleep(0.2)

        #from measurements FR shoulder angle is 360-138 and elbow angle is 180-75
        initial_shoulder_angle = np.radians(360-self.shoulder_ang_measured)
        initial_elbow_angle = np.radians(180-self.elbow_ang_measured)
        shoulder_x, shoulder_y = 0, 0
        elbow_x = self.L1 * np.cos(initial_shoulder_angle)
        elbow_y = self.L1 * np.sin(initial_shoulder_angle)
        self.initial_foot_x = elbow_x + self.L2 * np.cos(initial_shoulder_angle + initial_elbow_angle)
        self.initial_foot_y = elbow_y + self.L2 * np.sin(initial_shoulder_angle + initial_elbow_angle)



    def set_angle(self,motor_id, degrees):
        """
        set the angle of a specific motor to a given angle
        :param motor_id: the motor id
        :param degrees: the angle to put the motor to
        :returns: void
        """
        self.kit.servo[motor_id].angle = degrees

    def rad_to_degree(self,rad):
        """
        Converts radians to degrees
        :param rad: radians
        :returns: the corresponding degrees as a float
        """
        return rad*180/math.pi

    def calibrate(self):
        """
        sets the robot into the default "middle position" use this for attaching legs in right location
        :returns: void
        
        OLD CODE:
        self.set_angle(Motor.FR_SHOULDER, 87) #60 27 
        self.set_angle(Motor.FR_ELBOW, 58) # 85 27
        self.set_angle(Motor.FR_HIP, 95)
#        sleep(0.5)
        self.set_angle(Motor.FL_SHOULDER, 90) #117
        self.set_angle(Motor.FL_ELBOW, 94) #67
        self.set_angle(Motor.FL_HIP, 75)
        #sleep(0.5)
        self.set_angle(Motor.BR_SHOULDER, 73) #46
        self.set_angle(Motor.BR_ELBOW, 62) #89
        #sleep(0.5)
        self.set_angle(Motor.BL_SHOULDER, 86) #113
        self.set_angle(Motor.BL_ELBOW, 90) #87
        """
        self.set_angle(Motor.FR_SHOULDER, self.pos_dict[Motor.FR_SHOULDER]) #60 27 
        self.set_angle(Motor.FR_ELBOW, self.pos_dict[Motor.FR_ELBOW]) # 85 27
        self.set_angle(Motor.FR_HIP, self.pos_dict[Motor.FR_HIP])
        #sleep(0.5)
        self.set_angle(Motor.FL_SHOULDER, self.pos_dict[Motor.FL_SHOULDER]) #117
        self.set_angle(Motor.FL_ELBOW, self.pos_dict[Motor.FL_ELBOW]) #67
        self.set_angle(Motor.FL_HIP, self.pos_dict[Motor.FL_HIP])
        sleep(0.1)
        self.set_angle(Motor.BR_SHOULDER, self.pos_dict[Motor.BR_SHOULDER]) #46
        self.set_angle(Motor.BR_ELBOW, self.pos_dict[Motor.BR_ELBOW]) #89
        #sleep(0.5)
        self.set_angle(Motor.BL_SHOULDER, self.pos_dict[Motor.BL_SHOULDER]) #113
        self.set_angle(Motor.BL_ELBOW, self.pos_dict[Motor.BL_ELBOW]) #87


    def sit(self):
            
        self.set_angle(Motor.BR_SHOULDER, self.pos_dict[Motor.BR_SHOULDER]- 40) #46
        self.set_angle(Motor.BR_ELBOW, self.pos_dict[Motor.BR_ELBOW]) #89
        #sleep(0.5)
        self.set_angle(Motor.BL_SHOULDER, self.pos_dict[Motor.BL_SHOULDER] + 40) #113
        self.set_angle(Motor.BL_ELBOW, self.pos_dict[Motor.BL_ELBOW]) #87

        sleep(0.5)

        self.set_angle(Motor.FR_SHOULDER, self.pos_dict[Motor.FR_SHOULDER] - 10) #60 27 
        self.set_angle(Motor.FR_ELBOW, self.pos_dict[Motor.FR_ELBOW]) # 85 27
        self.set_angle(Motor.FR_HIP, self.pos_dict[Motor.FR_HIP])
        #sleep(0.5)
        self.set_angle(Motor.FL_SHOULDER, self.pos_dict[Motor.FL_SHOULDER] + 10) #117
        self.set_angle(Motor.FL_ELBOW, self.pos_dict[Motor.FL_ELBOW]) #67
        self.set_angle(Motor.FL_HIP, self.pos_dict[Motor.FL_HIP])
    
    
    def inverse_kinematics(self, shoulder_num, elbow_num, hip_num, x, y, z, right):
        d = np.sqrt(x**2 + y**2)
        #print(d)
        if d > (self.L1 + self.L2) or d < abs(self.L1 - self.L2):
            return None, None  # The target is unreachable
        theta2 = np.radians(180)-np.arccos((self.L1**2 + self.L2**2 - d**2) / (2 * self.L1 * self.L2))
        phi = np.arccos((self.L1**2 + d**2 - self.L2**2) / (2 * self.L1 * d))
        theta1 = np.arctan2(y, x) - phi
        #print((np.degrees(theta1),np.degrees(theta2),np.degrees(phi)))

        
        ch_right = 1
        if not right:
            ch_right = -1
        shoulder_servo_angle = self.pos_dict[shoulder_num] - ((np.degrees(theta1) + self.shoulder_ang_measured) * ch_right)
        elbow_servo_angle = self.pos_dict[elbow_num] + (((180-np.degrees(theta2)) - self.elbow_ang_measured) * ch_right)

        self.set_angle(shoulder_num, shoulder_servo_angle)
        self.set_angle(elbow_num, elbow_servo_angle)
        if(hip_num != None):
            hip_servo_angle = self.pos_dict[hip_num] + z.item() + 90
            #print(z)
            #print(hip_servo_angle)

            self.set_angle(hip_num, hip_servo_angle)
            #print(np.degrees(z))
        #print((shoulder_servo_angle, elbow_servo_angle))

        return theta1, theta2
    
    def move(self, radiusX, radiusY, direction):

        arr_len = 60
        arr_len_half = arr_len/2
        t = np.linspace(0, 2 * np.pi, arr_len)

        #no phase change
        center_x = self.initial_foot_x + radiusX #change to + for other leg
        center_y = self.initial_foot_y

        foot_x = center_x - radiusX * np.cos(t) # change to - for other leg

        #foot_y = center_y + (radiusY + FR_BL_y_offset) * np.sin(t) #change to + for other leg
        foot_y = np.zeros(arr_len)
        foot_y[0:30] = center_y + (radiusY+2) * np.sin(t[0:30])
        foot_y[30:60] = center_y + radiusY * np.sin(t[30:60])
    
        #change phase by 180 degrees
        center_x_inv = self.initial_foot_x - radiusX #change to + for other leg
        center_y_inv = self.initial_foot_y

        foot_x_inv = center_x_inv + radiusX * np.cos(t) # change to - for other leg
        foot_y_inv = center_y_inv - radiusY * np.sin(t) #change to + for other leg

        #Turning
        foot_z = np.ones(60) * -90
        foot_z_inv = np.ones(60) * -90
        swing_range_degrees = 30  # Adjust this value to change the swing range in degrees
        midpoint_degrees = -90  # The constant midpoint of the swing

        if(direction == 0): #forward comp
            swing_range_degrees = 8
            foot_z = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * np.sin(t) / np.radians(90)  
            foot_z = np.degrees(foot_z)

            foot_z_inv = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * -np.sin(t) / np.radians(90)
            foot_z_inv = np.degrees(foot_z_inv)

        if(direction == 1): #back comp
            swing_range_degrees = 3
            foot_z = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * np.sin(t) / np.radians(90)  
            foot_z = np.degrees(foot_z)

            foot_z_inv = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * -np.sin(t) / np.radians(90) 
            foot_z_inv = np.degrees(foot_z_inv)

        if(direction == 2): #right
            foot_z = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * np.sin(t) / np.radians(90)  
            foot_z = np.degrees(foot_z)

            foot_z_inv = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * -np.sin(t) / np.radians(90)  
            foot_z_inv = np.degrees(foot_z_inv)

        if(direction == 3): #left
            foot_z = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * -np.sin(t) / np.radians(90)  
            foot_z = np.degrees(foot_z)

            foot_z_inv = np.radians(midpoint_degrees) + np.radians(swing_range_degrees) * np.sin(t) / np.radians(90) 
            foot_z_inv = np.degrees(foot_z_inv)

        if(direction == 1):
            foot_x = foot_x[::-1]
            foot_y = foot_y[::-1]
            foot_x_inv = foot_x_inv[::-1]
            foot_y_inv = foot_y_inv[::-1]

        for x, y, z, x2, y2, z2 in zip(foot_x, foot_y, foot_z, foot_x_inv, foot_y_inv, foot_z_inv):
            theta1, theta2 = self.inverse_kinematics(Motor.FR_SHOULDER, Motor.FR_ELBOW, Motor.FR_HIP, x, y, z, right = True)
            theta1, theta2 = self.inverse_kinematics(Motor.BL_SHOULDER, Motor.BL_ELBOW, None, x, y, z, right = False)

            theta1, theta2 = self.inverse_kinematics(Motor.FL_SHOULDER, Motor.FL_ELBOW, Motor.FL_HIP, x2, y2, z, right = False)
            theta1, theta2 = self.inverse_kinematics(Motor.BR_SHOULDER, Motor.BR_ELBOW, None, x2, y2, z, right = True)


    # def calculate_leg_positions(shoulder_angle, elbow_angle):
    #     shoulder_x, shoulder_y = 0, 0
        
    #     elbow_x = L1 * np.cos(shoulder_angle)
    #     elbow_y = L1 * np.sin(shoulder_angle)
        
    #     foot_x = elbow_x + L2 * np.cos(elbow_angle + shoulder_angle)
    #     foot_y = elbow_y + L2 * np.sin(elbow_angle + shoulder_angle)

    #     return (shoulder_x, shoulder_y), (elbow_x, elbow_y), (foot_x, foot_y)

    def pushups(self):
        self.calibrate()
        sleep(1)
        self.set_angle(Motor.BR_SHOULDER, self.pos_dict[Motor.BR_SHOULDER]- 40) #46
        self.set_angle(Motor.BR_ELBOW, self.pos_dict[Motor.BR_ELBOW]) #89
        #sleep(0.5)
        self.set_angle(Motor.BL_SHOULDER, self.pos_dict[Motor.BL_SHOULDER] + 40) #113
        self.set_angle(Motor.BL_ELBOW, self.pos_dict[Motor.BL_ELBOW]) #87
        sleep(1)
        for i in range(10):
            self.set_angle(Motor.FR_SHOULDER, self.pos_dict[Motor.FR_SHOULDER] - 40) #60 27 
            self.set_angle(Motor.FR_ELBOW, self.pos_dict[Motor.FR_ELBOW]) # 85 27
            self.set_angle(Motor.FR_HIP, self.pos_dict[Motor.FR_HIP])
            #sleep(0.5)
            self.set_angle(Motor.FL_SHOULDER, self.pos_dict[Motor.FL_SHOULDER] + 40) #117
            self.set_angle(Motor.FL_ELBOW, self.pos_dict[Motor.FL_ELBOW]) #67
            self.set_angle(Motor.FL_HIP, self.pos_dict[Motor.FL_HIP])
            sleep(1)
            # print("up")
            self.set_angle(Motor.FR_SHOULDER, self.pos_dict[Motor.FR_SHOULDER]) #60 27 
            self.set_angle(Motor.FR_ELBOW, self.pos_dict[Motor.FR_ELBOW]) # 85 27
            self.set_angle(Motor.FR_HIP, self.pos_dict[Motor.FR_HIP])
            #sleep(0.5)
            self.set_angle(Motor.FL_SHOULDER, self.pos_dict[Motor.FL_SHOULDER]) #117
            self.set_angle(Motor.FL_ELBOW, self.pos_dict[Motor.FL_ELBOW]) #67
            self.set_angle(Motor.FL_HIP, self.pos_dict[Motor.FL_HIP])
            sleep(1)
            
        self.calibrate()

    

    def steps(self, num, radiusX, radiusY, direction):
        self.calibrate()
        for i in range(num):
            if(direction == 0 or direction == 1): #forward or backward
                self.move(radiusX, radiusY, direction)
            elif(direction == 2 or direction == 3): #right or left
                self.move(0, radiusY, direction)

