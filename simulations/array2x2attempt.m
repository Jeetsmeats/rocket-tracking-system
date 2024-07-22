
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

% some constants

% assume signal has been downconverted from 1000HMz to Baseband

% where a 1Mhz signal has been placed. sampling at 20MHz.



% input source angles here
azimuth_angle = 15;
elevation_angle = 30;






NoiseStr = 0;

c = physconst('LightSpeed');        % sound light m/s

M = 4;                  % number of  elements

D = 0.010;              % Array dimension (distance between antennas)

CarrierFreq=1e9;    % 1GHz

SamplingFreq = 20e6;    % guessing what the sampling rate is: 20MHz

NumData = 1024;         % number of timeseries in simulated source

WidthofBeams=60;        % width of the beams (i.e. dont need to do 180deg)

FFTSize = 1024;   % FFT size

Fss = SamplingFreq;     %simulation of source sampling ADC

tss = 1/Fss;            % data simulator sampling time in sec

fd = 1e6;      % freq of Signal of Interest

Lamda = c/CarrierFreq;   % wavelength of Signal frequency

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

azimuthA = -ThetaWidth:ThetaIncremRad:ThetaWidth; % range of azimuth angles

elevationA = 0:ThetaIncremRad:ThetaWidth; % range of elevation angles

NumAzimuthAngles = length(azimuthA);

NumElevationAngles = length(elevationA);

NumAnglePairs = NumAzimuthAngles*NumElevationAngles;

A = ones(M,NumAnglePairs);

% M = number of elements (antennas)

if M==4

    Phi(1)=45*pi/180;

    Phi(2)=135*pi/180;

    Phi(3)=(135+90)*pi/180;

    Phi(4)=(135+90+90)*pi/180;

end

%%%%%%%%%%%%%%%%%%%

% Steering Matrix A

% NOTE WE WILL NEED TO RECALCULATE STEERING MATRIX

% IF WE DO ANOTHER FREQ OTHER THAN fd
curr_azimuth_angle = 0;
curr_elevation_angle = 0;
idx = 0;

for i = 1:NumAzimuthAngles
    for j = 1:NumElevationAngles
        curr_azimuth_angle = azimuthA(i);
        curr_elevation_angle = elevationA(j);
        idx = (i-1)*NumElevationAngles + j;
        for k = 1:M
            mua = 2*pi*R*( cos(Phi(k))*cos(curr_azimuth_angle)*cos(curr_elevation_angle) + sin(Phi(k))*sin(curr_azimuth_angle)*cos(curr_elevation_angle) ) / (Lamda);
            A(k, idx) = exp(-1i*mua);
        end
       
    end
end


% now make steering vector for the AngleOfSource only (to make our

% simulated data)

AzimuthOfSourceRad = azimuth_angle*pi/180; %Rad
ElevationOfSourceRad = elevation_angle*pi/180; %Rad

 

for i=1:M

    mua=2*pi*R*( cos(Phi(i))*cos(AzimuthOfSourceRad)*cos(ElevationOfSourceRad) + sin(Phi(i))*sin(AzimuthOfSourceRad)*cos(ElevationOfSourceRad) ) / (Lamda);
    Asource(i)=exp(-1i*mua)';
end

 

% Making data

nn = [0:NumData-1];

y=exp(1i*2*pi*fd*tss*nn);

y1 = (y.*Asource(1))+NoiseStr*(randn(size(nn))+1i*randn(size(nn))); %.*hann(NumData);

y2 = (y.*Asource(2))+NoiseStr*(randn(size(nn))+1i*randn(size(nn))); %.*hann(NumData);

y3 = (y.*Asource(3))+NoiseStr*(randn(size(nn))+1i*randn(size(nn)));% .*hann(NumData);

y4 = (y.*Asource(4))+NoiseStr*(randn(size(nn))+1i*randn(size(nn)));% .*hann(NumData);

 

% Now get data from the source at each Antenna

Xx=zeros(M,NumData);        % Prime the data Matrix (4 antennas of Data)

Xf = zeros(M, FFTSize);     % Prime the Matrix of FFTs

 

% relative to M=1 element

%

K=FFTSize;

y=zeros(M, FFTSize);

 

Xf(1,:) = fft(y1(1:FFTSize).*hann(1024)', FFTSize); % do FFT for the Antenna

Xf(2,:) = fft(y2(1:FFTSize).*hann(1024)', FFTSize); % do FFT for the Antenna

Xf(3,:) = fft(y3(1:FFTSize).*hann(1024)', FFTSize); % do FFT for the Antenna

Xf(4,:) = fft(y4(1:FFTSize).*hann(1024)', FFTSize); % do FFT for the Antenna

 
 

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


% POWER CALCULATION

% Get Power for each steering angle of the data.

P=zeros(1,NumAnglePairs);

Rxx = conj(Xs)'*Xs;

for i=1:NumAnglePairs

    P(i) = conj(A(:,i))'*Rxx*(A(:,i));

end

 

% estimating the angle
[max_val, max_idx] = max(10*log10(abs(P)/max(abs(P))));
min_val = min(10*log10(abs(P)/max(abs(P))));
estimated_azimuth = -60 + 5*floor((max_idx-1)/13);
estimated_elevation = 5*mod(max_idx-1, 13);
disp('Estimated Azimuth Angle: ')
disp(estimated_azimuth)
disp('Estimated Elevation Angle: ')
disp(estimated_elevation)

% heat map
ordered_data = reshape(10*log10(abs(P)/max(abs(P))), 13, 25);
h = heatmap(ordered_data);

h.XLabel = 'Azimuth Angles';
h.YLabel = 'Elevation Angles';
h.Title = 'Heatmap of Relative Power of Angle Pairs';
xLabels = {'-60', '-55', '-50', '-45', '-40', '-35', '-30', '-25', '-20', '-15', '-10', '-5', '0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'};
yLabels = {'0', '5', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55', '60'};
h.XDisplayLabels = xLabels;
h.YDisplayLabels = yLabels;
h.ColorLimits = [min_val*0.3, max_val];
colormap jet