#!/usr/bin/env python
# coding: utf-8

# In[11]:


#import the required libraries
import numpy as np 

import pandas as pd 
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)

import json 

from geopy.geocoders import Nominatim 

import requests 
from bs4 import BeautifulSoup 

from pandas.io.json import json_normalize 


import matplotlib.cm as cm
import matplotlib.colors as colors


from sklearn.cluster import KMeans

import folium 

print("All imported.")


# In[12]:


#pass in the web address to the URL
URL = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'


# In[13]:


#pass in the URL to the request method
dr = requests.get(URL).text
soup = BeautifulSoup(dr, 'html.parser')


# In[14]:


#set up the lists
postalCode = []
borough = []
neighborhood = []


# In[15]:


#Loop to populate the lists while stripping unnecessary text
for row in soup.find('table').find_all('tr'):
    cells = row.find_all('td')
    if(len(cells) > 0):
        postalCode.append(cells[0].text.rstrip('\n'))
        borough.append(cells[1].text.rstrip('\n'))
        neighborhood.append(cells[2].text.rstrip('\n'))


# In[16]:


#constructing the dataframe
dftoronto = pd.DataFrame({"PostalCode": postalCode,
                           "Borough": borough,
                           "Neighborhood": neighborhood})

dftoronto.head()


# In[17]:


#drop rows with values equal to "Not assigned"
dftoronto_dropna = dftoronto[dftoronto.Borough != "Not assigned"].reset_index(drop=True)
dftoronto_dropna.head()


# In[18]:


#group by
dftoronto_grouped = dftoronto_dropna.groupby(["PostalCode", "Borough"], as_index=False).agg(lambda x: ", ".join(x))
dftoronto_grouped.head()


# In[19]:


for index, row in dftoronto_grouped.iterrows():
    if row["Neighborhood"] == "Not assigned":
        row["Neighborhood"] = row["Borough"]
        
dftoronto_grouped.head()


# In[22]:


column_names = ["PostalCode", "Borough", "Neighborhood"]
dftest = pd.DataFrame(columns=column_names)

test_list = ["M5G", "M2H", "M4B", "M1J", "M4G", "M4M", "M1R", "M9V", "M9L", "M5V", "M1B", "M5A"]

for postcode in test_list:
    dftest = dftest.append(dftoronto_grouped[dftoronto_grouped["PostalCode"]==postcode], ignore_index=True)
    
dftest


# In[23]:


dftoronto_grouped.shape


# In[30]:


#passing the geospatial data link to pandas
coordinates = pd.read_csv("https://cocl.us/Geospatial_data")
coordinates.head()


# In[31]:


#renaming column names to be cinsistent with the requirements
coordinates.rename(columns={"Postal Code": "PostalCode"}, inplace=True)
coordinates.head()


# In[32]:



dftoronto_new = dftoronto_grouped.merge(coordinates, on="PostalCode", how="left")
dftoronto_new.head()


# In[33]:


dftoronto_new = dftoronto_grouped.merge(coordinates, on="PostalCode", how="left")
dftoronto_new.head()


# In[35]:


column_names = ["PostalCode", "Borough", "Neighborhood", "Latitude", "Longitude"]
dftest = pd.DataFrame(columns=column_names)

test_list = ["M5G", "M2H", "M4B", "M1J", "M4G", "M4M", "M1R", "M9V", "M9L", "M5V", "M1B", "M5A"]

for postcode in test_list:
    dftest = dftest.append(dftoronto_new[dftoronto_new["PostalCode"]==postcode], ignore_index=True)
    
dftest


# In[ ]:




