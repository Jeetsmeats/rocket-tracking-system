fs = 20000000;

s = dir('rx1.raw');         
N1 = s.bytes;
s = dir('rx2.raw');
N2 = s.bytes;
if (N2 < N1)
    N1 = N2;
else
    N2 = N1;
end

fid1 = fopen('rx1.raw', 'r');  
fid2 = fopen('rx2.raw', 'r');  
K = 1000000;
M = floor(N1/K);
D = zeros(1,M);
figure(1); clf;
for k = 1:M
    k;
    A_1 = fread(fid1, [2, K/2], 'int8').';
    fseek(fid1, (k-1)*K, -1);
    A = A_1(1:end,1) + sqrt(-1)*A_1(1:end,2);
    An = A/rms(A);

    A_2 = fread(fid2, [2, K/2], 'int8').';
    fseek(fid2, (k-1)*K, -1);
    B = A_2(1:end,1) + sqrt(-1)*A_2(1:end,2);
    Bn = B/rms(B);    
    C = real(An).* real(Bn);    
    Crf = fft(C);
    D(k) = Crf(1);

    % figure(1); 
    % plot(1:length(An),real(An),1:length(Bn),real(Bn));
    % drawnow;
    % pause;
end
fclose(fid1);
fclose(fid2);

hold off;

figure(1);
clf;
plot(real(D)/length(C))
return;

fs = 10e6;
Alpf = lowpass(A,.02/fs);
Af = fft(A);
Aflpf = fft(Alpf);
f = [0:length(Af)/2-1]*fs/length(Af);
plot(f,10*log10(abs(Af(1:length(Af)/2))),f,10*log10(abs(Aflpf(1:length(Af)/2))));

return;



return;

s = dir('rx2.cs8');         
if (s.bytes < N1)
    N1 = s.bytes;
end
fid2 = fopen('rx2.cs8', 'r');
A_745cf = fread(fid2, [2, N1/2], 'int8').';
fclose(fid2);
B = A_745cf(1:end,1) + sqrt(-1)*A_745cf(1:end,2);
Bn = B/rms(B);
Br = reshape(Bn(1:floor(length(Bn)/10000)*10000),10000,[]);

return;

if (length(B) > length(A))
    L = length(A);
else 
    L = le
ngth(B);
end
figure(1);clf;
plot(1:30000,real(A(10000:40000-1)),1:30000,imag(A(10000:40000-1)),'r');
return;
plot(1:30000,real(A(10000:40000-1)), 1:30000, real(B(10000:40000-1)),'r');

return;
L = 10000000;
C = real(A(1:L)).* real(B(1:L));
Cr = reshape(C(1:floor(length(C)/10000)*10000),10000,[]);
Crf = fft(Cr(1:9476,:));
figure(1); clf;
plot((abs(Crf(1:50,100:200))));
Crdc = Crf(1,:);
figure(2); clf; 
plot(abs(Crdc));
return;

for k = 1:200:4700
figure(2); clf; 
plot(1:10000, real(Ar(:,1)), 1:10000, real(Br(:,1)));
hold on;
plot(1:10000, real(Ar(:,k)), 1:10000, real(Br(:,k)));
drawnow;
pause 
end



return;

return;

B = fft(s_745cf);
C = fft(s_c76cf);
temp = abs(B);
Bidx = find(temp(1:10000) == max(temp(1:10000)));
temp = abs(C);
Cidx = find(temp(1:10000) == max(temp(1:10000)));
if (Bidx ~= Cidx) 
    error('max(FFT) indices do not match');
end
(angle(C(Bidx)) - angle(B(Bidx)))*180/pi



return;

file1 = 'rx1.raw'; % board A
file2 = 'rx2.raw'; % board C

fid1 = fopen(file1, 'r');
s1_dat = fread(fid1, [2,8000000], 'float32').';
fclose(fid1);
s1 = s1_dat(:,1) + sqrt(-1)*s1_dat(:,2);

fid2 = fopen(file2, 'r');
s2_dat = fread(fid2, [2,8000000], 'float32').';
fclose(fid2);
s2 = s2_dat(:,1) + sqrt(-1)*s2_dat(:,2);

figure(1);
clf;
%plot(real(s1), imag(s1),'.');
% hold on; 
% plot(real(s2(1:20000)), imag(s2(1:20000)), '.r');
% xlim([-1 1]);
% ylim([-1 1]);
plot(real(s1(1:20000))); 



%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
fc = 240;
fs = 10*fc;
Ts = 1/fs;
Np = 10;
P = 1/fc;
t = [0:Np*P/Ts-1]*Ts;
s = cos(2*pi*fc*t);
S = fft(s);
f =[0:1:length(S)-1]*fs/length(S);
f = [0:length(S)/2-1]*fs/length(S);
plot(f,10*log10(abs(S(1:length(S)/2))));
xlabel('Hz');



