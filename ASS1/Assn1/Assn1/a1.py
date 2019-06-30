'''
COMP9321 Assignment One Code Template 2019T1
Name:Yizheng Ying
Student ID:z5141180
'''
import csv
import re
import json
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as img
import matplotlib.colors as colors 

def q1():
    readFile = open('accidents_2017.csv','r')
    temp = csv.reader(readFile)
    i = 0
    for item in temp:
        result = ''
        if i <= 10:
            for itempart in item:
                itempart = itempart.rstrip()
                if ' ' in itempart:
                    if i == 0:
                        result += '"'+itempart+'"'+' '
                        #print ('"'+itempart+'"',end=' ')
                    else:
                        itempart = itempart.split()
                        content = ''
                        for s in itempart:
                            if s == 'la' or s == 'de' or "d'" in s or "l'" in s:
                                content+=s+' '
                            else:
                                content+=s.title()+' '
                        result += '"'+content.rstrip()+'"'+' '
                        #print ('"'+content+'"',end=' ')
                else:
                    result += itempart+' '
            print(result.rstrip())
        i+=1
    '''
    Put Your Question 1's code in this function
    '''
    readFile.close()
    pass 

def q2():
    readFile = open('accidents_2017.csv','r')
    temp = csv.reader(readFile)
    saveFile = []
    i = 0
    for item in temp:
        saveFile1 = []
        if 'Unknown' not in item:
            for itempart in item:
                itempart = itempart.rstrip()
                if i == 0:
                    saveFile1.append(itempart)
                else:
                    if ' ' in itempart:
                        itempart = itempart.split()
                        content = ''
                        for s in itempart:
                            if s == 'la' or s == 'de' or "d'" in s or "l'" in s:
                                content+=s+' '
                            else:
                                content+=s.title()+' '
                    #print ('"'+content+'"',end=' ')
                        saveFile1.append(content.rstrip())
                    else:
                        saveFile1.append(itempart)
            #print()
            if saveFile1 != []:
                saveFile.append(saveFile1)
            i += 1
    #print(saveFile[0],saveFile[1])
    with open("result_q2.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerows(saveFile)
    '''
    Put Your Question 2's code in this function 
    '''
    readFile.close()
    pass 

def q3():
    readFile = open('result_q2.csv','r')
    temp = csv.reader(readFile)
    temp_dict={}
    i = 0
    a = []
    for item in temp:        
        if i != 0:
            if item not in a:
                a.append(item)
                if item[1] not in temp_dict:
                    temp_dict[item[1]] = 1
                else:
                    temp_dict[item[1]] += 1
##            if item[1] != 'Unknown' and item[1] != '-' and item[1] != 'NA':
##                if item[1] not in temp_dict:
##                    temp_dict[item[1]] = 1
##                else:
##                    temp_dict[item[1]] += 1
        i +=1
    print('"District Name" "Total numbers of accidents"')    
    for key,value in sorted(temp_dict.items(),key=lambda item:item[1],reverse=True):
        if ' ' in key:
            print('"'+key+'"',value)
        else:
            print(key,value)
    '''
    Put Your Question 3's code in this function 
    '''
    readFile.close()
    pass 

def q4():
    readFile = open('air_stations_Nov2017.csv','r')
    temp = csv.reader(readFile)
    result = []
    i = 0
    stationdict = {}
    for stationitem in temp:
        if i == 0:
            name1 = stationitem[0]
            name2 = stationitem[4]
        else:
            dict = {}
            temp1 = ''
            temp2 = ''
            a1 = stationitem[0].split()
            a2 = stationitem[4].split()
            for item1 in a1:
                if item1 == 'la' or item1 == 'de' or "d'" in item1 or "l'" in item1:
                    temp1+=item1+' '
                else:
                    temp1+=item1.title()+' '
            dict[name1] = temp1.rstrip()
            for item2 in a2:
                if item2 == 'la' or item2 == 'de' or "d'" in item2 or "l'" in item2:
                    temp2+=item2+' '
                else:
                    temp2+=item2.title()+' '
            dict[name2] = temp2.rstrip()
            stationdict[stationitem[0]] = stationitem[4]
            result.append(dict)
        i += 1
    print(json.dumps(result))
    readFile.close()
    
    readFilequality = open('air_quality_Nov2017.csv','r')
    tempquality = csv.reader(readFilequality)
    j = 0
    for qualityitem in tempquality:
        content = ''
        if j == 0:
            j += 1
            for qualityitempart in qualityitem:
                if ' ' in qualityitempart:
                    content += '"'+qualityitempart+'"'+' '
                else:
                    content += qualityitempart+' '
            print(content)

        elif j >= 1 and j < 11:
            if qualityitem[1] != 'Good' and qualityitem[1] != '--':
                j += 1
                for qualityitempart in qualityitem:
                    if qualityitempart != '-' and qualityitempart != 'NA':
                        if ' ' in qualityitempart:
                            content += '"'+qualityitempart+'"'+' '
                        else:
                            content += qualityitempart+' '
                print(content)

    readFilequality.close()

    readFilequality2 = open('air_quality_Nov2017.csv','r')
    tempquality2 = csv.reader(readFilequality2)
    saveQualityFile = []
    savetemp = ["District Name","Neighborhood Name",
                "Weekday","Month","Day","Hour","Part of the day"]
    k = 0
    qualitylist = []
    week = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    month = [0,"January","February","March","April","May","June",
             "July","August","September","October","November","December"]
    for itemquality in tempquality2:
        if 'NA' not in itemquality:
            if itemquality[1] != 'Good' and itemquality[1] != '--':
                if itemquality[0] in stationdict:
                    date = datetime.datetime.strptime(itemquality[13], '%d/%m/%Y %H:%M')
                    qualitylist.append([stationdict[itemquality[0]],itemquality[2],itemquality[3],week[date.weekday()],month[date.month],date.day,date.hour])
    readFileaccident = open('accidents_2017.csv','r')
    tempaccidnet = csv.reader(readFileaccident)
    count = 0
    resultlist = []
    for title in tempaccidnet:
        if count ==0:
            resultlist.append(title)
            break
    #for j in qualitylist:
     #   count +=1
      #  print(j)
    for qualitylistitem in qualitylist:
        #print(qualitylistitem)
        matchresult = matchlist(qualitylistitem)
        if matchresult != []:
            for tempaccident in matchresult:
                resultlist.append(tempaccident)
        
        
                
    #print(len(resultlist))
    with open("result_q4.csv","w",newline='') as csvfile: 
        writer = csv.writer(csvfile)
        writer.writerows(resultlist)
    '''
    Put Your Question 4's code in this function 
    '''
    
    readFilequality2.close()
    pass 
def matchlist(quality):
    readFileaccident = open('accidents_2017.csv','r')
    tempaccidnet = csv.reader(readFileaccident)
    temp = []
    for tempaccidnetitem in tempaccidnet:
        if quality[0] == tempaccidnetitem[1] and quality[4] == tempaccidnetitem[5] and quality[5] == int(tempaccidnetitem[6]) and quality[6] == int(tempaccidnetitem[7]):
            finalsesult = []
            for item in tempaccidnetitem:
                item = item.rstrip()
                
                if ' ' in item:
                    temp1 = ''
                    item = item.split()
                    
                    for item1 in item:
                        if item1 == 'la' or item1 == 'de' or "d'" in item1 or "l'" in item1:
                            temp1+=item1+' '
                        else:
                            temp1+=item1.title()+' '
                    finalsesult.append(temp1.rstrip())
                else:
                    finalsesult.append(item)
            
            temp.append(finalsesult)
    
    return temp
def q5():
    readFile = open('accidents_2017.csv','r')
    temp = csv.reader(readFile)
    i = 0
    tempdata1 = []
    tempdata2 = []
    tempdata3 = []
    for item in temp:
        if i > 0 and item[1] != 'Unknown' and item[1] != '-':
            tempdata1.append(((float(item[13])-1.9168051)/(2.4232102-1.9168051))*946)
            tempdata2.append(((float(item[14])-41.2829106)/(41.4936091-41.2829106))*575)
            tempdata3.append(int(item[9]) + int(item[10]) + int(item[11]) + int(item[12]))
            
        i += 1
    
    #lon = np.array(result[0:][0])
    #accident_num = np.array(result[0:][2])
    lat = np.array(tempdata2[0:len(tempdata2)])
    lon = np.array(tempdata1[0:len(tempdata1)])
    num = np.array(tempdata3[0:len(tempdata3)])
    #plt.scatter(lat,lon,s=num,alpha=0.5,c='y',marker='.')
    image = np.flipud(img.imread('Map.png'))

    plt.imshow(image)
    plt.hist2d(lon,lat,bins= (946,575),cmap='Blues',alpha=0.5,range=np.array([(0,946),(0,575)]),weights=num,cmin=1)
    plt.axis('off')
    fig =plt.gcf()
    fig.set_size_inches(9.46,5.75)
    plt.gca().xaxis.set_major_locator(plt.NullLocator())
    plt.gca().yaxis.set_major_locator(plt.NullLocator())
    plt.subplots_adjust(top=1,bottom=0,right=1,left=0,hspace=0,wspace=0)
    plt.savefig('map.png')
     
    '''
    Bonus Question(Optional).
    Put Your Question 5's code in this function.
    '''
    pass 

q4()
