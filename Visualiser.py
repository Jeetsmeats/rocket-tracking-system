# Imports
import numpy as np
from numpy.fft import fft, fftshift
import matplotlib.pyplot as plt
import matplotlib as mpl
import matplotlib.animation as animation
from time import sleep

class Visualiser(object):
    """_summary_
    
    Visualisation of data stream
    """
    
    def __init__(self, NUM_DEVICES, N, SAMPLE_RATE, SDR_NAMES, PLOT_SAMPLES=None, NUM_SAMPLES=None):
        """_summary_

        Args:
            NUM_DEVICES (_type_): _description_
            N (_type_): _description_
            SAMPLE_RATE (_type_): _description_
            SDR_NAMES (_type_): _description_
            PLOT_SAMPLES (_type_, optional): _description_. Defaults to None.
            NUM_SAMPLES (_type_, optional): _description_. Defaults to None.
        """
        
        # Properties
        if NUM_SAMPLES is not None and PLOT_SAMPLES is not None:
            self.NUM_SAMPLES = NUM_SAMPLES
            self.PLOT_SAMPLES = PLOT_SAMPLES
            
        self.NUM_DEVICES = NUM_DEVICES
        self.N = N
        self.SAMPLE_RATE = SAMPLE_RATE
        self.SDR_NAMES = SDR_NAMES
        
        self.plots = []
        
        # Set up the animation plot for all figures
        n_plot_types = 3
        self.sup_figure, self.sup_axis = plt.subplots(n_plot_types, self.NUM_DEVICES, constrained_layout=True)
        
        mpl.rcParams['mathtext.fontset'] = 'cm'
        mpl.rcParams['mathtext.rm'] = 'serif'
        
    def argand_diagram(self, input, ax):
        """_summary_

        Args:
            input (_type_): _description_
            ax (_type_): _description_
        """
        for x in range(len(input)):
            
            val = input[x]
            ax.plot([0, val.real],[0, val.imag],'r.',markersize=2)
    
    def argand_diagram_reset(self, input, p):
        """_summary_

        Args:
            input (_type_): _description_
            p (_type_): _description_
        """
        
        for x in range(len(input)):
            
            val = input[x]
            p.set_data([0, val.real],[0, val.imag])
            
    def plot_IQ_constellation(self, title, data):
        """_summary_

        Plot the argand diagram.
        Args:
            figure_name (_type_): _description_
            data (_type_): _description_
        """
        
        fig, ax = plt.subplots(self.PLOT_SAMPLES, self.NUM_DEVICES, constrained_layout=True)
                
        # Figure title
        fig.suptitle(title)
        
        for device_num in range(self.NUM_DEVICES): 
            for p_sample, sample_num in enumerate(range((self.NUM_SAMPLES - self.PLOT_SAMPLES), self.NUM_SAMPLES)):
                
                # Data for each sample
                y = data[device_num][sample_num]                       

                # Plot Data
                self.argand_diagram(y, ax[p_sample][device_num])     
                
                # Plot Labels
                ax[p_sample][device_num].set_title(f'{self.SDR_NAMES[device_num]} (Sample {sample_num + 1})')
                ax[p_sample][device_num].set_xlabel('Real')
                ax[p_sample][device_num].set_ylabel('Imaginary')
            
                # Grid Lines
                ax[p_sample][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
                ax[p_sample][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
                
                limit = 1.5                                     # Set axis limits
                ax[p_sample][device_num].set_xlim((-limit,limit))
                ax[p_sample][device_num].set_ylim((-limit,limit))
    
    def plot_fft(self, title, fft, f):
        """_summary_
        
        Plot the absolute FFT diagram
        Args:
            figure_name (_type_): _description_
            fft (_type_): _description_
            f (_type_): _description_
        """
        
        # Get figure and axes
        fig, ax = plt.subplots(self.PLOT_SAMPLES, self.NUM_DEVICES, constrained_layout=True)
        
        # Figure title
        fig.suptitle(title)

        f = f / (10 ** 6)                                           # Frequency in MHz        
        
        for device_num in range(self.NUM_DEVICES): 
            for p_sample, sample_num in enumerate(range((self.NUM_SAMPLES - self.PLOT_SAMPLES), self.NUM_SAMPLES)):
                
                # FFT for each sample
                y = fft[device_num][sample_num]   
                y_shifted = fftshift(y)
                y_shifted = np.abs(y_shifted) / (self.N * self.SAMPLE_RATE)
                
                # Plot Data
                ax[p_sample][device_num].plot(f, y_shifted, color='blue')      
                
                # Plot Labels
                ax[p_sample][device_num].set_title(f'{self.SDR_NAMES[device_num]} (Sample {sample_num + 1})')
                ax[p_sample][device_num].set_xlabel('$f (MHz)$')
                ax[p_sample][device_num].set_ylabel('Magnitude')
            
                # Grid Lines
                ax[p_sample][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
                ax[p_sample][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
                    
    def plot_psd(self, title, fft, f):
        """_summary_
        
        Plot the Power Spectral Density.
        Args:
            title (_type_): _description_
            fft (_type_): _description_
            data (_type_): _description_
            f (_type_): _description_
        """
        
        # Get figure and axes
        fig, ax = plt.subplots(self.PLOT_SAMPLES, self.NUM_DEVICES, constrained_layout=True)
        
        # Figure title
        fig.suptitle(title)

        f = f / (10 ** 6)                                           # Frequency in MHz        

        for device_num in range(self.NUM_DEVICES): 
            for p_sample, sample_num in enumerate(range((self.NUM_SAMPLES - self.PLOT_SAMPLES), self.NUM_SAMPLES)):
                
                # FFT for each sample
                y = fft[device_num][sample_num]   
                y_shifted = fftshift(y)
                
                PSD = np.abs(y_shifted) / (self.N * self.SAMPLE_RATE)
                PSD_log = 20.0 * np.log10(PSD)
                
                # Plot Data
                ax[p_sample][device_num].plot(f, PSD_log, color='blue')      
                
                # Plot Labels
                ax[p_sample][device_num].set_title(f'{self.SDR_NAMES[device_num]} (Sample {sample_num + 1})')
                ax[p_sample][device_num].set_xlabel('$f (MHz)$')
                ax[p_sample][device_num].set_ylabel('Magnitude (dB)')
            
                # Grid Lines
                ax[p_sample][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
                ax[p_sample][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
    
    def create_figure(self, title):
        """_summary_

        Create a super figure including all relevant plots.
        Args:
            title (_type_): _description_
        """
        
        # Figure title
        self.sup_figure.suptitle(title)
        
        # Set plot labels
        for device_num in range(self.NUM_DEVICES):
            
            # Sub plot (IQ Constellation)
            self.sup_axis[0][device_num].set_title(f'{self.SDR_NAMES[device_num]}')
            self.sup_axis[0][device_num].set_xlabel('Real')
            self.sup_axis[0][device_num].set_ylabel('Imaginary')
            
            self.sup_axis[0][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
            self.sup_axis[0][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
            
            limit = 1.5                                     # Set axis limits
            self.sup_axis[0][device_num].set_xlim((-limit,limit))
            self.sup_axis[0][device_num].set_ylim((-limit,limit))
            
            # Sub plot (FFT)
            self.sup_axis[1][device_num].set_title(f'{self.SDR_NAMES[device_num]}')
            self.sup_axis[1][device_num].set_xlabel('$f (MHz)$')
            self.sup_axis[1][device_num].set_ylabel('Magnitude')
            
            self.sup_axis[1][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
            self.sup_axis[1][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)
            
            # Sub plot (PSD)
            self.sup_axis[2][device_num].set_title(f'{self.SDR_NAMES[device_num]}')
            self.sup_axis[2][device_num].set_xlabel('$f (MHz)$')
            self.sup_axis[2][device_num].set_ylabel('Magnitude (dB)')
            
            self.sup_axis[2][device_num].grid(which='major', color='#DDDDDD', linewidth=0.8)
            self.sup_axis[2][device_num].grid(which='minor', color='#EEEEEE', linestyle=':', linewidth=0.5)

            plot1, = self.sup_axis[0][device_num].plot([], [], 'r.', markersize=2)
            plot2, = self.sup_axis[1][device_num].plot([], [], 'b')
            plot3, = self.sup_axis[2][device_num].plot([], [], 'b')
            
            # Add empty plots
            self.plots.append([plot1, plot2, plot3]) 
        
        plt.ion()
        
    def plot_all(self, fft, data, f):
        """_summary_

        Real time plotting function.
        Args:
            title (_type_): _description_
            fft (_type_): _description_
            data (_type_): _description_
            f (_type_): _description_
        """
        
        f = f / (10 ** 6)                                           # Frequency in MHz        
        
        # Create the figures
        for device_num in range(self.NUM_DEVICES): 
            
            # Erase previous plot
            # self.sup_axis[0][device_num].clear()
            # self.sup_axis[1][device_num].clear()
            # self.sup_axis[2][device_num].clear()
            
            # Raw Data
            data_sample = data[device_num]
            
            # FFT for each sample
            fft_sample = fft[device_num]
            fft_sample = fftshift(fft_sample)
            
            fft_abs = np.abs(fft_sample) / (self.N * self.SAMPLE_RATE)              # Absolute value of s-domain data
            
            # Power Spectral Density (PSD)            
            PSD = np.abs(fft_sample) / (self.N * self.SAMPLE_RATE)
            # PSD_log = 20.0 * np.log10(PSD)

            # Plot IQ Constellation
            self.argand_diagram_reset(data_sample, self.plots[device_num][0])     
        
            # Plot FFT
            self.plots[device_num][1].set_data(f, fft_abs)      
      
            # Plot PSD
            self.plots[device_num][2].set_data(f, PSD) 

            plt.draw()
        sleep(0.5)
