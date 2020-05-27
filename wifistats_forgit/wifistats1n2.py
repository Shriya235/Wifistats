import re
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.dates as md
from datetime import datetime
import numpy as np



def to_cal_percent(rate):
    rates=rate
    tminus1=[]
    t=[]
    delta_list=[]
    percent=[]
    curve=[]
    for z in range(len(rates)-1):                                       #make empty lists to append the delta values and %s
            delta_list.append([])
            percent.append([])
    count=0
    for x in range(len(rates)-1):                                       #Here 2 adjacent lists and their elements are subtracted
            count+=1
            tminus1=rates[x]
            t=rates[x+1]
            for (m,n) in zip(tminus1,t):
                delta=int(n)-int(m)
                delta_list[count-1].append(delta)
    co=0
    for s in delta_list:                                                #to find the %
            sum1=0
            co+=1
            for r in s:
                sum1=sum1+int(r)
            if sum1!=0:                
                for r in s:
                    per=int(r)/sum1
                    percent[co-1].append(per)                   
            else:
                break
    mcs_size=len(percent[0])
    for x in range(mcs_size):
        curve.append([])
    coun=0
    for y in range(mcs_size):                                           #to collect all 0:values, 1:values in seperate lists            
        coun+=1                             
        for z in percent:                   
            curve[coun-1].append(z[y])
    
    return curve

def curves(yaxis,times,start,end):                                      #to plot the graph
    ax=plt.gca()
    xfmt = md.DateFormatter('%Y-%m-%d %H:%M:%S')
    ax.xaxis.set_major_formatter(xfmt)
    plt.xticks( rotation=30, horizontalalignment='right' )
    #colormap = plt.cm.gist_ncar
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, len(yaxis)+1))))
    for i in range(len(yaxis)):
        plt.plot(times,yaxis[i],label=i)
        lis=yaxis[i]
        plt.text(times[i],lis[i],i)
     
    plt.title(start.replace(end,' '))    
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.show()
       
    
def wifistats(catch_start,catch_end,logfile):
    results = []
    mcs=[]
    last=[]
    rates=[]
    curv=[]
    tim=[]
    time1=[]
    with open(logfile, 'r') as f1:
        lines = f1.readlines()        
    i = 0
    while i < len(lines):
        if catch_start in lines[i]:
            for j in range(i + 1, len(lines)):
                if catch_end in lines[j] or j == len(lines)-1:
                    results.append(lines[i:j])
                    i = j
                    break
        else:
            i += 1
    if "9" in catch_start:                                                        #tx_mcs classification
        for a in results:
            for b in a:
                if 'tx_mcs' in b and not 'ac_mu_mimo_tx_mcs' in b and not "ax_mu_mimo_tx_mcs" in b and not "ofdma_tx_mcs" in b :
                    mcs.append(re.split(r'[:,\s]\s*', b))
                    time1.append(re.split(r'[|\s]\s*',b))
        
        for a in mcs:
            rates.append(a[3:30:2])                                             #list only of rates        
        curv= to_cal_percent(rates)                                             #function call and recieves %tx_mcs
        del time1[0]
        for l in time1:                                                         #time axis
           tim.append(l[16]+" "+l[17])
        date_obj = []
        for temp in tim:
            date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
        dates = md.date2num(date_obj)
        curves(curv,dates,catch_start,catch_end)                                #calls for the graph
        last=mcs[len(mcs)-1]
        labels = last[2:29:2]                                                   #collect last values for piechart
        for i in range(0, len(labels)): 
            labels[i] = int(labels[i])
        sizes = last[3:30:2]
        for j in range(0, len(sizes)):
            sizes[i] = int(sizes[i])        
    elif "10" in catch_start:                                                   #rx_mcs classification
        for a in results:
            for b in a:
                if 'rx_mcs' in b and not "ul_ofdma_rx_mcs" in b:
                    mcs.append(re.split(r'[:,\s]\s*', b))
                    time1.append(re.split(r'[|\s]\s*',b))
        for a in mcs:
            rates.append(a[3:26:2])
        curv= to_cal_percent(rates)
        del time1[0]
        for l in time1:
           tim.append(l[14]+" "+l[15])
        date_obj = []
        for temp in tim:
            date_obj.append(datetime.strptime(temp, '%Y-%m-%d %H:%M:%S.%f'))
        dates = md.date2num(date_obj)
        curves(curv,dates,catch_start,catch_end)
        last=mcs[len(mcs)-1]
        labels = last[2:25:2]
        for i in range(0, len(labels)): 
            labels[i] = int(labels[i])
        sizes = last[3:26:2]
        for j in range(0, len(sizes)):
            sizes[i] = int(sizes[i])    
    fig1, ax1 = plt.subplots()
    plt.gca().set_prop_cycle(plt.cycler('color', plt.cm.jet(np.linspace(0, 1, len(curv)))))
    ax1.pie(sizes , labels=labels,shadow=False, startangle=90)                  #piechart plot       
    ax1.axis('equal')
    ax1.set_title(catch_start.replace(catch_end,' '))
    plt.show()

def wifistats_call(logfile,wifi):                                               #wifi=['wifistats wifi0 9',"wifistats wifi0 10"] in config
    for a in wifi:
        wifistats("root@OpenWrt:/# "+a ,"root@OpenWrt:/#",logfile)



