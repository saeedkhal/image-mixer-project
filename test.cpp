
#include <iostream>
#include <iomanip>
#include <complex>
#include <cmath>
#include <valarray> /* val arrsy to easy making slice for the our arry */
extern "C"


using namespace std;

const double PI = 3.14159265359;
typedef std::complex<double> Complex;
typedef std::valarray<Complex> CArray;
extern "C"

void calcfft(CArray &samples)
{


    const size_t N = samples.size();

    if (N <= 1) {return;}

    // divide
    CArray even = samples[std::slice(0, N/2, 2)];
    CArray  odd = samples[std::slice(1, N/2, 2)];

    // conquer
    calcfft(even);
    calcfft(odd);

    // combine
    for (size_t k = 0; k < N/2; ++k)
    {
        Complex t = std::polar(1.0, -2 * PI * k / N) * odd[k];
        samples[k    ] =(even[k] + t);
        samples[k+N/2] = (even[k] - t);
    }
}
extern "C"








void fft (double sample_num,double *input,double *real_output,double*img_output){


    long vOut = (long)sample_num; //convert sample number to long long 
    Complex test[vOut];

    for (int i = 0; i < sample_num; ++i)
    {
        std::complex<double>sample= input[i]; //for convert everysamle to an complex 
        test[i]=sample;
        /* code */
    }

    CArray data(test, sample_num);
    // forward fft
    calcfft(data);

    for (int i = 0; i < sample_num; ++i)
    {
        real_output[i]=data[i].real();
        img_output[i]=data[i].imag();
    }

}
/*end  of  fast  fourer transform */


/*start of  discert fourer transform */
extern "C"

void dft (double numer_of_samples , double *input, double *real_output ,double *img_output ){
    complex<double> wn = exp(-2* 1/numer_of_samples * PI * 1i ); // Euler's formula




    for (int k = 0; k < numer_of_samples; ++k)
    {
    	for (int j = 0; j < numer_of_samples; ++j)
    	{
    		real_output[k]+=input[j]*real(exp(-2*PI*j*(k)*(1/numer_of_samples)*1i ));
    		img_output[k]+=input[j]*imag(exp(-2*PI*j*(k)*(1/numer_of_samples)*1i ));
    	}
    }

}






int main()
{

	double input[4] ={4.0,5.0,5.0,5.0};
	double real_output[4]={};
	double img_output[4]={};
	//fft(4,input,real_output,img_output); //this for calling fft 
    fft(4,input,real_output,img_output);
	for (int i = 0; i < 4; ++i)
	{
		cout<<std::fixed<<real_output[i]<<endl;
		cout<<std::fixed<<img_output[i]<<endl;
	}



}
