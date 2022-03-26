import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import datetime

# This simple file plots the history in both currency formats to visualize
# the gains/losses in time

history = pd.read_excel("history.xlsx")

sns.set_theme(style="darkgrid")

plt.figure(figsize = (15,8))
plt.title("TRY Assets against time")
sns.lineplot(data = history , x="DATE" , y = "TRY") 

plt.figure(figsize = (15,8))
plt.title("USD Assets against time")
sns.lineplot(data = history , x="DATE" , y = "USD") 


# This function extracts the date from the name of the file in the asset_outputs folder
def extract_date(file_name):
    date_str = file_name[0:-5]
    date = date_str.split("-")
    day = date[0]
    month = date[1]
    year = date[2]
    return datetime.date(day = int(day) , month = int(month) , year = int(year))

asset_outputs = os.listdir("asset_outputs")
dates = [extract_date(name) for name in asset_outputs]
max_idx = dates.index(max(dates))

latest_file = asset_outputs[max_idx]

assets = pd.read_excel("asset_outputs/"+latest_file,index_col="Currency")

# Line below creates a piechart of the currencies according to their rates in the total wealth
plot = assets.plot.pie(y = "TRY", figsize=(11, 6),legend=True,autopct="%1.0f%%")

plt.show()