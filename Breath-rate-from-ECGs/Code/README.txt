README

The attached Python file contains programs written by Hespera 
Henzell to complete the COMP90072 Respiratory Rates project,
as well as some examples of the programs in use.

Together, with these programs you can:
- read an ECG
- graph an ECG
- find the time the heart beats (the  time of the R-peak)
- find the RR-interval
- graph the RR-interval
- estimate the breath frequency from the RR interval
- perform a FFT on an ECG and graph the segments of the ECG
  where we expect the heartbeat and breath frequency
- do the above with a spectrogram of the ECG

These programs were written with the ultimate aims of:
- finding the R-peaks in an ECG
- estimating the breathing frequency from the RR-interval
- finding a segment of the ECG where we can see the
  breathing frequency in the FFT

Most of the programs in this file depend on others to operate. It is 
important to run all the code before a program to guarantee it will
work.

All the programs written use a common set of parameters and variables:

--------------------------------------------------------------------
Parameters and Variables
--------------------------------------------------------------------
record     name of the record (as a string)
offset     time of recording (seconds) to start reading the data
seconds    number of seconds of the ECG we wish to save
ecg        a segment of an ECG read into a useable form by ecg_r
sig        same as ecg - used for FFTs
freq       frequency of record (Hz)
time_step  1/freq, or number of seconds per reading
byte       number of  bytes reading in ECG is stored in
AD         A/D units per mV in record
--------------------------------------------------------------------
--------------------------------------------------------------------
Data
--------------------------------------------------------------------
The data is ECG recordings taken to detect sleep apnea, made freely
available on PhysioNet for the CinC Challenge 2000.

The following programs run on the .dat files available in the database.
To run these programs, please download the .dat files from the
database and place them in the directory structure listed below.

The dataset is described in: 
T Penzel, GB Moody, RG Mark, AL Goldberger, JH Peter. 
The Apnea-ECG Database. Computers in Cardiology 2000;27:255-258. 

The dataset is held in the PhysioNet Database, the citation for which
is:
Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, 
Mietus JE, Moody GB, Peng C-K, Stanley HE. PhysioBank, PhysioToolkit, 
and PhysioNet: Components of a New Research Resource for Complex 
Physiologic Signals. Circulation 101(23):e215-e220 [Circulation 
Electronic Pages; http://circ.ahajournals.org/content/101/23/e215.full];
 2000 (June 13). 

--------------------------------------------------------------------
Directory Structure
--------------------------------------------------------------------
These programs assume the .dat files is in the folder "data".
ie. the path for a01.dat is "data/a01.dat".

--------------------------------------------------------------------
Programs
--------------------------------------------------------------------
READING AND GRAPHING THE DATA

ecg_r: 
Reads a segment of the ECGs in the .dat files into Python, and converts 
them from
binary to integers.

ecg_g:
graphs the segments of the ECGs read by ecg_r 


FINDING THE HEARTBEATS/ R PEAKS

peak_find:
when triggered, finds a local maximum and decides whether it is an R peak
based on width

find_threshold:
sets an initial threshold to start finding peaks above

heartbeat_vector:
reads a segment of an ecg with ecg_r, and finds peaks with peak_find when
the ecg reaches a certain threshold (initially set by find_threshold, then
updated)

test_ecg:
plots R-peaks found with heartbeat_vector over the segment of the ECG
it was given to check heartbeat_vector's performance


ROUGHLY ESTIMATING THE BREATH RATE FROM THE RR-INTERVAL

RR_int:
finds the RR-interval from the R-peaks given by heartbeat_vector, and the
time the interval occurs at (taken mid-interval)

RR_int_g:
plots the intervals vs. the time they occur at found by RR_int

pbf:
estimates the breathing frequency from RR_int and plots the intervals


PERFORMING A FAST FOURIER TRANSFORM TO FIND BREATH RATE

fft_g:
performs an FFT on a segment of the ECG read by ecg_r, and graphs the 
frequencies we expect the heartbeat and breathing frequency at

fft_spect_g:
does the same as fft_g, and additionally plots a spectrogram of the 
segment of ECG the FFT is take from
