function [] = plotData(filename)
figure();

fileID = fopen(filename,'r');
formatSpec = '%f';
amp = fscanf(fileID,formatSpec);
fclose(fileID);

fs = 44100;
t = 1/fs:1/fs:(length(amp)/fs);

if (strcmp(filename,'ideal_output.txt'))
    target = amp(1);
    t = t(2:end);
    amp = amp(2:end);
    plot(t,repmat(target,length(t),1),'g');
    hold on;
    plot(t,amp,'b');
    xlabel('Time (s)');
    ylabel('Amplitude');
elseif (strcmp(filename,'phase_change.txt'))
    plot((0:length(amp)-1),amp,'b');
    xlabel('Iterations');
    ylabel('Amplitude');
elseif (strcmp(filename,'equalize.txt'))
    target = amp(1);
    t = t(2:end);
    plot(t,repmat(target,length(t),1),'g');
    hold on;
    plot(t,amp(2:end),'b');
    xlabel('Time (in 0.1s intervals)');
    ylabel('Amplitude');
end

end