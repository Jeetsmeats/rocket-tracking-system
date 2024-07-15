% Demo of FD Beamformer

% Demo of Freq Domain DOA

% using a uniform linear array

% SPECIFIC FREQ VERSION

%

% Len Sciacca

%

% Circular Array M elements (4, 8, 16)

%

%    *2      *1

%

%        ..........0 Degrees

%

%    *3      *4

%

% The steering matrix A was made to be relative to 0 deg +-180

% Angle of source is +-180 relative to the zero degrees

%

% sends a signal 19th 1MHz sine wave

% samples at 20MHz

 

 

clear all

disp(' Circular/Square Array Demo')

disp('  ')

 

% some constants

% assume signal has been downconverted from 1000HMz to Baseband

% where a 1Mhz signal has been placed. sampling at 20MHz.

c = physconst('LightSpeed');        % sound light m/s

M = 4;                  % number of  elements ONLY 4 or 8 or 16

D = 0.010;              % Array dimension (distance between antennas)

AngleOfSourceDeg = +5;    % 10 degrees - source direction Az

SamplingFreq = 20e6;    % guessing what the sampling rate is: 20MHz

NumData = 1024;         % number of timeseries in simulated source

WidthofBeams=30;        % width of the beams (i.e. dont need to do 180deg)

FFTSize = 1024;   % FFT size

 

Fss = SamplingFreq;     %simulation of source sampling ADC

tss = 1/Fss;            % data simulator sampling time in sec

 

fd = 1e6;      % freq of Signal of Interest

Lamda = c/fd;   % wavelength of Signal frequency

 

R = sqrt((D/2)^2 + (D/2)^2); % Radius of the Circle

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

if M==4,

    Phi(1)=45*pi/180;

    Phi(2)=135*pi/180;

    Phi(3)=(135+90)*pi/180;

    Phi(4)=(135+90+90)*pi/180;

end;

 

if M>4, % 8 or 16

    for i = 1:M,

        Phi(i)=((i-1)*45*pi/180);

    end;

end;

 

%%%%%%%%%%%%%%%%%%%

% Steering Matrix A

% NOTE WE WILL NEED TO RECALCULATE STEERING MATRIX

% IF WE DO ANOTHER FREQ OTHER THAN fd

for ii=1:NumAngles,

    for i=1:M,

        mua=2*pi*R*cos(ThetaA(ii)-Phi(i))/Lamda;

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

nn = [0:NumData];

y=exp(1i*2*pi*fd*tss*nn);

y1 = y.*Asource(1);

y2 = y.*Asource(2);

y3 = y.*Asource(3);

y4 = y.*Asource(4);

 

% Now get data from the source at each Antenna

Xx=zeros(M,NumData);        % Prime the data Matrix (4 antennas of Data)

Xf = zeros(M, FFTSize);     % Prime the Matrix of FFTs

 

% relative to M=1 element

%

K=FFTSize;

y=zeros(M, FFTSize);

 

Xf(1,:) = fft(y1(1:FFTSize), FFTSize); % do FFT for the Antenna

Xf(2,:) = fft(y2(1:FFTSize), FFTSize); % do FFT for the Antenna

Xf(3,:) = fft(y3(1:FFTSize), FFTSize); % do FFT for the Antenna

Xf(4,:) = fft(y4(1:FFTSize), FFTSize); % do FFT for the Antenna

 

% Plot Raw data

% plot((y(:,1:50)')); title('Raw data of each element');

%disp('Press any key to continue')

% pause

 

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

 

% Plot FFT

figure(1)

plot((0:Fss/(FFTSize-1):Fss/2)/1000, abs(Xf(:,1:FFTSize/2)'))

xlabel('MHz');title('FFT for antenna');

 

 

% POWER CALCULATION

% Get Power for each steering angle of the data.

P=zeros(1,NumAngles);

Rxx = conj(Xs)'*Xs;

for i=1:NumAngles,

    P(i) = conj(A(:,i))'*Rxx*(A(:,i));

end; %i

 

figure(2)

plot(ThetaA*180/pi,-10*log10(abs(P)/max(abs(P))))

hold on; plot(AngleOfSourceDeg, (max(-10*log10(abs(P)/max(abs(P))))), 'r*', 'MarkerSize', 18);

grid on

hold off