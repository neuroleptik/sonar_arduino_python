import serial
import time
from math import pi
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np
from drawnow import drawnow


"""
Original Author : Wojjy72
git : https://github.com/Wojjy72.

Rewritten by : Jean-Baptiste BRASSELET

Creates a 180 degree graph for a sonar
Recieves input through a com port, in b"nr_of_degrees(1-179) distance_to_object(0-160)\r\n" form,
and creates a semi-circular graph around (0,0), with a radius of 160cm. It then graphs the input on
said graph.
External libraries used:
pySerial, https://pythonhosted.org/pyserial/;
matplotlib, https://matplotlib.org/;
NumPy, http://www.numpy.org/;
drawnow, https://github.com/stsievert/python-drawnow.
"""

data = np.zeros((180, 2)) #create empty array for data
line = np.zeros((2, 2)) #create array for line

fig = plt.figure() #create plot

 #40cm circle
fourx = np.linspace(-40, 40, 25)
foury = np.sqrt(1600 - (fourx * fourx))

#80cm circle
eightx = np.linspace(-80, 80, 50)
eighty = np.sqrt(6400 - (eightx * eightx))

#120cm circle
twox = np.linspace(-120, 120, 75)
twoy = np.sqrt(14400 - (twox * twox))

#160cm circle
sixx = np.linspace(-160, 160, 100)
sixy = np.sqrt(25600 - (sixx * sixx))

def redraw():
    #redraw graph
    #resize & rename
    plt.axis((-160, 160, 0, 160))
    plt.axes().set_aspect('equal', 'datalim')
    plt.title('RADAR (cm)')

    #define lines every 40cm
    four = mlines.Line2D([],[],color='#006400', label='40')
    eight = mlines.Line2D([],[],color='#FF8C00', label='80')
    two = mlines.Line2D([],[],color='r', label='120')
    six = mlines.Line2D([],[],color='k', label='160')

    #draw all lines
    x = data[serial_line[0] - 1, 0]
    y = data[serial_line[0] - 1, 1]

    if x < 150 and y < 150:
    	liste_points_x.append(x)
    	liste_points_y.append(y)

    plt.plot(liste_points_x,liste_points_y,'s',marker='o', markersize=3, color="red")
    #plt.plot(data[:,0], data[:,1], color ='#fc0000')
    plt.plot(line[:,0], line[:,1], color ='#00FC00')
    plt.plot(fourx,foury, color='#006400')
    plt.plot(eightx,eighty, color='#FF8C00')
    plt.plot(twox,twoy, color='r')
    plt.plot(sixx,sixy, color='k')

    #draw legend
    plt.legend(handles=[four, eight, two, six])

time.sleep(1) #delay before starting main()


if __name__ == "__main__":

	print("debut")
	port = "COM5"
	liste_points_x = []
	liste_points_y = []
	ser = serial.Serial(port, baudrate = 9600, timeout = 1)
	if ser.isOpen():
		while True:
			serial_line = ser.readline()
			serial_line = serial_line.decode('UTF-8')
			serial_line = serial_line.replace("\r\n","")
			serial_line = serial_line.split() #array of words from string
			serial_line = list(map(int, serial_line)) #string array to int array
			if not len(serial_line) == 2: #if serial data is incorrect
				serial_line = [1, 0]
			data[serial_line[0] - 1, 0] = serial_line[1] * np.cos((pi * serial_line[0])/180) #get x co-ord within circle graph
			data[serial_line[0] - 1, 1] = serial_line[1] * np.sin((pi * serial_line[0])/180) #get y co-ord within circle graph
			line[0, 0] = 160 * np.cos((pi * serial_line[0])/180)#get x co-ord within circle graph
			line[0, 1] = 160 * np.sin((pi * serial_line[0])/180)#get y co-ord within circle graph
			drawnow(redraw) #refresh graph
			if serial_line[0] == 180 or serial_line[0] == 0 :
				liste_points_x = []
				liste_points_y = []
			time.sleep(0.0001)
		ser.close()