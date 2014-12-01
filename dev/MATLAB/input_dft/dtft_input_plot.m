function [ output_args ] = dtft_input_plot(input_arg)
%DTFT_INPUT_PLOT Summary of this function goes here
%   Detailed explanation goes here

[xn fs]=wavread(input_arg);
nf=106000; %number of point in DTFT
Y1 = fft(xn,nf);
Y1db = mag2db(abs(Y1));
f1 = fs/2*linspace(0,1,nf/2+1);
plot(f1,Y1db(1:nf/2+1));

end

