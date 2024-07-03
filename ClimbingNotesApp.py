import sys
import csv
import re
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QPushButton, QTextEdit, QVBoxLayout, QCalendarWidget, QLabel, QGridLayout, QRadioButton, QMessageBox, QComboBox, QScrollArea # type: ignore
from PyQt6.QtGui import QIcon, QIntValidator, QColor, QBrush, QFont # type: ignore
from PyQt6.QtCore import QDate, pyqtSignal, Qt # type: ignore
from datetime import datetime
from matplotlib.figure import Figure # type: ignore
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas # type: ignore
import matplotlib.pyplot as plt # type: ignore
import numpy as np
import matplotlib.dates as mdates


class MainWindow(QWidget):
    def __init__ (self):
        super().__init__()
        self.setWindowTitle('Main Window')
        self.setWindowIcon(QIcon('./DaMan.jpg'))
        self.resize(1250, 700) #width, height       

        #CSV Filepath for Calendar
        calendarFilePath = '\\Users\\grant\\Downloads\\ClimbNotes\\CSVStorage\\GBClimbingStats.csv'

        #Main Layout
        self.mainLayout = QGridLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)  # Remove margins
        self.mainLayout.setSpacing(0)  # Remove spacing


        #Dropdown Menu for Layout Selector
        self.layoutSelector = QComboBox()
        self.layoutSelector.addItem('Main View')
        self.layoutSelector.addItem('Calendar View')
        self.layoutSelector.addItem('Hangboard Full View')
        self.layoutSelector.addItem('Regular Workout Full View')
        self.layoutSelector.addItem('Good/Bad Climbing Day Full View')
        self.layoutSelector.addItem('Boulder Graph')
        self.layoutSelector.currentIndexChanged.connect(self.switchLayout)
        self.mainLayout.addWidget(self.layoutSelector)

        #Container For different layouts
        self.container = QWidget()
        self.mainLayout.addWidget(self.container)

        #widgets
        self.hangButton = QPushButton('&Add Hangboard Workout', clicked=self.newHangLogWindow)
        self.workButton = QPushButton('&Add Regular Workout', clicked=self.newRegWorkWindow)
        self.GBClimbButton = QPushButton('&Add Good/Bad Climb', clicked=self.newGBWindow)
        self.boulderWindowButton = QPushButton('&Add Boulder Climb', clicked=self.boulderMaxNewWindow)
        self.sportWindowButton = QPushButton('&Add Sport Climb', clicked=self.sportMaxNewWindow)                
        self.updateHangGraphButton = QPushButton('&Refresh Hangboard Graph', clicked=self.updateHangGraph)
        self.calendar = ClimbingCalendar(calendarFilePath, self)
        self.graphWidget = hangboardGraphStats(self)
        self.boulderScatterPlotWidget = FigureCanvas(plt.Figure())
        self.regWorkViewLabel = QLabel()
        self.hangboardViewLabel = QLabel()
        self.gBViewLabel = QLabel()
        self.scrollWheel = QScrollArea()
        self.hangScrollWheel = QScrollArea()
        self.gBScrollWheel = QScrollArea()


        #Add Widgets
        self.mainLayout.addWidget(self.regWorkViewLabel)
        self.mainLayout.addWidget(self.hangboardViewLabel)
        self.mainLayout.addWidget(self.gBViewLabel)
        self.mainLayout.addWidget(self.boulderWindowButton)
        self.mainLayout.addWidget(self.sportWindowButton)
        self.mainLayout.addWidget(self.hangButton)
        self.mainLayout.addWidget(self.workButton)
        self.mainLayout.addWidget(self.GBClimbButton)
        self.mainLayout.addWidget(self.updateHangGraphButton)        
        self.mainLayout.addWidget(self.graphWidget)
        self.mainLayout.addWidget(self.calendar)
        self.mainLayout.addWidget(self.scrollWheel)
        self.mainLayout.addWidget(self.hangScrollWheel)
        self.mainLayout.addWidget(self.gBScrollWheel)
        self.mainLayout.addWidget(self.boulderScatterPlotWidget)

        # Create a scroll area
        self.scrollWheel.setWidgetResizable(True)
        self.scrollWheel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollWheel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.scrollWheel.setWidget(self.regWorkViewLabel)

        self.hangScrollWheel.setWidgetResizable(True)
        self.hangScrollWheel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.hangScrollWheel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.hangScrollWheel.setWidget(self.hangboardViewLabel)

        self.gBScrollWheel.setWidgetResizable(True)
        self.gBScrollWheel.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.gBScrollWheel.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.gBScrollWheel.setWidget(self.gBViewLabel)
        

        #Hide the widgets initially for Main View
        self.calendar.hide()
        self.regWorkViewLabel.hide()
        self.hangboardViewLabel.hide()
        self.gBViewLabel.hide()
        self.scrollWheel.hide()
        self.hangScrollWheel.hide()
        self.gBScrollWheel.hide()
        self.boulderScatterPlotWidget.hide()

        #Initially Show data for Hangboard Graph
        self.updateHangGraph()
        
        #Hangboard display
        self.hangboardViewLabel.setFont(QFont("Arial", 14))
        self.hangboardViewLabel.setStyleSheet("color: white;")  # Assuming dark mode based on the screenshot
        self.hangboardViewLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hangboardViewLabel.setWordWrap(True)  # Allow text wrapping
        self.hangboardViewLabel.setMargin(10)

        #Regular Workout Display
        self.regWorkViewLabel.setFont(QFont("Arial", 14))
        self.regWorkViewLabel.setStyleSheet(""""color: white;""")  # Assuming dark mode based on the screenshot
        self.regWorkViewLabel.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.regWorkViewLabel.setWordWrap(True)  # Allow text wrapping
        self.regWorkViewLabel.setMargin(10)

        #G/B Display

        
    def updateHangGraph(self):
        filepath = '\\Users\\grant\\Downloads\\ClimbNotes\\CSVStorage\\HangboardStats.csv'
        dates, weights, workouts = readCsvDataHangBoard(filepath)
        self.graphWidget.plotWeightOverTime(dates, weights, workouts)

    def newHangLogWindow(self, checked):
        filepath = '\\Users\\grant\\Downloads\\ClimbNotes\\CSVStorage\\HangboardStats.csv'
        self.w = SubWinHang(filepath)
        self.w.show()

    def newRegWorkWindow(self, checked):
        filepath = '\\Users\\grant\\Downloads\\ClimbNotes\\CSVStorage\\RegWorkoutStats.csv'
        self.w = SubWinRegWorkout(filepath)
        self.w.show()

    def newGBWindow(self, checked):
        filepath = '\\Users\\grant\\Downloads\\ClimbNotes\\CSVStorage\\GBClimbingStats.csv'
        self.w = SubWinGBClimb(filepath)
        self.w.climbAdded.connect(self.calendarRefreshMain)
        self.w.show()

    def boulderMaxNewWindow(self, checked):
        filepath = r'C:\Users\grant\Downloads\ClimbNotes\CSVStorage\maxBoulder.csv'
        self.w = boulderMaxSubWin(filepath)
        self.w.show()
    
    def sportMaxNewWindow(self, checked):
        filepath = r'C:\Users\grant\Downloads\ClimbNotes\CSVStorage\maxSport.csv'
        self.w = sportMaxSubWin(filepath)
        self.w.show()

    def switchLayout(self, index):
        #Clear Current Layout
        self.clearLayout(self.container.layout())

        #Add selected layout
        if index == 0: #Main View
            self.gBScrollWheel.hide()
            self.gBViewLabel.hide()
            self.calendar.hide()
            self.regWorkViewLabel.hide()
            self.scrollWheel.hide()
            self.hangScrollWheel.hide()
            self.boulderScatterPlotWidget.hide()
            self.graphWidget.show()
            self.hangButton.show()
            self.workButton.show()
            self.updateHangGraphButton.show()


        elif index == 1: #Calendar View
            self.calendar.show()
            self.GBClimbButton.show()
            self.graphWidget.hide()
            self.hangButton.hide()
            self.workButton.hide()
            self.updateHangGraphButton.hide()
            self.regWorkViewLabel.hide()
            self.scrollWheel.hide()
            self.hangScrollWheel.hide()
            self.gBScrollWheel.hide()
            self.gBViewLabel.hide()
            self.boulderScatterPlotWidget.hide()

        elif index == 2: #Hangboard Full View
            self.hangFullView()
            self.graphWidget.hide()
            self.hangButton.hide()
            self.workButton.hide()
            self.updateHangGraphButton.hide()
            self.GBClimbButton.hide()
            self.calendar.hide()
            self.hangboardViewLabel.show()
            self.regWorkViewLabel.hide()
            self.hangScrollWheel.show()
            self.gBScrollWheel.hide()
            self.gBViewLabel.hide()
            self.boulderScatterPlotWidget.hide()


        elif index == 3: #Regular Workout View
            self.regWorkoutView()
            self.graphWidget.hide()
            self.hangButton.hide()
            self.workButton.hide()
            self.updateHangGraphButton.hide()
            self.GBClimbButton.hide()
            self.calendar.hide()
            self.hangScrollWheel.hide()
            self.regWorkViewLabel.show()
            self.scrollWheel.show()
            self.gBScrollWheel.hide()
            self.gBViewLabel.hide()
            self.boulderScatterPlotWidget.hide()

        elif index == 4: #G/B View
            self.gBFullView()
            self.graphWidget.hide()
            self.hangButton.hide()
            self.workButton.hide()
            self.updateHangGraphButton.hide()
            self.GBClimbButton.hide()
            self.calendar.hide()
            self.hangScrollWheel.hide()
            self.regWorkViewLabel.hide()
            self.scrollWheel.hide()
            self.boulderScatterPlotWidget.hide()
            self.gBScrollWheel.show()
            self.gBViewLabel.show()
            self.boulderScatterPlotWidget.hide()

        elif index == 5:
            self.boulderPlotInMain()
            self.graphWidget.hide()
            self.hangButton.hide()
            self.workButton.hide()
            self.updateHangGraphButton.hide()
            self.GBClimbButton.hide()
            self.calendar.hide()
            self.hangScrollWheel.hide()
            self.regWorkViewLabel.hide()
            self.scrollWheel.hide()
            self.gBScrollWheel.hide()
            self.gBViewLabel.hide()
            self.boulderScatterPlotWidget.show()


    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                child = layout.takeAt(0)
                if child.widget() is not None:
                    child.widget().deleteLater()
    
    def calendarRefreshMain(self):
        self.calendar.calendarRefresh()

    def regWorkoutView(self):
        filepath = '\\Users\\grant\\Downloads\\ClimbNotes\\CSVStorage\\RegWorkoutStats.csv'
        transformedWorkoutText = readCsvDataRegWorkout(filepath)
        self.regWorkViewLabel.setText(transformedWorkoutText)
    
    def hangFullView(self):
        filepath = r'C:\Users\grant\Downloads\ClimbNotes\CSVStorage\HangboardStats.csv'
        testvariable = readCsvDataHangWork(filepath)
        self.hangboardViewLabel.setText(testvariable)

    def gBFullView(self):
        filepath = r'C:\Users\grant\Downloads\ClimbNotes\CSVStorage\GBClimbingStats.csv'
        testvariable = readCsvDataGBClimb(filepath)
        self.gBViewLabel.setText(testvariable)

    def boulderPlotInMain(self):
        filepath = r'C:\Users\grant\Downloads\ClimbNotes\CSVStorage\maxBoulder.csv'
        data = boulderScatterReadCsv(filepath)
        boulderPlotScatter(data, self.boulderScatterPlotWidget)

class SubWinHang(QWidget):
    #Custom signal to update hangboard graph after adding information
    updateGraph = pyqtSignal()

    def __init__(self, filepath):
        #Initialize the Window
        super().__init__()
        self.filepath = filepath
        self.setWindowTitle('Hangboard Workout')
        self.setWindowIcon(QIcon('./DaMan.jpg'))
        self.resize(500, 400) #width, height

        #App Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #Widgets Section
        #Workout Input
        self.workoutInputField = QLineEdit()
        self.workoutInputField.setPlaceholderText('Enter HandBoard Workout')

        #Max Hanging Weight Input
        self.maxWeightInputField = QLineEdit()
        self.maxWeightInputField.setValidator(QIntValidator())
        self.maxWeightInputField.setPlaceholderText('Enter Max Hang Weight')

        #Save Info into CSV File
        saveButton = QPushButton('&Save', clicked=self.saveStats)
        saveButton.setStyleSheet('background-color: green;')

        #Add Widgets to the Page
        layout.addWidget(self.workoutInputField)
        layout.addWidget(self.maxWeightInputField)
        layout.addWidget(saveButton)
    
    #Save Stats Button
    def saveStats(self):

        #Current Year/Month/Day
        currentDate = datetime.now().strftime('%Y-%m-%d') 
        workout = self.workoutInputField.text()
        maxWeight = self.maxWeightInputField.text()

        if workout and maxWeight:
            #Inputed text from the user converted into readable string
            text_to_append = workout + ',' + maxWeight + ',' + currentDate
            
            #Open predetermined file path and append user data into text file
            with open(self.filepath, 'a') as file:
                file.write(text_to_append + '\n')
            
            #Clear User inputed data
            self.workoutInputField.clear()
            self.maxWeightInputField.clear()

            #Emit signal that data was succsefully added
            self.updateGraph.emit()
            
            #Close SubWindow
            self.close()
        else:
            QMessageBox.warning(self, 'Hangboard', 'Please make sure to enter your max weight and workout')

class SubWinRegWorkout(QWidget):
    def __init__(self, filepath):
        #Initialize the Window
        super().__init__()
        self.filepath = filepath
        self.setWindowTitle('Normal Workout')
        self.setWindowIcon(QIcon('./DaMan.jpg'))
        self.resize(500, 400) #width, height

        #App Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #Widgets Section
        #Workout Input
        self.workoutInputField = QLineEdit()
        self.workoutInputField.setPlaceholderText('Enter Your Workout, seperate different exerecises with a ;')

        #Save Info into CSV File
        saveButton = QPushButton('&Save', clicked=self.saveStats)
        saveButton.setStyleSheet('background-color: green;')

        #Add Widgets to the Page
        layout.addWidget(self.workoutInputField)
        layout.addWidget(saveButton)
    
    def saveStats(self):

        #Current Year/Month/Day
        currentDate = datetime.now().strftime('%Y-%m-%d') 
        workoutText = None

        workoutText = self.workoutInputField.text()

        if workoutText:
            #Inputed text from the user converted into readable string
            text_to_append = workoutText + ',' + currentDate
            
            #Open predetermined file path and append user data into text file
            with open(self.filepath, 'a') as file:
                file.write(text_to_append + '\n')
            
            #Clear User inputed data
            self.workoutInputField.clear()

            #Close SubWindow
            self.close()
        else:
            QMessageBox.warning(self, 'Workout','Please input your workout into the workout field.')

class SubWinGBClimb(QWidget):
    climbAdded = pyqtSignal()

    def __init__(self, filepath):
        super().__init__()
        self.filepath = filepath
        self.setWindowTitle('Normal Workout')
        self.setWindowIcon(QIcon('./DaMan.jpg'))
        self.resize(500, 400) #width, height

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.goodButton = QRadioButton('&Good')
        self.badButton = QRadioButton('&Bad')
        self.shortResponse = QTextEdit()
        submitButton = QPushButton('&Submit', clicked=self.submit)
        self.reason = QLabel('Reason:')


        layout.addWidget(self.goodButton)
        layout.addWidget(self.badButton)
        layout.addWidget(self.reason)
        layout.addWidget(self.shortResponse)
        layout.addWidget(submitButton)

    def submit(self):
        selected_option = None

        if self.goodButton.isChecked():
            selected_option = 'Good'
        elif self.badButton.isChecked():
            selected_option = 'Bad'

        reason = self.shortResponse.toPlainText()

        if selected_option:
            #Current Year/Month/Day
            currentDate = datetime.now().strftime('%Y-%m-%d') 

            #Inputed text from the user converted into readable string
            text_to_append = selected_option + ',' + reason +',' + currentDate
            
            #Open predetermined file path and append user data into text file
            with open(self.filepath, 'a') as file:
                file.write(text_to_append + '\n')
            
            #Clear User inputed data
            self.shortResponse.clear()

            #Emit signal to indicate new climb has been added
            self.climbAdded.emit()

            #Close SubWindow
            self.close()
        else:
            QMessageBox.warning(self, 'Selection', 'Please select either Good or Bad')

# Graph Widget For Main Window
class hangboardGraphStats(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)
        self.canvas = FigureCanvas(Figure())
        self.layout.addWidget(self.canvas)
        self.ax = self.canvas.figure.add_subplot(111)
        self.canvas.mpl_connect('motion_notify_event', self.onHover)
        self.setLayout(self.layout)
        self.annotation = self.ax.annotate('The Testing Grounds', xy=(0,0), xytext=(0,1),
                                           textcoords='offset points',
                                           bbox=dict(boxstyle='round, pad=0.5', fc='yellow', alpha=0.7),
                                           arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        self.annotation.set_visible(False)
        self.line = None
        self.data = None

    def plotWeightOverTime(self, dates, weights, workouts):
        self.ax.clear()
        self.data = list(zip(dates, weights, workouts))
        self.line = self.ax.plot(dates, weights, marker='o', linestyle='-')[0]
        self.ax.set_title('Hangboard Weight OVT')
        self.ax.set_xlabel('Date')
        self.ax.set_ylabel('Weight in lbs')
        self.ax.grid(True)
        self.canvas.draw()

    def onHover(self, event):
        vis = self.annotation.get_visible()
        #print(vis)
        if event.inaxes == self.ax and self.line is not None:
            cont, ind = self.line.contains(event)
            #print(cont)
            #print(ind)
            if cont:
                x, y = self.line.get_xydata()[ind['ind'][0]]
                idx = ind['ind'][0]
                date = self.data[idx][0].strftime('%Y-%m-%d')
                weight = self.data[idx][1]
                workout = self.data[idx][2]
                self.annotation.xy = (x, y)
                text = f'Date: {date}\nWeight: {weight}\nWorkout: {workout}'
                self.annotation.set_text(text)
                self.annotation.set_visible(True)
                self.canvas.draw()
            else:
                if vis:
                    self.annotation.set_visible(False)
                    self.canvas.draw()

class ClimbingCalendar(QCalendarWidget):
    def __init__(self, csv_file, parent=None):
        super().__init__(parent)
        self.csv_file = csv_file
        self.sessions = self.load_sessions_from_csv(csv_file)

    def load_sessions_from_csv(self, csv_file):
        sessions = {}
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Strip whitespace from the keys
                #row = {k.strip(): v for k, v in row.items()}
                # Debug: print the row to ensure it's being read correctly
                if 'Date' in row and 'GB' in row:
                    date = QDate.fromString(row['Date'], "yyyy-MM-dd")
                    session = row['GB']
                    sessions[date] = session
                else:
                    print("Missing expected columns in row:", row)
        return sessions

    def calendarRefresh(self):
        self.sessions = self.load_sessions_from_csv(self.csv_file)
        self.updateCells()

    def paintCell(self, painter, rect, date):
        super().paintCell(painter, rect, date)
        
        if date in self.sessions:
            session = self.sessions[date]
            color = QColor('green') if session == 'Good' else QColor('red')
            color.setAlpha(100)

            painter.save()
            painter.setBrush(QBrush(color))
            painter.drawRect(rect)
            painter.restore()

class maxBoulderClimbStats(QWidget):
    def __init__(self, filepath, parent=None):
        super().__init__(parent)
        self.initUi()

   # def initUi(self):
        
class sportMaxSubWin(QWidget):
    #Custom signal to update hangboard graph after adding information
    updateGraph = pyqtSignal()

    def __init__(self, filepath):
        #Initialize the Window
        super().__init__()
        self.filepath = filepath
        self.setWindowTitle('Boulder Stats')
        self.setWindowIcon(QIcon('./DaMan.jpg'))
        self.resize(500, 400) #width, height

        #App Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #Widgets Section
        #Dropdown box of boulder grades
        self.sportClimbSelector = QComboBox()
        self.sportClimbSelector.addItem('5.5')
        self.sportClimbSelector.addItem('5.6')
        self.sportClimbSelector.addItem('5.7')
        self.sportClimbSelector.addItem('5.8')
        self.sportClimbSelector.addItem('5.9')
        self.sportClimbSelector.addItem('5.10a/b')
        self.sportClimbSelector.addItem('5.10c/d')
        self.sportClimbSelector.addItem('5.11a/b')
        self.sportClimbSelector.addItem('5.11c/b')
        self.sportClimbSelector.addItem('5.12a/b')
        self.sportClimbSelector.addItem('5.12c/d')
        self.sportClimbSelector.addItem('5.13a/b')
        self.sportClimbSelector.addItem('5.13c/d')
        self.sportClimbSelector.setPlaceholderText('Enter Max Sport Grade')
        self.sportClimbSelector.currentIndexChanged.connect(self.gradeSelector)
        layout.addWidget(self.sportClimbSelector)

        #Highest Grade Climb Counter
        self.counterMaxClimbs = QLineEdit()
        self.counterMaxClimbs.setValidator(QIntValidator())
        self.counterMaxClimbs.setPlaceholderText('Highest Grade Climb Counter')

        #Highest Grade Climb Counter
        self.favoriteClimbName = QLineEdit()
        self.favoriteClimbName.setPlaceholderText('Favorite Climb Name')

        #Save Info into CSV File
        saveButton = QPushButton('&Save', clicked=self.saveStats)
        saveButton.setStyleSheet('background-color: green;')

        #Add Widgets to the Page
        layout.addWidget(self.counterMaxClimbs)
        layout.addWidget(self.favoriteClimbName)
        layout.addWidget(saveButton)
    
        self.grade = None
    def gradeSelector(self, index):

        if index == 0:
            self.grade = '5.5'
        elif index == 1:
            self.grade = '5.6'
        elif index == 2:
            self.grade = '5.7'
        elif index == 3:
            self.grade = '5.8'
        elif index == 4:
            self.grade = '5.9'
        elif index == 5:
            self.grade = '5.10a/b'
        elif index == 6:
            self.grade = '5.10c/d'
        elif index == 7:
            self.grade = '5.11a/b'
        elif index == 8:
            self.grade = '5.11c/d'
        elif index == 9:
            self.grade = '5.12a/b'
        elif index == 10:
            self.grade = '5.12c/d'
        elif index == 11:
            self.grade = '5.13a/b'    
        elif index == 12:
            self.grade = '5.13c/d'

    #Save Stats Button
    def saveStats(self):

        #Current Year/Month/Day
        currentDate = datetime.now().strftime('%Y-%m-%d') 
        saveGrade = self.grade
        highestGradeCounter = self.counterMaxClimbs.text()
        favoriteClimbName = self.favoriteClimbName.text()


        if saveGrade and highestGradeCounter:
            #Inputed text from the user converted into readable string
            text_to_append = saveGrade + ',' + highestGradeCounter + ',' + favoriteClimbName +','+ currentDate
            
            #Open predetermined file path and append user data into text file
            with open(self.filepath, 'a') as file:
                file.write(text_to_append + '\n')
            
            #Clear User inputed data
            self.counterMaxClimbs.clear()
            self.favoriteClimbName.clear()

            #Emit signal that data was succsefully added
            #self.updateGraph.emit()
            
            #Close SubWindow
            self.close()
        else:
            QMessageBox.warning(self, 'Sport', 'Please make sure to enter your max Sport Grade and max Count, Sport Name Optional')

class boulderMaxSubWin(QWidget):
    #Custom signal to update hangboard graph after adding information
    updateGraph = pyqtSignal()

    def __init__(self, filepath):
        #Initialize the Window
        super().__init__()
        self.filepath = filepath
        self.setWindowTitle('Sport Climbing Stats')
        self.setWindowIcon(QIcon('./DaMan.jpg'))
        self.resize(500, 400) #width, height

        #App Layout
        layout = QVBoxLayout()
        self.setLayout(layout)

        #Widgets Section
        #Dropdown box of boulder grades
        self.sportClimbSelector = QComboBox()
        self.sportClimbSelector.addItem('VB')
        self.sportClimbSelector.addItem('V0')
        self.sportClimbSelector.addItem('V1')
        self.sportClimbSelector.addItem('V2')
        self.sportClimbSelector.addItem('V3')
        self.sportClimbSelector.addItem('V4')
        self.sportClimbSelector.addItem('V5')
        self.sportClimbSelector.addItem('V6')
        self.sportClimbSelector.addItem('V7')
        self.sportClimbSelector.addItem('V8')
        self.sportClimbSelector.addItem('V9')
        self.sportClimbSelector.addItem('V10')
        self.sportClimbSelector.setPlaceholderText('Enter Max Boulder')
        self.sportClimbSelector.currentIndexChanged.connect(self.gradeSelector)
        layout.addWidget(self.sportClimbSelector)

        #Highest Grade Climb Counter
        self.counterMaxClimbs = QLineEdit()
        self.counterMaxClimbs.setValidator(QIntValidator())
        self.counterMaxClimbs.setPlaceholderText('Highest Grade Climb Counter')

        #Highest Grade Climb Counter
        self.favoriteClimbName = QLineEdit()
        self.favoriteClimbName.setPlaceholderText('Favorite Climb Name')

        #Save Info into CSV File
        saveButton = QPushButton('&Save', clicked=self.saveStats)
        saveButton.setStyleSheet('background-color: green;')

        #Add Widgets to the Page
        layout.addWidget(self.counterMaxClimbs)
        layout.addWidget(self.favoriteClimbName)
        layout.addWidget(saveButton)
    
        self.grade = None
    def gradeSelector(self, index):

        if index == 0:
            self.grade = 'VB'
        elif index == 1:
            self.grade = 'V0'
        elif index == 2:
            self.grade = 'V1'
        elif index == 3:
            self.grade = 'V2'
        elif index == 4:
            self.grade = 'V3'
        elif index == 5:
            self.grade = 'V4'
        elif index == 6:
            self.grade = 'V5'
        elif index == 7:
            self.grade = 'V6'
        elif index == 8:
            self.grade = 'V7'
        elif index == 9:
            self.grade = 'V8'
        elif index == 10:
            self.grade = 'V9'
        elif index == 11:
            self.grade = 'V10'    

    #Save Stats Button
    def saveStats(self):

        #Current Year/Month/Day
        currentDate = datetime.now().strftime('%Y-%m-%d') 
        saveGrade = self.grade
        highestGradeCounter = self.counterMaxClimbs.text()
        favoriteClimbName = self.favoriteClimbName.text()


        if saveGrade and highestGradeCounter:
            #Inputed text from the user converted into readable string
            text_to_append = saveGrade + ',' + highestGradeCounter + ',' + favoriteClimbName +','+ currentDate
            
            #Open predetermined file path and append user data into text file
            with open(self.filepath, 'a') as file:
                file.write(text_to_append + '\n')
            
            #Clear User inputed data
            self.counterMaxClimbs.clear()
            self.favoriteClimbName.clear()

            #Emit signal that data was succsefully added
            #self.updateGraph.emit()
            
            #Close SubWindow
            self.close()
        else:
            QMessageBox.warning(self, 'Boulder', 'Please make sure to enter your max Boulder and max Count, Boulder Name Optional')

#Reads the CSV Data for the hangboarding stats
def readCsvDataHangBoard(filepath):
    dates = []
    weights = []
    workouts = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            dates.append(datetime.strptime(row['Date'], '%Y-%m-%d'))
            weights.append(float(row['Weight']))
            workouts.append(row['Workout'])
    return dates, weights, workouts

def readCsvDataRegWorkout(filepath):
    dates = []
    workouts = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            row = {k.strip(): v.strip() for k, v in row.items()}
            if 'Date' in row and 'Workout' in row:
                date_str = row['Date']
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                    sanitized_workout = sanitizeText(row['Workout'])
                    dates.append(date)
                    workouts.append(sanitized_workout)
                except ValueError as e:
                    print(f"Error parsing date: {date_str}, error: {e}")
            else:
                print('Missing expected column in row:', row)
    readable_text = [f'Date: {date} \nWorkout:\n{workout}\n' for date, workout in zip(dates, workouts)]
    print('\n'.join(readable_text))
    return '\n'.join(readable_text)

def readCsvDataHangWork(filepath):
    dates = []
    weights = []
    workouts = []

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:

            row = {k.strip(): v.strip() for k, v in row.items()}

            if 'Date' in row and 'Workout' in row and 'Weight' in row:
                date_str = row['Date']
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                    sanitized_weight = sanitizeText(row['Weight'])
                    sanitized_workout = sanitizeText(row['Workout'])
                    dates.append(date)
                    weights.append(sanitized_weight)
                    workouts.append(sanitized_workout)
                except ValueError as e:
                    print(f"Error parsing date: {date_str}, error: {e}")
            else:
                print('Missing expected column in row:', row)

    readable_text = [f'Date: {date}\nMax Weight: {weight}\nWorkout: {workout}\n' for date, weight, workout in zip(dates, weights, workouts)]
    result = '\n'.join(readable_text)

    return result

def readCsvDataGBClimb(filepath):
    dates = []
    reasons = []
    GBs = []
    
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Strip whitespace from keys and values
            row = {k.strip(): v.strip() for k, v in row.items()}
            if 'GB' in row and 'Reason' in row and 'Date' in row:
                date_str = row['Date']
                try:
                    date = datetime.strptime(date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                    sanitized_reason = sanitizeText(row['Reason'])
                    sanitized_GB = sanitizeText(row['GB'])
                    dates.append(date)
                    reasons.append(sanitized_reason)
                    GBs.append(sanitized_GB)
                except ValueError as e:
                    print(f"Error parsing date: {date_str}, error: {e}")
            else:
                print('Missing expected column in row:', row)
    
    readable_text = [f'Date: {date}\nGood/Bad: {gb}\nReason: {reason}\n' for date, gb, reason in zip(dates, GBs, reasons)]
    result = '\n'.join(readable_text)
    
    return result

def sanitizeText(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def boulderScatterReadCsv(filepath):
    data = []
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            highest_grade = row['HighestGrade']
            count = int(row['Count'])
            date = datetime.strptime(row['Date'], '%Y-%m-%d')
            data.append((highest_grade, count, date))
    return data

def boulderGradeToNumeric(grade):
    if grade.startswith('V'):
        try:
            if grade == 'VB':
                return -1  # Define a special numeric value for 'VB'
            else:
                return int(grade[1:])  # Strip the 'V' and convert the rest to an integer
        except ValueError:
            return 0  # Return 0 or some other value for invalid grades
    return 0  # Default value for grades that don't start with 'V'

def boulderPlotScatter(data, canvas):
    # Convert data to separate lists
    grades = [boulderGradeToNumeric(grade) for grade, count, date in data]
    counts = [count for grade, count, date in data]
    dates = [date.toordinal() for grade, count, date in data]  # Convert datetime to ordinal

    fig, ax = plt.subplots()
    scatter = ax.scatter(grades, counts, c=dates, cmap='viridis', alpha=0.6, edgecolors='w', linewidth=0.5)
    cbar = fig.colorbar(scatter, ax=ax, label='Date')
    cbar.ax.yaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax.set_xlabel('Highest Grade')
    ax.set_ylabel('Count')
    ax.set_title('Scatter Plot of Highest Grade vs Count by Date')

    canvas.figure = fig
    canvas.draw()


app = QApplication(sys.argv)    #sys.argv lets us run this from the command line
app.setStyleSheet('''
    QWidget {
        font-size: 25px;
    }
                  
    QPushButton {
        font-size: 20px;
    }
''')

window = MainWindow()
window.show()   #Shows application

sys.exit(app.exec())    #Clean Exit