%        *2



%        ..........0 Degrees



%        *1



 

 

clear all


 

% some constants

% assume signal has been downconverted from 1000HMz to Baseband

% where a 1Mhz signal has been placed. sampling at 20MHz.

AngleOfSourceDeg = +5;    % 10 degrees - source direction Az

for im = -30:1:30,

    AngleOfSourceDeg = im;

 

NoiseStr = 0.1;

 

 

c = physconst('LightSpeed');        % sound light m/s

M = 2;                  % number of  elements ONLY 4 or 8 or 16

R = 0.005;              % Array dimension (distance between antennas)

CarrierFreq=1e9;    % 1GHz

SamplingFreq = 20e6;    % guessing what the sampling rate is: 20MHz

NumData = 1024;         % number of timeseries in simulated source

WidthofBeams=60;        % width of the beams (i.e. dont need to do 180deg)

FFTSize = 1024;   % FFT size

 

Fss = SamplingFreq;     %simulation of source sampling ADC

tss = 1/Fss;            % data simulator sampling time in sec

 

fd = 1e6;      % freq of Signal of Interest

Lamda = c/CarrierFreq;   % wavelength of Signal frequency

 

%R = sqrt((D/2)^2 + (D/2)^2); % Radius of the Circle

tsim = 0:tss:tss*(NumData-1);  % create a time series of NumData points

t=tsim;                     % simplify

w=2*pi*fd;                  % omega

   

 

 

ThetaIncremDeg = 5; % angle increements around the array for steering vector

 

%%%%%%%%%%%%%%%%%%

% now make steering Matrix for 10 angles (or 10 possible sources)!

%

% Build A - correlator Array in case

% test for the following angles

ThetaIncremRad = (ThetaIncremDeg)*pi/180; %Rad

ThetaWidth = WidthofBeams*pi/180;

ThetaA = -ThetaWidth:ThetaIncremRad:ThetaWidth; % range of angles

NumAngles = length(ThetaA);


A = ones(M,NumAngles);

% M = number of elements (antennas)
Phi = zeros(1,2);
Phi(1) = pi/2;
Phi(2) = -pi/2;
 

%%%%%%%%%%%%%%%%%%%

% Steering Matrix A

% NOTE WE WILL NEED TO RECALCULATE STEERING MATRIX

% IF WE DO ANOTHER FREQ OTHER THAN fd

for ii=1:NumAngles,

    for i=1:M,

        mua=2*pi*R*cos(ThetaA(ii)+Phi(i))/Lamda;

        A(i,ii)=exp(-1i*mua);

    end;

end;

   

% now make steering vector for the AngleOfSource only (to make our

% simulated data)

AngleOfSourceRad = (AngleOfSourceDeg)*pi/180; %Rad

 

for i=1:M,

    mua=2*pi*R*cos(AngleOfSourceRad-Phi(i))/Lamda;

    Asource(i)=exp(-1i*mua);

end;

 

 

%%%%%%%%%%%%%%%%%%

   

% Making data

% to make a sine wave from exponential -= exp(i*2*pi*freq*tau*numb0toN)

% +0.001*(randn(size(nn))+1i*randn(size(nn)))

nn = [0:NumData-1];

y=exp(1i*2*pi*fd*tss*nn);

y1 = (y.*Asource(1))+NoiseStr*(randn(size(nn))+1i*randn(size(nn))); %.*hann(NumData);

y2 = (y.*Asource(2))+NoiseStr*(randn(size(nn))+1i*randn(size(nn))); %.*hann(NumData);


 

% Now get data from the source at each Antenna

Xx=zeros(M,NumData);        % Prime the data Matrix (4 antennas of Data)

Xf = zeros(M, FFTSize);     % Prime the Matrix of FFTs

 

% relative to M=1 element

%

K=FFTSize;

y=zeros(M, FFTSize);

 

Xf(1,:) = fft(y1(1:FFTSize).*hann(1024)', FFTSize); % do FFT for the Antenna

Xf(2,:) = fft(y2(1:FFTSize).*hann(1024)', FFTSize); % do FFT for the Antenna



 





 

% Find Freq closest to fd in the FFTs (integer arithmetic to find

% index)

% find the Freq closest to fd

fi=0:Fss/(FFTSize-1):Fss/2;

dist    = abs(fi - fd);

minDist = min(dist);

fidx     = find(dist == minDist);

 

% find the signal value at the frequency point

for i=1:M

    Xs(i)=Xf(i,fidx);

end

 

% Plot raw signal (1MHz signal)



% Plot FFT





 


 

 

% POWER CALCULATION

% Get Power for each steering angle of the data.

P=zeros(1,NumAngles);

Rxx = conj(Xs)'*Xs;

for i=1:NumAngles,

    P(i) = conj(A(:,i))'*Rxx*(A(:,i));

end; %i

 

% estimating the angle

 

 

figure(3)

plot(ThetaA*180/pi,10*log10(abs(P)/max(abs(P)))), title('Relative Power Curve vs Angle')

hold on; plot(AngleOfSourceDeg, (max(10*log10(abs(P)/max(abs(P))))), 'r*', 'MarkerSize', 18);

 

xlabel('Angle deg')

grid on

hold off

 

end;