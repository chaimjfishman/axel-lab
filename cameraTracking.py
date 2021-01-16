# -*- coding: utf-8 -*-
"""
Created on Fri Aug 28 13:39:09 2015

@author: Jay Fishamn
"""

#import numpy as np

import cv2
#imports for camera and picture manipulations
from Tkinter import Frame, Tk, Button, W, Label, Entry, END, Text, WORD
#imports for GUI
import matplotlib.pyplot as plt
#imports for graph
import time

  
 
class buttons(Frame):
#This class inherets from the 'tkinter' class 'Frame'

    
    def __init__(self, master):
    #'master is the parent class
    
        Frame.__init__(self, master)
        #initializes the Tkinter Frame method
        self.grid()
        #puts the GUI on  the screen
        
        self.createTakePhotoButton()
        
        self.text = Text(self, width = 25, height = 1, wrap = WORD)
        #creates space to write text (time passed since program start).
        self.text.grid(row = 5, column = 0, sticky = W) 
        #puts it on grid
        self.text.insert(1.1, 'Time passed:')
        #inserts in row 1.column 1 text ('Time passed:')
        
    def createTakePhotoButton(self):
        """
        Creates button to take initial photo 
        """
        #Whenever this button is pressed the 'takePhoto'
        #..method is invoked
        self.take_button = Button(self, text = 'Take photo', 
                                    command = self.takePhoto)
        self.take_button.grid(row = 1, column = 0, sticky = W)
        #puts button on grid.
        
    def takePhoto(self):
        
        self.cam = cv2.VideoCapture(0)
        #initialze camera
        # 0 = webcam, 1 = USB camera
        
        
        ret, self.no_mouse = self.cam.read()
        #take photo without the mouse in the assay
  
        cv2.imshow('frame',self.no_mouse)
        time.sleep(1)
        cv2.destroyAllWindows()

        self.inputTime()
        #invoke the inputTime method from the app instance
        self.SubmitButton()
        #invoke the SubmitButton method from the app instance
            
        
    def inputTime(self):
        """
        Waits for the user to input how long program should run 
        """
        global entry
        
        self.entry = Label(self, text = 'Enter run time (seconds):')
        #creates a Label with text
        self.entry.grid(row = 1, column = 0 , sticky = W)
        #puts the label on the grid.
        #Specify which row, column, and side('W'est)
        #to put on GUI (optional).
        
        self.entry = Entry(self)
        #create space to enter doc name
        self.entry.grid(row = 2, column = 0 , sticky = W)
        #puts it on grid
        
    def SubmitButton(self):
        """
        Creates button to submit the time
        """
        #Whenever this button is pressed the 'createProgramButton'
        #..method is invoked
        self.submit_button = Button(self, text = 'submit time', 
                                    command = self.createProgramButton)
        self.submit_button.grid(row = 3, column = 0, sticky = W)
        #puts button on grid.
                
        
    def createProgramButton(self):
        """
        Creates button to start running the main program
        """
        #Whenever this button is pressed the 'programLoop'
        #..method is invoked
        self.program_button = Button(self, text = 'Start filming', 
                                    command = self.preProgramLoop)
        self.program_button.grid(row = 4, column = 0, sticky = W)
        #puts button on grid.
        
    def preProgramLoop(self):
        self.xValues = []
        self.yValues = []
        self.xCoord = []
        self.yCoord = []
        #create lists for the x and y positions of the mouse
        #Since will delete some to keep graph clear need another
        #list that will ahve all values
        
        self.program_start_time = time.time()
        self.program_run_time = int(self.entry.get())
        #gets the time the user entered in the GUI

        self.after_idle(self.programLoop)  
        #invokes the 'programLoop' method
        
    def programLoop(self):
        
        self.after_idle(self.writeTimeGUI)
                
        if time.time() - self.program_start_time < self.program_run_time:
        #If the time the program was set to run did not pass yet..
         
            ret, self.with_mouse = self.cam.read()
            #take photo
            
            self.after_idle(self.determineMousePosition)
            #invoke the determineMousePosition function
            
        else:
            self.cam.release()
            #closes camera
            cv2.destroyAllWindows()
            #closes windows`
    
            
     
    def determineMousePosition(self):
        """Determines the position of the mouse and draws a 
        red rectangle around it"""
        
        self.only_mouse = self.with_mouse - self.no_mouse
        #get a photo that only has the mouse in it by subtracting the
        #initial photo (without the mouse) from the photo with the mouse
        #So only the mouse is left
        
        #==============================================================================
        #     #Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
        #     element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
        #     only_mouse = cv2.erode(only_mouse,element, iterations=2)
        #     only_mouse = cv2.dilate(only_mouse,element,iterations=2)
        #     only_mouse = cv2.erode(only_mouse,element)
        #==============================================================================
        
        self.imageThreshold = cv2.inRange(self.only_mouse, cv2.cv.Scalar(3,3,125),\
        cv2.cv.Scalar(40,40,255),)
        #only colors that are in specific RGB range appear in white. All other
        #colors are black. (need to write B, G, R)
         
        contours, hierarchy = cv2.findContours(self.imageThreshold,\
        cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)         
        
        bestContour = None
        #Create variable to check if there're 
        #any objects in the specified color range
        maximumArea = 0
        #Create variable to find the largest object on the screen that's 
        
         
        for contour in contours:
        #for  all the countours.. 
        #(i.e. all objects that are in the color range given)
        
            currentArea = cv2.contourArea(contour)
            #determines the area of each object    
             
            if currentArea > maximumArea and 100 < currentArea < 13000: 
            #If  the object detected is bigger than any of the other objects
            #and its size is in the given range..
                bestContour = contour
                #set that object as the selected object
                maximumArea = currentArea
                #set maximumArea to that objects area.
        
        if bestContour is not None:
        #if there're any objects in the specified color range..
            x,y,w,h = cv2.boundingRect(bestContour)
            cv2.rectangle(self.with_mouse, (x,y),(x+w,y+h), (0,0,255), 3)
            #create red rectangle around selected object 
            
            xCenter = x+w/2
            yCenter = (y+h/2)*(-1)
            
            xCenter-=643
            yCenter+=360
            #makes the center of the picture as the (0,0) coordinate
            
            self.xValues.append(xCenter)
            self.yValues.append(yCenter)
            self.xCoord.append(xCenter)
            self.yCoord.append(yCenter)
            
            #Show the original camera feed with a bounding box overlayed 
            cv2.imshow('frame',self.with_mouse)
            
            if len(self.xValues) > 480:
            #if there are more than 480 elements in the lists..
            #(i.e. if take picture every 0.25 seconds[250 milliseconds]
            #there will be 480 pictures in 2 minutes)
                del self.xValues[0]
                del self.yValues[0]
                #del the first element of the lists.
                plt.clf()
                #clears all the points on the window so the 
                #previous points get deleted
                 
    
            self.after_idle(self.graph,self.xValues, self.yValues)
            #invokes the 'graph' function and gives the xValues, yValues
            #listd as the parameters. 
            
            
        else:
            
            cv2.imshow('frame',self.with_mouse)
            #Show the original camera feed
            self.after(250, self.programLoop)
            #after 250  milliseconds invoke the programLoop method
        
        
    def graph(self, x, y):
        """
        graphs the position of the mouse
    
        """
        plt.plot(x, y, 'r-')
        #plot red dot
        plt.plot(x, y, 'bo')
        #plot blue line connecting the dots
        plt.show()
        #shows the points on the graph
        self.after(250, self.programLoop)
        #after 250  milliseconds invoke the programLoop method
        
    def writeTimeGUI(self):
        """writes the time passed since program start on GUI
        """
        time_now = time.time()
        time_passed = str((time_now - self.program_start_time)/60)
        #determines the time passed since start by
        #..subtracting the time the program started 
        #..from the current time.
        #Divide by 60 to convert to minutes
        
        if time.time() - self.program_start_time > self.program_run_time:
            time_passed = 'Program finished'
        
        self.text.delete(1.0, END)
        #deletes what was previously written
        #starting from row 1.column 0 until END  
        self.text.insert(1.1, time_passed)
        #inserts the text recieved as the parameter
        #in position row 1.column 

        
def main():
    """creates and sets the window for the GUI."""
      
    
    root = Tk()
    #create a window for the GUI
    root.title ('Title goes here...')
    #sets window's title.
    root.geometry('200x200+0+0')
    #set window's dimensions("WidthxHeight")
    #..and x y cooridantes
    app = buttons(root)
    #create object of 'program' class
    root.mainloop()
    #start event loop that constantly checks if
    #..any of the GUI buttons are pressed.
        

main()
#call the 'main' function to start entire program.


#==============================================================================
#==============================================================================
#==============================================================================





"""upload image"""


#==============================================================================
# no_mouse = cv2.imread('ne.jpg')
# with_mouse = cv2.imread('middle.jpg')
# only_mouse = with_mouse - no_mouse
# only_mouse2 =  no_mouse - with_mouse
# 
# imageThreshold = cv2.inRange(only_mouse, cv2.cv.Scalar(15,15,15), cv2.cv.Scalar(130,130,130),)
# imageThreshold2 = cv2.inRange(only_mouse2, cv2.cv.Scalar(70,70,70), cv2.cv.Scalar(120,120,210),)
# #only colors that are in specific RGB range appear in white. All other
# #colors are black. (need to write B, G, R)
# cv2.imshow('imageThreshold', imageThreshold)
# 
# #cv2.imshow('mouse', imageThreshold)
# cv2.imshow('mouse2', only_mouse)
# 
# 
# #Get rid of background noise using erosion and fill in the holes using dilation and erode the final image on last time
# element = cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
# only_mouse = cv2.erode(only_mouse,element, iterations=2)
# only_mouse = cv2.dilate(only_mouse,element,iterations=2)
# only_mouse = cv2.erode(only_mouse,element)
# 
# cv2.imshow('mouse5', only_mouse)
# 
# imageThreshold = cv2.inRange(only_mouse, cv2.cv.Scalar(15,15,15), cv2.cv.Scalar(130,130,130),)
# cv2.imshow('imageThreshold2', imageThreshold)
# 
#  
# contours, hierarchy = cv2.findContours(imageThreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#  
# 
# bestContour = None
# #Create variable to check if there're 
# #any objects in the specified color range
# maximumArea = 0
# #Create variable to find the largest object on the screen that's 
# 
#  
# for contour in contours:
# #for  all the countours..
# 
# 
#     currentArea = cv2.contourArea(contour)
#     #determines the area of each contour    
#      
#     if currentArea > maximumArea and 100 < currentArea < 13000:
#         print 'size:', int(currentArea)         
#         bestContour = contour
#         maximumArea = currentArea
#         #set maximumArea to that objects area.
# 
# if bestContour is not None:
# #if there're any objects in the specified color range..
#     x,y,w,h = cv2.boundingRect(bestContour)
#     cv2.rectangle(with_mouse, (x,y),(x+w,y+h), (0,0,255), 3)
#     #create red rectangle around object 
#     
#     print x,',', y
# 
#     
# #Show the original camera feed with a bounding box overlayed 
# cv2.imshow('frame',with_mouse)
#     
# while True:    
#     esc = cv2.waitKey(10)
#     if esc == 27:
#         #if 'esc' key is pressed close window
#         #('esc' button id #27 on the keyboard)
#     
#         cv2.destroyAllWindows()
#         break
#==============================================================================
