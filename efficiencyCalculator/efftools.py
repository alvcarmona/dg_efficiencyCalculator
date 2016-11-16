#!/usr/bin/env python

#from pylab import *
#from scipy import * 
import pylab as pl
#import scipy as sp

def efficiency2particles(d,R1,R2,sigma):
	"""This script is the implementation of Equations from 3.11 to 3.16 from page 63 on Francesco's PhD thesis (download from twiki). The output is efficiency for a BS layer and a T layer,
	varibles must be scalar, d is the thickness of the coating, R1 and R2 effective ranges of the two partciles emitted back-to-back (as defined at page 60 according to an energy threshold),
	sigma the macroscopic cross section. Note that if you want ot consider an inclined layer you just need to feed into sigma the effective sigma (Equation 3.9 page 62) which is sigma/sin(theta),
	with theta the angle between neutron beam and the layer (defined in Fig. 3.1 page 59)."""

	# assert isinstance(R1,float) or isinstance(R1,int)
	# assert isinstance(R2,float) or isinstance(R2,int)

	d=float(d)
	R1=float(R1)
	R2=float(R2)
	sigma=float(sigma)
	if R1<R2:
		R1,R2=R2,R1

	assert R2<=R1

	eff=pl.zeros((2,1))

	if d!=0:
		if d<R2:
			#d<R2<R1 (3.11)
			#Back scattering
			eff[0,0]=(1.-1./(2.*sigma*R1)-1./(2.*sigma*R2))*(1.-pl.exp(-sigma*d))+(1./(2.*R1)+1./(2.*R2))*d*pl.exp(-sigma*d)
			#Transmission
			eff[1,0]=(1.+1./(2.*sigma*R1)+1./(2.*sigma*R2))*(1.-pl.exp(-sigma*d))-(1./(2.*R1)+1./(2.*R2))*d
		elif d>=R2 and d<R1:
			#R2<d<R1
			#Back scattering
			eff[0,0]=(1.-1./(2.*R1*sigma)-1./(2.*R2*sigma))+((pl.exp(-sigma*R2))/(2.*sigma*R2))-(1.-1./(sigma*R1)-d/R1)*((pl.exp(-sigma*d))/2.)
			#Transmission
			eff[1,0]=((pl.exp((R2-d)*sigma))/(2.*R2*sigma))-(1.+1./(2.*R1*sigma)+1/(2.*R2*sigma))*(pl.exp(-sigma*d))+ (1./2.)*(1.+1./(sigma*R1)-d/R1)

		else:
			#R2<R1<d
			#Back scattering
			eff[0,0]=(1.-1./(2.*R1*sigma)-1./(2.*R2*sigma))+ ((pl.exp(-sigma*R2))/(2.*sigma*R2))+((pl.exp(-sigma*R1))/(2.*sigma*R1))
			#Transmission
			eff[1,0]=(pl.exp(-sigma*d))*(-1.-1./(2.*R1*sigma)-1./(2.*R2*sigma)+((pl.exp(sigma*R2))/(2.*sigma*R2))+((pl.exp(sigma*R1))/(2.*sigma*R1)))
	return eff

def efficiency4boron(d,Ralpha94,RLi94,Ralpha06,RLi06,sigma):
	"""Francesco's PhD thesis (download from twiki) is the reference for these scripts. The output is efficiency for a blade (2 layers BS+T in this order), a BS layer and a T layer of B4C,
	all varibles must be scalar, d is the thickness of the coating, R are the 4 effective ranges of the two partciles emitted back-to-back (as defined at page 60 according to an energy threshold),
	sigma the macroscopic cross section. Note that if you want ot consider an inclined layer you just need to feed into sigma the effective sigma (Equation 3.9 page 62) which is sigma/sin(theta),
	with theta the angle between neutron beam and the layer (defined in Fig. 3.1 page 59)"""

	d=float(d)
	Ralpha94=float(Ralpha94)
	RLi94=float(RLi94)
	Ralpha06=float(Ralpha06)
	RLi06=float(RLi06)
	sigma=float(sigma)

	temp1=efficiency2particles(d,Ralpha94,RLi94,sigma)
	temp2=efficiency2particles(d,Ralpha06,RLi06,sigma)

	eff=pl.zeros((3,1))

	eff[1,0]= 0.94*temp1[0,0]+0.06*temp2[0,0]          #backscatt
	eff[2,0]= 0.94*temp1[1,0]+0.06*temp2[1,0]          #transmission
	eff[0,0]= eff[1,0] + (pl.exp(-d*sigma))*eff[2,0]      #total eff blade

	return eff



#def sigma(wavelength,theta,massdensity,composition)
#"""Francesco's PhD thesis (download from twiki) is the reference for these scripts. The #output is the effective  macroscopic cross section  """
# sigmadqdx = wiefn
#return sigmanum

if __name__=='__main__':
	print efficiency2particles(3,2,1,1)
	print efficiency4boron(2, 4, 1, 3, 5, 3)
	print 'ciao'
