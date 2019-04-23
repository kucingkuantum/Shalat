import sys
#from PyQt5.QtCore import *
#from PyQt5.QtGui import QFileDialog
from PyQt5 import QtWidgets  
from PyQt5.QtWidgets import QApplication, QFileDialog, QMessageBox
from PyQt5.Qt import QMainWindow,qApp,  QTimer, QTime
from PyQt5.QtCore import (QCoreApplication, QObject, QRunnable, QThread, QThreadPool,pyqtSignal)
from ramadan import Ui_MainWindow
from datetime import datetime
from hijriconverter import convert
from datetime import date
import datetime
from adhan import adhan
from adhan.methods import  ASR_STANDARD, MUSLIM_WORLD_LEAGUE
from yahoo_weather.weather import YahooWeather
from yahoo_weather.config.units import Unit
import pandas as pd


class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self,parent=None):
        super(MyMainWindow, self).__init__(parent)
        qApp.installEventFilter(self)
        self.setupUi(self)
        self.day()
        
        self.watch()
        timer = QTimer(self)
        timer.timeout.connect(self.watch)
        timer.start(1000)

#        self.watch()
      
        
        
    def watch(self):
        time = QTime.currentTime()
        text = time.toString('hh:mm')
        texif = time.toString('hh:mm:ss')
        if (time.second() % 2) == 0:
            text = text[:2] + ' ' + text[3:]

        self.lcdNumberClock.display(text)
        
        if texif == self.ishaa+":00":
            self.Weather()
        if texif == self.imsak+":00":
            self.Weather()
        if texif == self.fajr+":00":
            self.Weather()
        if texif == self.zuhr+":00":
            self.Weather()
        if texif == self.asr+":00":
            self.Weather()
        if texif == self.maghrib+":00":
            self.Weather()
        
        if texif == "00:00:01":
            self.day()
        
        
            
       

    
    def day(self):  
        date1 = datetime.date.today().strftime("%A, %d %b %Y")
        self.labelDate.setText(date1)
        hij = convert.Gregorian.today().to_hijri()
        month = hij.month_name()
        day = hij.datetuple()[2]
        year = hij.datetuple()[0]
        self.labelHijri.setText(str(day)+" "+str(month)+" "+str(year))
        df = pd.read_csv('juz.csv',header=None)
        juz = df.iloc[day-1,1]
        self.labelTadarus.setText(juz)

        self.shalat()
        self.Weather()


    def shalat(self):
        params = {}
        params.update(MUSLIM_WORLD_LEAGUE)
        params.update(ASR_STANDARD)

        adhan_times = adhan(
        day=date.today(),
        location=(55.70584, 13.19321),
        parameters=params,
        timezone_offset=1/5)
        
       
        self.fajr =adhan_times['fajr'].strftime('%H:%M')
        imsak =adhan_times['fajr'] - datetime.timedelta(minutes = 10)
        self.imsak = imsak.strftime('%H:%M')
        self.zuhr =adhan_times['zuhr'].strftime('%H:%M')
        self.asr =adhan_times['asr'].strftime('%H:%M')
        self.maghrib =adhan_times['maghrib'].strftime('%H:%M')
        self.ishaa =adhan_times['isha'].strftime('%H:%M')
        
        self.lcdNumberIshaa.display(self.ishaa)
        self.lcdNumberImsak.display(self.imsak)
        self.lcdNumberFajr.display(self.fajr)
        self.lcdNumberDhuhr.display(self.zuhr)
        self.lcdNumberAsr.display(self.asr)
        self.lcdNumberMaghrib.display(self.maghrib)
        
    def Weather(self):
        data = YahooWeather(APP_ID="",
                     api_key="",
                     api_secret="")

        data.get_yahoo_weather_by_city("lund", Unit.celsius)
   
        self.labelWeather.setText(data.condition.text)
        self.labelTemperature.setText(str(data.condition.temperature)+' Celcius')
    

        
       
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())

    
    