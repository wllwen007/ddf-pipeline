#!/usr/bin/python

# try to find dynamic range in a FITS image and catalogue

from astropy.table import Table
from astropy.io import fits
import numpy as np
from make_subim import extract_subim
from crossmatch_utils import select_isolated_sources

def do_dr_checker(tname,imname,peak=0.1,cutout=60,blank=10,verbose=False,write_subims=False):

    drlist=[]
    t=Table.read(tname)
    t=select_isolated_sources(t,cutout)
    filter=(t['Peak_flux']>peak)
    if verbose:
        print np.sum(filter)
    filter&=(t['DC_Maj']<0.003)
    t=t[filter]
    if verbose:
        print len(t)
    for i,r in enumerate(t):
        h=extract_subim(imname,r['RA'],r['DEC'],cutout/3600.0,verbose=False)
        ys,xs=h[0].data.shape
        h[0].data[int(ys/2)-blank:int(ys/2)+blank,int(xs/2)-blank:int(xs/2)+blank]=np.nan
        offpeak=np.nanmax(np.abs(h[0].data))
        if verbose:
            print r['Peak_flux'],offpeak,r['Peak_flux']/offpeak
        drlist.append(r['Peak_flux']/offpeak)
        if write_subims:
            h.writeto('testim-%i.fits' %i,clobber=True)
    return np.array(drlist)


if __name__=='__main__':
    print np.median(do_dr_checker('image_full_ampphase_di_m.NS.cat.fits','image_full_ampphase_di_m.NS_shift.app.facetRestored.fits'))
    
    
