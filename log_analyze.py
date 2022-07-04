import matplotlib.pyplot as plt
import streamlit as st
import os



def Log_analyze():
    
    logLists = []
    infoNum = 0
    warnNum = 0

    docsNum = 0
    openapiNum = 0
    locationNum = 0
    coordinatesNum = 0
    displayNum = 0
    countNum = 0
    givenNumberNum = 0
    maximumNum = 0
    truncatedNum = 0
    
    if os.stat("reports/logfile.log").st_size == 0:
        st.markdown("log is empty")
    else:
        with open("reports/logfile.log", encoding='utf-8') as lines:
            for line in lines:
                if "loglevel=" in line:
                    data = line.split(" ")
                    list = []
                    if(data[2] == "loglevel=INFO"):
                        list.append(data[2])
                        list.append(data[5].split("\n")[0])
                    else:
                        list.append(data[2])
                        list.append(data[3].split("\n")[0])
                    logLists.append(list)
        
        for part in logLists:
            if(part[0] == 'loglevel=INFO'): infoNum = infoNum + 1
            elif(part[0] == 'loglevel=WARNING'): warnNum = warnNum + 1
            
            if(part[1] == '/docs'): docsNum = docsNum + 1
            elif(part[1] == '/openapi.json'): openapiNum = openapiNum + 1
            elif(part[1] == '/img/airplane/location'): locationNum = locationNum + 1
            elif(part[1] == '/img/airplanes/coordinates'): coordinatesNum = coordinatesNum + 1
            elif(part[1] == '/img/display'): displayNum = displayNum + 1
            elif(part[1] == '/img/airplanes/count'): countNum = countNum + 1
            elif(part[1] == '/img/airplanes/givenNumber'): givenNumberNum = givenNumberNum + 1
            elif(part[1] == '/img/airplanes/maximum'): maximumNum = maximumNum + 1
            elif(part[1] == '/img/airplanes/truncated'): truncatedNum = truncatedNum + 1
            
        infoNum = infoNum - warnNum

        st.markdown('Pass & Warning Graph')
        labels = "Pass","Warning"
        sizes = [infoNum, warnNum]
        explode = (0, 0)
        
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax1.axis('equal')

        st.pyplot(fig1)
        
        
        st.markdown('API Used Times Graph')
        labels2 = "API 1: Search by Location", "API 2: Get all coordinates", "API 3: Get top size aircraft", "API 4: Count airplanes", "API 5: Search by number", "API 6: Get top number aircraft", "API 7: Get top number truncated"
        sizes2 = [locationNum, coordinatesNum, displayNum, countNum, givenNumberNum, maximumNum, truncatedNum]
        explode2 = (0, 0, 0, 0, 0, 0, 0)
        
        
        fig2, ax2 = plt.subplots()
        ax2.pie(sizes2, explode=explode2, labels=labels2, autopct='%1.1f%%',
                shadow=True, startangle=90)
        ax2.axis('equal')

        st.pyplot(fig2)
        
        
        
        
        
        