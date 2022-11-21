import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
import os
import re 
from sklearn.decomposition import PCA
import numpy as np
import time
from tkinter import *
from tkinter import ttk



win = Tk()

# setting the windows size
win.geometry('500x250')

# declaring string variable
# for storing name and password
var=StringVar()


plt.rcParams['figure.figsize'] = (10, 6)#12,10 chilo
#/Users/shemontod/Desktop/shemonto/das_chunk25

c = 0
retrived_index = 0
ind = 0
obj = 0
###### Making Chunk of Data and Saving as CSV in folder

def slideMinuteToChunk(minute, overlap):
  if overlap != 0:
    calculated_min = ((minute*overlap)/100)
    overlap_chunk = calculated_min*60*5     
  regular_chunk = minute*60*5
  #print(overlap_chunk)
  #print(regular_chunk)
  makeChunk(regular_chunk,overlap_chunk)


def makeChunk(chunk_size,overlap_size):  
  found = 1 
  batch_no=1
  for chunk in pd.read_csv('/Users/shemontod/Desktop/shemonto/Copy of 146000017_trim.csv',chunksize=chunk_size):
    chunk.to_csv('/Users/shemontod/Desktop/shemonto/das_chunk25/chunk'+str(batch_no)+'.csv',index=False) #1500
    
    batch_no = 1 + int(batch_no)
    


#######    Windowing of Data

def read_chunks(sorted_list,window_time,overlap_time):
  
  listOfList = []
  l=[]
  
  for i in range(len(sorted_list)):
    df = pd.read_csv('/Users/shemontod/Desktop/shemonto/das_chunk25/chunk' + sorted_list[i]+'.csv', parse_dates=['TimeStamp']) #here i can get the chunk name
    name = 'chunk'+ sorted_list[i]+'.csv'
    #listOfName.append(name)
    df['TimeStamp'] = pd.to_datetime(df.TimeStamp)
    k = df['TimeStamp']
    start = k.min()
    end = k.max()
    time_start = start
    #print(f'start {start} end: {end}')
    #window_time = 20 #time to query
    #overlap_time = 10 #time to add
    time_end = time_start + pd.Timedelta(window_time, unit='s') #end time of window
    while (time_end <= end):
      window = df[(df['TimeStamp'] >= time_start) & (df['TimeStamp'] <= time_end)] #queried part
      sf=stat_feature(l,window)   # l is an empty list in which stat feature will be appended 
      listOfList.append(sf[-13:])   # [-6:] to access the last three elemnets of the list
      listOfName.append(name)  # appending the correspodig file name of each statistical row for trackinng
      #increments the window by a factor of overlap time
      time_start = time_start + pd.Timedelta(overlap_time, unit='s')
      time_end = time_end + pd.Timedelta(overlap_time, unit='s')
      #print(f'overlap st: {time_start} overlap end: {time_end}\n')


  return listOfList
  


# Statistical Feature Calculation /Users/shemontod/Desktop/shemonto/shemonto_csvfolder

def stat_feature(l,df):
  l.append(df['TimeStamp'].min())
  l.append(df['TimeStamp'].max())
  l.append(df[' Magnitude'].mean())
  l.append(df[' Magnitude'].median())
  l.append(df[' Magnitude'].var())
  l.append(df[' Magnitude'].skew())
  l.append(df[' Magnitude'].std())
  l.append(df[' Magnitude'].quantile(.10))
  l.append(df[' Magnitude'].quantile(.25))
  l.append(df[' Magnitude'].quantile(.75))
  l.append(df[' Magnitude'].quantile(.90))
  l.append(df[' Magnitude'].min())
  l.append(df[' Magnitude'].max())

  return l



def resultant_csv(listOfList):
  data = pd.DataFrame(listOfList) # Aikhane .T hobe na cuz nested list
  # add columns
  data.columns = ['TimeStamp_start','TimeStamp_end','mean', 'median','variance','skewness','standard deviation','Q10','Q25','Q75','Q90','min','max']
  # display
  #return(data)

  # CONVERTING A DATAFRAME TO A CSV FILE
  data.to_csv('/Users/shemontod/Desktop/shemonto/shemonto_csvfolder/chunk7.csv', index=False) #ai folder a connverted csv data gula thakbe
  #new_result = pd.read_csv('/content/shemonto_csvfolder/chunk7.csv')
  return data
  


#########       MAIN File where all call are being made

slideMinuteToChunk(5,50) #180,50 chilo
window_time = 20 #time to query in secs.chilo 20/1800
overlap_time = 10 #time to add in secs.chilo 10/600

dir = '/Users/shemontod/Desktop/shemonto/das_chunk25'
file_list = os.listdir(dir)
lis = []
listOfName = []
for file in os.listdir(dir):
  if file.endswith(".csv"):
    filename = re.sub(r'[^0-9]*', "", file) 
    lis.append(filename)
lis.sort(key=int)
#print(lis)
catch_list = read_chunks(lis,window_time,overlap_time) #listoflists ta aikhane ache
print_result = resultant_csv(catch_list)
#print("hello")
#print(print_result)



#####          Scaling, Scatter point and Retriving Data

# pca_df is the dataframe without time columns

pca_df = print_result.drop(['TimeStamp_start','TimeStamp_end'], axis=1)
#pca_df.shape

# Scaled and rounded dataframe  


sc =  MinMaxScaler()#min max scaling
scaled_arr = sc.fit_transform(pca_df)
#type(scaled_arr)     it was array

# This is the scaled dataframe. Index of this matches with the origial data(print_result).np.round_(scaled_arr, decimals = 3)
scaled_df = pd.DataFrame(np.round_(scaled_arr, decimals = 5), columns = pca_df.columns)
scaled_df

from sklearn.decomposition import PCA

pca = PCA(n_components = None)
components = pca.fit_transform(scaled_df) #returns transformed values
pca_scores_df = pd.DataFrame((np.round_(components, decimals = 5)), columns = pca_df.columns)# change the header

#components.shape
#print(components)



###############  Event Picker and Plot

#fig = plt.figure()
#ax = fig.add_subplot(111)
#ax.set_title('click on points')
fig,axs = plt.subplots(1,2)
axs[0].set_title('click on points')

x = (np.round_(components[:,0], decimals = 5))
y = (np.round_(components[:,1], decimals = 5))
#line, = ax.plot(np.random.rand(100), 'o', picker=5)  # 5 points tolerance
scatter = axs[0].scatter(x,y, color=["blue"]*len(components),picker=True) #previously plt.scatter chilo

#axs.set_title('click on points')


#######   Step2 : Create Annotation Object

annotation = axs[0].annotate("", xy=(0,0), xytext=(20,20),textcoords="offset points",
                    bbox=dict(boxstyle="round", fc="w"),
                    arrowprops=dict(arrowstyle="->"))
annotation.set_visible(False)

# Step3 : Implementing Hover Event

def motion_hover(event):
    annotation_visibility = annotation.get_visible()
    if event.inaxes == axs[0]:  #if mouse cursor is inside ax
        is_conatained, annotation_index = scatter.contains(event) # detecting whether cursor is on a data point
        if is_conatained:
            data_point_location = scatter.get_offsets()[annotation_index['ind'][0]] 
            annotation.xy = data_point_location

            scatter_query = pca_scores_df[(pca_scores_df['mean'] == (data_point_location[0])) & (pca_scores_df['median'] == (data_point_location[1]))]
            scatter_ind = scatter_query.index[0]
            
            #text_label = '({0:2f},{0:2f})'.format(data_point_location[0],data_point_location[1])
            text_label = listOfName[scatter_ind]
            annotation.set_text(text_label)
            annotation.set_visible(True) # it is set to false by default
            fig.canvas.draw_idle() # recreate the figure


    else:
        if annotation_visibility:
            annotation.set_visible(False)
            fig.canvas.draw_idle()



fig.canvas.mpl_connect('motion_notify_event', motion_hover)



#fig2 = plt.figure(2)
#axs = fig2.add_subplot()
#fig2,axs = plt.subplots()

def scatter_file_name(param):
  file_name=listOfName[param.index[0]]
  print(file_name) #string
  k,k1 = scatter_read_file(file_name)
  return k,k1
  #scatter_read_file(file_name)

def scatter_read_file(name):
  retrived_file = pd.read_csv('/Users/shemontod/Desktop/shemonto/das_chunk25/' + name, parse_dates=['TimeStamp'])
  return retrived_file, name
  #scatter_rawdata_plot(retrived_file, name)


def scatter_rawdata_plot(rawdata_file, title):

  #mplcursors.cursor(ax).connect(
  #  "add", lambda sel: sel.annotation.set_text(title))

  plt.figure(figsize=(10, 6))
  plt.subplot(1, 2, 1)
  plt.plot(rawdata_file['TimeStamp'], rawdata_file[' Magnitude'])
  plt.title(title, fontsize=18)
  plt.xlabel("TimeStamp", fontsize=15)
  plt.ylabel("Magnitude", fontsize=15)
  plt.show()

labels = ("a","b","c")

def submit():
    global name
    print('hello  ',ind)
    scatter._facecolors[obj.ind,:] = (0.1, 0.2, 0.5, 0.3)
    name=var.get()
    new_test(name)
    print("The label is : " + name)
    var.set("")


def new_test(p_name):
    df_test = print_result
    rowIndex = df_test.index[retrived_index]
    df_test.loc[rowIndex, 'user_label'] = p_name
    a_test = df_test.loc[[rowIndex]]
    #print("JOY BANGLA")
    print(a_test)


#binding mouse events with tkinter

def hello(event):
    print("Single Click, Button-l") 
def quit(event):                           
    print("Double Click, so let's stop") 
    import sys; sys.exit() 





def onpick(event):
  global c
  global retrived_index
  global line1
  global ind
  global obj
  c=c+1
  obj= event
  ind = event.ind
  ttk.Label(win, text = "Annotation Widget",background = 'green', foreground ="white",font = ("Times New Roman", 15)).grid(row = 0, column = 1)
  
  cb= ttk.Combobox(win, textvariable= var)
  cb['values']= labels
  cb['state']= 'readonly'

  # Create a button to clear the selected combobox text value
  button= Button(win, text= "submit", command= submit)
  button.grid(column = 1, row = 27)

  cb.grid(column = 1, row = 25)
  cb.current()

#   widget = tk.Button(None, text='Mouse Clicks')
#   widget.pack()
#   widget.bind('<Button-1>', hello)
#   widget.bind('<Double-1>', quit) 
  
  #root.mainloop() #without it the tinker gui is not shown
  #ind = event.ind
  print('onpick3 scatter:', ind, x[ind], y[ind])
  print(x[ind][0])
  print(y[ind][0])
  #scatter._facecolors[event.ind,:] = (0.1, 0.2, 0.5, 0.3)
  scatter_query = pca_scores_df[(pca_scores_df['mean'] == (x[ind][0])) & (pca_scores_df['median'] == (y[ind][0]))]
  retrived_index = scatter_query.index[0]
  print(scatter_query.index[0]) # as this index will match with the original raw dataframe
  print(scatter_query)
  final,final1 = scatter_file_name(scatter_query)

  a,b = final['TimeStamp'], final[' Magnitude']
  #line1, = axs.plot(a,b)
  #plt.title(final1, fontsize=18)
  axs[1].set_title(final1, fontsize=18)
  axs[1].set_xlabel("TimeStamp", fontsize=15)
  axs[1].set_ylabel("Magnitude", fontsize=15)
  #fig2.canvas.draw()
  #plt.draw()
  if c == 1:
    line1, = axs[1].plot(a,b)
    axs[1].set_title(final1, fontsize=18)
    axs[1].set_xlabel("TimeStamp", fontsize=15)
    axs[1].set_ylabel("Magnitude", fontsize=15)
    #fig2.canvas.draw_idle()
    #axs[1].draw_idle()
    win.mainloop()

  else:
     axs[1].clear() # clearing the first plot in this axs
     line1.set_xdata(a)  # updating a and y values of scatter plot
     line1.set_ydata(b)
     line1, = axs[1].plot(a,b)
     axs[1].set_title(final1, fontsize=18)
     axs[1].set_xlabel("TimeStamp", fontsize=15)
     axs[1].set_ylabel("Magnitude", fontsize=15)
     #fig2.canvas.draw_idle()
     #axs[1].draw_idle()
     win.mainloop()

  #plt.show()
  #axs = fig2.add_subplot()
  ### if else statement
  #https://www.geeksforgeeks.org/how-to-update-a-plot-on-same-figure-during-the-loop/

  
  #scatter_plot()  

fig.canvas.mpl_connect('pick_event', onpick)
#plt.figure(figsize=(10, 6))

plt.show()
