#!/usr/bin/env  python
#=======================================================================
"""utils_colormap.py
Collection of customed tools related to plotting 
Development on going. Don't forget to git pull from time to time...
"""
#=======================================================================

def make_cmap(colors, position=None, bit=False):
    '''
    make_cmap takes a list of tuples which contain RGB values. The RGB
    values may either be in 8-bit [0 to 255] (in which bit must be set to
    True when called) or arithmetic [0 to 1] (default). make_cmap returns
    a cmap with equally spaced colors.
    Arrange your tuples so that the first color is the lowest value for the
    colorbar and the last is the highest.
    position contains values from 0 to 1 to dictate the location of each color.
    '''
    
    import matplotlib as mpl
    import numpy as np
    bit_rgb = np.linspace(0,1,256)
    if position == None:
        position = np.linspace(0,1,len(colors))
    else:
        if len(position) != len(colors):
            sys.exit("position length must be the same as colors")
        elif position[0] != 0 or position[-1] != 1:
            sys.exit("position must start with 0 and end with 1")
    if bit:
        for i in range(len(colors)):
            colors[i] = (bit_rgb[colors[i][0]],
                         bit_rgb[colors[i][1]],
                         bit_rgb[colors[i][2]])
    cdict = {'red':[], 'green':[], 'blue':[]}
    for pos, color in zip(position, colors):
        cdict['red'].append((pos, color[0], color[0]))
        cdict['green'].append((pos, color[1], color[1]))
        cdict['blue'].append((pos, color[2], color[2]))

    cmap = mpl.colors.LinearSegmentedColormap('my_colormap',cdict,256)
    return cmap


def make_NCLcolormap(reverse=False):
    ''' Define a custom cmap from NCL bipolar cmap.
    Parameters: 
    * Reverse (default=False). If true, will  create the reverse colormap
    ''' 

    ### colors to include in my custom colormap
    colors_NCLbipo=[(11,76,95),(0,97,128),(0,161,191),(0,191,224),(0,250,250),(102,252,252),(153,250,250),(255,255,255),(255,255,255),(252,224,0),(252,191,0),(252,128,0),(252,64,0),(252,33,0),(128,0,0),(0,0,0)]

    ### Call the function make_cmap which returns my colormap
    my_cmap_NCLbipo = make_cmap(colors_NCLbipo[:], bit=True)
    my_cmap_NCLbipo_r = make_cmap(colors_NCLbipo[::-1], bit=True)
    
    if reverse==True:
        my_cmap_NCLbipo = my_cmap_NCLbipo_r

    return(my_cmap_NCLbipo)

    
def showcmap(cmap):  
        ''' Just make a color plot of random matrix to show the cmap colormap given as argument.
        '''
        import numpy as np
        import matplotlib.pyplot as plt

        ### Display my colormap
        figcol = plt.figure(figsize=([3,3]),facecolor='white')
        #ax = fig.add_subplot(311)
        plt.pcolor(np.random.rand(10,10), cmap=cmap)
        plt.colorbar()
        plt.show()  
        



def plotmap(fig1,ehonan,nav_lon,nav_lat,cm_base='viridis',plto='tmp_plot',vmin='0',vmax='0',Nincr=10,typlo='contourf',Nbar=10,glo=True,coastL=False,coastC=False,xlim=(0,10),ylim=(0,10),su='b',so='k',loncentr=0.,latcentr=0.,labelplt="",gloproj='Robinson'):
        '''
        PURPOSE: Plot regional or global map of gridded data (shading).
        Uses Cartopy, xarray, matplotlib, numpy.
        
        ARGUMENTS: 
        fig1: fig id,
        ehonan: 2-d array to plot (geographical data)
        nav_lon: corresponding lon array . Works with lat and lon given as 1-d vectors (if regular grid such as DREAM model) or 2-d arrays (unregular grid such as the ORCA-NEMO-grid)
        nav_lat: corresponding lat array
        
        OPTIONS: (Note that you can omit these options when calling the plot function and in this case defaut values are applied.)
        - cm_base: colormap (defaut=cm.viridis)
        - plto: plo name (defaut='tmpplot')
        - vmin: data min value to plot (color shading) (defaut vmin='0')
        - vmax: data max value to plot (color shading) (defaut vmax='0')
        - Nincr: number of color segments of the colormap (defaut Nincr=10)
        - typlo: type of plot (can be 'contourf', 'pcolormesh' or 'scatter', defaut is contourf, 'scater is not yet fully implemented')
typlo:='contourf'
 : True or False. Type of plotting function (if false then contourf is used)
        - Nbar: number of labels on the colorbar (defaut Nbar=10)
        - glo: global=True (default) sets that  map is global (the projection will be Robinson in nthat case). It is PlateCarre if regional map.
        - coastL: set to True  to plot continents as lines (defaut is False)
        - coastC: set to True to fill continents with colors
        - xlim: set regional limits in longitude (degrees) if glo==False (default xlim=(0,10))
        - ylim=(0,10): set regional limits in latitude (degrees) if glo==False (default ylim=(0,10))
        - su: set the color of the values under vmin (appears as a triangle at the edge of the colorbar). Defaut is 'b' blue.
        - so: set the color of the values over vmax (appears as a triangle at the edge of the colorbar). Defaut is 'k' black.
        - loncentr: longitude to center the map projectionn (defaut is 0).
        - labelplt: label of the colorbar (defaut is nothing)
        
        LEFT-TO-DO:
        * Some color choices (for gridlines, for labels, for continents) are still coded in hard below. 
        They will be added as options in a later version of this code.
        
        '''
        
        ## imports
        import os,sys
        import numpy as np

        # xarray
        import xarray as xr

        # plot
        import cartopy.crs as ccrs
        import cartopy.feature as ccf
        import matplotlib.pyplot as plt
        from matplotlib.colors import Colormap
        import matplotlib.colors as mcolors
        import matplotlib.dates as mdates
        import matplotlib.cm as cm
        import matplotlib.dates as mdates
        import matplotlib.ticker as mticker
        
        # Colormap & levels
        cmap = plt.get_cmap(cm_base)
        cmap.set_under(su,1.)
        cmap.set_over(so,1.) 
        
        if ((vmin==0)&(vmax==0)):
            levels = mticker.MaxNLocator(nbins=Nincr).tick_values(ehonan.min(), ehonan.max())        
        else:
            levels = mticker.MaxNLocator(nbins=Nincr).tick_values(vmin, vmax)
        norm   = mcolors.BoundaryNorm(levels, ncolors=cmap.N,clip=True)
        
        # Projection
        trdata  = ccrs.PlateCarree() 
        # Note: if data points are given in classical lat lon coordinates this should
        #       be set to ccrs.PlateCarree() whatever the map projection is.
        
        if glo:
            if gloproj=='Robinson':
                ax = plt.axes(projection=ccrs.Robinson(central_longitude=loncentr))
            if gloproj=='Orthographic':
                ax = plt.axes(projection=ccrs.Orthographic(central_longitude=loncentr,central_latitude=latcentr))
            # marker size
            sm=0.1
        else:
            ax = plt.axes(projection= ccrs.PlateCarree())
            # marker size
            sm=0.5
        
        if glo:
            ax.set_global() 
            
        if glo:
            ax.outline_patch.set_edgecolor('#585858')
        else:
            ax.outline_patch.set_edgecolor('white')
            

        # grid on map
        if glo:
            gl = ax.gridlines(linewidth=1, color='#585858', alpha=0.2, linestyle='--') 
        else:
            gl = ax.gridlines(draw_labels=True,linewidth=1, color='#585858', alpha=0.2, linestyle='--')
            # grid labels
            label_style = {'size': 12, 'color': 'black', 'weight': 'bold'}
            gl.xlabel_style = label_style
            gl.xlabels_bottom = False
            gl.xlocator = mticker.FixedLocator(np.arange(-180,180,20,dtype=float))
            gl.ylabel_style = label_style
            gl.ylabels_right = False
            gl.ylocator = mticker.FixedLocator(np.arange(-90,90,20,dtype=float))
       
        # Add Coastlines and or plain continents
        if coastC:
            ax.add_feature(ccf.LAND, facecolor='#585858', edgecolor='none')
        if coastL:
            ax.coastlines(color='#585858')
        
        ### PLOTS:
        
        if typlo=='pcolormesh':
            cs  = plt.pcolormesh(nav_lon, nav_lat, ehonan,cmap=cmap,transform=trdata,norm=norm,vmin=vmin,vmax=vmax)
        
        if typlo=='contourf':
            cs  = plt.contourf(nav_lon, nav_lat, ehonan,transform=trdata,levels=levels,norm=norm,cmap=cmap,extend='both')

        if typlo=='scatter':
            print('Sorry, not implemented yet. Will be soon.')
            return

        if glo==False:
            #limits
            plt.xlim(xlim)
            plt.ylim(ylim) 

        # plot colorbar
        cb = plt.colorbar(cs, extend='both',  pad=0.04, orientation='horizontal', shrink=0.75)
        cb.ax.tick_params(labelsize=15) 
        cb.set_label(labelplt,size=15)
        ticks = np.linspace(levels.min(),levels.max(),Nbar)
        cb.set_ticks(ticks)
        new_tickslabels = ["%.2f" % i for i in ticks]
        cb.set_ticklabels(new_tickslabels)

        
def printdatestring(time,it):
        '''
        Read time in xarray (datetime64 format) and return date in a set format (string)

        Parameters:
        time is the time coordinnate of an xarray, converted to index. For example time as input can be time = air.time.to_index() where air is the xarray of the temperature.
        it is the time index of the date to read and print
        '''    
        
        ## imports
        # xarray
        import xarray as xr
        
        if (time.hour[it]<12):
            adh=str("0")
        else:
            adh=str()
        if (time.month[it]<10):
            adm=str("0")
        else:
            adm=str()
        if (time.day[it]<10):
            add=str("0")
        else:
            add=str()    
        return(str(time.year[it])+"-"+adm+str(time.month[it])+"-"+add+str(time.day[it])+" "+adh+str(time.hour[it])+":00")
