#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!pip list


# In[79]:


from tabula import read_pdf
from tabulate import tabulate
import pandas as pd
import numpy as np


# In[80]:


# [top,left,bottom,width]
area= [109,25.64,516,492.14]


# In[81]:


pdf_path_input= input("What's your PDF's URL? \n\nURL of the Tadawul PDF:")


# In[82]:


pdf_date= pdf_path_input.rsplit('.pdf', 1)[0][-10:]


# In[83]:


#pdf_path_input= "https://www.saudiexchange.sa/wps/wcm/connect/b8ea220d-77bf-42b8-9622-fc51eb72169a/Weekly+Trading+and+Ownership+By+Nationality+Report+06-01-2022.pdf?MOD=AJPERES&CONVERT_TO=url&CACHEID=ROOTWORKSPACE-b8ea220d-77bf-42b8-9622-fc51eb72169a-nU-ScDt"

page_5 = read_pdf(pdf_path_input, pages= [5], area= area, stream=True)


# In[84]:


value_nationality_investor_type= page_5[0]


# In[85]:


value_nationality_investor_type_idx = np.r_[1, 3:5, 6:8]


# In[86]:


value_nationality_investor_type.drop(value_nationality_investor_type.columns[value_nationality_investor_type_idx], axis=1, inplace=True)


# In[87]:


value_nationality_investor_type.rename(columns={ value_nationality_investor_type.columns[0]: "investor_type", value_nationality_investor_type.columns[1]: "buy_sar", value_nationality_investor_type.columns[2]: "sell_sar"}, inplace = True)

value_nationality_investor_type = value_nationality_investor_type.iloc[3:]


# In[88]:


value_nationality_investor_type= value_nationality_investor_type.reset_index(drop=True)


# # Next: add columns, clean dataframe, and calculate the rest of the columns

# In[89]:


wrong_indexes= [4, 5, 10, 11, 14, 16, 20, 23, 24]

value_nationality_investor_type.drop(wrong_indexes, inplace=True)

value_nationality_investor_type= value_nationality_investor_type.reset_index(drop=True)


# In[90]:


value_nationality_investor_type['Nationality'] = 0
Saudi = list(range(0, 8))
GCC = list(range(8, 11))
Foreign = list(range(11, 16))
value_nationality_investor_type.loc[Saudi, 'Nationality'] = 'Saudi'
value_nationality_investor_type.loc[GCC, 'Nationality'] = 'GCC'
value_nationality_investor_type.loc[Foreign, 'Nationality'] = 'Foreign'


# In[91]:


cols = value_nationality_investor_type.columns.tolist()


# In[92]:


cols = cols[-1:] + cols[:-1]


# In[93]:


value_nationality_investor_type = value_nationality_investor_type[cols]


# In[94]:


value_nationality_investor_type['buy_sar'] = value_nationality_investor_type['buy_sar'].str.replace(r',', '')

value_nationality_investor_type['sell_sar'] = value_nationality_investor_type['sell_sar'].str.replace(r',', '')

value_nationality_investor_type.fillna(0, inplace=True)


# In[95]:


value_nationality_investor_type["buy_sar"] = value_nationality_investor_type["buy_sar"].astype('int64')

value_nationality_investor_type["sell_sar"] = value_nationality_investor_type["sell_sar"].astype('int64')


# In[96]:


#value_nationality_investor_type.info()


# In[97]:


total_nationality_investor_buys= value_nationality_investor_type['buy_sar'].sum()

total_nationality_investor_sells= value_nationality_investor_type['sell_sar'].sum()


# In[98]:


value_nationality_investor_type['percentage_of_total_buys']= value_nationality_investor_type['buy_sar']/total_nationality_investor_buys

value_nationality_investor_type['percentage_of_total_sells']= value_nationality_investor_type['sell_sar']/total_nationality_investor_sells


# In[99]:


value_nationality_investor_type['percentage_of_total_buys'] = pd.Series(["{0:.2f}%".format(val * 100) for val in value_nationality_investor_type['percentage_of_total_buys']], index = value_nationality_investor_type.index)

value_nationality_investor_type['percentage_of_total_sells'] = pd.Series(["{0:.2f}%".format(val * 100) for val in value_nationality_investor_type['percentage_of_total_sells']], index = value_nationality_investor_type.index)


# In[100]:


value_nationality_investor_cols= ['Nationality', 'investor_type', 'buy_sar', 'percentage_of_total_buys', 'sell_sar', 'percentage_of_total_sells']

value_nationality_investor_type = value_nationality_investor_type[value_nationality_investor_cols]


# In[101]:


value_nationality_investor_type = value_nationality_investor_type.rename(columns={'investor_type': 'Investor Type', 'buy_sar': 'Buy Sar', 'percentage_of_total_buys': 'Percentage of Total Buys', 'sell_sar': 'Sell Sar', 'percentage_of_total_sells': 'Percentage of Total Sells'})


# In[102]:


page_6 = read_pdf(pdf_path_input, pages= [6], area= area, stream=True)


# In[103]:


value_investor_classification= page_6[0]


# In[104]:


value_investor_classification_idx = np.r_[2, 4, 5]

value_investor_classification.drop(value_investor_classification.columns[value_investor_classification_idx], axis=1, inplace=True)

value_investor_classification.columns = ['investor_classification', 'buy_sar', 'sell_sar']


# In[105]:


value_investor_classification= value_investor_classification.iloc[2:4]


# In[106]:


value_investor_classification


# In[107]:


value_investor_classification = value_investor_classification.replace(',','', regex=True)


# In[108]:


value_investor_classification.fillna(0, inplace=True)


# In[109]:


value_investor_classification.loc[:,"buy_sar"] = value_investor_classification["buy_sar"].astype('int64')

value_investor_classification.loc[:,"sell_sar"] = value_investor_classification["sell_sar"].astype('int64')


# In[110]:


total_investor_classification_buys= value_investor_classification['buy_sar'].sum()

total_investor_classification_sells= value_investor_classification['sell_sar'].sum()


# In[111]:


value_investor_classification.loc[:,'percentage_of_total_buys']= value_investor_classification['buy_sar']/total_investor_classification_buys

value_investor_classification.loc[:,'percentage_of_total_sells']= value_investor_classification['sell_sar']/total_investor_classification_sells


# In[112]:


value_investor_classification.loc[:,'percentage_of_total_buys'] = pd.Series(["{0:.2f}%".format(val * 100) for val in value_investor_classification['percentage_of_total_buys']], index = value_investor_classification.index)

value_investor_classification.loc[:,'percentage_of_total_sells'] = pd.Series(["{0:.2f}%".format(val * 100) for val in value_investor_classification['percentage_of_total_sells']], index = value_investor_classification.index)


# In[113]:


investor_classification_cols= ['investor_classification', 'buy_sar', 'percentage_of_total_buys', 'sell_sar', 'percentage_of_total_sells']

value_investor_classification = value_investor_classification[investor_classification_cols]


# In[114]:


value_investor_classification = value_investor_classification.rename(columns={'investor_classification': 'Investor Classification', 'buy_sar': 'Buy Sar', 'percentage_of_total_buys': 'Percentage of Total Buys', 'sell_sar': 'Sell Sar', 'percentage_of_total_sells': 'Percentage of Total Sells'})


# In[115]:


value_investor_classification = value_investor_classification.reset_index(drop=True)


# In[116]:


value_nationality_investor_type.to_csv(('Value Traded by Nationality and Investor Type ' + pdf_date + ' .csv'), index=False)


# In[117]:


value_investor_classification.to_csv(('Value Traded by Investor Classification ' + pdf_date + ' .csv'), index=False)


# In[118]:


print('Success!\n\nYour Tadawul data has been extracted.')

