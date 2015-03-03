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
else
    plot(t,amp,'b');
end

end