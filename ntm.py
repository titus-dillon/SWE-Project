#####################################################################################################
# 	CSE 4214, Intro to Software Engineering, Fall 2016
# 	Lab Section 2, Group 3, Next Top Model
#
#####################################################################################################
# 	Contributors:
# 			Alex Palacio, Christopher Cole, Jia Zhao,
# 			Nathan Frank, Reid Montague, Titus Dillon
#
#####################################################################################################
#  TODO:
#       0.  Fix MalletCaller.py to process mallet correctly... (my bad)
#               - It processes mallet to completion but for some reason disregards the # of topics
#       1.  Display models
#               - Figure out how to send radio button states as arguments to modeler
#               - Send radio button states, # of topics and type of model to modeler?
#               - Figure out how to display the model in the GUI
#                   -- A new image widget?
#       2.  Testing on Windows / Linux
#               - Everything works on Linux up to displaying the models but that has not been implemented yet.
#       3.  Non-Functional Requirements
#               - Clean up code, unify formatting across all modules
#               - GUI changes to make it more intuitive, simplified?
#               - Add some kind of progress bar or loading spinner when other modules are processing
#                   -- There are notifications when the processes are done but not during processing
#                   -- It would just be "nicer" as a user to tell that stuff is happening in the program
#               - Any reason for us to have a menu bar?  How would it be used?  How would it make user's lives easier?
#               - Security issues:
#                   -- [None, at the moment]
#               - Performance Testing:
#                   -- Performance while idle
#                   -- Performance while processing
#                   -- Performance while the final model is displayed
#
#####################################################################################################
#  Program info:
# 	- This is the GUI that the user will interface with and drive the program.
#
#####################################################################################################
# !/usr/bin/python

from subprocess import call
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import os


# from VisualModeler import *
import VisualModeler
import TopicStocker
import FileFilter
import MalletCaller
import ExcelParser


class Form(QWidget):

    def __init__(self, parent=None):
        super(Form, self).__init__(parent)

        # setGeometry(self, ax, ay, aw, ah) -> x, y, width, height
        x = 500
        y = 200
        self.setGeometry(x, y, x, y)

        # Create layout boxes (makes things line up nicely)
        vertBox = QVBoxLayout()
        hInputBox = QHBoxLayout()
        hNumTopicBox = QHBoxLayout()
        hMalletBox = QHBoxLayout()
        hRadioBox = QHBoxLayout()


        # Create input file label, text line, search button and the parser button
        inputLabel = QLabel('Input Excel File Location:')
        self.inputLine = QLineEdit('/Path/To/Input/File')
        self.inputLine.setReadOnly(True)
        self.inputLine.setToolTip('This is the path to the input file Mallet should process.')
        self.inputSearch = QPushButton("...")
        self.inputSearch.setToolTip('Find the file Mallet should process.')
        self.inputSearch.clicked.connect(self.fileSearch)

        # Add the first set of widgets to the window (input file stuff)
        vertBox.addWidget(inputLabel)
        hInputBox.addWidget(self.inputLine)
        hInputBox.addWidget(self.inputSearch)
        vertBox.addLayout(hInputBox)

        # Create spin box widget to get the # of desired topics displayed in the model
        numTopicLabel = QLabel('Number of Topics:  ')
        self.numTopicBox = QSpinBox()
        self.numTopicBox.setRange(1, 20)  # Arbitrarily picked 20, idk what the max should be
        self.numTopicBox.setToolTip('Number of topics to be displayed (10 by default).')
        self.numTopicBox.setValue(10)
        # todo: add function to handle change in number of topics

        # Add # of topics box
        hNumTopicBox.addWidget(numTopicLabel)
        hNumTopicBox.addWidget(self.numTopicBox)
        vertBox.addLayout(hNumTopicBox)

        # Create mallet label, text line, search button and call mallet button
        malletLabel = QLabel('Mallet Location:')
        self.malletLine = QLineEdit('/Path/To/Mallet/Program')
        self.malletLine.setReadOnly(True)
        self.malletLine.setToolTip('This is the path to where the Mallet program is located.')
        self.malletSearch = QPushButton("...")
        self.malletSearch.setToolTip('Find the Mallet program.')
        self.malletSearch.clicked.connect(self.fileSearch)
        self.malletSearch.setEnabled(False)

        # Add the second set of widgets to the window (mallet stuff)
        vertBox.addWidget(malletLabel)
        hMalletBox.addWidget(self.malletLine)
        hMalletBox.addWidget(self.malletSearch)
        vertBox.addLayout(hMalletBox)

        # Create Run button to parse input file and call mallet
        self.runButton = QPushButton('Execute')
        self.runButton.setToolTip('Parses Excel Input File and Calls Mallet')
        self.runButton.clicked.connect(self.runProg)
        self.runButton.setEnabled(False)

        # Add run button to window
        vertBox.addWidget(self.runButton)

        # Create check boxes, these will be used later
        self.enhRadio = QRadioButton('View Enhancements')
        self.enhRadio.setChecked(True)
        self.enhRadio.setToolTip('Show Enhancements?')
        self.bugRadio = QRadioButton('View Bugs')
        self.bugRadio.setChecked(False)
        self.bugRadio.setToolTip('Show Bugs?')
        # todo: add function to handle what type of graph is displayed or remove radio buttons and only depend on typebox

        # Add checkboxes and other widgets to window
        hRadioBox.addWidget(self.enhRadio)
        hRadioBox.addWidget(self.bugRadio)
        vertBox.addLayout(hRadioBox)

        # Looking for some widget to use to change model types
        self.graphTypeBox = QComboBox()
        graphTypeList = ['All Enhancements', 'Dates of Enhancements', 'All Bugs', 'Multi Date View of Bug', 'Date Divided View of Bug']
        self.graphTypeBox.insertItems(0, graphTypeList)
        self.graphTypeBox.setToolTip('Choose what kind of graph the data should be displayed as.')
        # todo: add function to activate topic number

        # Add graphTypeBox to window
        vertBox.addWidget(self.graphTypeBox)

        self.graphTopicBox = QComboBox()
        graphTopicList = []
        for num in range(1, 11):
            graphTopicList.append("Topic " + str(num))
        self.graphTopicBox.insertItems(0, graphTopicList)
        self.graphTopicBox.setToolTip('Choose which topic for graph')
        self.graphTopicBox.setEnabled(False)

        vertBox.addWidget(self.graphTopicBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(vertBox, 0, 1)

        self.setLayout(mainLayout)
        self.setWindowTitle('Next Top Model')

    def runProg(self):
        print('GUI - Run button pressed.')
        malletPath = str(self.malletLine.text())
        inputFilePath = str(self.inputLine.text())

        print('GUI - Testing Mallet Path...')
        # checks for valid mallet path first
        if malletPath == '':
            QMessageBox.information(self, 'Error',
                                    'No path found.  Please enter the Mallet Program.')
            return
        elif 'mallet' not in malletPath:
            QMessageBox.information(self, 'Error',
                                    'Mallet not found in path.  Please enter the Mallet Program.')
            return
        else:
            print('GUI - Valid mallet path found, testing input file path.')

            # if the mallet path is valid, check input file path
            if inputFilePath == '':
                QMessageBox.information(self, 'Error',
                                        'No path found.  Please enter the input file path.')
                return

            elif '.xls' not in inputFilePath and '.xlsx' not in inputFilePath:
                QMessageBox.information(self, 'Error',
                                        'Valid Excel File not found.  Please enter a valid input file.')
                return

            else:
                # if both paths are valid, go ahead and run the modules
                print('GUI - Input File and Mallet paths are valid, running...')

                # Call Parser
                print('GUI - ExcelParser.py executing -- Please Wait.')
                ExcelParser.main(inputFilePath, 1, ["3", "4"])

                # Call MalletCaller.py
                print('GUI - MalletCaller.py executing -- Please Wait.')
                MalletCaller.main(malletPath, self.numTopicBox.value())

                # Call FileFilter.py
                print('GUI - FileFilter.py executing -- Please Wait.')
                FileFilter.main()

                # Call TopicStocker.py
                print('GUI - TopicStocker.py executing -- Please Wait.')
                topics = TopicStocker.main(self.numTopicBox.value())

                # Call the VisualModeler.py
                print('GUI - VisualModeler.py executing -- Please Wait.')
                VisualModel = VisualModeler.VisualModeler()
                graphType = self.graphTypeBox.currentText()
                    # Find the arrays of topics
                enhTopics = topics.getEnhTopics()
                bugTopics = topics.getBugTopics()
                
                # 'All Enhancements', 'Dates of Enhancements'
                # 'All Bugs', 'Multi Date View of Bug', 'Date Divided View of Bug'

                if self.enhRadio.isChecked():
                    # Enhancements. one of: modelVolumeEnhView or modelDateView
                    if graphType == 'All Enhancements':
                        plot = VisualModel.modelVolumeEnhView(enhTopics)
                        print(plot)

                    elif graphType == 'Dates of Enhancements':
                        # When the user specifies the enhancement they want, pass that topic to the modeler
                        enhTopic = enhTopics[self.graphTopicBox.currentIndex()]
                        plot = VisualModel.modelDateView(enhTopic)
                        print(plot)

                elif self.bugRadio.isChecked():
                    # Bugs. one of: modelVolumeBugView, modelMultiDateView, modelDividedView
                    if graphType == 'All Bugs':
                        plot = VisualModel.modelVolumeBugView(bugTopics)
                        print(plot)

                    elif graphType == 'Multi Date View of Bug':
                        # When the user specifies the bug they want, pass that topic to the modeler
                        bugTopic = bugTopics[self.graphTopicBox.currentIndex()]
                        plot = VisualModel.modelMultiDateView(bugTopic)
                        print(plot)

                    elif graphType == 'Date Divided View of Bug':
                        # When the user specifies the bug they want, pass that topic to the modeler
                        bugTopic = bugTopics[self.graphTopicBox.currentIndex()]
                        plot = VisualModel.modelDividedView(bugTopic)
                        print(plot)

                print('GUI - All modules done processing.')
                QMessageBox.information(self, 'Processing Completed', 'Modules have finished processing.')

    def fileSearch(self):
        print('GUI - File Search button pressed')
        fname = QFileDialog.getOpenFileName(self, 'Open file')

        fname1 = str(fname).split()

        inputLen = len(fname1[0])               # we need to know how long the input is
        inputLen -= 2                                   # get rid of the last two characters ',
        inputFile = fname1[0][2:inputLen]    # strip off the first two characters ('

        # These print statements show exactly what the problem was and how it was progressively resolved
        # print(str(fname))
        # print(fname1[0])
        # print(inputfile)

        print('GUI - Testing:  ' + inputFile)
        # Is the input the mallet path or the input file path?
        if 'Mallet' in inputFile or 'mallet' in inputFile:
            print('GUI - Mallet input path detected, setting Mallet line.')
            self.malletLine.setText(inputFile)
            self.runButton.setEnabled(True)
            return
        elif '.xls' in inputFile or '.xlsx' in inputFile:
            print('GUI - Excel input path detected, setting Excel line.')
            self.inputLine.setText(inputFile)
            self.malletSearch.setEnabled(True)
            return
        else:
            QMessageBox.information(self, 'Error', 'Please enter a valid input file')
            return

# code below looks for inputdirectory in the program path location, if it is not found, the program makes one
ipDir = 'inputdirectory'
if not os.path.exists(ipDir):
    print('GUI - No Input Directory Found, Creating Input Directory')
    os.makedirs(ipDir)      # Chris:  I'm pretty sure this will work just fine on Windows as well
else:
    print('GUI - Input Directory Found.')

if __name__ == '__main__':
    import sys
 
    app = QApplication(sys.argv)
 
    screen = Form()
    screen.show()
 
    sys.exit(app.exec_()) 

