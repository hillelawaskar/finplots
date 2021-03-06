"""
Created on 05-Apr-2015

@author: vivejha
"""
#from . import log
import pandas as pd
import numpy as np

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc

from finplots.overlays import plot_sma
from finplots.overlays import plot_volume
from finplots.overlays import plot_bollinger_bands

from finplots.macd import plot_macd
from finplots.rsi import plot_rsi
from finplots.stochastics import plot_slow_stochastic

from finplots import style

# global settings
# plt.style.use('dark_background')
# plt.style.use('ggplot')
# changes the fontsize
matplotlib.rcParams.update({'font.size':10})

def candlestick_plot(df,
                     smas=[100, 50, 5 , 10],
                     style=style,
                     figsize=(18, 10),
                     rsi_setup = dict(period=14),
                     macd_setup = dict(slow=26, fast=12, ema=8),
                     bbands_setup = dict(period=20, multiplier=2),
                     sstoch_setup = dict(period=14, smoothing=3)
                     ):
    """ plot candlestick chart """

    fig = plt.figure(figsize=figsize, facecolor=style.face_color)  # 18, 10 for full screen

    # create main axis for charting prices
    ax1 = plt.subplot2grid((10,4), (0,0),
                           rowspan=6,
                           colspan=4,
                           axisbg=style.axis_bg_color)

    if 'volume' not in df:
        df['volume'] = np.zeros(len(df))
#   times = pd.date_range('2014-01-01', periods=l, freq='1d')
    df.date = pd.to_datetime(df.date)
    df.date = [mdates.date2num(d) for d in df.date]

    df = df[::-1]

    payload = df[['date', 'open', 'high', 'low', 'close', 'volume']].values
    candlestick_ohlc(ax1, payload, width=0.5, colorup=style.cdl_up_color, colordown=style.cdl_down_color)

    annotate_max(ax1, df)

    ax1.grid(True, alpha=style.grid_alpha, color=style.grid_color)
    plt.ylabel('Stock Price', color=style.label_color)

    # determines number of points to be displayed on x axis
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(50))
    ax1.yaxis.set_major_locator(mticker.MaxNLocator(15))

    # determines format of markers on the xaxis
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%d-%m-%y'))

    # label color
    ax1.yaxis.label.set_color(style.label_color)

    # tick params color
    ax1.tick_params(axis='y', colors=style.tick_color)

    # spine colors
    ax1.spines['bottom'].set_color(style.spine_color)
    ax1.spines['top'].set_color(style.spine_color)
    ax1.spines['left'].set_color(style.spine_color)
    ax1.spines['right'].set_color(style.spine_color)

    # make the x tick label invisible
    plt.setp(ax1.get_xticklabels(), visible=False)

    # OVERLAY SIMPLE MOVING AVERAGES
    for idx, period in enumerate(smas):
        ax1 = plot_sma(ax1, df,
                       period=period,
                       color=style.sma_colors[idx])

    # OVERLAY BOLLINGER BAND
    ax1 = plot_bollinger_bands(ax1, df, period=bbands_setup['period'], multiplier=bbands_setup['multiplier'])

    # OVERLAY VOLUME
    # it is important to plot volume after the simple moving
    # average to avoid a warning message 'no labelled objects found'
    if 'volume' in df:
        ax1 = plot_volume(ax1, df)

    # show tick params on right axis as well
    ax1.tick_params(labelright=True)

    # RELATIVE STRENGTH INDEX
    ax_rsi = plt.subplot2grid((10,4), (9,0),
                           rowspan=1,
                           colspan=4,
                           sharex=ax1,
                           axisbg=style.axis_bg_color)
    plot_rsi(ax_rsi, df, period=rsi_setup['period'])

    # MOVING AVERAGE CONVERGENCE DIVERGENCE
    ax_macd = plt.subplot2grid((10,4), (8,0),
                           rowspan=1,
                           colspan=4,
                           sharex=ax1,
                           axisbg=style.axis_bg_color)

    ax_macd = plot_macd(ax_macd, df,
                        slow=macd_setup['slow'],
                        fast=macd_setup['fast'],
                        ema=macd_setup['ema'])

    # SLOW STOCHASTIC
    # create axis for charting prices
    ax_sstoch = plt.subplot2grid((10,4), (6,0),
                           rowspan=2,
                           colspan=4,
                           sharex=ax1,
                           axisbg=style.axis_bg_color)

    ax_sstoch = plot_slow_stochastic(ax_sstoch, df,
                                     period=sstoch_setup['period'],
                                     smoothing=sstoch_setup['smoothing'])

    #
    # ema_fast, ema_slow, macd = moving_average_convergence_divergence(df.close)
    # ema9 = exponential_moving_average(macd, nema)
    #
    # # plot_macd(ax_macd, df, style=style, slow=macd_setup['slow'], fast=macd_setup['fast'], ema=macd_setup['nema'] )
    # ax3.plot(df.index, macd, linewidth=2, color='lime')
    # ax3.plot(df.index, ema9, linewidth=2, color='hotpink')
    #
    #
    #
    #
    # # FROM HERE
    # # prune the yaxis
    # ax3.yaxis.set_major_locator(mticker.MaxNLocator(nbins=3, prune='lower'))
    #
    # # print text
    # ax3.text(0.015, 0.95, 'MACD 12,26,9', va='top', color='white', transform=ax3.transAxes)
    # # put markers for signal line
    # # following line needs as many stuff as there are markers
    # # hence we have commented this out.
    # # ax_rsi.axes.yaxis.set_ticklabels([30, 70])
    #
    # #ax3.set_yticks([])
    #
    # # provide the yaxis range
    # #ax3.set_ylim(0, 100)
    #
    # # draw horizontal lines
    # # ax3.axhline(70, color=style.rsi_signal_line_color, alpha=style.rsi_signal_line_alpha)
    # # ax3.axhline(50, color=style.rsi_signal_line_color, alpha=style.rsi_signal_line_alpha)
    # #ax3.axhline(0, color='w')
    # # ax3.axhline(30, color=style.rsi_signal_line_color, alpha=style.rsi_signal_line_alpha)
    #
    # # fill color
    # div = macd - ema9
    # ax3.fill_between(df.index, div, 0, facecolor='deepskyblue', edgecolor='w', alpha=0.3)
    #
    # # ax3.fill_between(df.index, rsi_data, 30, where=(rsi_data<=30), facecolor=style.rsi_oversold_color)
    # # label color
    # ax3.yaxis.label.set_color(style.label_color)
    #
    # # spine colors
    # ax3.spines['bottom'].set_color(style.spine_color)
    # ax3.spines['top'].set_color(style.spine_color)
    # ax3.spines['left'].set_color(style.spine_color)
    # ax3.spines['right'].set_color(style.spine_color)
    #
    # # tick params color
    # ax3.tick_params(axis='y', colors='w')
    # ax3.tick_params(axis='x', colors='w')
    #
    # # plot the grids.
    # ax3.grid(True, alpha=style.grid_alpha, color=style.grid_color)
    # plt.ylabel('MACD', color=style.label_color)
    # plt.setp(ax3.get_xticklabels(), visible=False)
    # # Till here




    # make the labels a bit rotated for better visibility
    for label in ax_rsi.xaxis.get_ticklabels():
        label.set_rotation(45)

    # adjust the size of the plot
    #plt.subplots_adjust(left=0.10, bottom=0.19, right=0.93, top=0.95, wspace=0.20, hspace=0.0)
    plt.subplots_adjust(left=0.07, bottom=0.10, right=0.97, top=0.95, wspace=0.20, hspace=0.0)

    # plt.xlabel('Date', color=style.label_color)
    plt.suptitle('Stock Price Chart', color=style.label_color)

    plt.show()


def annotate_max(ax, df, text='Max'):
    #import ipdb; ipdb.set_trace()
    max = df.high.max()
    idx = df.high.tolist().index(max)
    ax.annotate(text,
                xy=(df.date[idx], df['high'][idx]),  # theta, radius
                xytext=(0.5, 1),    # fraction, fraction
                xycoords='data',
                textcoords='axes fraction',
                arrowprops=dict(facecolor='grey', shrink=0.05),
                horizontalalignment='left',
                verticalalignment='bottom',
                )

def marker(idx, ycord, text, orgin, color):
    pass

