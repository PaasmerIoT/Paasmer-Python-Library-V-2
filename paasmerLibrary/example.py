from Paasmer import *
import time

#Callback functions for subscribed feeds
def feed1_CB(name):
	print("This is in feed4")
	print(name)
	if name == 1 :
                test.Xbee_write(8,"on") #controlling via Zigbee 

        elif name == 0 :
                test.Xbee_write(8,"off")

def feed2_CB(name):
	print("This is in feed7")
	print(name)
def feed3_CB(name):
	print("it is feed33")
	print(name)

###connecting to the Paasmer Edge docker device
test = Paasmer()
test.host = "192.168.100.144"   #IP address of the Paasmer Edge docker device.
test.connect()

###installing Wifi Protocol support
test.InstallWiFi()

###installing BLE protocol support
test.InstallBLE()

###connect to zigbee with serial port
test.Xbee_connect("/dev/ttyUSB0") # Enter the Port to which the Co-ordinartor zigbee is connected to the device (eg - /dev/ttyUSB0)

#subscribing to the feeds with callback functions
test.subscribe("Act1",feed1_CB)
test.subscribe("Act2",feed2_CB)
test.subscribe("Act3",feed3_CB)

#loop start
test.loop_start()

#configuring the ML with model name, which already created in paasmer cloud platform
test.ML_config(feedName = "mlfeed",modelName = "Demo2")

while True:
	#publishing the feed details to Paasmer Edge docker device
	'''
	you can use the following analytics
	1.filter
	2.aggregate
	3.feedMonitoring
	4.average
	for filter, provide the analytics condition like "function(x) x < 5.0"
	for aggrgate, provide the number of values you want to do aggregate
	for average, provide the number of values you want to do average

	you can control following devices for wifi and BLE protocol support with autodiscover functionality.

	With WiFi
	1.Philips Hue
	2.Belkin
	
	with BLE
	1.magicblue bulbs
	'''

	#Discovering WiFi
	test.DiscoverWifi()

	#Discovering BLE
        test.DiscoverBlue()	


	#publishing the feed details with filter analytics 
	test.publish("feed5",feedValue = 2,analytics = "filter",analyticsCondition="function(x) x > 3.0")
	time.sleep(2)
	
	#publishing the feed details without any analytics 
	test.publish("feed6",feedValue = 70)
	time.sleep(2)
	
	#publishing the feed details with aggregate analytics
	test.publish("feed1",feedValue = 10,analytics = "aggregate",analyticsCondition = "3")
	time.sleep(2)
	
	#publishing the feed details with feedMonitoring
	test.publish("feed3",feedValue = 10,analytics = "feedMonitoring")
	time.sleep(2)
	
	#publishing the feed details with average analytics
        test.publish("feed2",feedValue = 350,analytics = "average",analyticsCondition = "12")
        time.sleep(2)
	
	#predicting the ml output by giving input
	test.ML_predict(feedName = "mlfeed",modelName = "Demo2",data = {"eng":29,"lang":27,"maths":15,"sci":25,"soc":31})
	time.sleep(2)

	#Reading a value from xbee and publishing
	data = test.Xbee_read(5) #Reading via Zigbee 
	test.publish("feed7",feedValue = data)
