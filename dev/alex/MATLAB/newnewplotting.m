function x=newnewplotting(f,x1,y1,x2,y2,p1,p2)
r=(344/f);
n=6;

delay1=p1/360*r;
delay2=p2/360*r;
t=linspace (-pi,pi);
x11=sin(t)'*linspace(r/4+delay1,r*(n-1)+r/4+delay1,n)+x1;
y11=cos(t)'*linspace(r/4+delay1,r*(n-1)+r/4+delay1,n)+y1;

x22=sin(t)'*linspace(r/4+delay2,r*(n-1)+r/4+delay2,n)+x2;
y22=cos(t)'*linspace(r/4+delay2,r*(n-1)+r/4+delay2,n)+y2;

x3=sin(t)'*linspace(r*3/4+delay1,r*(n-1)+r*3/4+delay1,n)+x1;
y3=cos(t)'*linspace(r*3/4+delay1,r*(n-1)+r*3/4+delay1,n)+y1;

x4=sin(t)'*linspace(r*3/4+delay2,r*(n-1)+r*3/4+delay2,n)+x2;
y4=cos(t)'*linspace(r*3/4+delay2,r*(n-1)+r*3/4+delay2,n)+y2;


hold on
plot (x11,y11,'b');
plot (x22,y22,'b');
plot (x3,y3,'r');
plot (x4,y4,'r');




end