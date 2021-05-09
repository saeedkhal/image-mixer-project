

import numpy as np
from modesEnum import Modes


from scipy import fftpack, ndimage
import cv2




class imageClass:
    def __init__(self):
        self.fourier=[]
        self.image_arr=[]
        self.mag_arr=[]
        self.phase_arr=[]
        self.imaginary_arr=[]
        self.real=[]
    def fillByPath(self,filepath):
        self.image_arr=cv2.imread(filepath,cv2.IMREAD_GRAYSCALE)
        self.fourier=np.fft.fft2(self.image_arr)
        #fshift=np.fft.fftshift(fourier)
        self.mag_arr=(np.abs(self.fourier))
        self.phase_arr=np.angle(self.fourier)
        self.real_arr=np.real(self.fourier)
        self.imaginary_arr=np.imag(self.fourier)

    #this function for mixing the two images 

    def mixTwoImages(img1,img2,percentage_of_component1_image1,percentage_of_component2_image1,component1Enum,component2Enum):
        #the following mixing componant1= 0.9*real(img1)+(0.1)*real(img2)  >>0.1=1-0.9
        #                     componant2= 0.7*imaginary (img1)+(1-0.7)*imaginary(img2) 
        if(component1Enum==Modes.MagnitudeComponent and component2Enum==Modes.PhaseComponent):
            component1=percentage_of_component1_image1*img1.mag_arr+(1-percentage_of_component1_image1)*img2.mag_arr
            component2=percentage_of_component2_image1*img1.phase_arr+(1-percentage_of_component2_image1)*img2.phase_arr
        elif(component1Enum==Modes.MagnitudeComponent and component2Enum==Modes.Uni_Phase_Image_2):
            component1=percentage_of_component1_image1*img1.mag_arr+(1-percentage_of_component1_image1)*img2.mag_arr
            component2=np.zeros(img2.phase_arr)
        elif(component1Enum==Modes.MagnitudeComponent and component2Enum==Modes.Uni_Phase_Image_1):
            component1=percentage_of_component1_image1*img1.mag_arr+(1-percentage_of_component1_image1)*img2.mag_arr
            component2=np.zeros(img1.phase_arr)
        elif(component1Enum==Modes.PhaseComponent and component2Enum==Modes.MagnitudeComponent):
            component1=percentage_of_component2_image1*img1.mag_arr+(1-percentage_of_component2_image1)*img2.mag_arr
            component2=percentage_of_component1_image1*img1.phase_arr+(1-percentage_of_component1_image1)*img2.phase_arr
        elif(component1Enum==Modes.PhaseComponent and component2Enum==Modes.Uni_Magnitude_Image_1):
            component1=np.ones_like(img1.mag_arr)
            component2=percentage_of_component1_image1*img1.phase_arr+(1-percentage_of_component1_image1)*img2.phase_arr
        elif(component1Enum==Modes.PhaseComponent and component2Enum==Modes.Uni_Magnitude_Image_2):
            component1=np.ones_like(img2.mag_arr)
            component2=percentage_of_component1_image1*img1.phase_arr+(1-percentage_of_component1_image1)*img2.phase_arr
        elif(component1Enum==Modes.Uni_Magnitude_Image_1 and component2Enum==Modes.PhaseComponent):
            component1=np.ones_like(img1.mag_arr)
            component2=percentage_of_component2_image1*img1.phase_arr+(1-percentage_of_component2_image1)*img2.phase_arr
        elif((component1Enum==Modes.Uni_Magnitude_Image_1 and component2Enum==Modes.Uni_Phase_Image_1) or (component2Enum==Modes.Uni_Magnitude_Image_1 and component1Enum==Modes.Uni_Phase_Image_1)):
            component1=np.ones_like(img1.mag_arr)
            component2=np.zeros_like(img1.phase_arr)
        elif((component1Enum==Modes.Uni_Magnitude_Image_1 and component2Enum==Modes.Uni_Phase_Image_2) or (component2Enum==Modes.Uni_Magnitude_Image_1 and component1Enum==Modes.Uni_Phase_Image_2)):
            component1=np.ones_like(img1.mag_arr)
            component2=np.zeros_like(img2.phase_arr)
        elif((component1Enum==Modes.Uni_Magnitude_Image_2 and component2Enum==Modes.Uni_Phase_Image_2) or (component1Enum==Modes.Uni_Phase_Image_2 and component2Enum==Modes.Uni_Magnitude_Image_2)):
            component1=np.ones_like(img2.mag_arr)
            component2=np.zeros_like(img2.phase_arr)
        elif((component1Enum==Modes.Uni_Magnitude_Image_2 and component2Enum==Modes.Uni_Phase_Image_1) or (component2Enum==Modes.Uni_Magnitude_Image_2 and component1Enum==Modes.Uni_Phase_Image_1)):
            component1=np.ones_like(img2.mag_arr)
            component2=np.zeros_like(img1.phase_arr)
        elif(component1Enum==Modes.Uni_Magnitude_Image_2 and component2Enum==Modes.PhaseComponent):
            component1=np.ones_like(img2.mag_arr)
            component2=percentage_of_component2_image1*img1.phase_arr+(1-percentage_of_component2_image1)*img2.phase_arr
        elif(component1Enum==Modes.Uni_Phase_Image_1 and component2Enum==Modes.MagnitudeComponent):
            component1=percentage_of_component2_image1*img1.mag_arr+(1-percentage_of_component2_image1)*img2.mag_arr
            component2=np.zeros_like(img1.phase_arr)
        elif(component1Enum==Modes.Uni_Phase_Image_2 and component2Enum==Modes.MagnitudeComponent):
            component1=percentage_of_component2_image1*img1.mag_arr+(1-percentage_of_component2_image1)*img2.mag_arr
            component2=np.zeros_like(img2.phase_arr)
        elif(component1Enum==Modes.RealComponent):
            component1=percentage_of_component1_image1*img1.real_arr+(1-percentage_of_component1_image1)*img2.real_arr
            component2=percentage_of_component2_image1*img1.imaginary_arr+(1-percentage_of_component2_image1)*img2.imaginary_arr
        elif(component1Enum==Modes.ImagComponent):
            component1=percentage_of_component2_image1*img1.real_arr+(1-percentage_of_component2_image1)*img2.real_arr
            component2=percentage_of_component1_image1*img1.imaginary_arr+(1-percentage_of_component1_image1)*img2.imaginary_arr
       
        
        if(component1Enum==Modes.PhaseComponent or component1Enum==Modes.Uni_Magnitude_Image_2 or component1Enum==Modes.Uni_Magnitude_Image_1 or component1Enum ==Modes.MagnitudeComponent or component1Enum==Modes.Uni_Phase_Image_1 or component1Enum==Modes.Uni_Phase_Image_2):
            multiplying=np.multiply(component1,np.exp(1j*component2))
            output=(np.fft.ifft2(multiplying))
        else:
            output=np.fft.ifft2(np.add(component1,(1j*component2)))
        print(len(output))
        return output