


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mtp_dates
import matplotlib.ticker as mtp_ticker

from datetime import datetime

#### BOXING ####
df_boxing = pd.read_csv('boxing.tsv',sep = "\t")


del df_boxing['Result']
del df_boxing['Carrier']

df_boxing['Buy rate'] =  df_boxing['Buy rate'].str[:-4]
df_boxing['Buy rate'] =  df_boxing['Buy rate'].str.replace(",","")
df_boxing['Buy rate'] = df_boxing['Buy rate'].map(lambda x: int(x))

df_boxing['Date'] = df_boxing['Date'].map(lambda x: x.replace("July","Jul"))
df_boxing['Date'] = pd.to_datetime(df_boxing['Date'],format= "%b %d, %Y")

df_boxing.sort(['Buy rate'], ascending = True, inplace=True)
df_boxing['Year'] = df_boxing['Date'].map(lambda x: x.year)

# boxing date from 2001
df_boxing = df_boxing[df_boxing['Year']>=2001]

# most/less watchers number boxing
min_buy_rate_boxing = df_boxing['Buy rate'].min()
max_buy_rate_boxing = df_boxing['Buy rate'].max()
max_rate_event = df_boxing[df_boxing['Buy rate'] == max_buy_rate_boxing]



#### MMA ####
df_mma = pd.read_csv('mma.csv',sep = "\t")
df_mma['PPV'] =  df_mma['PPV'].str.replace(",","")
df_mma['DATE'] = pd.to_datetime(df_mma['DATE'],format= "%m/%d/%Y")
#canceled event
df_mma = df_mma[df_mma['PPV']!="Canceled"]

df_mma['PPV'] = df_mma['PPV'].map(lambda x: int(x))
df_mma.sort(['PPV'],ascending=True,inplace = True)
df_mma_ppv = df_mma[df_mma['PPV']>min_buy_rate_boxing] # take bigger mma event, then min in boxing

# most/less watchers number MMA
min_ppv_mma = df_mma['PPV'].min()
max_ppv_mma = df_mma['PPV'].max()
max_ppv_event = df_mma[df_mma['PPV'] == max_ppv_mma]



#### FIGURE ####
ax = plt.figure(figsize = (10,10))

# numeric axis-x


dates_boxing = mtp_dates.date2num(df_boxing['Date'].astype(datetime))
dates_mma = mtp_dates.date2num(df_mma_ppv['DATE'].astype(datetime))
# top boxing event date
top_boxing_event = mtp_dates.date2num(max_rate_event['Date'].astype(datetime))
top_mma_event =  mtp_dates.date2num(max_ppv_event['DATE'].astype(datetime))

plt.plot_date(dates_boxing,df_boxing['Buy rate'].values, label='Boxing')
plt.plot_date(dates_mma,df_mma_ppv['PPV'].values, color = 'red',label='MMA')


plt.ylabel('Number of watchers', fontsize =20)
plt.gca().set_ylim([0,5000000])
plt.gca().get_yaxis().set_major_formatter(mtp_ticker.FuncFormatter(lambda x, p: format(int(x), ',')))

#pointer on figure
plt.annotate(max_rate_event['Fight'].values[0], xy=(top_boxing_event, max_rate_event['Buy rate']), xytext=(top_boxing_event-2000, max_rate_event['Buy rate']*1.1),
            arrowprops=dict(facecolor='black', shrink=0.1)
            )
plt.annotate(max_ppv_event['MAIN EVENT'].values[0], xy=(top_mma_event, max_ppv_event['PPV']), xytext=(top_mma_event-2000, max_ppv_event['PPV']*1.1),
            arrowprops=dict(facecolor='black', shrink=0.1)
            )


plt.legend()
plt.title('Pay-per-view comparison', fontsize = 30)

plt.show()


