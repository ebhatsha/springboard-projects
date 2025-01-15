#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pandas as pd
import numpy as np
import matplotlib.plyplot as plt

# variable called url_LondonHousePrices and assigned the following link:
url_LondonHousePrices = "https://data.london.gov.uk/download/uk-house-price-index/70ac0766-8902-4eb5-aab5-01951aaed773/UK%20House%20price%20index.xls"

# The dataset we're interested in contains the Average prices of the houses, and is 
# actually on a particular sheet of the Excel file. 
# As a result, we need to specify the sheet name in the read_excel() method.
# Put this data into a variable called properties.  
properties = pd.read_excel(url_LondonHousePrices, sheet_name='Average price', index_col= None)

##2. Cleaning, Transforming, and Visualizing Data

##2.1 Exploring Data
properties.shape #to look at the number of rows
properties.head()  #to look at the state of data

##2.2 Cleaning Data
properties_transposed = properties.T #transposes (switches columns and rows) the data
properties_transposed.index          #to confirm what the row indices are
properties_transposed = properties_transposed.reset_index()
properties_transposed.index
properties_transposed.head()

properties_transposed.columns()
properties_transposed.illoc[[0]] #to look at that row 
properties_transposed.columns = properties_transposed.iloc[0]
properties_transposed.head() #check the visual chart again
properties_transposed = properties_transposed.drop(0) 
properties_transposed.head()

properties_transposed = properties_transposed.rename(columns = {'Unnamed: 0':'London_Borough', pd.NaT: 'ID'}) 
properties_transposed.head() # check out the DataFrame again
properties_transposed.columns

##2.3 Transforming the Data
clean_properties = pd.melt(properties_transposed, id_vars= ['London_Borough', 'ID']) # compacts data into fewer columns
clean_properties.head()

clean_properties['Average_price'] = pd.to_numeric(clean_properties['Average_price']) #change into calculable values (float numeric type)

clean_properties.dtypes # Check out the new data types
clean_properties.count() # To see if there are any missing values

##2.4 Cleaning again 
##fewer data points than anticipated
clean_properties['London_Borough'].unique() #how to check for strange or missing values

clean_properties[clean_properties['London_Borough'] == 'Unnamed: 34'].head() #subset to see what information is contained in rows where London_Boroughs is 'Unnamed’
clean_properties[clean_properties['London_Borough'] == 'Unnamed: 37'].head()

clean_properties[clean_properties['ID'].isna()] #look for how many rows hav na

NaNFreeDF1 = clean_properties[clean_properties['Average_price'].notna()] # new variable called *NaNFreeDF1* and assign to the result of filtering *clean_properties
NaNFreeDF1.head(48)
 
NaNFreeDF1.count() # See how many rows have complete information

# to compare the dimenions of clean_properties, NaNFreeDF1, and NaNFreeDF2: 
print(clean_properties.shape)
print(NaNFreeDF1.shape)
print(NaNFreeDF2.shape)

#creating a list of non-boroughs to drop with the isna() application
nonBoroughs = ['Inner London', 'Outer London', 
               'NORTH EAST', 'NORTH WEST', 'YORKS & THE HUMBER', 
               'EAST MIDLANDS', 'WEST MIDLANDS',
              'EAST OF ENGLAND', 'LONDON', 'SOUTH EAST', 
              'SOUTH WEST', 'England']

# Filter *NanFreeDF2* first on the condition that the rows' values for *London_Borough* is *in* the *nonBoroughs* list. 
NaNFreeDF2[~NaNFreeDF2.London_Borough.isin(nonBoroughs)] #The tilde (~) negates the boolean Series, effectively filtering rows where the London_Borough is not in the nonBoroughs list.
NaNFreeDF2.head()
 
df = NaNFreeDF2 #define df, final data analysis ready dataframe
df.head()
df.dtypes


##2.5 Visualizing Data
camden_prices = df[df['London_Borough'] == 'Camden'] # assigned to result of filtering df

ax = camden_prices.plot(kind ='line', x = 'Month', y='Average_Price')
ax.set_ylabel('Price')
df['Year'] = df['Month'].apply(lambda t: t.year)
df.tail()

dfg = df.groupby(by=['London_Borough', 'Year']).mean() #'groupby' will help calculate the mean for each year and for each Borough
dfg.sample(10)

dfg = dfg.reset_index()
dfg.head()

##3 Modeling Data
def create_price_ratio(d):
    y1998 = float(d['Average_price'][d['Year']==1998])
    y2018 = float(d['Average_price'][d['Year']==2018])
    ratio = [y2018/y1998]
    return ratio

create_price_ratio(dfg[dfg['London_Borough']=='Barking & Dagenham']) # Testing the function

# We want to do this for all of the London Boroughs. 

final = {} # store the ratios for each unique London_Borough

for b in dfg['London_Borough'].unique():             # iterate through each of the unique elements of the 'London_Borough' column dfg
    borough = dfg[dfg['London_Borough'] == b]        # make parameter for create_price_ratio function (subset dfg on 'London_Borough' == b)
    final[b] = create_price_ratio(borough)           # a new entry in the final dictionary whose value is the result of calling create_price_ratio with the argument: borough 
print(final)        # use the function and incorporate that into a new key of the dictionary


df_ratios = pd.DataFrame(final)
df_ratios.head()

df_ratios_T = df_ratios.T
df_ratios = df_ratios_T.reset_index()
df_ratios.head()

df_ratios.rename(columns={'index':'Borough', 0:'2018'}, inplace=True) # rename the 'index' column as 'London_Borough', and the '0' column to '2018'
df_ratios.head()

top15 = df_ratios.sort_values(by='2018',ascending=False).head(15)
print(top15)
 
ax = top15[['Borough','2018']].plot(kind='bar') # plot the boroughs that have seen the greatest changes in price
ax.set_xticklabels(top15.Borough)

