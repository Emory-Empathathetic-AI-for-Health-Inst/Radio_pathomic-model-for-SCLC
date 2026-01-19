%%%%%%%VERSION 2
%%ANOTHER DESCRIBTION OF GABOR FILTER

%The Gabor filter is basically a Gaussian (with variances sx and sy along x and y-axes respectively)
%modulated by a complex sinusoid (with centre frequencies U and V along x and y-axes respectively) 
%described by the following equation
%%
%                            -1     x' ^     y'  ^             
%%% G(x,y,theta,f) =  exp ([----{(----) 2+(----) 2}])*cos(2*pi*f*x');
%                             2    sx'       sy'
%%% x' = x*cos(theta)+y*sin(theta);
%%% y' = y*cos(theta)-x*sin(theta);

%% Describtion :

%% I : Input image
%% Sx & Sy : Variances along x and y-axes respectively
%% f : The frequency of the sinusoidal function
%% theta : The orientation of Gabor filter

%% G : The output filter as described above
%% gabout : The output filtered image



%%  Author : Ahmad poursaberi  e-mail : a.poursaberi@ece.ut.ac.ir
%%          Faulty of Engineering, Electrical&Computer Department,Tehran
%%          University,Iran,June 2004

function [G,gabout,gaboutReal,gaboutImg] = GaborFilter(I,Sx,Sy,Scale,Orientation);

if isa(I,'double')~=1 
    I = double(I);
end


m_dSigma  = 2*pi;
m_dfrequency = sqrt(2);
m_dKmax  = pi/2;

HeightBottom  = -fix(Sy/2);
HeightTop     = fix(Sy/2);

WidthBottom  = -fix(Sy/2);
WidthTop     = fix(Sy/2);

postConstant    = exp(-m_dSigma*m_dSigma/2);


preConstant_Kuv = (m_dKmax / m_dfrequency^Scale)^2;
Phi = Orientation;
Kv  = m_dKmax / (m_dfrequency^Scale);


m_dSigmaY = 2*pi;
m_dSigmaX = 2*pi;


for x = WidthBottom:WidthTop
    for y = HeightBottom:HeightTop 
        %xPrime = x * cos(theta) + y * sin(theta);
        %yPrime = y * cos(theta) - x * sin(theta);
        
        exppart = exp(-1 * preConstant_Kuv/2 * (x*x/(m_dSigmaX*m_dSigmaX) + y*y/(m_dSigmaY*m_dSigmaY))) * preConstant_Kuv / (m_dSigmaX*m_dSigmaY) ;
        %pImagereal[k] =  exppart * ( cos(  Kv*(  cos(Phi)*x + sin(Phi)*y ) ) - postConstant );
	    %pImageconj[k] =  exppart * ( sin(  Kv*(  cos(Phi)*x + sin(Phi)*y ) ) );
				
        
        G(WidthTop+x+1,HeightTop+y+1) = exppart * ( cos(  Kv*(  cos(Phi)*x + sin(Phi)*y ) ) - postConstant ) + i* exppart * ( sin(  Kv*(  cos(Phi)*x + sin(Phi)*y ) ) );
        
        %exp(-.5*((xPrime/Sx)^2+(yPrime/Sy)^2))*cos(2*pi*f*xPrime);
    end
end

Imgabout = conv2(I,double(imag(G)),'same');
Regabout = conv2(I,double(real(G)),'same');

gabout = sqrt(Imgabout.*Imgabout + Regabout.*Regabout);
gaboutImg = Imgabout;
gaboutReal = Regabout;