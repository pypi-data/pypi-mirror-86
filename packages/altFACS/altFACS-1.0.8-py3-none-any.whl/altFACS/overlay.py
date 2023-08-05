import sys
import pandas as pd
import matplotlib.pyplot as plt

def overlayPlot(data1: pd.DataFrame, data2: pd.DataFrame, x_channel: str, y_channel: str, **kwargs):
    '''function to generate a plot comparing mean signal across a number of bins'''
    
    #Get **kwargs
    bins      = kwargs.get('bins', None)
    plot      = kwargs.get('plot', True)
    title     = kwargs.get('title', 'overlayPlot_figure.pdf')
    con_color = kwargs.get('con_color', 'lightgrey') 
    exp_color = kwargs.get('exp_color', 'green')
    x_label   = kwargs.get('x_label', x_channel)
    y_label   = kwargs.get('y_label', y_channel)
    labels    = kwargs.get('labels', ['control', 'experiment'])
    xlim      = kwargs.get('xlim', [-1000, 10000])
    ylim      = kwargs.get('ylim', [-1000, 10000])
    save      = kwargs.get('save', False)
    savepath  = kwargs.get('savepath', './')
    
    fig, ax = plt.subplots()
    
    if plot==False:
        plt.ioff()

    data1.plot(ax=ax, x=x_channel, y=y_channel, kind='scatter', c=con_color, alpha =0.1)
    data2.plot(ax=ax, x=x_channel, y=y_channel, kind='scatter', c=exp_color, alpha =0.1)

    #Bin data into 22 bins
    if bins is None:
        bins = list(range(-1000, 10000, 500))
        
    data1.loc[:,'bin'] = pd.cut(data1[x_channel], bins)
    data2.loc[:,'bin'] = pd.cut(data2[x_channel], bins)

    #Group by bin
    data1 = data1.groupby(by=['bin']).mean().reset_index()
    data2 = data2.groupby(by=['bin']).mean().reset_index()

    #for n, data in enumerate([data1, data2]):
    #    data.plot(ax=ax, kind='line', x=x_channel, y=y_channel, color=colors[n])
    data1.plot(ax=ax, kind='line', x=x_channel, y=y_channel, label=labels[0], color=con_color, xlim=xlim, ylim=ylim)
    data2.plot(ax=ax, kind='line', x=x_channel, y=y_channel, label=labels[1], color=exp_color, xlim=xlim, ylim=ylim)
        
    #Label Plot
    plt.xlabel(x_label);
    plt.ylabel(y_label);
    
    if save:
        plt.savefig(savepath+title)
    
    if plot==False:
        plt.close()

        
def shiftPlot(data, control_file_index, experiment_file_index, channel='646nm', **kwargs):
    
    x_limits       = kwargs.get('x_limits', (-1000, 8000))
    control_color  = kwargs.get('control_color', 'lightgrey')
    channel_colors = kwargs.get('channel_colors', {})
    
    control    = data[data.File.eq(control_file_index)]
    experiment = data[data.File.eq(experiment_file_index)]
    
    ##How do I overlay these?
    control[channel].plot.kde(color=control_color);
    experiment[channel].plot.kde(color=channel_colors.get(channel, 'k')); #default to black
    plt.xlabel(channel);
    plt.xlim(*x_limits);