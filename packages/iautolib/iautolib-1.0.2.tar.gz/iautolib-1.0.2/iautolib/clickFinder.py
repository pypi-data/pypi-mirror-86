from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
import sys
import os
import os.path
from PyQt5.uic import loadUiType
import cv2
import numpy as np
from PIL import Image, ImageGrab 
from selenium.webdriver.common.action_chains import ActionChains
import pyperclip

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyTnstaler"""
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

ui,_ = loadUiType(resource_path('waitimage.ui'))
img = None

class MainApp(QMainWindow, ui):
    def __init__(self, parent = None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.initUi()
        self.handleButtons()
        
        
        # radiobutton.toggled.connect(self.onClicked)
        # layout.addWidget(radiobutton, 0, 0)
        
    def initUi(self):
        self.tabWidget.tabBar().setVisible(False)
        self.line1.setVisible(False)
        self.line2.setVisible(False)
        style = open(resource_path('themes/classic.css'), 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def handleButtons(self):
        self.browse.clicked.connect(self.handleBrowse)
        self.load.clicked.connect(self.loadImage)
        self.copy.clicked.connect(self.handleCopy)
        self.generate.clicked.connect(self.generateCode)
        self.copyCodes.clicked.connect(self.copyCode)
        self.copyCodes2.clicked.connect(self.copyCode2)
        self.home.clicked.connect(self.openHome)
        self.imgLoader.clicked.connect(self.openImageLoader)
        self.codeGen.clicked.connect(self.openCodeGenerator)
        self.settings.clicked.connect(self.openSettings)
        self.darkTheme.clicked.connect(self.applyDarkBlue)
        self.qdarkTheme.clicked.connect(self.applyQDark)
        self.defaultTheme.clicked.connect(self.applyDefaultTheme)
        self.sClick.clicked.connect(self.singleClick)
        self.lClick.clicked.connect(self.leftClick)
        self.DBClick.clicked.connect(self.doubleClick)
        self.rClick.clicked.connect(self.rightClick)
    
    def handleBrowse(self):
        saveLocation = QFileDialog.getOpenFileName(self, caption= "save as ", directory=".", filter="All Files(*.*)")
        self.imageLocation.setText(str(saveLocation[0]))
    
    def handleCopy(self):
        points = self.genText.text()
        pyperclip.copy(points)
    
    def saveBrowse(self):
        pass
    
    
        
    def loadImage(self):
        saveLocation = self.imageLocation.text()
        if saveLocation == '':
            QMessageBox.warning(self, 'Error', 'Browse image location to continue')            
        else:
            def click_event(event, x, y, flags, param):    
                if event == cv2.EVENT_LBUTTONDOWN:
                    print(x,', ' ,y)
                    self.genText.setText(str(x) + ',' + str(y))
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    strXY = str(x) + ', '+ str(y)
                    cv2.putText(img, strXY, (x, y), font, .5, (255, 255, 0), 2)
                    cv2.imshow('image', img)
                    QApplication.processEvents
                if event == cv2.EVENT_RBUTTONDOWN:
                    blue = img[y, x, 0]
                    green = img[y, x, 1]
                    red = img[y, x, 2]
                    font = cv2.FONT_HERSHEY_SIMPLEX
                    strBGR = str(blue) + ', '+ str(green)+ ', '+ str(red)
                    cv2.putText(img, strBGR, (x, y), font, .5, (0, 255, 255), 2)
                    cv2.imshow('image', img)
                    QApplication.processEvents

    #img = np.zeros((512, 512, 3), np.uint8)
            img = cv2.imread(saveLocation)
            cv2.imshow('image', img)
            
            cv2.setMouseCallback('image', click_event)


            cv2.waitKey(0)
            cv2.destroyAllWindows()
        
            QApplication.processEvents
            
        
    def copyCode(self):
        code = self.codeText.text()
        pyperclip.copy(code)
        
    def copyCode2(self):
        code = self.codeText2.text()
        pyperclip.copy(code)

    
        
    def generateCode(self):
        saveLocation = self.imageLocation.text()
        self.codeText.setText('template = setTemplate(' + f"r'{saveLocation }'"+')'+'\nwaitImageLeftDBClick(template, ' + pyperclip.paste() + ', duration = 10)')
        self.line1.setVisible(True)
        self.line2.setVisible(True)
        QApplication.processEvents
    





    def openHome(self):
        self.tabWidget.setCurrentIndex(0)

    def openImageLoader(self):
        self.tabWidget.setCurrentIndex(1)

    def openCodeGenerator(self):
        self.tabWidget.setCurrentIndex(2)

    def openSettings(self):
        self.tabWidget.setCurrentIndex(3)
    
    def singleClick(self):
        self.codeText2.setText("""import time
import numpy as np
import cv2
import pyautogui
from PIL import Image, ImageGrab

def setTemplate(path):
    template = cv2.imread(path, 0)
    return template
    
def waitImageLeftDBClick(template, x , y, **options):
    
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    threshold = 0.85
    start = time.perf_counter()
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + x 
                global poiY 
                poiY = pt[1] + y
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > options["duration"]:
            Wait = False
    pyautogui.moveTo(poiX, poiY, duration = 2)
    pyautogui.click()""")
    
        
    # def singleClick(self):
    #     self.codeText2.setText('pyautogui.click()')
    
    def doubleClick(self):
        self.codeText2.setText("""import time
import numpy as np
import cv2
import pyautogui
from PIL import Image, ImageGrab

def setTemplate(path):
    template = cv2.imread(path, 0)
    return template
    
def waitImageLeftDBClick(template, x , y, **options):
    
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    threshold = 0.85
    start = time.perf_counter()
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + x 
                global poiY 
                poiY = pt[1] + y
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > options["duration"]:
            Wait = False
    pyautogui.moveTo(poiX, poiY, duration = 2)
    pyautogui.doubleClick()""")
        # self.codeText2.setText('pyautogui.doubleClick()')
    

    def leftClick(self):
        self.codeText2.setText("""import time
import numpy as np
import cv2
import pyautogui
from PIL import Image, ImageGrab

def setTemplate(path):
    template = cv2.imread(path, 0)
    return template
    
def waitImageLeftDBClick(template, x , y, **options):
    
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    threshold = 0.85
    start = time.perf_counter()
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + x 
                global poiY 
                poiY = pt[1] + y
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > options["duration"]:
            Wait = False
    pyautogui.moveTo(poiX, poiY, duration = 2)
    pyautogui.leftClick()""")


    # def leftClick(self):
    #     self.codeText2.setText('pyautogui.leftClick()')

    def rightClick(self):
        self.codeText2.setText("""import time
import numpy as np
import cv2
import pyautogui
from PIL import Image, ImageGrab

def setTemplate(path):
    template = cv2.imread(path, 0)
    return template
    
def waitImageLeftDBClick(template, x , y, **options):
    
    if "wait" in options:
        time.sleep(options["wait"])
        
    Wait = True
    threshold = 0.85
    start = time.perf_counter()
    while Wait:  
        #load screenshot
        screen = np.array(ImageGrab.grab(bbox=None))
        grey_img = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)
        w, h = template.shape[::-1]

        #Template matching
        res = cv2.matchTemplate(grey_img, template, cv2.TM_CCOEFF_NORMED)
        loc = np.where(res >= threshold)

        time_elapsed =  time.perf_counter() - start

        if len(loc[0]) != 0:
            for pt in zip(*loc[::-1]):
                Wait = False
                print("point coordinate: {}".format(pt))
                cv2.rectangle(screen, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                global poiX
                poiX = pt[0] + x 
                global poiY 
                poiY = pt[1] + y
            
        print(f"Time elapsed { time_elapsed }")
        
        
        if time_elapsed > options["duration"]:
            Wait = False
    pyautogui.moveTo(poiX, poiY, duration = 2)
    pyautogui.rightClick()""")


    # def rightClick(self):
    #     self.codeText2.setText('pyautogui.rightClick()')
        
    ############## App Themes ###############
    
    def applyDarkBlue(self):
        style = open(resource_path('themes/darkblue.css'), 'r')
        style = style.read()
        self.setStyleSheet(style)
    
    def applyQDark(self):
        style = open(resource_path('themes/qdark.css'), 'r')
        style = style.read()
        self.setStyleSheet(style)
        #34,29
    
    def applyDefaultTheme(self):
        style = open(resource_path('themes/classic.css'), 'r')
        style = style.read()
        self.setStyleSheet(style)
    
def main():
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    app.exec_()
    
if __name__ == "__main__":
    main()