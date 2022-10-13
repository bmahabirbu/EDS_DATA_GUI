import sys
import tkinter
import customtkinter
from scipy import stats
from tkinter import filedialog
import pandas as pd
import numpy as np
import math
import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import PIL.Image
import PIL.ImageTk
import os
from sklearn.linear_model import LinearRegression

try:
    from tkinter import *
    #from tkintertable import TableCanvas, TableModel
except ImportError:
    pass

PATH = os.path.dirname(os.path.realpath(__file__))

customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green


'''MAIN GUI CLASS FOR EDS ANALYSIS'''
class EDS:
    '''INSTANTIATION'''
    def __init__(self, root):
        # initialize the application
        self.root = root
        self.root.title("EDS Data Analysis Tool")
        self.root.geometry("650x550")


        '''CONSTANTS'''
        # header constants from the csv files
        self.testing_cols_list = ['Temperature(C)', 'Humidity(%)', 'GPOA(W/M2)', 'Voc_Before(V)', 'Voc_After(V)',
                                 'Isc_Before(A)', 'Isc_After(A)', 'Pout_Before(W)', 'Pout_After(W)', 
                                 'PR_Before', 'PR_After', 'SI_Before', 'SI_After']
        
        # global variables
        self.mode = ''
        self.filepath = ''
        self.window = 1
        

        '''LABELS'''
        # labels for the program title
        self.title_label = customtkinter.CTkLabel(root, text="EDS DATA ANALYSIS TOOL", text_font=("Helvetica", 20))
        self.title_label.grid(row=0, column=0, padx=10,pady=15, sticky=W)
        
        #self.Panel1 = customtkinter.CTkLabel(root, text="Panel 1", text_font=("Arial", 16))
        #self.Panel1.grid(row=2, column=0, columnspan=3, padx=70, pady=20, sticky=N+W)
        
        #self.Panel2 = customtkinter.CTkLabel(root, text="Panel 2", text_font=("Arial", 16))
        #self.Panel2.grid(row=2, column=0, columnspan=3, padx=70, pady=50, sticky=N+W)
        
        self.raw_data_selector = customtkinter.CTkLabel(root, text="Please Select Panel and Raw Data to Graph", text_font=("Arial", 16))
        self.raw_data_selector.grid(row=2, column=0, columnspan=3, padx=10, pady=195, sticky=N+W)
        
        # load image with PIL and convert to PhotoImage
        image = PIL.Image.open(PATH + "\Sol-Clarity-Logo.png").resize((200, 100))
        self.bg_image = PIL.ImageTk.PhotoImage(image)

        self.image_label = tkinter.Label(master=root, image=self.bg_image)
        self.image_label.place(relx=0.6, rely=0.6, anchor=tkinter.NW)
        
        # labels for showing testing/manual/noon mode
        self.eds_label = customtkinter.CTkLabel(root, text="Data Check", text_font=("Arial", 14), borderwidth=1.4, relief="solid", width=18, height=3)
        self.eds_label.grid(row=1, column=0)

        '''BUTTONS'''
        # button to get the path of the data csv file
        self.file_btn = customtkinter.CTkButton(root, text="Find CSV File", text_font=("Arial", 14), command= self.find_file, borderwidth=2, relief="raised")
        self.file_btn.grid(row=2, column=0, columnspan=3, padx=20, pady=20, sticky=N+W)

        # button to display soiling rate values
        self.sr_btn = customtkinter.CTkButton(root, text="Get Soiling Rates", text_font=("Arial", 14), command= self.show_sr)
        self.sr_btn.grid(row=2, column=0, columnspan=3, padx=20, pady=80, sticky=N+W)
        
        self.opr_btn = customtkinter.CTkButton(root, text="Get OPR", text_font=("Arial", 14), command= self.show_opr)
        self.opr_btn.grid(row=2, column=0, columnspan=3, padx=20, pady=120, sticky=N+W)\
        
        self.cmp_btn = customtkinter.CTkButton(root, text="EDS Panel Efficiency", text_font=("Arial", 14), command= self.cmp_restored)
        self.cmp_btn.grid(row=2, column=0, columnspan=3, padx=20, pady=160, sticky=N+W)
        
        # create button to plot the table
        self.plot_btn = customtkinter.CTkButton(root, text="Submit", text_font=("Arial", 14), command= self.plot_raw)
        self.plot_btn.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=280, padx=160)
        
        '''ENTRY FIELDS'''
        # entry field to display path for data csv file
        self.file_entry = customtkinter.CTkEntry(root, width=320)
        self.file_entry.grid(row=2, column=0, columnspan=3, padx=175, pady=20, sticky=N+W)
        
        '''Check Box'''
        # Dictionary with options
        choices = ['EDS-PV1','EDS-PV2','EDS-PV3','EDS-PV4','EDS-PV5','CTRL-PV1','CTRL-PV2','User-Data']
        
        self.box_1 = customtkinter.CTkCheckBox(master=self.root,
                                                    text="EDS-PV1",
                                                    onvalue="EDS-PV1",
                                                    offvalue="",
                                                    text_font=("Arial", 12))
        self.box_1.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=240, padx=10)
        
        self.box_2 = customtkinter.CTkCheckBox(master=self.root,
                                                     text="EDS-PV2",
                                                     onvalue="EDS-PV2",
                                                     offvalue="",
                                                     text_font=("Arial", 12))
        self.box_2.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=270, padx=10)
        
        self.box_3 = customtkinter.CTkCheckBox(master=self.root,
                                                     text="EDS-PV3",
                                                     onvalue="EDS-PV3",
                                                     offvalue="",
                                                     text_font=("Arial", 12))
        self.box_3.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=300, padx=10)
        
        self.box_4 = customtkinter.CTkCheckBox(master=self.root,
                                                     text="EDS-PV4",
                                                     onvalue="EDS-PV4",
                                                     offvalue="",
                                                     text_font=("Arial", 12))
        self.box_4.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=330, padx=10)
        
        self.box_5 = customtkinter.CTkCheckBox(master=self.root,
                                                     text="EDS-PV5",
                                                     onvalue="EDS-PV5",
                                                     offvalue="",
                                                     text_font=("Arial", 12))
        self.box_5.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=360, padx=10)
        
        self.box_6 = customtkinter.CTkCheckBox(master=self.root,
                                                     text="CTRL-PV1",
                                                     onvalue="CTRL-PV1",
                                                     offvalue="",
                                                     text_font=("Arial", 12))
        self.box_6.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=390, padx=10)
        
        self.box_7 = customtkinter.CTkCheckBox(master=self.root,
                                                     text="CTRL-PV2",
                                                     onvalue="CTRL-PV2",
                                                     offvalue="",
                                                     text_font=("Arial", 12))
        self.box_7.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=420, padx=10)
        
        
        #Drop down for raw data
        # Dictionary with options
        choices = [ 'GPOA', 'Voc', 'Isc', 'Pout', 'PR', 'SI']
        self.raw_data_selection = customtkinter.CTkOptionMenu(root, text_font=("Arial", 14), values=choices)
        self.raw_data_selection.grid(row=2, column=0, columnspan=3, sticky=N+W, pady=240, padx=160)

    '''Button Functions'''
    # function to get csv file path
    def find_file(self):
        # clear the entry field
        self.file_entry.delete(0, END)
        # clear the color for the testing modes
        self.clear_mode_buttons()
        # get the path for the csv file
        self.root.filename = filedialog.askopenfilename(initialdir=".", title="Select A CSV File", 
                                                        filetypes=(("CSV Files", "*.csv"),("All Files", "*.*")))
        self.filepath = self.root.filename 
        # insert the path to the entry field
        self.file_entry.insert(0, root.filename)
        # based on path, figure out which mode
        self.mode = root.filename.split("/")[-1]
        if self.mode == 'eds_data.csv':
            self.eds_label.config(bg="green")
        else:
            self.eds_label.config(bg="red")
    
    def show_opr(self):
        # new window for soiling rate data
        self.opr_window = customtkinter.CTkToplevel()
        self.opr_window.geometry("600x600")
        self.opr_title = customtkinter.CTkLabel(self.opr_window, text="OPR Values:", text_font=("Arial", 18)).pack()
        if self.mode == 'eds_data.csv':
                avg_data1, graph_data1 = self.calc_opr("EDS-PV1")
                avg_data2, graph_data2 = self.calc_opr("EDS-PV2")
                avg_data3, graph_data3 = self.calc_opr("EDS-PV3")
                avg_data4, graph_data4 = self.calc_opr("EDS-PV4")
                avg_data5, graph_data5 = self.calc_opr("EDS-PV5")
                # prepare the label message
                opr1 = str("EDS-PV1")+" Average OPR: " +str(avg_data1)
                opr2 = str("EDS-PV2")+" Average OPR: " +str(avg_data2)
                opr3 = str("EDS-PV3")+" Average OPR: " +str(avg_data1)
                opr4 = str("EDS-PV4")+" Average OPR: " +str(avg_data2)
                opr5 = str("EDS-PV5")+" Average OPR: " +str(avg_data1)
                message = opr1 + '\n' + opr2 + '\n' + opr3 + '\n' + opr4 + '\n'  + opr5
                # display the message
                opr_contents = customtkinter.CTkLabel(self.opr_window, text=message, text_font=("Arial", 14)).pack()
        else:
            #display error in the new window
            self.error_msg = customtkinter.CTkLabel(self.opr_window, text="Please Select Valid CSV File For Analysis", fg = 'red', text_font=("Arial", 14)).pack()

    def cmp_restored(self):
        
        self.cmp_window = customtkinter.CTkToplevel()
        self.cmp_window.geometry("600x600")
        self.cmp_title = customtkinter.CTkLabel(self.cmp_window, text="Average of Power(W) Difference per Activation:", text_font=("Arial", 18)).pack()
        
        if self.mode == 'eds_data.csv':
            edspanels = ['EDS-PV1','EDS-PV2','EDS-PV3','EDS-PV4','EDS-PV5']
            data = pd.read_csv(self.filepath, parse_dates=['Date'])
            data.set_index('EDS/CTRL(#)', inplace=True)

            #get average temp and humidity
            data['Temperature(C)'] = pd.to_numeric(data['Temperature(C)'], errors='coerce')
            data['Humidity(%)'] = pd.to_numeric(data['Humidity(%)'], errors='coerce')
            temp_humid_avg = data[['Temperature(C)', 'Humidity(%)']].mean(axis='index').tolist()

            #Locate each eds panels pout before and after data
            
            edspanelframe_1 = data.loc[['EDS-PV1']]
            edspanelframe_1_pout = edspanelframe_1[['Pout_Before(W)','Pout_After(W)']]
            edspanelframe_1_pout = edspanelframe_1_pout.reset_index()
            edspanelframe_1_pout = edspanelframe_1_pout.drop(['EDS/CTRL(#)'], axis=1)
            #edspanelframe_1.set_index('Date', inplace=True)
            
            edspanelframe_2 = data.loc[['EDS-PV2']]
            edspanelframe_2_pout = edspanelframe_2[['Pout_Before(W)','Pout_After(W)']]
            edspanelframe_2_pout = edspanelframe_2_pout.reset_index()
            edspanelframe_2_pout = edspanelframe_2_pout.drop(['EDS/CTRL(#)'], axis=1)
            #edspanelframe_2.set_index('Date', inplace=True)
            
            edspanelframe_3 = data.loc[['EDS-PV3']]
            edspanelframe_3_pout = edspanelframe_3[['Pout_Before(W)','Pout_After(W)']]
            edspanelframe_3_pout = edspanelframe_3_pout.reset_index()
            edspanelframe_3_pout = edspanelframe_3_pout.drop(['EDS/CTRL(#)'], axis=1)
            #edspanelframe_3.set_index('Date', inplace=True)
            
            edspanelframe_4 = data.loc[['EDS-PV4']]
            edspanelframe_4_pout = edspanelframe_4[['Pout_Before(W)','Pout_After(W)']]
            edspanelframe_4_pout = edspanelframe_4_pout.reset_index()
            edspanelframe_4_pout = edspanelframe_4_pout.drop(['EDS/CTRL(#)'], axis=1)
            #edspanelframe_4.set_index('Date', inplace=True)
            
            edspanelframe_5 = data.loc[['EDS-PV5']]
            edspanelframe_5_pout = edspanelframe_5[['Pout_Before(W)','Pout_After(W)']]
            edspanelframe_5_pout = edspanelframe_5_pout.reset_index()
            edspanelframe_5_pout = edspanelframe_5_pout.drop(['EDS/CTRL(#)'], axis=1)
            #edspanelframe_5.set_index('Date', inplace=True)
            
            #Concact all dataframes into one
            
            edspanelframe = pd.concat([edspanelframe_1_pout, edspanelframe_2_pout, edspanelframe_3_pout, edspanelframe_4_pout, edspanelframe_5_pout], axis=1, ignore_index=True)
            #Zscore outlier remover
            edspanelframe_zscore = edspanelframe[np.abs((edspanelframe - edspanelframe.mean())/edspanelframe.std(ddof=0)) < 3]

            #Calculate mean of each column
            edspanelframe_avg = edspanelframe_zscore.mean(axis='index').tolist()
            
            perc_inc_avg = []
            kwh_dif = 0
            p_generate = 0

            #Percentage increase
            for i in range(0,len(edspanelframe_avg),2):
                avg_post = edspanelframe_avg[i]
                avg_pre = edspanelframe_avg[i+1]
                inc = ((avg_post-avg_pre) / (avg_pre))*100
                #Electricity Saved scaled to 100kwh (current FTU is at 125 watt) scale is 800 times more
                #Lets say on average that the watt measured is generated at that rate for at least 3 hours
                kwh_dif += ((((avg_post-avg_pre)/1000)*800*3))
                p_generate += ((((avg_post-avg_pre)/1000)*800))
                perc_inc_avg.append(inc)

            kwh_money_saved = ((kwh_dif)*21.85)
            message = "\n"
            counter = 1
            
            for perc in perc_inc_avg:
                perc_str = "EDS-PV"+(str(counter))+" efficiency = "+str(format(perc, '.2f'))+"%\n"
                message += perc_str
                counter += 1
            
            #Electricity Saved

            message += "\n Scaled to 100 KW\n"
            message += "\n Electricty saved  = "+str(format(kwh_dif, '.2f'))+" KWH \n Money saved 21.85 ¢/kWh = $"+str(format(kwh_money_saved, '.2f'))+"\n"

            #Water saved

            h20 = ((p_generate)*24)*0.264172*1.01
            h20_money_saved = h20*0.8

            #1KW = 24 liters per year
            #20 gallons per megawatt hour
            #https://docs.google.com/spreadsheets/d/1v-2COFxeCa61EBgZ4hPeFGDcaJuCKz0N/edit#gid=493027415

            message += "\n Equivalent Water usage per KW = "+str(format(h20, '.2f'))+" Gallons \n Money saved 8¢ per gallon = $"+str(format(h20_money_saved, '.2f'))+"\n"

            #Temperature and Humidity average

            message += "\n Average Temperature = "+str(format(temp_humid_avg[0], '.2f'))+" C\n Average Humidity  = "+str(format(temp_humid_avg[1], '.2f')+"%")
            
            #"per 1000 gallons 7.967$ for first 19"
            #"21.85 ¢/kWh"
            #"Ryan prices"
            #"17.9 ¢/kWh"

            # display the message
            cmp_contents = customtkinter.CTkLabel(self.cmp_window, text=message,text_font=("Arial", 14)).pack()

            #Graph chart
            for edsname in edspanels:
                self.graph_pout_diff(edsname)
            plt.show()
            
            
            
            
            
        else:
            #display error in the new window
            self.error_msg = Label(self.cmp_window, text="Please Select Valid CSV File For Analysis", fg = 'red').pack()

                
    def show_sr(self):
        # new window for soiling rate data
        self.sr_window = customtkinter.CTkToplevel()
        self.sr_window.geometry("600x600")
        self.sr_title = customtkinter.CTkLabel(self.sr_window, text="Soiling Rate Values:", text_font=("Arial", 18)).pack()
        if self.mode == 'eds_data.csv':
            data = self.calc_soiling_rate(self.mode)
            # error check the calculation
            if data == "error":
                #display error in the new window
                self.error_msg = Label(self.sr_window, text="Data is wrong", fg = 'red').pack()
            else:
                # prepare the label message
                eds1 = "EDS1 Soiling Rate: " + str(data['EDS1_PRE']) + "%(PRE), " + str(data['EDS1_POST']) + "%(POST)"
                eds2 = "EDS2 Soiling Rate: " + str(data['EDS2_PRE']) + "%(PRE), " + str(data['EDS2_POST']) + "%(POST)"
                eds3 = "EDS3 Soiling Rate: " + str(data['EDS3_PRE']) + "%(PRE), " + str(data['EDS3_POST']) + "%(POST)"
                eds4 = "EDS4 Soiling Rate: " + str(data['EDS4_PRE']) + "%(PRE), " + str(data['EDS4_POST']) + "%(POST)"
                eds5 = "EDS5 Soiling Rate: " + str(data['EDS5_PRE']) + "%(PRE), " + str(data['EDS5_POST']) + "%(POST)"
                ctrl1 = "CTRL1 Soiling Rate: " + str(data['CTRL1_PRE']) + "%(PRE), " + str(data['CTRL1_POST']) + "%(POST)"
                ctrl2 = "CTRL2 Soiling Rate: " + str(data['CTRL2_PRE']) + "%(PRE), " + str(data['CTRL2_POST']) + "%(POST)"
                message = eds1 + '\n' + eds2 + '\n' + eds3 + '\n' + eds4 + '\n' + eds5 + '\n' + ctrl1 + '\n' + ctrl2
                # display the message
                sr_contents = customtkinter.CTkLabel(self.sr_window, text=message,text_font=("Arial", 14)).pack()
        else:
            #display error in the new window
            self.error_msg = customtkinter.CTkLabel(self.sr_window, text="Please Select Valid CSV File For Analysis", fg = 'red').pack()
    
    # plot the table
    def plot_raw(self):
        # check which mode selected
        if self.mode == 'eds_data.csv':
            
            panel_list = []
            
            panel_list.append(self.box_1.get())
            panel_list.append(self.box_2.get())
            panel_list.append(self.box_3.get())
            panel_list.append(self.box_4.get())
            panel_list.append(self.box_5.get())
            panel_list.append(self.box_6.get())
            panel_list.append(self.box_7.get())
            panel_list = list(filter(None, panel_list))
            
            if not panel_list :
                print('Please make a selection!')
                return
                
            
            if self.raw_data_selection.get() == 'Isc':
    
                self.graph_isc(panel_list)
                    
            elif self.raw_data_selection.get() == 'GPOA':
                
                self.graph_gpoa(panel_list)
            
            elif self.raw_data_selection.get() == 'Voc':
               
               self.graph_voc(panel_list)
                
            elif self.raw_data_selection.get() == 'Pout':
                
                self.graph_pout(panel_list)
                
            elif self.raw_data_selection.get() == 'PR':
                
                self.graph_pr(panel_list)
                
            elif self.raw_data_selection.get() == 'SI':
                
                self.graph_si(panel_list)
       
        else:
            print('Please Enter CSV first!')

    '''Non Button Functions'''
    # function to clear the mode buttons
    def average(self, lst):
        return sum(lst) / len(lst)

    
    def calc_opr(self, edsname):
        
        df = pd.read_csv(self.filepath, parse_dates=['Date'])
        df.set_index('EDS/CTRL(#)', inplace=True)
        EDS = df.loc[[edsname]]
        EDS_isc = EDS[['Isc_Before(A)','Isc_After(A)']].dropna()
        EDS_isc_values = EDS_isc.values
        count = 0
        opr = []
        isc_og = 0
        for isc_before, isc_after in EDS_isc_values:
            if count == 0:
                isc_og = 0.68
                opr.append((isc_after-isc_before)/(isc_og-isc_before)*100)
                isc_og = isc_after
            else:
                opr.append((isc_after-isc_before)/(isc_og-isc_before)*100)
                isc_og = isc_after
            count = count + 1
        opr_neo = [x for x in opr if np.isfinite(x) == True]
        avg_opr = self.average(opr_neo)
        return avg_opr, opr_neo

    def clear_mode_buttons(self):
        self.eds_label.config(bg="white")
        #self.manual_label.config(bg="white")
        #self.noon_label.config(bg="white")
    
    # load sorted data as pandas dataframe
    def load_sorted(self,name):
        # file location for the csv file
        file = name
        # return pandas dataframe of the csv file
        df = pd.read_csv(file)
        # remove all NaN entries
        df.drop(df.filter(regex="Unname"),axis=1, inplace=True)
        return df
    
    # function to calculate the soiling rate of the table's data
    def calc_soiling_rate(self, mode):
        # check which mode of operation
        if self.mode == 'eds_data.csv':
            # get the file to find the soiling rate
            df = self.load_sorted(self.filepath)
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
            # error check the data to make sure it can compute soiling rate
            for x in labels:
                if len(soiling_index[x])==0:
                    return "error"
                elif len(soiling_index[x])==1:
                    return "error"
            # calculate the soiling rate values
            for y in labels:
                soiling_rates[y] = stats.theilslopes(soiling_index[y], np.arange(len(soiling_index[y])), 0.90)[0].round(2)
            # return the dictionary
            return soiling_rates
        elif self.mode == 'testing_data.csv':
            # update the soiling rate value
            self.sr_label.config(text= "Soiling Rate: N/A (This mode does not measure SR)")
        else:
            # return error
            self.error_label.config(text="Select Valid CSV File For Analysis")
    
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
    def graph_pout_diff(self, edsname):
        data = self.df_load()
        
        #set ggplot style
        plt.style.use('ggplot')

        #plot data
        fig, ax = plt.subplots(figsize=(7,4))
        
        data_diff = data.loc[[edsname]]
        data_diff.set_index('Date', inplace=True)
        data_diff = data_diff[['Pout_Before(W)','Pout_After(W)']].ffill()
        x = list(range(0,len(data_diff)))
        y = (data_diff['Pout_After(W)']-data_diff['Pout_Before(W)']).to_numpy()
        m  = np.polyfit(x, y, 1)
        poly1d_fn = np.poly1d(m)
        ax.plot(data_diff.index, y, 'o-', data_diff.index, poly1d_fn(x), '--k', label="Difference "+str(edsname))
            
        #set date as index
        data.set_index('Date',inplace=True)
            
        #Set x axis with date
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %d %y'))
        
        ax.set_title('Preformance Ratio Difference graph'+str(edsname))
        ax.set_ylabel('Watts')
        ax.set_xlabel('Date')
        plt.legend(loc='upper right')

        #plt.show()

        
    def df_load(self):
        
        data = pd.read_csv(self.filepath, parse_dates=['Date'])
        data.set_index('EDS/CTRL(#)', inplace=True)
        # code to delete measured only data at noon time
        # delete if measured only data is put into seperate file
        data_filtered = data[ ~(
            (data.Time.str.split(":").str[0].astype(int) == 12) &
            (data.Time.str.split(":").str[1].astype(int) <= 3))]
        return data_filtered

# run the program
root = customtkinter.CTk()
gui = EDS(root)
root.mainloop()