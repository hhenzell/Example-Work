
##-------------------------------------------------------------##
##              Art of Scientific Computing                    ##
##   Respiratory Rate Determination by Non-Invasive Means      ##
##                   Final Report Code                         ##
##            Student: Hespera Henzell                         ##
##-------------------------------------------------------------##
##                                                             ##
##  This file contains all the programs written to read the    ##
##  ECGs, find the heartbeat, find the RR-interval,            ##
##  estimate the breath rate and find the signal for the       ##
##  breath rate in the FFT                                     ##
##-------------------------------------------------------------##

from scipy import fft
from scipy import signal
import numpy as np
import matplotlib.pyplot as plt
from datetime import timedelta
import statistics

##-------------------------------------------------------------##
##                        Parameters                           ##
##-------------------------------------------------------------##
## All programs only use parameters from this list:            ##
## Record: name of the record (as a string)                    ##
## Offset: time of recording (seconds) to start reading the    ##
##         data                                                ##
## Seconds: number of seconds of the ECG we wish to record     ##
## ecg: a segment of an ECG read into a usuable form by        ##
##      program ecg_r                                          ##
##-------------------------------------------------------------##

##-------------------------------------------------------------##
##                        Programs                             ##
##-------------------------------------------------------------##

## ecg_r reads a segment of the 16 bit, two's complement binary data 
## into a list of intergers

def ecg_r(record, offset, seconds):
    filepath = "data/" + record + ".dat"
    freq = 100               #frequency of record (Hz)
    byte = 2                 #bytes of data each number is stored in
    AD   = 200               #A/D units per mV
    points = seconds * freq  #number of datapoints to read
    ecg=[]
    with open(filepath, "rb") as f:
        f.seek(offset * freq * byte)
        for i in range(0,points):
            b=f.read(byte)
            ecg.append(int.from_bytes(b, byteorder='little', signed=True)/AD)
    return(ecg)

## ecg_g will plot the ecg using ecg_r


def ecg_g(record, offset, seconds):    
    y=ecg_r(record, offset, seconds)
    x=[]
    for i in range(1, len(y)+1):
         x.append(i/100)
    
    # plotting record:
    width = 12           # this worked well for viewing on my computer 
    height= 3.5
    plt.figure(figsize=(width, height))        
    plt.plot(x,y, 'firebrick')
    plt.xlabel('Time(sec) from start')
    plt.ylabel('Voltage(mV)')
    time = timedelta(seconds = offset)
    plt.title("ECG from record "+record+" starting at "+str(time)+' (hr:min:sec)')


## Example of ecg_g
ecg_g("a01",0,60)


## peak_find find a local maximum and tests whether it is a R peak based on its width.
## If peak find runs into an index error it will not register a peak

def peak_find(ecg, i, threshold):
    c=0   #set a counter to 0
    height=threshold
    
    # Find peak:
    while c<5:
    # This loop stops when we get 
    # 5 numbers lower than our current maximum
        try:
            if ecg[i]>height:
                height =ecg[i]
                time   =i
            else:
                c+=1
            i+=1
        except IndexError:
            return("Not Peak")
        
    # Find width of peak (by moving down the left and right side until we are below
    # half the height of the peak):
    left  = time-1
    right = time+1
    try:
        while (ecg[left]>height/2):
            left  = left-1
        while (ecg[right]>height/2):
            right = right+1
        width = right - left
    except IndexError:
        return("Not Peak")
    
    # Use width to decide whether we are in a peak:
    if width<8:
        return(time)
    else:
        return("Not Peak")


## find_threshold decides what initial threshold we should start looking for R peaks at

def find_threshold(ecg):
    freq = 100
    if len(ecg) > freq*10:
        ecg = ecg[0 : freq*10]  #take first 10 seconds of ecg if possible
    else:
        ecg = ecg               #take the whole ecg if there's less than 10 seconds
    
    # set threshold halway between the maximum and mean value:
    upper=max(ecg)
    mean =statistics.mean(ecg)
    threshold = mean + abs(upper-mean)*0.5
    return threshold


## Given an ecg recording, heartbeat_vector returns a vector of R-peak times

def heartbeat_vector(ecg):
    threshold=find_threshold(ecg)
    freq = 100    #frequency of record (Hz)
    i=0
    
    # Find peaks:
    peaks=[]
    while i < len(ecg):
        if ecg[i] > threshold:          
            peak = peak_find(ecg, i, threshold)
            if peak == "Not Peak":
                i+=10   #skip ahead 0.1 seconds to get out of the T-wave
            else:
                peaks.append(peak/freq)
                i= peak + 20 #skip ahead 0.2 of a second
                if i > 500:
                    threshold = 0.65*ecg[peak]

        else:
            i+=1
    return(peaks)


## test_ecg plots the ecg overlaid with peaks found with peak_find

def test_ecg(record, offset, seconds):
    
    ecg   = ecg_r(record, offset, seconds)
    peaks = heartbeat_vector(ecg)
        
    ecg_g(record, offset, seconds)
    for i in peaks:
        plt.axvline(i, 0, 1, ls="--")
    plt.show()


## Example of test_ecg on a segment with high T-waves
test_ecg("b02", 10, 10)


## RR_int finds the RR_interval and the time it occurs

def RR_int(record, offset, seconds):
    ecg = ecg_r(record, offset, seconds)
    beats = heartbeat_vector(ecg)
    RR_int = []
    times = []
    for i in range(1, len(beats)):
            interval = round(beats[i] - beats[i-1], 4) #RR-interval
            time = beats[i-1] + 0.5* interval  #time interval occurs (taken mid-interval)
            RR_int.append(interval)
            times.append(time)
    return(RR_int,times)



## RR_int_g graphs the RR-interval

def RR_int_g(record, offset, seconds):
    
    beats, times = RR_int(record, offset, seconds)
    plt.plot(times, beats,'k+')
    plt.ylim(0, max(beats)+0.05)
    plt.xlabel("Time(seconds) (at middle of interval)")
    plt.ylabel("Interval length (seconds)")
    plt.title("Interval between heartbeats from "+ str(offset)+ " seconds for " + record)
    plt.show()


## Example of RR_int_g
RR_int_g("c01",1800,20)


## pbf predicts breathing frequency from the RR-interval and graphs the RR-interval

def pbf(record, offset, seconds):
    #Find RR-interval:
    beats = RR_int(record, offset, seconds)
    beats, times = RR_int(record, offset, seconds)
    
    #Plot RR-interval:
    plt.plot(times, beats,'k+')
    plt.xlabel("Time(seconds) (at middle of interval)")
    plt.ylabel("Interval length (seconds)")
    plt.title("Interval between heartbeats from "+ str(offset)+ " seconds for " + record)
    plt.show()
    
    #Calculate breathing frequency:
    breaths = len(signal.find_peaks(beats)[0])
    breath_freq = round(breaths/seconds, 2)
    print("Predicted breathing frequency is " + str(breath_freq) + " Hz \n")


## Example of pbf
pbf("c06",3600,400)


## fft_g performs a fast fourier transform of a segment of the ecg
## and graphs the frequencies of the signal where we expect
## the heartbeat and breathing frequency"


def fft_g(record, offset, seconds):
    
    sig = ecg_r(record, offset, seconds)
    
    ## Perform FFT
    sig_fft = fft.fft(sig)
    power = np.abs(sig_fft)    #Remove complex values from the FFT
    freq = 100                 #frequency of record (Hz)
    time_step = 1/freq
    sample_freq = fft.fftfreq(len(sig), d=time_step)
    
    #Plot 1 - shows heart rate
    FFT, (ax1, ax2) = plt.subplots(1, 2, sharey=True)  
    ax1.plot(sample_freq, power)
    ax1.set_xlim(0,1.5)
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('power')
    ax1.set_title("Heart rate frequencies")
    
    #Plot 2 - shows breath rate
    ax2.plot(sample_freq, power)
    ax2.set_xlim(0,0.4)
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_title("Breath rate frequencies")
    
    FFT.suptitle("FFT from " + record +". Offset:" + str(offset) +"s, Duration: " + str(seconds) + "s")


#Example of pbf and fft_g for a segment of data with noise

record, offset, seconds = "c02",2000,4888

pbf(record, offset, seconds)
fft_g(record, offset, seconds)


#Example of pbf and fft_g for a segment of data without noise

record, offset, seconds = "c03",4600,400

pbf(record, offset, seconds)
fft_g(record, offset, seconds)


## fft_spect_g of fast fourier transform of a segment of the ecg,
## graphs the frequencies where we expect the heartbeat and breath rate
## and creates a spectrogram of the signal"


def fft_spect_g(record, offset, seconds):
    
    sig = ecg_r(record, offset, seconds)
    
    ## Perform FFT
    sig_fft = fft.fft(sig)
    power = np.abs(sig_fft)    #Remove complex values from the FFT
    freq = 100                 #frequency of record (Hz)
    time_step = 1/freq
    sample_freq = fft.fftfreq(len(sig), d=time_step)
    
   #Plot 1 - shows heart rate
    FFT, (ax1, ax2) = plt.subplots(1, 2, sharey=True)  
    ax1.plot(sample_freq, power)
    ax1.set_xlim(0,1.5)
    ax1.set_xlabel('Frequency [Hz]')
    ax1.set_ylabel('power')
    ax1.set_title("Heart rate frequencies")
    
    #Plot 2 - shows breath rate
    ax2.plot(sample_freq, power)
    ax2.set_xlim(0,0.4)
    ax2.set_xlabel('Frequency [Hz]')
    ax2.set_title("Breath rate frequencies")
    
    FFT.suptitle("FFT from " + record +". Offset:" + str(offset) +"s, Duration: " + str(seconds) + "s")
    
    # create Spectrogram and plot it
    freqs, times, spectrogram = signal.spectrogram(np.array(sig), fs = time_step)
    
    plt.figure(figsize=(5, 4))
    plt.imshow(spectrogram, aspect='auto', cmap='hot_r', origin='lower')
    plt.title('Spectrogram')
    plt.ylabel('Frequency band')
    plt.xlabel('Time window')
    plt.show()



#Example of fft_spect_g on a segment of data with noise
fft_spect_g("c03",4600, 600)





