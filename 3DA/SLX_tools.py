#!/usr/bin/env python
########################################################################
# name: SLX_tools.py													   
"""
This is a collection of routines to read 3DA data on the server on which i work, and it also contains a few routines i use to extract a subregion of the data and plot a time spectrum or initialize a custom map. 
"""

## standart libraries
import os,sys,glob
import numpy as np
import numpy.ma as ma

import matplotlib.pyplot as plt


# xarray
import xarray as xr

###############################################
def readOCCIPUTmb1():
    """
    Read OCCIPUT member 1 on the MEOM server
    """
    # directory
    diri_occi = "/mnt/meom/MEOM-OPENDAP/CMEMS_3DA/SUBSET1_PRELIM_GOM025/"

    # file name (read OCCIPUT member 1)
    fili_occi="GOM025-GSL301.001_y1993-2012.1d_gridT.nc"

    # variable name in the file:
    varna_occi = 'ssh'

    # variable names for lat lon:
    latna_occi = "nav_lat"
    lonna_occi = "nav_lon"

    # READ
    SSH_occi     = xr.open_dataset(diri_occi+fili_occi)[varna_occi].squeeze()
    nav_lon_occi = xr.open_dataset(diri_occi+fili_occi)[lonna_occi].squeeze() 
    nav_lat_occi = xr.open_dataset(diri_occi+fili_occi)[latna_occi].squeeze() 
    
    return SSH_occi,nav_lon_occi,nav_lat_occi


def readAVISO():
    """
    Read AVISO SLA 2004 and MDT member  on the MEOM server
    """
    # directory
    diri_aviso = "/mnt/meom/workdir/lerouste/AVISO/"
    diri_mdt = diri_aviso+"MDT_CNES-CLS13/"

    # file name 
    fili_aviso="GMex_AVISO_SLA_y2004_1d.nc"
    fili_mdt = "GMex_mdt-cnes-cls13-global.nc"

    # variable name in the file:
    varna_aviso = 'sla'
    varna_mdt   = 'mdt'

    # READ
    sla = xr.open_dataset(diri_aviso+fili_aviso)[varna_aviso].squeeze()
    mdt = xr.open_dataset(diri_mdt+fili_mdt)[varna_mdt].squeeze()

    # add MDT
    SSH_aviso = sla + mdt
    return SSH_aviso,SSH_aviso.lon,SSH_aviso.lat

def readORCA12():
    """
    Read ORCA12 on the MEOM server
    """
    # directory
    diri_orca12 = "/mnt/meom/MEOM-OPENDAP/CMEMS_3DA/SUBSET2_GOM12/"

    # file name (read OCCIPUT member 1)
    fili_orca12="GOM12-MJM189_y2004.1d_SSH.nc"

    # variable name in the file:
    varna_orca12 = 'sossheig'

    # variable names for lat lon:
    latna_orca12 = "nav_lat"
    lonna_orca12 = "nav_lon"

    # READ
    SSH_orca12     = xr.open_dataset(diri_orca12+fili_orca12)[varna_orca12].squeeze()
    nav_lon_orca12 = xr.open_dataset(diri_orca12+fili_orca12)[lonna_orca12].squeeze() 
    nav_lat_orca12 = xr.open_dataset(diri_orca12+fili_orca12)[latna_orca12].squeeze() 
    
    return SSH_orca12,nav_lon_orca12,nav_lat_orca12


def myGMexPlotsettings():
    """ 
    Initialize my mapplot settings with  my favorite values. 
    Can be changed in the script afterwards if needed.
    # For more details about the arguments, see my plot function plotSP.
    #
    glo= False : True if global plot.
    xlim=(-100,-75)
    ylim=(15,32)
    #
    ### Coaslines
    coastL=False
    coastC=True
    coastLand=True
    #
    ### Color shading
    typlo='pcolormesh'  : type of plot 
    #
    # min/max values
    vmin=-0.5
    vmax=0.5
    #
    # number of color segments in the colormap
    Nincr=50
    #
    # color of the values smaller than vmin
    su='#EFF5FB'
    # color of the values larger than vmax
    so='#F8E0E0'
    #
    # colorbar label 
    labelplt= "SLA"
    #
    # number of labels on the colorbar
    Nbar=5
    #
    #------------ plot output
    # plot format
    pltty = ".png"
    #
    # plot resolution (dpi)
    dpifig=300
    #
    # output directory for plots
    diro="./"
    #
    """
    #------------ geography
    # Global plot
    glo= False

    xlim=(-100,-75)
    ylim=(15,32)

    # Coaslines
    coastL=False
    coastC=True
    coastLand=True

    #------------ color shading
    # type of plot 
    typlo='pcolormesh'

    # min/max values
    vmin=-0.5
    vmax=0.5

    # number of color segments in the colormap
    Nincr=50

    # color of the values smaller than vmin
    su='#EFF5FB'
    # color of the values larger than vmax
    so='#F8E0E0'

    # colorbar label 
    labelplt= "SLA"

    # number of labels on the colorbar
    Nbar=5

    #------------ plot output
    # plot format
    pltty = ".png"

    # plot resolution (dpi)
    dpifig=300

    # output directory for plots
    diro="./"
    return glo,xlim,ylim,coastL,coastC,coastLand,typlo,vmin,vmax,Nincr,su,so,labelplt,Nbar,pltty,dpifig,diro


def extractsubreg(lomi,loma,lami,lama,nav_loni,nav_lati,SSHi):
    """
    Extract a subregions from data.
    lomi,loma,lami,lama are the longitude and latitude bounds.
    nav_loni,nav_lati are the latitude and longitude arrays of the initial data.
    SSHi is the xarray of data.
    """ 
    lonlatbounds=  np.zeros((4))      
    lonlatbounds[0]=lomi
    lonlatbounds[1]=loma
    lonlatbounds[2]=lami
    lonlatbounds[3]=lama

    reg = SSHi.where((((nav_lati<lonlatbounds[3])&(nav_lati>lonlatbounds[2]))&((nav_loni>lonlatbounds[0]) & (nav_loni<lonlatbounds[1]))),drop=True)

    if (nav_lati.shape == SSHi[0,:,:].shape):
        nav_lat = nav_lati.where((((nav_lati<lonlatbounds[3])&(nav_lati>lonlatbounds[2]))&((nav_loni>lonlatbounds[0]) & (nav_loni<lonlatbounds[1]))),drop=True)
        nav_lon = nav_loni.where((((nav_lati<lonlatbounds[3])&(nav_lati>lonlatbounds[2]))&((nav_loni>lonlatbounds[0]) & (nav_loni<lonlatbounds[1]))),drop=True)
    else:
        nav_lat = nav_lati.where((((nav_lati<lonlatbounds[3])&(nav_lati>lonlatbounds[2]))),drop=True)
        nav_lon = nav_loni.where(((nav_loni>lonlatbounds[0]) & (nav_loni<lonlatbounds[1])),drop=True)

    return reg,nav_lat,nav_lon
    
    
def plotSP(freqs,spdat2plot,xmin,xmax,sp2=[0.],sp3= [0.],co='#DF3A01',co2='#0B4C5F',co3='#D0FA58',ti1='no',ti2='no',ti3='no',title='no'):
        """
        Plot time spectrum (up to 3 lines).
        """
        ax2 =  plt.gca() 

        l1 = plt.plot(freqs,spdat2plot,co,linewidth=2,label=ti1)
        if any(sp2)!=0:
            l2 = plt.plot(freqs,sp2,co2,linewidth=0.5,linestyle="-",label=ti2)
        if any(sp3)!=0:
            l3 = plt.plot(freqs,sp3,co3,linewidth=2,label=ti3)  
            
        ax2.set_xscale('log', nonposx='clip')
        ax2.set_yscale('log', nonposy='clip')

        #---- X-Ticks 
        ax2.set_xlabel('Frequency (cpd)', fontsize=12)
        ax2.xaxis.label.set_size(13)
        ax2.set_xlim(10 ** xmin, 10 ** xmax)\

        #---- Second axis with spatial wave lengths 
        twiny = ax2.twiny()

        twiny.set_xscale('log', nonposx='clip')
        twiny.set_xlim(10 ** xmin, 10 ** xmax)

        # major ticks
        new_major_ticks = 10 ** np.arange(xmin+1 , xmax, 1.)
        new_major_ticklabels = 1. / new_major_ticks
        new_major_ticklabels = ["%.0f" % i for i in new_major_ticklabels]

        twiny.set_xticks(new_major_ticks)
        twiny.set_xticklabels(new_major_ticklabels, rotation=60, fontsize=12)

        # minor ticks
        A = np.arange(2, 10, 2)[np.newaxis]
        B = 10 ** (np.arange(-xmax, -xmin, 1)[np.newaxis])
        C = np.dot(B.transpose(), A)

        new_minor_ticklabels = C.flatten()
        new_minor_ticks = 1. / new_minor_ticklabels
        new_minor_ticklabels = ["%.0f" % i for i in new_minor_ticklabels]
        twiny.set_xticks(new_minor_ticks, minor=True)
        twiny.set_xticklabels(new_minor_ticklabels, minor=True, rotation=60,
                              fontsize=12)
        twiny.set_xlabel('Period (day)', fontsize=12)

        # Y-Axis
        ax2.set_ylabel('PSD (m$^2$ cpd$^{-1}$)', fontsize=12)
        
        # Title
        if ti1!='no':
            ax2.legend(loc=3)
        
        if title!='no':
            plt.title(title)
        
        # Grid
        ax2.grid(True, which='both')

        return ax2

    
   
