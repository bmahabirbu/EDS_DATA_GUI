import sys
from scipy import stats
import pandas as pd
import numpy as np
import math
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook


def calc_soiling_rate(file_name, validator):
        if validator == 'Valid':
            df = pd.read_csv(file_name)
            df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
            labels = ['EDS1_PRE', 'EDS2_PRE', 'EDS3_PRE', 'EDS4_PRE', 'EDS5_PRE', 'CTRL1_PRE', 'CTRL2_PRE',
                      'EDS1_POST','EDS2_POST','EDS3_POST','EDS4_POST','EDS5_POST','CTRL1_POST','CTRL2_POST']
            # declare soiling index dictionary
            soiling_index = {
                'EDS1_PRE':[],
                'EDS2_PRE':[],
                'EDS3_PRE':[],
                'EDS4_PRE':[],
                'EDS5_PRE':[],
                'CTRL1_PRE':[],
                'CTRL2_PRE':[],
                'EDS1_POST':[],
                'EDS2_POST':[],
                'EDS3_POST':[],
                'EDS4_POST':[],
                'EDS5_POST':[],
                'CTRL1_POST':[],
                'CTRL2_POST':[],
            }
            # get the soiling index values
            data_SI = df[['EDS/CTRL(#)', 'SI_Before','SI_After']]
            data_SI.set_index('EDS/CTRL(#)', inplace=True)

            EDS1 = data_SI.loc[['EDS-PV1']]
            EDS2 = data_SI.loc[['EDS-PV2']]
            EDS3 = data_SI.loc[['EDS-PV3']]
            EDS4 = data_SI.loc[['EDS-PV4']]
            EDS5 = data_SI.loc[['EDS-PV5']]
            CTRL1 = data_SI.loc[['CTRL-PV1']]
            CTRL2 = data_SI.loc[['CTRL-PV2']]

            #SI Before
            EDS1_Pre = EDS1[['SI_Before']].values.flatten() #get numpy array and flatten to 1d
            soiling_index['EDS1_PRE'].extend(EDS1_Pre)#append to soiling index dictionary

            EDS2_Pre = EDS2[['SI_Before']].values.flatten()
            #EDS2_Pre = EDS2[EDS2.loc[~(EDS2==0).all(axis=1)]]
            soiling_index['EDS2_PRE'].extend(EDS2_Pre)

            EDS3_Pre = EDS3[['SI_Before']].values.flatten()
            #EDS3_Pre = EDS3[~np.isnan(EDS3_Pre)]
            soiling_index['EDS3_PRE'].extend(EDS3_Pre)

            EDS4_Pre = EDS4[['SI_Before']].values.flatten()
            #EDS4_Pre = EDS4[~np.isnan(EDS4_Pre)]
            soiling_index['EDS4_PRE'].extend(EDS4_Pre)

            EDS5_Pre = EDS5[['SI_Before']].values.flatten()
            #EDS5_Pre = EDS5[~np.isnan(EDS5_Pre)]
            soiling_index['EDS5_PRE'].extend(EDS5_Pre)

            CTRL1_Pre = CTRL1[['SI_Before']].values.flatten()
            soiling_index['CTRL1_PRE'].extend(CTRL1_Pre)

            CTRL2_Pre = CTRL2[['SI_Before']].values.flatten()
            soiling_index['CTRL2_PRE'].extend(CTRL2_Pre)

            #SI After
            EDS1_Post = EDS1[['SI_After']].values.flatten()
            EDS1_Post = EDS1_Post[~np.isnan(EDS1_Post)] # remove persistant nan values
            soiling_index['EDS1_POST'].extend(EDS1_Post)

            EDS2_Post = EDS2[['SI_After']].values.flatten()
            EDS2_Post = EDS2_Post[~np.isnan(EDS2_Post)]
            soiling_index['EDS2_POST'].extend(EDS2_Post)

            EDS3_Post = EDS3[['SI_After']].values.flatten()
            EDS3_Post = EDS3_Post[~np.isnan(EDS3_Post)]
            soiling_index['EDS3_POST'].extend(EDS3_Post)

            EDS4_Post = EDS4[['SI_After']].values.flatten()
            EDS4_Post = EDS4_Post[~np.isnan(EDS4_Post)]
            soiling_index['EDS4_POST'].extend(EDS4_Post)

            EDS5_Post = EDS5[['SI_After']].values.flatten()
            EDS5_Post = EDS5_Post[~np.isnan(EDS5_Post)]
            soiling_index['EDS5_POST'].extend(EDS5_Post)

            CTRL1_Post = CTRL1[['SI_After']].values.flatten() #did not remove nan since no ctrl post values
            #ctrl post values could be wanted in future if so add the code that will remove nan values
            soiling_index['CTRL1_POST'].extend(CTRL1_Post)

            CTRL2_Post = CTRL2[['SI_After']].values.flatten()
            soiling_index['CTRL2_POST'].extend(CTRL2_Post)

            # declare soiling rate dictionary
            soiling_rates = {
                'EDS1_PRE':0,
                'EDS2_PRE':0,
                'EDS3_PRE':0,
                'EDS4_PRE':0,
                'EDS5_PRE':0,
                'CTRL1_PRE':0,
                'CTRL2_PRE':0,
                'EDS1_POST':0,
                'EDS2_POST':0,
                'EDS3_POST':0,
                'EDS4_POST':0,
                'EDS5_POST':0,
                'CTRL1_POST':0,
                'CTRL2_POST':0,
            }
            print(soiling_index["EDS1_PRE"])
            # error check the data to make sure it can compute soiling rate
            for x in labels:
                if len(soiling_index[x])==0:
                    return "error"
                elif len(soiling_index[x])==1:
                    return "error"
            # calculate the soiling rate values
            for y in labels:
                soiling_rates[y] = stats.theilslopes(soiling_index[y], range(len(soiling_index[y])), 0.90)[0].round(2)
            # return the dictionary
            return soiling_rates
        else:
            print("yo mama")

def graph_isc(self, panel_list):
        
        data = self.df_load()
        
        #set ggplot style
        plt.style.use('ggplot')

        #plot data
        fig, ax = plt.subplots(figsize=(15,7))
        
        count = 0
        for edsname in panel_list:
            edsname = data.loc[[edsname]]
            edsname.set_index('Date', inplace=True)
            edsname = edsname[['Isc_Before(A)','Isc_After(A)']].ffill()
            ax.plot(edsname.index, edsname['Isc_Before(A)'],'o-',label="Pre "+str(panel_list[count]))
            ax.plot(edsname.index, edsname['Isc_After(A)'],'o-',label="Post "+str(panel_list[count]))
            count = count+1
            
        #set date as index
        data.set_index('Date',inplace=True)
            
        #Set x axis with date
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))

        ax.set_title('ISC graph')
        ax.set_ylabel('Current(A)')
        ax.set_xlabel('Date')
        plt.legend(loc='upper right')

        plt.show()
        
def graph_gpoa(self, panel_list):
    
    data = self.df_load()
    
    #set ggplot style
    plt.style.use('ggplot')

    #plot data
    fig, ax = plt.subplots(figsize=(15,7))
    
    count = 0
    for edsname in panel_list:
        edsname = data.loc[[edsname]]
        edsname.set_index('Date', inplace=True)
        edsname = edsname[['GPOA(W/M2)']].ffill()
        ax.plot(edsname.index, edsname['GPOA(W/M2)'],'o-',label="Pre "+str(panel_list[count]))
        count = count+1
        
    #set date as index
    data.set_index('Date',inplace=True)
    '''
    for x,y in zip(EDS_isc.index, EDS_isc['GPOA(W/M2)']):

        label = "{:.2f}".format(y)
        
        plt.annotate(label, # this is the text
                        (x,y), # these are the coordinates to position the label
                        textcoords="offset points", # how to position the text
                        xytext=(0,10), # distance from text to points (x,y)
                        ha='center') # horizontal alignment can be left, right or center
    '''
    #Set x axis with date
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))

    ax.set_title('GPOA(W/M2) graph')
    ax.set_ylabel('GPOA(W/M2)')
    ax.set_xlabel('Date')
    plt.legend(loc='upper right')

    plt.show()
    
def graph_voc(self, panel_list):
    
    data = self.df_load()
    
    #set ggplot style
    plt.style.use('ggplot')

    #plot data
    fig, ax = plt.subplots(figsize=(15,7))
    
    count = 0
    for edsname in panel_list:
        edsname = data.loc[[edsname]]
        edsname.set_index('Date', inplace=True)
        edsname = edsname[['Voc_Before(V)','Voc_After(V)']].ffill()
        ax.plot(edsname.index, edsname['Voc_Before(V)'],'o-',label="Pre "+str(panel_list[count]))
        ax.plot(edsname.index, edsname['Voc_After(V)'],'o-',label="Post "+str(panel_list[count]))
        count = count+1
    
    #set date as index
    data.set_index('Date',inplace=True)
        
    #Set x axis with date
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))
    
    ax.set_title('Voc(V) graph')
    ax.set_ylabel('Voltage(A)')
    ax.set_xlabel('Date')
    plt.legend(loc='upper right')

    plt.show()
    
def graph_pout(self, panel_list):
    
    data = self.df_load()
    
    #set ggplot style
    plt.style.use('ggplot')

    #plot data
    fig, ax = plt.subplots(figsize=(15,7))
    
    count = 0
    for edsname in panel_list:
        edsname = data.loc[[edsname]]
        edsname.set_index('Date', inplace=True)
        edsname = edsname[['Pout_Before(W)','Pout_After(W)']].ffill()
        ax.plot(edsname.index, edsname['Pout_Before(W)'],'o-',label="Pre "+str(panel_list[count]))
        ax.plot(edsname.index, edsname['Pout_After(W)'],'o-',label="Post "+str(panel_list[count]))
        count = count+1
        
    #set date as index
    data.set_index('Date',inplace=True)
        
    #Set x axis with date
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))
    
    ax.set_title('Power graph')
    ax.set_ylabel('Watts(W)')
    ax.set_xlabel('Date')
    plt.legend(loc='upper right')

    plt.show()
    


def graph_pr(self, panel_list):
    
    data = self.df_load()
    
    #set ggplot style
    plt.style.use('ggplot')

    #plot data
    fig, ax = plt.subplots(figsize=(15,7))
    
    count = 0
    for edsname in panel_list:
        edsname = data.loc[[edsname]]
        edsname.set_index('Date', inplace=True)
        edsname = edsname[['PR_Before','PR_After']].ffill()
        ax.plot(edsname.index, edsname['PR_Before'],'o-',label="Pre "+str(panel_list[count]))
        ax.plot(edsname.index, edsname['PR_After'],'o-',label="Post "+str(panel_list[count]))
        count = count+1
        
    #set date as index
    data.set_index('Date',inplace=True)
        
    #Set x axis with date
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))
    
    ax.set_title('Preformance Ratio graph')
    ax.set_ylabel('%')
    ax.set_xlabel('Date')
    plt.legend(loc='upper right')

    plt.show()
    
def graph_si(self, panel_list):
    
    data = self.df_load()
    
    #set ggplot style
    plt.style.use('ggplot')

    #plot data
    fig, ax = plt.subplots(figsize=(15,7))
    
    count = 0
    for edsname in panel_list:
        edsname = data.loc[[edsname]]
        edsname.set_index('Date', inplace=True)
        edsname = edsname[['SI_Before','SI_After']].ffill()
        ax.plot(edsname.index, edsname['SI_Before'],'o-',label="Pre "+str(panel_list[count]))
        ax.plot(edsname.index, edsname['SI_After'],'o-',label="Post "+str(panel_list[count]))
        count = count+1
        
    #set date as index
    data.set_index('Date',inplace=True)
        
    #Set x axis with date
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))
    

    ax.set_title('Solar Index graph')
    ax.set_ylabel('%')
    ax.set_xlabel('Date')
    plt.legend(loc='upper right')

    plt.show()