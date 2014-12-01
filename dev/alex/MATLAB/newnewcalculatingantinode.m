function [a,b]=newnewcalculatingantinode(frequency,x1,y1,x2,y2,p1,p2)%
r=(344*(1/frequency));%calculate the distance that the sound travel within one period 
d=r/4;
i=1;
delay1=p1/360*r;
delay2=p2/360*r;
for p=0:5
    for q=0:5
syms x y
[x,y]=solve ((x-x1)^2+(y-y1)^2==(d*3+r*p+delay1)^2, (x-x2)^2+(y-y2)^2==(d+r*q+delay2)^2);

checking=isreal(double(x(1)));
   if checking==1
   a(i)=double(x(1));
   b(i)=double(y(1));
   i=i+1;
   a(i)=double(x(2));
   b(i)=double(y(2));
   i=i+1;
   end
    end
end
for m=0:5
    for n=0:5
syms w z
[w,z]=solve ((w-x1)^2+(z-y1)^2==(d+r*m+delay1)^2, (w-x2)^2+(z-y2)^2==(d*3+r*n+delay2)^2);

checking=isreal(double(w(1)));
   if checking==1
   a(i)=double(w(1));
   b(i)=double(z(1));
   i=i+1;
   a(i)=double(w(2));
   b(i)=double(z(2));
   i=i+1;
   end
    end
end
end