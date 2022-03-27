# Investment_Helper
This program simply has a daily procedure that creates a excel file containing the current values of the investments in the assets.xlsx file
Also, saves the total wealth of those assets in the history.xlsx file.

It also has a plot_assets file that creates a time series plot from the history file and a piechart from the last file in the asset outputs folder.

## USAGE

### 1- Install the required libraries using the requirements.txt

pip install requirements.txt

### 2- Get an API key from https://coinmarketcap.com/api

### 3- Enter your API key in the daily_procedure.py file

### 4- Enter your assets with their corresponding symbols to the assets.xlsx file.

## To Run the daily procedure:

You can run the daily procedure by command line, or if you are in windows, you can simply execute the daily_procedure.bat file.

You can also create a shortcut of the daily_procedure.bat file and paste it to the startup folder of windows so it will run everytime windows starts.

## To Plot your assets:

You can run the plot_assets file from the command line or you can simply execute the plot_assets.bat file if you are in windows.

## Further Development

Sınce I only have the basic api plan, I could not improve the daily procedure file. Normally, my plan was to create a procedure that runs on startup and records the every day passed since the last time procedure was run. Sınce I don't have a better api key, I could not test that but if you are interested in this functionality and need my help, feel free to contact me.

afsin1942@icloud.com
