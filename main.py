

from PyQt5.QtWidgets import QDialog, QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget 
from PyQt5 import QtWidgets, QtCore,QtGui
#from PyQt5 import uic
import sys
from PyQt5.uic import loadUi
import requests
import os # We need sys so that we can pass argv to QApplication
import pandas as pd

from pyqtgraph import PlotWidget, plot
import pyqtgraph as pg

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)

import numpy as np
import random
import xlsxwriter

    #methodes
import back_codes.lissage_expo_triple_vf as LissageholtWinters
from sklearn.metrics import mean_squared_error #calcul des erreurs
import back_codes.arima_function as Arima
import back_codes.lissage_simple_et_double_vf as lissage_simple_et_double


#centrer ecran
screen_center = lambda widget: QApplication.desktop().screen().rect().center()- widget.rect().center()
    #methode2
def centerWidgetOnScreen(widget):
    centerPoint = QtGui.QScreen.availableGeometry(QtWidgets.QApplication.primaryScreen()).center()
    fg = widget.frameGeometry()
    fg.moveCenter(centerPoint)
    widget.move(fg.topLeft())

    # evaluate forecasts
def erreur(données,predictions):
    rmse = sqrt(mean_squared_error(données, predictions))
    print('Test RMSE: %.3f' % rmse)


Type = {"T": "Temporelle",
        "C": "Causal"}
mType = {"Ad": 'additive',
         "Mu": 'multiplicative'}
Methodes = {
    "LS": "Lissage simple",
    "LD": "Lissage double",
    "LT": "Lissage triple",
    "LST": "LSTM",
    "RL": "Regression lineaire",
    "AR": "ARIMA" 
    }
Indices_méthodes = {
    "LS": 1,
    "LD": 2,
    "LT": 3,
    "RL": 4,
    "LST":5,
    "RP": 6,
    "AR": 7
    }
    
    
#initialisations
ListScreen = []
ListeEcrans = []
nb_screen = 0
Dict = {}
df = pd.read_csv('data\\sampledata.csv', usecols=[0], engine='python')
Data = {
    "TypeSerie": Type["C"],
    "ListeScreensEmpillés": ListScreen,
    "ListeEcrans": ListeEcrans,
    "nbScreen": nb_screen,
    "DictionnairesDesIndex": Dict,
    "DataFrame": df,
    "mType": mType['Ad'],
    "Dict_Methodes_Choisies": [1,2,3,7]
}



ListScreen = [1] #listes des number des ecrans en ordre!!!



def indexScreen(screenNumber):
    return Dict[screenNumber]
def goToScreen(widget,screenNumber):
    if screenNumber >8 and screenNumber!=13: widget.setFixedWidth(2.1*640);widget.setFixedHeight(1.5*480)
    else: widget.setFixedWidth(640);widget.setFixedHeight(480)
    widget.setCurrentIndex(indexScreen(screenNumber))
    widget.move(screen_center(widget))
    centerWidgetOnScreen(widget)
    ListScreen.append(screenNumber)
    print(ListScreen)
    print("On est passé à l'écran: ",screenNumber)
    if screenNumber==5:
        os.startfile("data\\excl.xlsx")
        print('''Data["TypeSerie"]''', Data["TypeSerie"])


def screenBackFrom(widget,screenNumber): #to screen
    NumberOfThescreenToLeft = ListScreen.pop()
    print(ListScreen)
    if NumberOfThescreenToLeft!= screenNumber: print("a huge pb")
    toScreen = ListScreen[-1]
    if toScreen >8: widget.setFixedWidth(2.1*640);widget.setFixedHeight(1.5*480)
    else: widget.setFixedWidth(640);widget.setFixedHeight(480)
    widget.move(screen_center(widget))
    centerWidgetOnScreen(widget)
    widget.setCurrentIndex(indexScreen(toScreen))
    #print(Data)



#def connectToScreen(screenNumber,buton,widget): #numero de l'écran; trouver le bouton dans le design; mettre le stackedWidget
 #   buton.clicked.connect(lambda x: goToScreen(widget, screenNumber))

def connectToScreen(buton,widget,screenToGONumber): #numero de l'écran; trouver le bouton dans le design; mettre le stackedWidget
    buton.clicked.connect(lambda x: goToScreen(widget, screenToGONumber))
def BackFromScreen(buton,widget,screenToLeftNumber): #numero de l'écran; trouver le bouton dans le design; mettre le stackedWidget
    buton.clicked.connect(lambda x: screenBackFrom(widget, screenToLeftNumber))










###########import into excel file
#exporter mles donnees dans une table excel
def to_excel(data): #data est une liste 
    workbook = xlsxwriter.Workbook()
    months = ('January', 'February', 'March',
             'April','May', 'June', 'July',
             'August', 'September', 'October',
             'November','December'
    )
    workbook = xlsxwriter.Workbook('C:\\Users\\SOS\\PycharmProjects\\pythonProject2\\data\\CreatedByCode.xlsx')
    ws       = workbook.add_worksheet()
    ws.write("A1", "Months")
    ws.write("B1", "Values")
    for i in range(len(data)):
        #Months
        ws.write("A{0}".format(i + 2), months[i % 12])
        #Data
        ws.write("B{0}".format(i + 2), data[i])
    workbook.close()
    
#exporter mles résulats dans une table excel
def to_excel_data(data): #data est une liste 
    workbook = xlsxwriter.Workbook()
    months = ('January', 'February', 'March',
             'April','May', 'June', 'July',
             'August', 'September', 'October',
             'November','December'
    )
    workbook = xlsxwriter.Workbook('C:\\Users\\SOS\\PycharmProjects\\pythonProject2\\data\\excl.xlsx')
    ws       = workbook.add_worksheet()
    ws.write("A1", "Months")
    ws.write("B1", "Values")
    for i in range(len(data)):
        #Months
        ws.write("A{0}".format(i + 2), months[i % 12])
        #Data
        ws.write("B{0}".format(i + 2), data[i])
    workbook.close()





def MAD(données, previsions):
    MAD  = 0
    n = min(len(données),len(previsions))
    for i in range (n):
        MAD+= abs(données[i]-previsions[i])
    return int(MAD)

#il retourbne le MSE et le RMSE 
    #il prends deux listes
def MSE(données, previsions):
    MSE  = 0
    n = min(len(données),len(previsions))
    for i in range (n):
        MSE+= abs((données[i]-previsions[i])**2)
    RMSE = np.sqrt(MSE)
    return int(MSE), int(RMSE/n)
        






class MainWindow(QDialog):

    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("files\\page1.ui",self)
        screenNumber = 3
        connectToScreen(self.pushButton, widget,screenNumber)

# class MainWindow(QDialog):

    # def __init__(self):
        # super(MainWindow,self).__init__()
        # loadUi("files\\page1.ui",self)
        # self.pushButton.clicked.connect(self.goToScreen3)

    # def goToScreen3(self):
        # screen3 = Screen3()
        # widget.addWidget(screen3)
        # widget.setCurrentIndex(widget.currentIndex()+1)
        # widget.setCurrentIndex(indexScreen(3))
# class MainWindow(QDialog):

    # def __init__(self):
        # super(MainWindow,self).__init__()
        # loadUi("files\\page1.ui",self)
        # self.pushButton.clicked.connect(self.goToScreen3)

    # def goToScreen3(self):
        # screen3 = Screen3()
        # widget.addWidget(screen3)
        # widget.setCurrentIndex(widget.currentIndex()+1)

class Screen2(QDialog):

    def __init__(self):
        super(Screen2,self).__init__()
        loadUi("files\\page2.ui",self)
        self.setWindowTitle("screen2")
        #print("screen2: ", widget.currentIndex())
        connectToScreen(self.pushButton, widget,screenToGONumber=3)


class Screen3(QDialog):
    def __init__(self):
        super(Screen3,self).__init__()
        loadUi("files\\page3.ui",self)
        self.setWindowTitle("screen3")
        #print("check= ", self.ChoixserieTemporelle.isChecked())
        #print("screen3: ", widget.currentIndex())
        BackFromScreen(self.retour, widget, screenToLeftNumber=3)
        #self.retour.clicked.connect(lambda x: print(self.ChoixserieTemporelle.isChecked()))
        self.openExcel.clicked.connect(lambda x: self.goToScreen5(widget))

    def goToScreen5(self,widget):
        isTemporel = self.ChoixserieTemporelle.isChecked()
        Data["TypeSerie"]= Type["T"] if isTemporel else Type["C"]
        print("toooooooooooooooooooooooooooooo")
        goToScreen(widget, screenNumber=5)






class Screen4(QDialog):
    def __init__(self):
        super(Screen4, self).__init__()
        self.setWindowTitle("screen4")
        loadUi("files\\page4.ui", self)
        connectToScreen(self.valider, widget,screenToGONumber=5)#self.pushButton.clicked.connect(self.goToScreen5)
        BackFromScreen(self.retour, widget, screenToLeftNumber=4)
        self.AfficherDonnées()
        #connectToScreen(self.valider, widget, screenToGONumber=41)
        

    def AfficherDonnées(self):
        Data["DataFrame"] = pd.read_csv('data\\sampledata.csv', usecols=[0], engine='python')
        
        print("Column headings:")
        print(Data["DataFrame"].columns)
        self.graphWidget = pg.PlotWidget()
        #self.setCentralWidget(self.graphWidget)

        hour = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
        temperature = [30, 32, 34, 32, 33, 31, 29, 32, 35, 45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)

class ScreenGraph41(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(ScreenGraph41, self).__init__(*args, **kwargs)

        self.graphWidget = pg.PlotWidget()
        self.setCentralWidget(self.graphWidget)

        hour = [1,2,3,4,5,6,7,8,9,10]
        temperature = [30,32,34,32,33,31,29,32,35,45]

        # plot data: x, y values
        self.graphWidget.plot(hour, temperature)

class Screen5(QDialog):
    def __init__(self):
        super(Screen5, self).__init__()
        loadUi("files\\page5.ui", self)
        self.setWindowTitle("screen5")
        self.enregistrer.clicked.connect(self.goToScreen)
        #connectToScreen(self.enregistrer, widget,screenToGONumber=6 if Data["TypeSerie"] == Type["T"] else 7)
        BackFromScreen(self.retour, widget, screenToLeftNumber=5)
        self.pushButton_generate_random_signal.setObjectName("pushButton_6")

        self.pushButton_generate_random_signal.clicked.connect(self.retrieve_Excel)
        
        self.navi_toolbar = NavigationToolbar(self.MplWidget.canvas, self) #mplwidget comme nom de.. dans le desiign
        self.navi_toolbar.setGeometry(QtCore.QRect(10, 10, 200, 100))

        self.myverticalLayout.addWidget(self.navi_toolbar)
        #self.myverticalLayout.setGeometry(QtCore.QRect(0, 130, 341, 251))
        #self.setLayout( self.myverticalLayout )
    def goToScreen(self):
        if Data["TypeSerie"] == Type["T"] :
            screenToGONumber = 6
        elif Data["TypeSerie"] == Type["C"] :
            screenToGONumber = 7
        else: screenToGONumber = 1
        goToScreen(widget, screenToGONumber)


    def retrieve_Excel(self):
        fichierEnregistré = True
        if fichierEnregistré == True:
            Array = Data["DataFrame"].values
            self.prevision()
    def prevision(self):
        DataFrame = Data['DataFrame']
        try:
            sdata = open('sampledata.csv')
        except:
            sdata = open('data\\sampledata.csv')
        tsA = sdata.read().split('\n')
        tsA = list(map(int, tsA))
        self.M = METHODES_DE_PREDICTION(Data['mType'],DataFrame)
        self.AfficherLissageTriple(self.M)
        
    def AfficherLissageTriple(self,M):
        toPlot,tsA,logs= self.M.LissageTriple()
       
        self.MplWidget.canvas.axes.clear()
        #self.MplWidget.canvas.axes.plot(toPlot)
        self.MplWidget.canvas.axes.plot(tsA)
        self.MplWidget.canvas.axes.legend(('prevision'), loc='upper right')
        self.MplWidget.canvas.axes.set_title('courbe de la prevision')
        self.MplWidget.canvas.draw()




    # def update_graph1(self):

        # fs = 500
        # f = random.randint(1, 100)
        # ts = 1/fs
        # length_of_signal = 100
        # t = np.linspace(0,1,length_of_signal)
        
        # cosinus_signal = np.cos(2*np.pi*f*t)
        # sinus_signal = np.sin(2*np.pi*f*t)

        # self.MplWidget.canvas.axes.clear()
        # self.MplWidget.canvas.axes.plot(t, cosinus_signal)
        # self.MplWidget.canvas.axes.plot(t, sinus_signal)
        # self.MplWidget.canvas.axes.legend(('cosinus', 'sinus'),loc='upper right')
        # self.MplWidget.canvas.axes.set_title('Cosinus - Sinus Signal')
        # self.MplWidget.canvas.draw()


#afficher la tendance obtenue dans l'hypothèse chronologique
class Screen6(QDialog):
    def __init__(self):
        super(Screen6, self).__init__()
        self.setWindowTitle("screen6")
        loadUi("files\\page6.ui", self)
        connectToScreen(self.continuer, widget, screenToGONumber=9)
        BackFromScreen(self.retour, widget, screenToLeftNumber=6)
        #self.afficher()
    #def afficher(self):
    #    df =

class Screen7(QDialog):
    def __init__(self):
        super(Screen7, self).__init__()
        self.setWindowTitle("screen7")
        loadUi("files\\page7.ui", self)
        connectToScreen(self.continuer, widget, screenToGONumber=8)
        BackFromScreen(self.retour_2, widget, screenToLeftNumber=7)
        #self.continuer.clicked.connect(self.goToScreen8)

class Screen8(QDialog):
    def __init__(self):
        super(Screen8, self).__init__()
        self.M = 0
        loadUi("files\\page8.ui", self)
        connectToScreen(self.continuer, widget, screenToGONumber=9)
        BackFromScreen(self.retour, widget, screenToLeftNumber=8)
class Screen9(QDialog):
    def __init__(self):
        super(Screen9, self).__init__()
        loadUi("files\\page9.ui", self)
        connectToScreen(self.AffinerPrevision, widget, screenToGONumber=13)
        connectToScreen(self.comparerMethodes, widget, screenToGONumber=13)
        connectToScreen(self.ChoisirMethode, widget, screenToGONumber=13)
        #connectToScreen(self.exporterResultats, widget, screenToGONumber=1)
        BackFromScreen(self.retour, widget, screenToLeftNumber=9)
        ###pour les courbes
        self.pushButton_generate_random_signal_2.setObjectName("pushButton_6")
        self.pushButton_generate_random_signal_2.clicked.connect(self.prevision)        
        
        
    def prevision(self):
        DataFrame = Data['DataFrame']
        try:
            sdata = open('data\\sampledata.csv')
        except:
            sdata = open('sampledata.csv')
            
        tsA = sdata.read().split('\n')
        tsA = list(map(int, tsA))
        #to_excel_data(tsA) #creer un fichier et mettre les donnees pour ke user. Il peut modifier
        self.M = METHODES_DE_PREDICTION(Data['mType'],DataFrame)
        self.AfficherLissageTriple(self.M)
        
    def AfficherLissageTriple(self,M):
        toPlot,tsA,logs= self.M.LissageTriple()
       
        self.MplWidget_2.canvas.axes.clear()
        self.MplWidget_2.canvas.axes.plot(toPlot)
        self.MplWidget_2.canvas.axes.plot(tsA)
        self.MplWidget_2.canvas.axes.legend(('prevision' 'realite'), loc='upper right')
        self.MplWidget_2.canvas.axes.set_title('courbe de la prevision')
        self.MplWidget_2.canvas.draw()


class Screen10(QDialog):
    def __init__(self):
        super(Screen10, self).__init__()
        self.M = 0
        loadUi("files\\page100.ui", self)
        BackFromScreen(self.retour, widget, screenToLeftNumber=10)
        # connectToScreen(self.parametres1, widget, screenToGONumber=13)
        # connectToScreen(self.parametres1, widget, screenToGONumber=14)
        # connectToScreen(self.parametres1, widget, screenToGONumber=15)
        # connectToScreen(self.parametres1, widget, screenToGONumber=16)
        self.afficher.setObjectName("pushButton_6")
        self.afficher.clicked.connect(self.prevision)
        self.ajuster1.clicked.connect(self.ajuster)
        self.ajuster2.clicked.connect(self.ajuster)
        self.ajuster3.clicked.connect(self.ajuster)
        self.ajuster4.clicked.connect(self.ajuster)
        

        self.progressBar.setValue(0)
    def ajuster(self):
        #vider les plot
        self.courbe1.canvas.axes.clear()
        self.courbe2.canvas.axes.clear()
        self.courbe3.canvas.axes.clear()
        self.courbe4.canvas.axes.clear()
        self.progressBar.setValue(0)
        self.afficher.setText("Rechargez les courbes")
        screenBackFrom(widget,screenNumber=10)
    def exporter(self,i,Liste_previsions):
        to_excel(Liste_previsions)
        
        
        ###pour les courbes
        ##self.prevision()
        #self.afficher.setObjectName("pushButton_6")
        #self.afficher.clicked.connect(self.prevision) 
        
    # def prevision(self):
        # DataFrame = Data['DataFrame']
        # self.M = METHODES_DE_PREDICTION(Data['mType'],DataFrame)
        # Array = DataFrame.values
        # self.AfficherLissageTriple(Array)
        
        # self.methode1(self.courbe1,Array) #lissage triple
        # self.methode2(self.courbe2,Array) #arima
        ##self.methode3(self.courbe3,Array)
        ##self.methode4(self.courbe4,Array)
    # def methode1(self,mplWidget,Array):
        # toPlot = self.M.LissageTriple()
        # toPlot = toPlot[0]
        # temps = Array[:,0]
        ##les demandes seront en position 1 dans le dataframe
        # demande = Array[:,1] #[30, 32, 34, 32, 33, 31, 29, 32, 35, 45]
        # mplWidget.canvas.axes.clear()
        # mplWidget.canvas.axes.plot(toPlot)
        # mplWidget.canvas.axes.plot(temps, demande)
        # mplWidget.canvas.axes.legend(('lissage triple prevision' 'realite'), loc='upper right')
        # mplWidget.canvas.axes.set_title('courbe de la prevision')
        # mplWidget.canvas.draw()
        ##calcul du mad
        # print("---------------------------------------------")
        # print("(len(demande)= ", len(demande))
        # print("len(toPlot) = ", len(toPlot))
    
    
    def prevision(self):
        DataFrame = Data['DataFrame']
        self.M = METHODES_DE_PREDICTION(Data['mType'])
        Array = DataFrame.values
        self.progressBar.setValue(0); 
        self.AfficherLissageTriple()
        self.progressBar.setValue(25);self.AfficherLissageSimple()
        self.progressBar.setValue(50);self.methode2(self.courbe2)
        self.progressBar.setValue(75);self.AfficherLissageDouble()
        self.progressBar.setValue(100)
        
        
    def AfficherLissageTriple(self):
        CoeffLissageSimplre = Data['Dict_Methodes_Choisies'][3]
        alpha = CoeffLissageSimplre[0]
        beta = CoeffLissageSimplre[1]
        beta = CoeffLissageSimplre[2]
        toPlot,tsA,logs= self.M.LissageTriple()
        #des tests
        print("---------------------------------")
        print("predictions triple: ",toPlot) #toPlot et tsA sont des listes  
        print("len = ",len(toPlot)) 
        print(len(tsA))#144
        n = min(len(tsA),len(toPlot))
        #les erreurs
        données, previsions = tsA, toPlot
        mad = MAD(données, previsions)
        mse, rmse = MSE(données, previsions)
        self.mad1.setText(str(mad))
        self.mse1.setText(str(mse))
        self.rmse1.setText(str(rmse))
        #les courbes
        self.courbe1.canvas.axes.clear()
        self.courbe1.canvas.axes.plot(toPlot,color='g', label='series')
        self.courbe1.canvas.axes.plot(tsA,color='r', label='result')
        self.courbe1.canvas.axes.legend(('prevision' 'realite'), loc='upper right')
        self.courbe1.canvas.axes.set_title('courbe de la prevision')
        self.courbe1.canvas.draw()
        self.exporter1.clicked.connect(lambda x: self.exporter(1,toPlot))
        
        ###calcul du mad
    def AfficherLissageSimple(self):
        CoeffLissageSimplre = Data['Dict_Methodes_Choisies'][1]
        alpha = CoeffLissageSimplre[0]
        toPlot,tsA,logs= self.M.LissageSimple(alpha)
        #to_excel_data(tsA)
        print("---------------------------------")
        print("predictions simple: ",toPlot)
        print("len = ",len(toPlot))
        print(len(tsA))
        #les erreurs
        données, previsions = tsA, toPlot
        mad = MAD(données, previsions)
        mse, rmse = MSE(données, previsions)
        self.mad3.setText(str(mad))
        self.mse3.setText(str(mse))
        self.rmse3.setText(str(rmse))
        #les courbes
        self.courbe3.canvas.axes.clear()
        self.courbe3.canvas.axes.plot(toPlot, color='g', label='series')
        self.courbe3.canvas.axes.plot(tsA, color='r', label='result')
        self.courbe3.canvas.axes.legend(('prevision' 'realite'), loc='upper right')
        self.courbe3.canvas.axes.set_title('prevision')
        # self.courbe3.canvas.axes.xlabel('period')
        # self.courbe3.canvas.axes.ylabel('demand')
        #self.courbe3.canvas.axes.set_title('courbe de la prevision')
        self.courbe3.canvas.draw()
        ###exporter
        self.exporter3.clicked.connect(lambda x: self.exporter(3,toPlot))
        

    def AfficherLissageDouble(self):
        CoeffLissageSimplre = Data['Dict_Methodes_Choisies'][2]
        alpha = CoeffLissageSimplre[0]
        beta = CoeffLissageSimplre[1]
        toPlot,tsA,logs= self.M.LissageDouble(alpha,beta)
        print("---------------------------------")
        print("predictions double: ",toPlot)
        print("len = ",len(toPlot))
        print(len(tsA))
        #les erreurs
        données, previsions = tsA, toPlot
        mad = MAD(données, previsions)
        mse, rmse = MSE(données, previsions)
        self.mad4.setText(str(mad))
        self.mse4.setText(str(mse))
        self.rmse4.setText(str(rmse))
        #les courbes
        self.courbe4.canvas.axes.clear()
        self.courbe4.canvas.axes.plot(toPlot, color='g', label='series')
        self.courbe4.canvas.axes.plot(tsA, color='r', label='result')
        self.courbe4.canvas.axes.legend(('prevision' 'realite'), loc='upper right')
        self.courbe4.canvas.axes.set_title('prevision')
        # self.courbe4.canvas.axes.xlabel('period')
        # self.courbe4.canvas.axes.ylabel('demand')
        #self.courbe4.canvas.axes.set_title('courbe de la prevision')
        self.courbe4.canvas.draw()
        ###exporter
        self.exporter4.clicked.connect(lambda x: self.exporter(4,toPlot))
        

        
        
        
    def methode2(self,mplWidget):
        tsA, predictions,Logs,rmse = self.M.ArimaMethod()
        print("---------------------------------")
        print("predictions arima3: ",predictions)
        print("len = ",len(predictions))
        print(len(tsA))
        #les erreurs
        données, previsions = tsA, predictions
        mad = MAD(données, previsions)
        mse, rmse = MSE(données, previsions)
        self.mad2.setText(str(mad))
        self.mse2.setText(str(mse))
        self.rmse2.setText(str(rmse))
        #les courbes
        mplWidget.canvas.axes.clear()
        mplWidget.canvas.axes.plot(predictions, color='r', label='result')
        mplWidget.canvas.axes.plot(tsA,color='g', label='series')
        mplWidget.canvas.axes.legend(('arima model' 'realite'), loc='upper right')
        mplWidget.canvas.axes.set_title('courbe de la prevision')
        mplWidget.canvas.draw()
        #exporter 
                
        self.exporter2.clicked.connect(lambda x: self.exporter(2,predictions))




class METHODES_DE_PREDICTION():
    def __init__(self,mtype = 'multiplicative',dataSet=None):
        self.mtype = mtype
        self.dataSet = 0
        self.tsA = [] #tsA comprte les demandes de dataSet sous forme d'une liste de shape = (n)
        #dataSet
        
        
    #cas temporel
    def LissageTriple(self,p=12, sp=4, ahead=24):
        try:
            sdata = open('data\\sampledata.csv')
        except:
            sdata = open('sampledata.csv')
        tsA = sdata.read().split('\n')
        tsA = list(map(int, tsA))
        #results = LissageholtWinters.holtWinters(dataSet, p=12, sp=4, ahead=24, mtype = 'multiplicative')
        results = LissageholtWinters.prediction_holtWinters(tsA, p=12, sp=4, ahead=24, mtype = self.mtype)
        Logs = []
        Logs.append(("TUNING: ", results['alpha'], results['beta'], results['gamma'], results['MSD']))
        Logs.append(("FINAL PARAMETERS: ", results['params']))
        Logs.append(("PREDICTED VALUES: ", results['predicted']))
        for log in Logs: print(log)
        return results['smoothed'],tsA, Logs #A plotter, Logs

    def LissageSimple(self,alpha):
        try:
            sdata = open('data\\sampledata.csv')
        except:
            sdata = open('sampledata.csv')
        tsA = sdata.read().split('\n')
        tsA = list(map(int, tsA))
        #results = LissageholtWinters.holtWinters(dataSet, p=12, sp=4, ahead=24, mtype = 'multiplicative')
        
        results = lissage_simple_et_double.single_exponential_smoothing(tsA,alpha)
        Logs = []
        #for log in Logs: print(log)
        return results,tsA, Logs #A plotter, Logs

    def LissageDouble(self,alpha,beta):
        try:
            sdata = open('data\\sampledata.csv')
        except:
            sdata = open('sampledata.csv')
        tsA = sdata.read().split('\n')
        tsA = list(map(int, tsA))
        #results = LissageholtWinters.holtWinters(dataSet, p=12, sp=4, ahead=24, mtype = 'multiplicative')
        
        results = lissage_simple_et_double.double_exponential_smoothing(tsA,alpha,beta)
        Logs = []
        #for log in Logs: print(log)
        return results,tsA, Logs #A plotter, Logs
        
    def ArimaMethod(self):
        try:
            sdata = open('data\\sampledata.csv')
        except:
            sdata = open('sampledata.csv')
        tsA = sdata.read().split('\n')
        tsA = list(map(int, tsA))
        predictions,rmse,tsA = Arima.prediction_arima(self.tsA) ##prediction et erreur quadratique
        
        ######logs
        Logs = []
        #Logs.append(('predicted=%f, expected=%f' % (yhat, obs)))
        #Logs.append(('Test RMSE: %.3f' % rmse))
        for log in Logs: print(log)
        
        #####mad
        mad = 0
        return tsA, predictions,Logs,rmse #A plotter, Logs, erreur quadratique

        self.sp.value()

class Screen11(QDialog):
    def __init__(self):
        super(Screen11, self).__init__()
        loadUi("files\\page11.ui", self)
        BackFromScreen(self.retour, widget, screenToLeftNumber=11)
        connectToScreen(self.parametresAvancees, widget, screenToGONumber=12)


Data['Dict_Methodes_Choisies'] = {1:[],2:[],3:[],7:[]}

class Screen12(QDialog):
    def __init__(self):
        super(Screen12, self).__init__()
        loadUi("files\\page12.ui", self)
        connectToScreen(self.retour, widget, screenToGONumber=11)
        BackFromScreen(self.retour, widget, screenToLeftNumber=12)
        
        
class Screen13(QDialog):
    def __init__(self):
        super(Screen13, self).__init__()
        loadUi("files\\page13.ui", self)
        BackFromScreen(self.retour, widget, screenToLeftNumber=13)
        self.envoyer.clicked.connect(lambda x: self.doIt(widget))
    def doIt(self,widget):
        self.setLissageSimple()
        self.setLissageDouble()
        self.setLissageTriple()
        #self.setLMTM(dict)
        #self.setMethodeArima()
        #self.setRegressionLineaire(dict)
        #self.setRegressionPolynomiale(dict)
        goToScreen(widget,screenNumber=10)
        
    def setLissageSimple(self):
        alpha = self.alpha1.value()
        Data['Dict_Methodes_Choisies'][1] = [alpha]
    def setLissageDouble(self):
        alpha = self.alpha2.value()
        beta = self.beta3.value()
        Data['Dict_Methodes_Choisies'][2] = [alpha,beta]
    def setLissageTriple(self):
        alpha = self.alpha3.value()
        beta = self.beta3.value()
        gamma = self.gamma3.value()
        Data['Dict_Methodes_Choisies'][3] = [alpha,beta,gamma]



app = QApplication(sys.argv)
widget = QtWidgets.QStackedWidget()


#def screens
mainWindow = MainWindow()
screen2 = Screen2()
screen3 = Screen3()
screen4 = Screen4()
screenGraph41 = ScreenGraph41()
screen5 = Screen5()
screen6 = Screen6()
screen7 = Screen7()
screen8 = Screen8()
screen9 = Screen9()
screen10 = Screen10()
screen11 = Screen11()
screen12 = Screen12()
screen13 = Screen13()


#ListeEcrans est une liste d'écrans associés à des nombres qui mle parlent bien
ListeEcrans = [(mainWindow,1),
               (screen2,2),
               (screen3,3),
               (screen4,4),
               (screenGraph41,41),
               (screen5,5),
               (screen6,6),
               (screen7,7),
               (screen8,8),
               (screen9,9),
               (screen13,13),
               (screen10,10),
               (screen11,11),
               (screen12,12)
               ]
Data["ListeEcrans"]=ListeEcrans
def findNumberFromScreen(screen):
    for screenn,num in ListeEcrans:
        if screenn ==screen: return num

print(findNumberFromScreen(mainWindow))
print(findNumberFromScreen(screen8))
print(findNumberFromScreen(screen12))
print(findNumberFromScreen(screen13))

#ce process permet de générer nouveau id
def process(id,Dict,number): #je choisis un nombre associé à chaque écran et le dictionnaire me retourne l'index assocé à chaque nombre
    id+=1; Dict[number]=id
    return id, Dict

#ce processsus permet de trouver l'index de chaque ecran. Ces index seront utilisés pour aller vers les écrans
def AddEm(ListeEcraans):
    Dict = {};index = -1
    for screen,number in ListeEcraans:
        widget.addWidget(screen)
        index,Dict = process(index,Dict,number)
    nb_screen = index+1
    return (nb_screen,Dict)

nb_screen,Dict = AddEm(ListeEcrans)

Data["nbScreen"]=nb_screen
Data["DictionnairesDesIndex"]=Dict

# index,Dict = process(index,Dict,1);  widget.addWidget(mainWindow)#0
# index,Dict = process(index,Dict,2); screen2 = Screen2()#1
# index,Dict = process(index,Dict,3); screen3 = Screen3()#2
# index,Dict = process(index,Dict,4); screen4 = Screen4() #indice3
# index,Dict = process(index,Dict,5); screen5 = Screen5() #indicde 4
# index,Dict = process(index,Dict,6); screen6 = Screen6() #5
# index,Dict = process(index,Dict,7); screen7 = Screen7() #6
# index,Dict = process(index,Dict,8); screen8 = Screen8() #6
# index,Dict = process(index,Dict,9); screen9 = Screen9()
# index,Dict = process(index,Dict,10); screen10 = Screen10()
# index,Dict = process(index,Dict,11); screen11 = Screen11()
# index,Dict = process(index,Dict,12); screen12 = Screen12()
# print (index)


print ("Dictionnaire qui contient la liste des écrans et leurs index: ",Dict)



#widget.setFixedWidth(640)
#widget.setFixedHeight(480)
widget.move(screen_center(widget))

widget.show()
app.exec_()
