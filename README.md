# The Follow-Me Fan


**Tian Zhang**

## Project Description

Fans are a common household appliance, and have not improved significantly in recent years. To add more novel function to the fan, we have developed the Follow-Me Fan. The Follow-Me Fan is a smart fan with the ability to follow the user to keep the air flow on them. The main objectives of the fan are to:
* make the fan point towards the user
* rotate in two direction
* control the speed of the fan to be proportional to the distance of the user from the fan
* have a manual mode setting in which the fan behaves like a regular fan


![Image of Smart Fan](http://i68.tinypic.com/1zmpelt.jpg)  ![Image of Fan_Base](http://i64.tinypic.com/11hqud5.jpg) 
![Image of Fan_Camaera](http://i65.tinypic.com/2ltqzdc.png) ![Image of Raspi](http://i63.tinypic.com/pydck.png)


### Technical Approach
The Follow-Me Fan is a smart fan with the ability to follow the user to keep airflow on the user. To accomplish this, there are three main objectives to accomplish. First, the fan must track the user’s angular position. we used a IR camera to detect the position of the human. Second, the fan must be able to move in response to the measurements taken by the camera. Instead of using a consumer-product fan now, we designed the whole fan by ourselves and we used two servo-motors to control the horizontal and vertical angular positions of the fan. Thirdly, the user’s distance from the fan must be measured. This will be accomplished using an ultrasonic sensor. Finally, we used a Raspberry PI to integrated with the camera and the motors.

### Code Description
I helped develop the algorithm in Python for this project. The follow diagram is the algorithm flow chart. The code is consisted by two main parts. The purpose of the first part is to determine the user position. The second part is for controling two motors towards to the user. 


![Image of flow_chart](http://i63.tinypic.com/nxtjyr.png)  


**Find Person Pseudocode**
1. Choose a cutoff temperature that is large percentage of the range from min to max. i.e. 0.95 x (max – min)
1. Based on cutoff temperature, create matrix of 1's and 0's where 1's represent pixels above the cutoff temperature, and 0's temperatures below the cutoff temperature
1. Search for rows and columns with the most contiguous 1's. This is done to find the top-left and bottom-left coordinates of an object
1. From the bottom-left corner, search to the right to find the bottom-right corner.
1. With Top-left and bottom-right corner coordinates, interpolate centre of person



**Motor Control Pseudocode**
1. Compare the previous user's position and current position
1. If they are the same, the motor stayed at the original angle. If they are different, gupdate the movement angle based on the user's position
1. transfer the angle into PWM pulse width to control the movement of motors
1. Meanwhie slow down the motor rotation speed in order to protect the whole fan


