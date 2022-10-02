import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt5.QtCore import Qt, QUrl, QTimer, QEvent
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineSettings
from PyQt5.QtGui import QMouseEvent
from PyQt5.QtWebEngineCore import QWebEngineUrlRequestInterceptor

import easyocr
import cv2
from matplotlib import pyplot as plt
import numpy as np

import time

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--prop', dest='prop', type=str, default='wind-speed', help='wind-speed, temperature, base')
parser.add_argument('--latitude', dest='latitude', default='0', type=str, help='latitude in string')
parser.add_argument('--longitude', dest='longitude', default='0',type=str, help='longitude in string')
args = parser.parse_args()

class Screenshot(QMainWindow):
    def capture(self, url, output_file):
        self.browser = QWebEngineView()
        self.output_file = output_file
        
        self.browser.load(QUrl(url))
        self.setCentralWidget(self.browser)
        self.browser.loadFinished.connect(self.on_loaded)
        #self.browser.urlChanged.connect(self.on_url_change)
        # Create hidden view without scrollbars
        self.setAttribute(Qt.WA_DontShowOnScreen)
        self.browser.page().settings().setAttribute(
            QWebEngineSettings.ShowScrollBars, False)
        self.show()
    def getRainfallDetails(self):
        IMAGE_PATH = 'base.png'
        #IMAGE_PATH = 'surf.jpeg'

        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH)
        #print(result)
        
        norain = True
        for i in result:
            currstr = i[len(i)-2].lower()
            stringsplitted = currstr.split(" ")
            #print(currstr)
            if "rain" in currstr:
                print("Rainfall: ", currstr)
                norain = False
                break
             
                
    def getTemperatureDetails(self):
        IMAGE_PATH = 'temperature.png'
        #IMAGE_PATH = 'surf.jpeg'

        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH)
        #print(result)
        
        for i in result:
            currstr = i[len(i)-2].lower()
            stringsplitted = currstr.split(" ")
            #print(currstr)
            if "*c" in currstr:
                print("Temperature: ", currstr)
                break
                
    def getWindDetails(self):
        
        IMAGE_PATH = 'wind-speed.png'
        #IMAGE_PATH = 'surf.jpeg'
        somestr = ""
        reader = easyocr.Reader(['en'])
        result = reader.readtext(IMAGE_PATH)
        #print(result)

        directions = ['n', 'nne', 'ne', 'ene', 'e', 'ese', 'se', 'sse', 's', 'ssw', 'sw', 'wsw', 'w', 'wnw', 'nw', 'nnw']
        directions2 = ['on', 'onne', 'one', 'oene', 'oe', 'oese', 'ose', 'osse', 'os', 'ossw', 'osw', 'owsw', 'ow', 'ownw', 'onw', 'onnw']
        directions3 = ['0n', '0nne', '0ne', '0ene', '0e', '0ese', '0se', '0sse', '0s', '0ssw', '0sw', '0wsw', '0w', '0wnw', '0nw', '0nnw']
        
        for i in result:
            currstr = i[len(i)-2].lower()
            stringsplitted = currstr.split(" ")
            #print(currstr)
            if "km/h" in currstr or "km1h" in currstr or "kmlh" in currstr:
                #print(currstr)
                for q in currstr:
                    q = q.replace("km/h", "")
                    q = q.replace("km1h", "")
                    q = q.replace("kmlh", "")
                    
                    if q.isnumeric():
                        print("Windspeed: ", q * 1/3.6, "m/s")
                        with open('windspeed.txt', 'wt') as windtxt:
                            windtxt.write(str(q * 1/3.6))
                        somestr += str(q * 1/3.6) + ","
            if "m/s" in currstr or "m1s" in currstr or "mls" in currstr:
                #print(currstr)
                for q in currstr:
                    q = q.replace("m/s", "")
                    q = q.replace("m1s", "")
                    q = q.replace("mls", "")
                    if q.isnumeric():
                        print("Windspeed: ", q, "m/s")
                        with open('windspeed.txt', 'wt') as windtxt:
                            windtxt.write(str(q))
                        somestr += str(q) + ","
                #print(currstr)
            
            
            for q in stringsplitted:
                if q in directions:
                    ind = directions.index(q)
                    print("Direction: ", ind * 22.5, " ", q)
                    somestr += str(ind * 22.5) + "\n"
                    with open('winddir.txt', 'wt') as windtxt:
                            windtxt.write(str(ind * 22.5))
                if q in directions2:
                    ind = directions2.index(q)
                    print("Direction: ", ind * 22.5, " ", directions[ind])
                    somestr += str(ind * 22.5) + "\n"
                    with open('winddir.txt', 'wt') as windtxt:
                            windtxt.write(str(ind * 22.5))
                if q in directions3:
                    ind = directions3.index(q)
                    print("Direction: ", ind * 22.5, " ", directions[ind])
                    somestr += str(ind * 22.5) + "\n"
                    with open('winddir.txt', 'wt') as windtxt:
                            windtxt.write(str(ind * 22.5))
                break
            
    
    def on_loaded(self):
        size = self.browser.page().contentsSize().toSize()
        self.browser.resize(size)
        # Wait for resize
        
        for child in self.browser.findChildren(QWidget):
            if (child.metaObject().className() == "QtWebEngineCore::RenderWidgetHostViewQtDelegateWidget"):
                print(child.metaObject().className())
                # Get the actual web content widget
                #child = self.findChildren(QWebEngineView)
                # Create a fake mouse move event
                print(self.rect().center())
                event = QMouseEvent(QEvent.MouseMove, 
                    self.rect().center(), 
                    Qt.NoButton, Qt.MouseButtons(Qt.NoButton), 
                    Qt.KeyboardModifiers(Qt.NoModifier))
                # Send the event
                QApplication.postEvent(child, event)
                print("Moved")
        
        #self.browser.current_url = self.browser.url().toString()

        print("Capturing")
        QTimer.singleShot(1500, self.take_screenshot)
    someval = False
    def take_screenshot(self):
        self.grab().save(self.output_file, b'PNG')
        self.app.quit()
        if args.prop == 'wind-speed':
            self.getWindDetails()
        elif args.prop == 'base':
            self.getRainfallDetails()
        elif args.prop == 'temperature':
            self.getTemperatureDetails()
        

#print (args.product_id)

app = QApplication(sys.argv)
screenshots = {}

screenshot = Screenshot()
screenshot.app = app
print('https://zoom.earth/maps/' + args.prop + '/#view=' + args.latitude + ',' + args.longitude + ',11z/overlays=labels:off')
screenshot.capture('https://zoom.earth/maps/' + args.prop + '/#view=' + args.latitude + ',' + args.longitude + ',11z/overlays=labels:off', args.prop + '.png')

sys.exit(app.exec_())