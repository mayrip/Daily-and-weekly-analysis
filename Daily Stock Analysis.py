#!/usr/bin/env python
# coding: utf-8

# # Daily and Weekly Returns Analysis

# In[687]:


#!pip install yfinance not needed


# In[688]:


get_ipython().system('pip install nsepy')


# In[689]:


from datetime import date
from nsepy import get_history
import pandas as pd
import pandas_datareader as pdr
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
get_ipython().run_line_magic('matplotlib', 'inline')


# In[690]:


Nifty = get_history(symbol='NIFTY 50',start=date(2000,5,1),
                   end=date(2021,7,30), index = True)
"""
Nifty = get_history(symbol='SBIN',
                   start=date(2015,1,1),
                   end=date(2021,7,30))
"""


# In[691]:


Nifty


# In[692]:


Nifty.tail(10)


# In[693]:



Nifty.drop(['Volume','Turnover'], axis =1)


# In[ ]:





# In[694]:


Nifty['Close'].plot(figsize=(10,7), grid =True)
plt.show()


# In[695]:


Nifty['intraday_returns'] = ((Nifty['Close']-Nifty['Open'])/Nifty['Open'])*100


# In[696]:


Nifty.head()


# In[697]:


sns.kdeplot(Nifty.intraday_returns)


# In[698]:


sns.set_style('darkgrid')


# In[699]:


Nifty.intraday_returns.plot(figsize=(12,8))


# In[700]:


sns.distplot(Nifty.intraday_returns)


# In[701]:


sns.histplot(Nifty.intraday_returns)


# In[702]:


sns.__version__


# In[703]:



len(Nifty)
    


# # Weekly Nifty movements

# https://stackoverflow.com/questions/34597926/converting-daily-stock-data-to-weekly-based-via-pandas-in-python

# In[704]:



Nifty.index = pd.to_datetime(Nifty.index)
Nifty.set_index(Nifty.index, inplace=True)
Nifty.sort_index(inplace=True)

def take_first(array_like):
    return array_like[0]

def take_last(array_like):
    return array_like[-1]
output = Nifty.resample('W').agg({'Open': 'first', 
                          'High': 'max',
                          'Low': 'min',
                          'Close': 'last',
                          'Volume': 'sum'}) 
output.index = output.index + pd.DateOffset(days=-6)
 # to put the labels to Monday

output = output[['Open', 'High', 'Low', 'Close', 'Volume']]


# In[705]:


output.tail()


# In[706]:


output['Weekly_returns'] = ((output['Close']-output['Open'])/output['Open'])*100


# In[707]:


output.Weekly_returns.plot(figsize=(12,8))


# In[708]:


total_week = len(output)


# In[709]:


positive_week = len(output[output['Weekly_returns']>0])


# In[710]:


neg_week = len(output[output['Weekly_returns']<0])


# In[711]:


sns.histplot(output.Weekly_returns)


# In[712]:


sns.distplot(output.Weekly_returns)


# In[713]:


print("Total : \n", total_week,"\n+ve :\n",positive_week,"\n -ve: \n",neg_week)


# In[714]:


pct_positive = (positive_week/total_week)*100
pct_negative = (neg_week/total_week)*100


# In[715]:


s = total_week, positive_week,neg_week,pct_positive, pct_negative
weekly_conclusion =pd.DataFrame(data =np.asarray(list(s)).reshape(1,5), columns =['total_week', 'positive_week', 'neg_week','pct_positive','pct_negative']) #,columns=['total_week', 'positive_week', 'neg_week']


# In[716]:


weekly_conclusion["pct_between_mod3"] =100*(len(output[(output['Weekly_returns']<3) & (output['Weekly_returns']>-3)])/total_week)


# In[717]:


weekly_conclusion


# In[718]:


weekly_conclusion["pct_between_mod2"] =100*(len(output[(output['Weekly_returns']<2) & (output['Weekly_returns']>-2)])/total_week)
weekly_conclusion["pct_between_mod2.5"] =100*(len(output[(output['Weekly_returns']<2.5) & (output['Weekly_returns']>-2.5)])/total_week)
weekly_conclusion["pct_between_mod1.5"] =100*(len(output[(output['Weekly_returns']<1.5) & (output['Weekly_returns']>-1.5)])/total_week)


# In[719]:


weekly_conclusion


# # Conclusion

# This note book aims to give an estimate of safe range for option writing, traders(Option writers) might find it usefull to make sound trading decisions.
# Things to note :
# 1. The drawdowns in this strategy is high and one must have SL/ Hedges to protect oneself from rare but hugely impacting adverse market scenario. 
# 2. It is also recommended not to use this in times of high sentiment event like Budgets, election etc. even if done should OTM should be far away from your usual rate (PS. you might get good premiums there as well if IV is high)
