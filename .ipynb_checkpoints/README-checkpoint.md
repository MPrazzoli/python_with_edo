# This application lets you download periodic data of upto 5000 stocks traded in US market.

# Requisities to run the project in your local machine.

# MacOS
1. Editor - Pycharm, VB Studio code or any other editor of your preference is fine.
2. Python 3.9
3. brew install pipenv # if you have brew installed
   pip3 install pipenv # if you don't have brew installed
   
# Windows
1. Editor - Pycharm, VB Studio code or any other editor of your preference is fine.
2. Python 3.9
3. 

# Project Architecture:
The project is divided into 4 main sections: Academy, Analysis, Database and Application.

# Academy
This folder consists of all the reading materials that could be useful for making qualitative/quantitative analysis on the stock data. 

# Analysis
This folder consists of all the files that are used for analysis the data retrieved for various stocks. You can create your individual files to customise your analysis.

# Database
The folder named pickle_obj is where all the stock data retrieved from yahoo finance and investing.com are stored on a folder within called stock_dataframes. Folder named 'not_found_records' is where stocks with less/coruppted data are stored and aren't used for analyse purpose.

# Application
You can either launch daily script or periodic script depending on your need. By running file daily_app.py you can download data of every stock for that and by running period_app.py, you can download data for custom time frame as you require.

