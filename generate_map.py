# preamble
# this is based on the https://www.youtube.com/watch?v=SgacOaHoJLs tutorial
# by Dario Festa - July 17, 2020

# folium is the library we are going to use to visualize our resuls on a map
import folium
locpath='.'


# other relevant libraries
import numpy as np
import pandas as pd
import os

# DataFrames with institutions and members
dfnames=pd.read_csv(os.path.join(locpath,'fakenames.csv'))
dfcoord=pd.read_csv(os.path.join(locpath,'coordinate.csv'))

def htmlpopup(df:pd.DataFrame) -> str:
    '''Transform institution name into a title and names and surnames within a dataframe into a html item list'''

    strstart="f\"\"\"<h1>" +str(pd.unique(df['istituzione'])[0])+ "</h1> "
    strbody=str(["<ul>" + str(c['nome']) + " " + str(c['cognome']) + " </ul>" for i,c in nomiCorr.iterrows()])
    strend=" \"\"\" "


    return (strstart+strbody[2:-2]+strend)

# Set the map up and center it on roughly the center of Italy
theMap = folium.Map(location = [43,12], zoom_start = 6, tiles = "CartoDB positron")

# Populate the map with all the institutions categories

## Enti per la ricerca
eprDf=pd.merge(dfnames,dfcoord[dfcoord['tipologia']=='EPR'],on='istituzione',how='inner')
eprFg=folium.FeatureGroup(name='EPR',show=True).add_to(theMap)

for l in pd.unique(eprDf['istituzione']):
   print (l)

   # Slice a DataFrame including just the current institution members
   nomiCorr=eprDf[eprDf['istituzione']==l]
   folium.Marker(location=[nomiCorr['long'].values[0],nomiCorr['lat'].values[0]],
                 popup=htmlpopup(nomiCorr),
                 tooltip=l,icon=folium.Icon(color='darkgreen')).add_to(eprFg)
   
## IRCSS
ircssDf=pd.merge(dfnames,dfcoord[dfcoord['tipologia']=='IRCSS'],on='istituzione',how='inner')
ircssFg=folium.FeatureGroup(name='IRCSS',show=True).add_to(theMap)

for l in pd.unique(ircssDf['istituzione']):
   print (l)

   # Slice a DataFrame including just the current institution members
   nomiCorr=ircssDf[ircssDf['istituzione']==l]
   folium.Marker(location=[nomiCorr['long'].values[0],nomiCorr['lat'].values[0]],
                 popup=htmlpopup(nomiCorr),
                 tooltip=l, icon=folium.Icon(color='lightred')).add_to(ircssFg)
   
## Universita
uniDf=pd.merge(dfnames,dfcoord[dfcoord['tipologia']=='UNI'],on='istituzione',how='inner')
uniFg=folium.FeatureGroup(name='Universita',show=True).add_to(theMap)

for l in pd.unique(uniDf['istituzione']):
   print (l)
   # Slice a DataFrame including just the current institution members
   nomiCorr=uniDf[uniDf['istituzione']==l]
   
   folium.Marker(location=[nomiCorr['long'].values[0],nomiCorr['lat'].values[0]],
                 popup=htmlpopup(nomiCorr),
                 tooltip=l).add_to(uniFg)
   
# Create the map
folium.LayerControl().add_to(theMap)
theMap.save("itrn-members.html")