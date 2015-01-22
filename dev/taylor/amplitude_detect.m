fileID = fopen('amplitude.txt','r');
formatSpec = '%f';
amp = fscanf(fileID,formatSpec);
fclose(fileID);

ref = 0; %Reference to compare increasing/decreasing
inc = 1; %1=True  0=False
index = 1; %Index for the number of maximums found
peaks = 0; %Array of peaks detected initialized to zeroes

for i=1:length(amp)
    if amp(i)>ref
        if inc==0
            peaks(index) = ref;
            index = index+1;
        end
        inc = 1;
        
    elseif amp(i)<ref
        if inc==1
            peaks(index) = ref;
            index = index+1;
        end
        inc = 0;
    end
    
ref = amp(i);
end

peaks
absavg = mean(abs(peaks)) %The average amplitude of the sound clip