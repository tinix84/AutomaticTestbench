function AlgorithmTest2()
%clear all the previous stuff
clc
clear all

%useful setting for debugging, comment it in normal mode
dbstop if error;

debugmode=0; %debug mode uses dummy instruments

load('./rawdata_summary.csv')
peak_detection = [];
peak_detection(:,1) = rawdata_summary(:,1);
%skip first 100 as in FPGA software plus header
meas_mat = rawdata_summary(:, 6001:end);
meas_mat = (meas_mat);
[min_value,min_index] = min(meas_mat');
peak_detection(:,2) = min_value;
peak_detection(:,3) = min_index+5999;

for ii = 1:size(meas_mat,1)
    wfm = rawdata_summary(ii, 2:end);
    time = 1:length(wfm);
    peak_idx = peak_detection(ii, 3)
    pkpar3p1d(ii,1)=Peak3pParabInterp(time, wfm, peak_idx, 1);
    pkpar3p2d(ii,1)=Peak3pParabInterp(time, wfm, peak_idx, 2);
    pkpar3p3d(ii,1)=Peak3pParabInterp(time, wfm, peak_idx, 3);
    pkgauss1d(ii,1)=PeakGaussInterp(time, wfm, peak_idx, 1);
    pkgauss2d(ii,1)=PeakGaussInterp(time, wfm, peak_idx, 2);
    pkgauss3d(ii,1)=PeakGaussInterp(time, wfm, peak_idx, 3);
    % local average of last 1000 samples till 10 samples before peak
    high_ref(ii,1) = mean(wfm(peak_idx-1010:peak_idx-10));
    low_ref(ii,1) = peak_detection(ii, 2);
    mid_ref(ii,1) = (high_ref(ii,1) + low_ref(ii,1))/2;
    
    ampl_vect = (wfm(peak_idx-40:peak_idx+40));
    peak_pos=41;
    t_vect = 1:length(ampl_vect);
    plot(t_vect, ampl_vect)
    hold on
    plot(high_ref(ii,1)*ones(size(t_vect)), 'g')
    plot(mid_ref(ii,1)*ones(size(t_vect)), 'r')
    hold off
    [ind,t0,s0,t0close,s0close] = crossing(ampl_vect, t_vect, mid_ref(ii,1), 'linear');
    widthn(ii,1) = t0(2) - t0(1);
    [ind,t0,s0,t0close,s0close] = crossing(ampl_vect, t_vect, high_ref(ii,1), 'linear');
    X = t0 - peak_pos; %21 is index position of min in ampl_vect
    rise(ii,1) = X(min(find(X>0)));
    fall(ii,1) = -X(max(find(X<0)));
    %     rise_time =
    %     fall_time =
    %     pulse_width_50 =
    
end

peak_detection(:,4) = high_ref';
peak_detection(:,5) = mid_ref';
peak_detection(:,6) = widthn';
peak_detection(:,7) = rise';
peak_detection(:,8) = fall';
peak_detection(:,9) = pkpar3p1d';
peak_detection(:,10) = pkpar3p2d';
peak_detection(:,11) = pkpar3p3d';
peak_detection(:,12) = pkgauss1d';
peak_detection(:,13) = pkgauss2d';
peak_detection(:,14) = pkgauss3d';
plot(meas_mat')
xmin = peak_detection(ii, 3) - 30-5999;
xmax = peak_detection(ii, 3) + 30-5999;
axis([xmin xmax 1.524e6 1.542e6])
save peak_detection
end

function pk=Peak3pParabInterp(time, wfm, idx, pt_distance)
% out of the 3 amplitudes y0 / y1 / y2 at samplingpositions i-1 / i / i+1
% with i = position
y=[]; ty=[];

dt=time(2)-time(1);
y(2)=wfm(idx);   ty(2)=time(idx);
y(1)=wfm(idx-pt_distance);      ty(1)=time(idx-pt_distance);
y(3)=wfm(idx+pt_distance);      ty(3)=time(idx+pt_distance);
cpar=polyfit([0 1 2],y,2);
%     newtime=linspace(0, 2, 100);
%     ypar=polyval(cpar,newtime);
%     hold on; plot([0 1 2], y); plot(newtime, ypar, 'r'); hold off;
tmaxrel=-cpar(2)/2/cpar(1); %xmax=-b/2a on x=[0,1,2]
pk=ty(1)+tmaxrel*dt;
end

% % SHORT DESCRIPTION
% % Calcs parameters of a peak indicated by R1
% % The real time position b of the real maximum of the gaussian peak is calculated
% % out of the 3 amplitudes y0 / y1 / y2 at samplingpositions i-1 / i / i+1  with i = position
% % of the maximum in histogram with the formulas:
% k = ln (y0/y1) / ln (y2/y1)
% % with dx = 30ns for 100MHz/3 corresponding to 4.5m basic resolution
% b = dx {i + (1-k) / (2k+2)}
function [pk, k, corr]=PeakGaussInterp(time, wfm, idx, pt_distance)
% out of the 3 amplitudes y0 / y1 / y2 at samplingpositions i-1 / i / i+1
% with i = position
y=[]; ty=[];
dt=time(2)-time(1);
y(2)=wfm(idx);   ty(2)=time(idx);
%if (idx==1 || idx==length(wfm)) break; end;
y(1)=wfm(idx-pt_distance); ty(1)=time(idx-pt_distance);
y(3)=wfm(idx+pt_distance); ty(3)=time(idx+pt_distance);
%plot(time,wfm);
k = log(y(1)/y(2))/log(y(3)/y(2));
corr = -(dt*(1-k)/(2*k+2));
pk= corr+ty(2);
end