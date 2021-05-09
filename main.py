from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox
import sys
import numpy as np
from PIL import Image
from task3 import Ui_MainWindow
import pyqtgraph as pg
from scipy import fftpack, ndimage
import cv2
from imageModel import imageClass
from modesEnum import Modes

from matplotlib import pyplot as plt

import logging
logging.basicConfig(filename="usertracing",level=logging.INFO)



class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(ApplicationWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.img_graphics_arr=[self.ui.image1_graphicsView,self.ui.image1_graphicsView_2]
        self.component_graphics_arr=[self.ui.components_graphicsView,self.ui.components_graphicsView2]
        self.combobox_arr=[self.ui.comboBox_img1,self.ui.comboBox_img2]
        image1=imageClass()
        image2=imageClass()
        self.image_arr=[image1,image2]
        self.ui.showImage_button.clicked.connect(self.browse1)
        self.ui.showImage2_button.clicked.connect(self.browse2)
        self.ui.applyChanges_Button.clicked.connect(self.mix_images)
        self.ui.comboBox_img1.currentTextChanged.connect(self.viewcomponents1)
        self.ui.comboBox_img2.currentTextChanged.connect(self.viewcomponents2)


    def browse1(self):
        self.Browse(0)
    def browse2(self):
        self.Browse(1)
    def viewcomponents1(self):
        self.showComponents(0)
    def viewcomponents2(self):
        self.showComponents(1)

    def mix_images(self):
        component1Enum=None
        component2Enum=None
        percentage_of_component1_image1=0.0
        percentage_of_component2_image1=0.0
        outputText=self.ui.comboBox_output.currentText()
        component1ComponentText=self.ui.component1_component_comboBox.currentText() 
        component1ImageText=self.ui.component1_image_comboBox.currentText()
        component2ComponentText=self.ui.component2_component_comboBox.currentText()
        component2ImageText=self.ui.component2_image_comboBox.currentText()
        if(outputText=="Choose output 1 or 2" or component1ComponentText=="choose component" or component1ImageText=="Choose image 1 or 2" or component2ComponentText=="choose component" or component2ImageText=="Choose image 1 or 2" ):
            self.show_popup("fill all comboboxes")
            return
        if((component1ComponentText=="Magnitude" and component2ComponentText != "Phase") and (component1ComponentText=="Magnitude" and component2ComponentText != "Uni_Phase") ):
            self.show_popup("you cannot mix by these components")
            return
        elif((component1ComponentText=="Phase" and component2ComponentText !="Magnitude") and (component1ComponentText=="Phase" and component2ComponentText !="Uni_Mag")):
            self.show_popup("you cannot mix by these components")
            return
        elif((component1ComponentText=="Uni_Mag" and component2ComponentText !="Phase") and (component1ComponentText=="Uni_Mag" and component2ComponentText !="Uni_Phase")):
            self.show_popup("you cannot mix by these components")
            return
        elif((component1ComponentText=="Uni_Phase" and component2ComponentText !="Magnitude") and (component1ComponentText=="Uni_Phase" and component2ComponentText !="Uni_Mag")):
            self.show_popup("you cannot mix by these components")
            return
        if(component1ComponentText=="Real" and component2ComponentText != "Imag"):
            self.show_popup("you cannot mix by these components")
            return
        elif(component1ComponentText=="Imag" and component2ComponentText !="Real"):
            self.show_popup("you cannot mix by these components")
            return

        if(component1ComponentText=="Magnitude"):
            component1Enum=Modes.MagnitudeComponent
        elif(component1ComponentText=="Phase"):
            component1Enum=Modes.PhaseComponent
        elif(component1ComponentText=="Real"):
            component1Enum=Modes.RealComponent
        elif(component1ComponentText=="Imag"):
            component1Enum=Modes.ImagComponent
       
        if(component2ComponentText=="Magnitude"):
            component2Enum=Modes.MagnitudeComponent
        elif(component2ComponentText=="Phase"):
            component2Enum=Modes.PhaseComponent
        elif(component2ComponentText=="Real"):
            component2Enum=Modes.RealComponent
        elif(component2ComponentText=="Imag"):
            component2Enum=Modes.ImagComponent   
        if(component1ImageText=="Image1"):
            percentage_of_component1_image1=self.ui.component1_Percentage.value()*0.01
            if(component1ComponentText=="Uni_Mag"):
                component1Enum=Modes.Uni_Magnitude_Image_1
            elif(component1ComponentText=="Uni_Phase"):
                component1Enum=Modes.Uni_Phase_Image_1
        else:
            percentage_of_component1_image1=(100-self.ui.component1_Percentage.value())*0.01
            if(component1ComponentText=="Uni_Mag"):
                component1Enum=Modes.Uni_Magnitude_Image_2
            elif(component1ComponentText=="Uni_Phase"):
                component1Enum=Modes.Uni_Phase_Image_2
        if(component2ImageText=="Image1"):
            percentage_of_component2_image1=self.ui.component2_Percentage.value()*0.01
            if(component2ComponentText=="Uni_Mag"):
                component2Enum=Modes.Uni_Magnitude_Image_1
            elif(component2ComponentText=="Uni_Phase"):
                component2Enum=Modes.Uni_Phase_Image_1
        else:
            percentage_of_component2_image1=(100-self.ui.component2_Percentage.value())*0.01
            if(component2ComponentText=="Uni_Mag"):
                component2Enum=Modes.Uni_Magnitude_Image_2
            elif(component2ComponentText=="Uni_Phase"):
                component2Enum=Modes.Uni_Phase_Image_2
        logging.info("Components for mixing are : " + component1ComponentText + " , " + component2ComponentText)
        output=imageClass.mixTwoImages(self.image_arr[0],self.image_arr[1],percentage_of_component1_image1,percentage_of_component2_image1,component1Enum,component2Enum)
        image=pg.ImageItem(output)
        image.rotate(270)
        if(outputText=="Output1"):
            logging.info("user chose mixture to be shown in Output1 window")
            self.ui.output1_graphicsView.clear()
            self.ui.output1_graphicsView.addItem(image)
        elif(outputText=="Output2"):
            logging.info("user chose mixture to be shown in Output2 window")
            self.ui.output2_graphicsView.clear()
            self.ui.output2_graphicsView.addItem(image)

    def show_popup(self,string):
        message= QMessageBox()
        logging.warning(string)
        message.setWindowTitle("Task3 Error Message")
        message.setText(string)
        #message.setIcon(QMessageBox.critical)
        x=message.exec_()

    def Pressed(self):
        
        print(self.ui.comboBox_img1.currentText())

    def Browse(self,i):
        self.img_graphics_arr[i].clear()
        filepath=None
        filepath= QtWidgets.QFileDialog.getOpenFileName()   
        if(filepath==('', '')):
            if(i==0):
                logging.warning("user didn't choose an image for window 1")
            elif(i==1):                
                logging.warning("user didn't choose an image for window 2") 
            return
        if(i==0):
            logging.info("user chose image for window 1")
        elif(i==1):
            logging.info("user chose image for window 2")
        self.image_arr[i].fillByPath(filepath[0])
        if(len(self.image_arr[0].image_arr)==len(self.image_arr[1].image_arr) or len(self.image_arr[0].image_arr)==0 or len(self.image_arr[1].image_arr)==0 ):
            print(len(self.image_arr[i].image_arr))
            imgItem=pg.ImageItem(self.image_arr[i].image_arr)
            imgItem.rotate(270)
            self.img_graphics_arr[i].addItem(imgItem)
            
        else:
            self.image_arr[i].image_arr=[]
            self.show_popup("browse an image of the same size")
            return

    def showComponents(self,i):
        self.component_graphics_arr[i].clear()
        text=self.combobox_arr[i].currentText()
        if(len(self.image_arr[i].image_arr)==0):
            self.show_popup("Choose image first")
            return
        print(text)
        if(text=="choose component"):
            return
        elif(text=="Phase"):
            phase_image=pg.ImageItem(self.image_arr[i].phase_arr)
            phase_image.rotate(270)
            self.component_graphics_arr[i].addItem(phase_image)
        elif(text=="Magnitude"):
            magnitude_image=pg.ImageItem(20*np.log(self.image_arr[i].mag_arr))
            magnitude_image.rotate(270)
            self.component_graphics_arr[i].addItem(magnitude_image)
        elif(text=="Real"):
            real_image=pg.ImageItem(self.image_arr[i].real_arr)
            real_image.rotate(270)
            self.component_graphics_arr[i].addItem(real_image)
        elif(text=="Imag"):
            imag_image=pg.ImageItem(self.image_arr[i].imaginary_arr)
            imag_image.rotate(270)
            self.component_graphics_arr[i].addItem(imag_image)

def main():
    app = QtWidgets.QApplication(sys.argv)
    application = ApplicationWindow()
    application.show()
    app.exec_()


if __name__ == "__main__":
    main()
