import numpy as np
import constants as cs
import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt


class Calculate_VTEC:
    def __init__(self, timeline, VTEC, satNumber, signal_one, signal_two):                   
        self.plotting_VTEC(timeline, VTEC, satNumber, signal_one, signal_two)

    def plotting_VTEC(self, timeline, VTEC, satNumber, signal_one, signal_two):
        plt.plot(timeline, VTEC, label='Phase smoothed delay')
        plt.xlabel('Time (UTC)', fontsize=15)
        plt.ylabel('VTEC (TECU)', fontsize=15)
        plt.title("Ionosphere Delay at {0} on {1} for {2} ({3} & {4})".format(self.marker_name, self.date, satNumber, signal_one, signal_two), fontsize=14)

        plt.tick_params(axis='x', labelsize=8)
        plt.tick_params(axis='y', labelsize=8)
        plt.legend(loc='lower right', fontsize=12)
        ax = plt.gca()
        plt.ticklabel_format(style='plain', axis='y', scilimits=(0,0))
        plt.grid()
        plt.savefig(self.VTECpath + 'VTEC_{0}'.format(satNumber))
        plt.close()   
        
        print "VTEC PRN {0} generated.".format(satNumber)

        
        ###### MANUALLY SET ZOOM PARAMETERS ######
        sat_pool = ['G10']
        ylim_low = [5]
        ylim_high = [13]
        start = [4680]
        end = [7920]
        polyfit_degree = [6]
        
            
        if satNumber in sat_pool:
            item_index = sat_pool.index(satNumber)
            ylim_low_uniq = ylim_low[item_index]
            ylim_high_uniq = ylim_high[item_index]
            start_uniq = start[item_index]
            end_uniq = end[item_index]
            self.zoomed_in_VTECplot(timeline, VTEC, satNumber, signal_one, signal_two, ylim_low_uniq, ylim_high_uniq, start_uniq, end_uniq) 
        else:
            pass                
        ###### MANUALLY SET ZOOM PARAMETERS ######  
        
        
    def zoomed_in_VTECplot(self, timeline, VTEC, satNumber, signal_one, signal_two, ylim_low, ylim_high, start, end):
        linspaceNum = end-start
        VTEC = VTEC.values
        # Code to check for nans, so limits can be set in the zoom process
    #             if np.isnan(VTEC).any():
    #                 print np.argwhere(np.isnan(VTEC))
        
        xdata = timeline[start:end]
        ydata = VTEC[start:end]
        
        levelling_type = 'Polyfit'
        rm_window_size = 4
        polyfit_degree = 5
        
        coefficients = np.polyfit(xdata, ydata, polyfit_degree)
        polynomial = np.poly1d(coefficients)

        xs = np.linspace(xdata[0], xdata[-1], num=linspaceNum) 

        if levelling_type == 'Polyfit':
            ys = polynomial(xs)
            levelling_type = 'Polyfit ({0}$^\circ$)'.format(polyfit_degree)
        elif levelling_type == 'Moving Mean':
            ys = pd.rolling_mean(ydata, window=10)
            levelling_type = 'Moving mean (size={0})'.format(rm_window_size)
        # Following lines to ensure arrays are the same size. MAY NOT ALWAYS BE NECESSARY
        if len(xs) > len(xdata):
            ys = ys[:-1]
            xs = xs[:-1]
            
        residuals = ydata - ys            
        fig1 = plt.figure(1)
        frame1 = fig1.add_axes((.1, .3, .8, .6))
        plt.plot(xs, ys, 'r--', label=levelling_type)                                
        plt.plot(timeline, VTEC, 'blue', label='Phase smoothed delay')               
        plt.legend(loc='lower right', fontsize=12)
        plt.axvline(x=7.54, linewidth=3, color='grey', linestyle='--') 

        plt.title("Ionospheric Delay for {0}".format(satNumber), fontsize=20)

        plt.ylabel('VTEC (TECU)', fontsize=18)
        plt.xlim([xdata[0], xdata[-1]])
        plt.ylim(ylim_low, ylim_high)
        plt.tick_params(axis='y', labelsize=9)
        frame1.set_xticklabels([])
        plt.grid(True)

        frame2 = fig1.add_axes((.1, .1, .8, .2))
        # Next two lines prevents overlapping labels
        nbins = len(frame2.get_xticklabels())
        frame2.yaxis.set_major_locator(MaxNLocator(nbins=nbins, prune='upper'))
        plt.plot(xs, residuals, color='grey', marker = 'o', markersize=2, label='Residuals')
        plt.legend(loc='lower right', fontsize=12)
        plt.axvline(x=7.54, linewidth=3, color='grey', linestyle='--')
        plt.xlabel('UTC Time (hh.hh)', fontsize=18)
        plt.xlim([xdata[0], xdata[-1]])
        plt.ylim(-1.8, 1.8)
        plt.tick_params(axis='x', labelsize=10)
        plt.tick_params(axis='y', labelsize=10)
        plt.grid(True)
        
        ax = plt.gca()
        ax.ticklabel_format(useOffset=False)

        workspacePath = os.getcwd()
        pathList = workspacePath.split(os.sep)
        if 'iMac' in pathList:
            macpath_vtec = r'<your_path>'
            if not os.path.exists(macpath_vtec):
                os.makedirs(macpath_vtec)
        else:
            macpath_vtec = r'<your_path>'
            if not os.path.exists(macpath_vtec):
                os.makedirs(macpath_vtec)

        ax.autoscale(enable=False, axis='both', tight=None)
        ax.autoscale_view(tight=None, scalex=True, scaley=True)
        
        plt.savefig(self.vZOOMpath + 'Zoom_{0}'.format(satNumber), bbox_inches="tight")
        plt.close()
        print "VTEC ZOOM plot for PRN {0} generated".format(satNumber)



