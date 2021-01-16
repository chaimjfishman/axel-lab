# -*- coding: utf-8 -*-
"""
Created on Wed Aug 19 10:00:09 2015

@author: Jay Fishman
"""

#Phidget specific imports 
from Phidgets.Devices.InterfaceKit import InterfaceKit
from Phidgets.PhidgetException import PhidgetException
#Imports for GUI.
from Tkinter import Frame, Tk, Button, Checkbutton, IntVar
from Tkinter import Text, WORD, END, W, Label, Entry
#Imports for graph.
import matplotlib.pyplot as plt
import numpy as np

import threading
import time
import sys

"""
outputs:
1-IR beam
2-odor
3-odor
4-water
6-laser


analogs/sensors:
1-IR beam
2- touch sensor

"""


#==========================================================================

class program(Frame):
#This class inherets from the 'tkinter' class 'Frame'

    
    def __init__(self, master):
        #'master is the parent class

        Frame.__init__(self, master)
        #initializes the Tkinter Frame method
        self.grid()
        #puts the GUI on  the screen
        
        
        self.myObject = InterfaceKit()
        #create an object/instance of the Phidgets class 'InterfaceKit'
        self.myObject.openPhidget()
        #open the phidget device.
        try:
            #check if the device is attached.
            self.myObject.waitForAttach(100)
        except PhidgetException:
            print"\nDEVICE NOT CONNECTED.\n"
            self.myObject.closePhidget()
            #close Phidget device
            sys.exit()
            #end program
        
        self.myObject.setOutputState(1, True)
        #set output state of beam to True
        #so light is constanly emitted.
        self.myObject.setOutputState(4, False)
        #set the output state to false so no signal is sent
        #and the mouse doesn't recieve water.

        self.program_run_time = 3600
        #set how many "seconds" the program should run
        
        self.inputFileName() 
        #invokes the 'inputFileName' method
        self.SubmitButton() 
        #invokes the 'SubmitButton' method
        
#-------------------------------------------------------------        
        
    def inputFileName(self):
        """
        Waits for the user to input a file name
        """
        self.entry = Label(self, text = 'Enter doc name:')
        #creates a Label with text
        self.entry.grid(row = 1, column = 0 , sticky = W)
        #puts the label on the grid.
        #Specify which row, column, and side('W'est)
        #to put on GUI (optional).
        
        self.document = Entry(self)
        #create space to enter doc name
        self.document.grid(row = 2, column = 0 , sticky = W)
        #puts it on grid
        
    def SubmitButton(self):
        """
        Creates button to submit the doc name
        """
        #Whenever this button is pressed the 'second__init__'
        #..method is invoked
        self.submit_button = Button(self, text = 'submit doc', 
                                    command = self.second__init__)
        self.submit_button.grid(row = 3, column = 0, sticky = W)
        #puts button on grid.
        
#---------------------------------------------------------------------            
        
    def second__init__(self):
        """
        Finishes initializing the program.
        """        
        self.file_name = str(self.document.get()) + '.xls'
        #sets the file name to what user entered in the GUI
               
        self.createStartButton()
        #invokes the 'createStartButton' method
        self.createGiveWaterButton()
        #invokes the 'createGiveWaterButton' method
        self.createCloseButton()
        #invokes the 'createCloseButton' method  
        self.createGiveOdorCheckbutton()
        #invokes the 'createGiveOdorCheckbutton' method 
        


        self.text = Text(self, width = 25, height = 1, wrap = WORD)
        #creates space to write text (time passed since program start).
        self.text.grid() 
        #puts it on grid
        self.text.insert(1.1, 'Time passed:')
        #inserts in row 1.column 1 text ('Time passed:')
        
        
        
        plt.title('Graph')
        #set name for the graphing window
        plt.xlabel('Time after program start (minutes)')
        #set name for the x-axis
        plt.ylabel('Number of times water valve opened')
        #set name for the y-axis
#----------------------------------------------------------------  
        
    def createGiveOdorCheckbutton(self):
        """creates a checkbutton that does NOT give odor
        to the mouse when checked"""
        #Whenever this button is checked the 'giveOdor'
        #..method is invoked
        self.var = IntVar()
        
        self.laserButton = Checkbutton(self, text = 'NO laser',
                                      variable = self.var)
        self.laserButton.grid(sticky = W)
        #makes the button appear on the grid.
        
#-----------------------------------------------------------------------        
        
    def createGiveWaterButton(self):
        """creates a button that gives water
        to the mouse whenever pressed"""
        #Whenever this button is pressed the 'giveWater'
        #..method is invoked
        self.WaterButton = Button(self, text = 'Give water',
                                  command = self.giveWater)
        self.WaterButton.grid(sticky = W)
        #makes the button appear on the grid.
        
        
    def giveWater(self):
        """gives water to the mouse for 50 miliiseconds."""
        #Every time setOutputState(n, True) it
        #..sends a signal allowing the mouse to 
        #.. get water until it's set to False
        self.myObject.setOutputState(4, True)
        print('\'GiveWater\' button pressed.')
        time.sleep(.05)
        #progrsm stops for 50 milliseconds.
        self.myObject.setOutputState(4, False)
#----------------------------------------------------------------------

    def checkIRbeam(self):
        """
        Constantly checks if the IR beam is broken and writes in a
         list all the times the IR beam was broken and unbroken
        """        
        self.IRbroken = []
        #create list to hold times beam was broken and unbroken

        while time.time() - self.program_start_time < self.program_run_time:
            #while the time the program was set to run has not yet passed...
        
            if self.myObject.getSensorValue(1) < 60:
            #If the IR beam < 60 (i.e. it's broken)..
                
                time_now = time.time()
                time_touched = time_now - self.program_start_time
                #determines the time beam was broken
                self.IRbroken.append('\t%s\t' % str(time_touched/60))
                #writes the time in the list.
                
                #'\t' (TAB) before and after makes the differnt
                #kinds of values (time the touch sensor was touched, beam-
                #broken, and unbroken) be in different coulmns when it's
                #written in the excel file at the end of the program.
                
                while self.myObject.getSensorValue(1) < 60:
                    continue
                #program is in a loop until the sensor is not anymore
                #broken.
                    
                time_now = time.time()
                time_touched = time_now - self.program_start_time
                #determines the time beam was unbroken
                self.IRbroken.append('%s \n' % str(time_touched/60))
                #writes the time in the list. 
                #'\n' makes a new row in the excel file afterwards


            else:
            #if the IR beam is not broken..
                continue 
                #start loop again
            
    def createStartButton(self):
        """creates a button to start the program"""
        #Whenever this button is pressed the 'preProgramLoop'
        #..method is invoked.
        self.startButton = Button(self, text = 'Run program',
                             command = self.preProgramLoop)
        self.startButton.grid(sticky = W)
        #makes the button appear on the grid.
        
        
    def preProgramLoop(self):
        """creates variables and lists needed in the program loop"""
        self.waterList = []
        #create a list to store the times when the..
        #..water valve was opened.

#----------------------------------------------------
        

        
        self.num_times_touched = 0
        #create a variable to keep track of how many 
        #..times the water valve was opened.
        self.x = []
        self.y = []
        #creates lists to store the x and y values for the graph.  
        
        
        self.program_start_time = time.time()
        #sets the time the program started.


        IRbeamThread = threading.Thread(target = self.checkIRbeam)
        #create a second thread in the program to run the 'checkIRbeam'
        #method and constantly check if the IR beam is broken. 
        IRbeamThread.start()
        #start running the thread.
                
                
        self.after_idle(self.programLoop)      
        #invokes the 'programLoop' method.
        #(Because 'programLoop' only has the paramter 'self'
        #no arguments are given. Othrewise need to write 
        #self.after_idle(self.programLoop, args))
        
    def programLoop(self):
        """Main program loop."""
        self.myObject.setOutputState(5, False)
        #set the output state to False so laser doesn't shine
        self.myObject.setOutputState(4, False)
        #set the output state to False so no water is given
          
        if time.time() - self.program_start_time < self.program_run_time:
        #If time the program was set to run has not yet passed...
        
            if self.myObject.getSensorValue(1) < 60:
            #If the IR beam < 60 (i.e. it's broken. 
            #..Indicates that the mouse is there)..
        
                if self.var.get() != 1:
                #if the 'NO laser' button is NOT equal to 1
                #(i.e. it's NOT checked)..
                    self.next = 'water'
                    #Set next equal to 'water' so after the loop in the 
                    #'shineLaser' method is finished the program knows to invoke 
                    #the 'waterLoop' next.
                    self.loop_start_time = time.time()
                    #Determines at what time the loop started
                    self.after_idle(self.shineLaser, 1)
                    #invokes the 'shineaLaser' method and gives '1' as the parameter
                    #in order to run the loop for 1 second.
                    
                else:
                #If the 'No laser' button is checked.
                    self.after(1000, self.waterLoop)
                    #waits 1000 milliseconds (1 second) and then
                    #.. invokes the 'waterLoop' method.
                    
            else:
            #If the beam was not broken
                
                time_now = time.time()
                self.time_touched = time_now - self.program_start_time
                #determines the time the sensor was touched by
                #..subtracting the time the program started 
                #..from the current time.
                self.after_idle(self.writeTimeGUI, self.time_touched/60)
                        
                self.after_idle(self.programLoop) 
                #The 'programLoop' method is invoked again right
                #away to check again if the sensor was touched.

                                
        else:
        #If time the program was set to run has already passed...
            self.after_idle(self.writeTimeGUI, 'time\'s up' )
            print'program run time has already passed.\n\
            press \'close program\' button if finished.'
            
     
        
    def waterLoop(self):
        if self.myObject.getSensorValue(2) > 900:                               
        #If the touch-sensor value > 900 (i.e. it's touched)...
        
            self.myObject.setOutputState(4, True)
            #..the output sends a signal allowing the 
            #..mouse to drink.
            
            time_now = time.time()
            self.time_touched = time_now - self.program_start_time
            #determines the time the sensor was touched by
            #..subtracting the time the program started 
            #..from the current time.
            self.waterList.append(str(self.time_touched/60))
            #appends (adds) that time to the waterList.
        
            self.after_idle(self.writeTimeGUI, self.time_touched/60)
            #invokes the 'writeTimeGUI' method and gives the current
            #time in minutes(/60) since program start as the parameter.
                        
            self.num_times_touched += 1
            #increase the times the sensor was touched by one.          

            self.x.append(self.time_touched/60)
            self.y.append(self.num_times_touched)  
            #Adds the current time the sensor was touched and the
            #..number of the times the sensor has already been
            #..touched as the x and y coordinates, respectivly, to
            #..the x and y lists.
            #(time_touched is divided by 60 so the graph intervals
            #are in minutes instead of seconds.)
            self.after_idle(self.graphData,
                            self.x, self.y)
            #Invokes the 'graphData' method  and gives updated
            #..x and y lists as the arguments for the graph.
                            
        else:
            self.after_idle(self.programLoop)
            #If the sensor was not touched, the 'programLoop'
            #.. method is invoked again right away to check again
            #..if the sensor was touched.
#------------------------------------------------------------------

    
    
    def graphData(self, xValues, yValues):
        """Graphs the number of times the sensor was touched with 
        respect to time passed since the program started."""
        self.xValues = xValues 
        self.yValues = yValues
        
        plt.plot(xValues, yValues, 'ro')
        #graphs the x and y values with red dots.
        plt.show()
        #shows the graph on the window.
        
        time.sleep(.05)
        self.myObject.setOutputState(4, False)
        #give water for .05 seconds (50 milliseconds).
            
        if self.var.get() != 1:
        #if the 'NO laser' button is NOT equal to 1
        #(i.e. it's NOT checked)..
            self.next = 'program'
            #Set next equal to 'program' so after the loop in the 
            #'shineLaser' method is finished the program knows to invoke 
            #the 'programLoop' next.
            self.loop_start_time = time.time()
            #Determines at what time the loop started
            self.after_idle(self.shineLaser, 2)
            #invokes the 'shineaLaser' method and gives '2' as the parameter
            #in order to run the loop for 2 seconds  
            
        else:
        #If the 'No laser' button is checked. 
            self.after(2000, self.programLoop)
            #wait 2000 milliseconds (2 seconds) and then goes back  
            #to the 'programLoop'.
            
#-------------------------------------------------------------------------  
                    
                    
    def shineLaser(self, duration):
        """Makes the laser blink for 50 milliseconds every 50 milliseconds
        while the IR beam is broken.
        """
        self.duration = duration    
        
        while time.time() - self.loop_start_time < self.duration:
        #while the time the loop was set to run has not yet passed...
            
            if self.myObject.getSensorValue(1) < 60:
                #If the IR beam < 60 (i.e. it's broken)..
                    
                while self.myObject.getSensorValue(1) < 60:
                    #program is in a loop until the sensor is not anymore
                    #broken.
                    if time.time() - self.loop_start_time < self.duration:
                    #If the time the program was set to run has not yet passed...
    
                        self.myObject.setOutputState(6, True)
                        #turn on the laser
                        time.sleep(.05)
                        #wait .05 seconds (50 milliseconds)
                        self.myObject.setOutputState(6, False)
                        #turn laser off
                        time.sleep(.05)
                        #wait .05 seconds (50 milliseconds)
                        
                    else:
                    #if loop run time passed.. 
                        break
                        #break out of the loop
    
            else:
                #if the IR beam is not broken..
                    continue 
                    #start loop again
                    
        if self.next == 'water':          
            self.after_idle(self.waterLoop)
        elif self.next == 'program':
            self.after_idle(self.programLoop)
        #Depending on what 'next' is equal to (which part of the program
        #the program is at) a different method is invoked.
                
                
                
#-----------------------------------------------------------------                
                
                

    def writeTimeGUI(self, text):
        """writes the time passed since program start on GUI
        """
        self.text.delete(1.0, END)
        #deletes what was previously written
        #starting from row 1.column 0 until END  
        self.text.insert(1.1, text)
        #inserts the text recieved as the parameter
        #in position row 1.column 1
                                    
#--------------------------------------------------------                                    
                                    
    def createCloseButton(self):
        """creates a button to close the program files and devices."""
        #Whenever this button is pressed the 'closeProgram'
        #..method is invoked.
        self.closeButton = Button(self, text = 'close program',
                             command = self.closeProgram)
        self.closeButton.grid(sticky = W)
        #makes the button appear on the grid.
                                
        
    def closeProgram(self):
        """closes the program files and devices."""
        self.myObject.setOutputState(6, False)
        #set the output state to False so laser doesn't shine
        self.myObject.setOutputState(4, False)
        #set the output state to False so no water is given
        
        self.after_idle(self.writeDataExternalFile)
        #invokes the 'writeDataExternalFile' method.
              
        self.myObject.closePhidget()
        #close Phidget device.
        print("\nPhidget device closed.")
 
#------------------------------------------------------------------
       
    def writeDataExternalFile(self):
        """
        Writes times the water valve opened, IR beam was broken
        and unbroken in an external file
        """
        
        """To be able to put the times the water valve was opened 
        and the times the IR beam was un/broken in the same file
        with the times the water valve opened in the first column
        and the times the beam was un/broken in 2nd & 3rd columns,
        need to insert the times the water valve opened in every third 
        position in the 'IRbroken' list.
        """        
        
        if len(self.waterList) > len(self.IRbroken)/2:
        #Determines if the 'waterList' has more items than 'IRbroken' list 
        #divided by 2.(i.e if mouse recieved water more times than the IR beam 
        #was broken)
        #If it does, will need another loop to insert '\n' after every item
        #after the IRbroken list is finished cuz need to put every time the 
        #mouse recieved water in a different row in file.
        
            another_loop = 'yes'
            length = int(len(self.IRbroken) + len(self.IRbroken)/2)
            #Determines length of IRbroken list plus half its size. 
            difference = len(self.waterList) - len(self.IRbroken)/2
            #Determines how many more times the mouse recieved water 
            #than broken the IR beam. 
        else:
        #If the IRbroken list is bigger than waterList
            another_loop = 'no'
            
        """If the mouse recieved water the same amount of times the IR
        beam was broken, the IRbroken list will increase by half its size 
        cuz add an item from 'waterList' in every third position.
        
        If waterList is greater than original IRbroken list (i.e. the mouse
        recieved water more times than the IR was broken)
        will need to insert '\n' (to print everytime the mouse recieved water
        in a seperate rowin the file) starting from the last item of the 
        original IRbroken list until the last item of the final IRbroken
        list. That's why need 'length' and 'difference' variables.
        """
      
            
        for times in range(len(self.waterList)):
        #For every item in the 'waterList' 
        #(contains the times water valve opened)
            self.IRbroken.insert(times*3, self.waterList[times])
            #Insert, in every third position in the
            #IRbroken list, the current item from waterList. 
            
        if another_loop == 'yes':
            
            print 'another loop'
            
            
        #If waterList is bigger than IRbroken
            for item in range(length + 1, length + difference*2, 2):
            #Starting from the last item from original IRbroken list
            #until the end of the current IRbroken list*, for every 
            #other position..
                self.IRbroken.insert(item, '\t0\t0\n')
                #..insert zeros
                
        """ * Write "difference '*2' " cuz since add item in every 
        other position, "difference" (the number of items in IRbroken
        from the last item of original IRbroken list until the last 
        item of the final IRbroken list.) will double.
        """
                        
        self.IRbroken.append('%s \t\t' % str(self.num_times_touched))
        #Add the total num of times mouse got water as last row in file.
        #(write '\t\t' to make all columns have same number of rows so
        #there's no error when analyzing the file.)
                   
        self.time_file = open(self.file_name, 'w')
        #create and open a file (name user gave at program start)  
        #to write times the water valve opened, IR beam was broken
        # and unbroken.
        #'w' opens it in 'w'riting mode
        self.time_file.writelines(self.IRbroken)
        #write all the items (stings) from current 'IRbroken' list.
        self.time_file.close()
        #close the external file.


#===========================================================================


def main():
    """creates and sets the window for the GUI."""
    root = Tk()
    #create a window for the GUI
    root.title ('Laser Program GUI')
    #sets window's title.
    root.geometry('200x200+0+0')
    #set window's dimensions("WidthxHeight")
    #..and x y cooridantes
    app = program(root)
    #create object of 'program' class
    root.mainloop()
    #start event loop that constantly checks if
    #..any of the GUI buttons are pressed.

main()
#call the 'main' function to start entire program.
