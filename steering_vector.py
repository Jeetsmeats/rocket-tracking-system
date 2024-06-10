import math
import numpy as np
import cmath

# constants
c = 299792458
M = 2
D = 0.010
CarrierFreq=1e9
SamplingFreq = 10e6
NumData = 1024
WidthofBeams=60
FFTSize = 1024
Fss = SamplingFreq
tss = 1/Fss
fd = 1e6
Lamda = c/CarrierFreq
R = math.sqrt((D/2)**2 + (D/2)**2)
ThetaIncremDeg = 5
ThetaIncremRad = (ThetaIncremDeg)*math.pi/180
ThetaWidth = WidthofBeams*math.pi/180
ThetaA = [num*ThetaIncremRad for num in range(int(-ThetaWidth/ThetaIncremRad), int(ThetaWidth/ThetaIncremRad+1))]
NumAngles = len(ThetaA)

Phi = [-math.pi/2, math.pi/2]
A = np.zeros((M, NumAngles), dtype=complex)

# create steering matrix
for i in range(NumAngles):
    for j in range(M):
        mua=2*math.pi*R*math.cos(ThetaA[i]-Phi[j])/Lamda
        A[j, i]=cmath.exp(1j*mua)

# to do:
# multiply your data (buff) by a hanning window (length = NumDataPoints). Take FFT of the result
# out of the 1024 frequency points in the FFT, find frequency closest to the signal generator output
# grab the FFT complex value (not magnitude) of the two HackRFs at that frequency
# follow the "POWER CALCULATION" steps in len's script
