#You can import any modules required here
import time
import RPi.GPIO as GPIO
import Adafruit_ADS1x15


#This is name of the module 
moduleName = "coffee"

#These are the words you must say for this module to be executed
commandWords = ["prepare","coffee"]

motor=11               # Servo motor pin 11
led_red=13               # LED pin 13
led_green=15               # LED pin 15
GPIO.setmode(GPIO.BOARD)   # connector pin numbering 

adc = Adafruit_ADS1x15.ADS1115()
GAIN = 1

#This is the main function which will be execute when the above command words are said
def execute(command):
    
    #read information from water level sensor
    #[0 to 4000-> empty] [over 10.000-> enough water]
    data = adc.read_adc(0, gain=GAIN)  # lectura data
    print(data)
    if data <10000:
        print("\n------------------Not enough water to make coffee-------------------\n")
        GPIO.setup(led_red,GPIO.OUT)
        #the red led is flashing 10 times
        t=10
        while t:
            GPIO.output(led_red,0) # on 
            time.sleep(0.5)
            GPIO.output(led_red,1) # off 
            time.sleep(1)      # seconds
            t-=1
    else:
        print("\n------------------Making coffee-------------------\n")
        GPIO.setup(led_green,GPIO.OUT)   
        GPIO.output(led_green,0) # turn on Green LED
        #turn on coffee machine
        # Set pin 11 as an output, and set servo1 as pin 11 as PWM
        #initially motor is set on 90 degrees(2->0 degrees, 7->90 degrees, 12->180 degrees etc.)
        GPIO.setup(motor,GPIO.OUT)
        servo1 = GPIO.PWM(motor,50) #  motor=11 is pin, 50 = 50Hz pulse
        servo1.start(0)
        #0 degrees
        servo1.ChangeDutyCycle(2)
        time.sleep(0.5)
        
        #wait until level of water decrease
        on=1;
        while(on):
            data = adc.read_adc(0, gain=GAIN)
            if data<6000:
                on=0
            time.sleep(0.5)
            
        #turn off the coffee machine    
        #back to 90 degrees
        servo1.ChangeDutyCycle(7)
        time.sleep(1)
        servo1.stop()
        
        GPIO.setup(led_green,GPIO.OUT)   
        GPIO.output(led_green,1) # turn off Green LED
        print("\n------------------Coffee ready-------------------\n")
     

