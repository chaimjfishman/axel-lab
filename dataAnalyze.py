# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:23:06 2015

@author: Jay Fishman
"""

from Tkinter import Frame, Tk, Button, W, Label, Entry
#imports for GUI
import matplotlib.pyplot as plt
#imports for graph
import numpy as np
#imports for calculations

class program(Frame):
#This class inherets from the 'tkinter' class 'Frame'

    
    def __init__(self, master):
        #'master is the parent class
    
        Frame.__init__(self, master)
        #initializes the Tkinter Frame method
        self.grid()
        #puts the GUI on  the screen
        
        
        self.whichFileAnalyze()
        #invokes the 'whichFileAnalyze' method
        self.createSubmitButton()
        #invokes the 'createSubmitButton' method
                
                
                
    def whichFileAnalyze(self):
        """
        Waits for the user to input a file name
        """
        self.entry = Label(self, text = 'enter doc name:')
        #creates a Label with text
        self.entry.grid(row = 1, column = 0 , columnspan = 2, sticky = W)
        #puts the label on the grid.
        #Specify which row, column, and side('W'est)
        #to put on GUI (optional).
        
        self.document = Entry(self)
        #create space to enter doc name
        self.document.grid(row = 2, column = 0 , sticky = W)
        #puts it on grid
        
    def createSubmitButton(self):
        """
        Creates button to submit the doc name
        """
        #Whenever this button is pressed the 'second__init__'
        #..method is invoked
        self.submit_button = Button(self, text = 'submit doc', 
                                    command = self.second__init__)
        self.submit_button.grid(row = 3, column = 0, sticky = W)
        #puts button on grid.
        
    def second__init__(self):
        """
        Finishes initializing the program.
        """        
        
        self.data = np.genfromtxt(str(self.document.get()), delimiter = '\t') 
        #Generates data from text file. 
        #'delimiter' = thing  that divides different data
        
        self.length = len(self.data[:,])
        #how many rows there are in file
        self.num_of_times_got_water = int(self.data[self.length -1: self.length][:,0])
        #num_of_times_got_water = last row in column 0 
        
        self.got_water = self.data[0:self.num_of_times_got_water][:,0]
        #Creates an array of column 0 starting from row 0 for 
        #all rows that are numbers (not 'NAN')in column 0 
        self.got_water.tolist()
        #converts the got_water array to a list to be able to find
        #total amount of times recieved water each minute later easier
        
    
        self.brokenIRtotal()
        #invokes the 'brokenIRtotal' method
        self.dataLabel()
        #invokes the 'dataLabel' method
        self.createGraphOriginalButton()
        #invokes the 'createGraphOriginalButton' method
        self.createGraphSecondButton()
        #invokes the 'createGraphSecondButton' method
        self.createClearGraphsButton()
        #invokes the 'createClearGraphsButton' method
        
        
    def brokenIRtotal(self):
        """
        Determines the total amount of time the mouse spent near the
        water/odor.
        """
        self.total_time_broken =0
        #create variable to hold the total time.
        for row in range(len(self.data[:,]) -1): 
        #For every row in the file (except last ['-1']cuz that only
        #has the total amount of times mouse recieved water)
            self.total_time_broken += self.data[row:row+1][:,2:3]\
            - self.data[row:row+1][:,1:2]
            #..adds the difference of column # 2 minus column # 1
            #(The time the beam was unbroken minus the time it was broken)
            #REMEMBER: Columns and rows start from 0
            
    #'\' allows to make a new line but the program still reads it as one
            
        
    def dataLabel(self):
        """Prints the total time IR beam was broken and mouse recieved water
        on the GUI.
        """
        
        myText = 'Total time IR beam broken:%s\n\
        Amount times mouse recieved water: %s' % (str(self.total_time_broken),\
        str(self.num_of_times_got_water))
        
        data_label = Label(self, text = myText)
        #creates a label to print 'myText' on the GUI
        data_label.grid(row = 4, column = 0, columnspan = 2, sticky = W)
        #puts the label on the grid.
        
                
        
    def createGraphOriginalButton(self):
        """creates a button that graphs the original graph"""
        #Whenever this button is pressed the 'graphOriginal'
        #..method is invoked
        self.GraphButton = Button(self, text = 'Graph Original',
                                  command = self.graphOriginal)
        self.GraphButton.grid(row = 6, column = 0, sticky = W)
        #makes the button appear on the grid.

        
    def graphOriginal(self):
        """regraphs the graph from program"""
        yValues =[]
        #creates a list/array for the y-valus of the graph
        for i in range(self.num_of_times_got_water):
        #every number between 0 and the number of times mouse recieved water 
            yValues.append(i)
            #..add to the list. 
            
        plt.plot(self.got_water, yValues, 'ro')
        #Create graph of red dots ('ro') using the 'got_water' array from
        #the 'second__init__' method as the x-values.  
        plt.show()
        #shows the graph on the window.
        
        
    def createGraphSecondButton(self):
        """creates a button that graphs the number of times
        the mouse recieved water each minute the program ran
        """
        #Whenever this button is pressed the 'graphSecond'
        #..method is invoked
        self.secondButton = Button(self, text = 'Graph Second',
                                  command = self.graphSecond)
        self.secondButton.grid(row = 7, column = 0, sticky = W)
        #makes the button appear on the grid.
        
        
    def graphSecond(self):
        """Graphs""" 
        x_values = []
        y_values = []
        #creates a list/array for the x and y-valus of the graph
        
        
        """ For each two consecutive integrs between 0 and 60 the program
        goes through each item in the 'got_water' list to check if it's
        between those two cosecutive integers. Like this know how many times 
        the mouse recieved water each minute of the program.
        """
        for number in range(60):
            times_in_min = sum(number<items<=number+1 for items in self.got_water)
            #times_in_min = the sum of the number of items that are between
            #the 2 consecutive integers in 'got_water' list.
            y_values.append(times_in_min)
            #append the number of times the mouse recieved water for that minute.
            x_values.append(number)
            #append every number between 0 and 60 to the x_values list
                
        plt.plot(x_values, y_values, 'bo')
        #graphs the x and y values with blue dots.
        plt.show()
        #shows the graph on the window.
        
        
    def createClearGraphsButton(self):
        """create a buuton to clear all of the graphs on the window.
        """
        #Whenever this button is pressed the 'clearGraphs'
        #..method is invoked
        self.clear_button = Button(self, text = 'Clear graphs', 
                                    command = self.clearGraphs)
        self.clear_button.grid(row = 8, column = 0, sticky = W)
        #puts the button on the grid
        
        
    def clearGraphs(self):
        plt.clf()
        #clears all the graphs on the window.

        

        




def main():
    """creates and sets the window for the GUI."""
    root = Tk()
    #create a window for the GUI
    root.title ('Title goes here...')
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





#==============================================================================
# data[0:4]
# #data from row 0(inclusive) to row 4(exclusive)
# 
# #   rows coulmns
# data[:,]  [:,0]
# #all rows only from column 0
# 
# data[:,]  [:,1:5]
# #all rows from columns 1,2,3,4 (5 not inclusive)

# want row 24 column 
# myData = data[23:24][:,1 ]
# print myData
#==============================================================================