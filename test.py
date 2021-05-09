import ctypes
from numpy.ctypeslib import ndpointer
import numpy as np
import time
import matplotlib.pyplot as plt
import math






# validation test array
# list=[np.arange(0, 10, dtype=float),np.arange(0, 100, dtype=float),np.arange(0, 1000, dtype=float),np.arange(0, 10000, dtype=float),np.arange(0, 100000, dtype=float),np.arange(0, 1000000, dtype=float)]
list=[
        np.arange(0, math.pow(2, 3),dtype=float),
        np.arange(0, math.pow(2, 5),dtype=float),
        np.arange(0, math.pow(2, 7),dtype=float),
        np.arange(0, math.pow(2, 9),dtype=float),
        np.arange(0, math.pow(2, 11),dtype=float),
        np.arange(0, math.pow(2, 13),dtype=float)
    ]
# list=[np.arange(0,8, dtype=float),np.arange(0,16, dtype=float),np.arange(0,32, dtype=float),np.arange(0,64, dtype=float),np.arange(0,128, dtype=float)]



lib = ctypes.cdll.LoadLibrary("C:\\Users\\saeed khaled\\Desktop\\fucking dsp\\outputFile.so") #pass of the so file







# arrays
dft_data_arr=[]
fft_data_arr=[]

fun_dft = lib.dft
fun_fft = lib.fft
ft_arr=[fun_dft,fun_fft]

ft_time_arr=[]
fft_time_arr=[]

ft_names_arr=[">>  FT OUTPUT",">>>  FFT OUTPOT"]
bands_names_arr=["band1","band2","band3","band4","band5","band6"]


for i in range(0,2):

    print (ft_names_arr[i])
    for j in range(0,len(list)):
        print (bands_names_arr[j])

        ft_arr[i].restype = None
        ft_arr[i].argtypes = [ctypes.c_double,
                              ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                              ndpointer(ctypes.c_double, flags="C_CONTIGUOUS"),
                              ndpointer(ctypes.c_double, flags="C_CONTIGUOUS")
                              ]

        indata =list[j] #np.array([4.0, 5.0, 5.0, 5.0])
        real_output = np.zeros(indata.size)
        img_output = np.zeros(indata.size)

        #timing
        begin = time.time()

        ft_arr[i](indata.size,
                  indata,
                  real_output,
                  img_output
                  )

        time.sleep(1)
        # store end time
        end = time.time()
        diff=end - begin
        # total time taken
        print(f"Total runtime of the {bands_names_arr[j]} is {diff}")

        if i==0:
            ft_time_arr.append(diff)

        if i==1:
            fft_time_arr.append(diff)


        Data = real_output + 1j * img_output
        print("the out ", np.round(Data, decimals=1))
        print("-------")
        if i==0:
            dft_data_arr =Data
        elif i==1:
            fft_data_arr = Data




######## analysis

# printing entire arrays
print (">> entire FT array :")
print (dft_data_arr)
print (">> entire FFT array :")
print (fft_data_arr)
print ("///////")
diff=np.subtract(dft_data_arr,fft_data_arr)
print (">> the difference bettwen FT and  FFT is :")
print (diff)
print("////////")
error=np.abs(np.square(np.subtract(dft_data_arr,fft_data_arr)).mean())
print (">> Mean Square Error is :")
print (error)






############### time plotting

X = np.arange(1,len(list)+1)
y = ft_time_arr
z = fft_time_arr

# Plotting both the curves simultaneously
plt.plot(X, y, color='r', label='ft')
plt.plot(X, z, color='g', label='fft')

# Naming the x-axis, y-axis and the whole graph
plt.xlabel("Band")
plt.ylabel("Time")
plt.title("Time comparison")

# Adding legend, which helps us recognize the curve according to it's color
plt.legend()

# To load the display window
plt.show()








































