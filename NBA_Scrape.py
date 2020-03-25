#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 25 17:37:56 2020

@author: james
"""

## Web Scraping at https://www.basketball-reference.com/leagues/NBA_2019_games.html
#%% Load some libraries
import sys
import os
import pandas as pd
import selenium
import time
from bs4 import BeautifulSoup
import random
from datetime import datetime
from sklearn.model_selection import train_test_split
from matplotlib import pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error
from sklearn.linear_model import LassoLarsCV
#%% try opening webpage
# adjust the path for Python to find the chrome driver
from selenium import webdriver as webd

# launch the "drone" browser - commanded from Python
mydriver = webd.Chrome()

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games.html")
#%%
def get_all_attributes_of_element(driver, element):
    xx = driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)
    return(xx)
#get_all_attributes_of_element(mydriver, box_score_link[0])

#%%
box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

#%%
def my_scrape_boxscore(driver, urlpage):
    try:
        driver.get(urlpage)
        
        myteams = driver.find_elements_by_class_name('game_summary.current')[0]
        win_team = myteams.find_elements_by_class_name('winner')[0]
        win_tname = win_team.find_element_by_css_selector('a').text
        lose_team = myteams.find_elements_by_class_name('loser')[0]
        lose_tname = lose_team.find_element_by_css_selector('a').text
        
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        win_table = soup.select("#box-" + str(win_tname) +"-game-basic")
        win_df = pd.read_html(str(win_table), header = 1)
        win_df = win_df[0]
        win_df["Starters"]  
        win_df["Opposing_Team"] = lose_tname
        
        date_area = driver.find_element_by_class_name("scorebox_meta")
        date_time = date_area.find_element_by_css_selector('div').text
        game_time, date = date_time.split(',', 1)
        win_df["game_time"] = game_time
        win_df["date"] = date
        
        lose_table = soup.select("#box-" + str(lose_tname) +"-game-basic")
        lose_df = pd.read_html(str(lose_table), header = 1)
        lose_df = lose_df[0]
        lose_df["Opposing_Team"] = win_tname
        lose_df["game_time"] = game_time
        lose_df["date"] = date
        
        full_box_score = pd.concat([win_df, lose_df], axis = 0).reset_index(drop = True)
        full_box_score = full_box_score[full_box_score.Starters != "Reserves"]
        full_box_score = full_box_score[full_box_score.Starters != "Team Totals"]
        
        return(full_box_score)
    except Exception as e:
        print("element is not clickable")
        print(e)
        
#%%
boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("/Users/james/Desktop/ADEC7430/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
#%%October
fulldf_oct = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_oct.to_csv("/Users/james/Desktop/ADEC7430/SavedData/fulldf_oct.csv")
#%%November

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-november.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("/Users/james/Desktop/ADEC7430/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_nov = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_nov.to_csv("/Users/james/Desktop/ADEC7430/SavedData")
#%%December
mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-december.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("/Users/james/Desktop/ADEC7430/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_dec = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_dec.to_csv("/Users/james/Desktop/ADEC7430/SavedData/fulldf_dec.csv")
#%%January

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-january.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("/Users/james/Desktop/ADEC7430/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_jan = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_jan.to_csv("/Users/james/Desktop/ADEC7430/SavedData/fulldf_jan.csv")

#%%February

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-february.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("/Users/james/Desktop/ADEC7430/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_feb = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_feb.to_csv("/Users/james/Desktop/ADEC7430/SavedDatafulldf_feb.csv")

#%%March

mydriver.get("https://www.basketball-reference.com/leagues/NBA_2019_games-march.html")

box_score_link = mydriver.find_elements_by_css_selector("td[data-stat = 'box_score_text']")
box_score_links = [x.find_elements_by_css_selector('a')[0].get_attribute('href') for x in box_score_link]
box_score_links

boxscoresdflist = []
for urlpage in box_score_links:
    print(urlpage)
    time.sleep(random.randint(2,4))
    xx = my_scrape_boxscore(mydriver, urlpage)
    team_name = urlpage.split('/')[-1].split('.')[0]
    xx.to_pickle(os.path.join("/Users/james/Desktop/ADEC7430/SavedData", team_name + ".pkl"))
    boxscoresdflist.append(xx.copy())
    
fulldf_mar = pd.concat(boxscoresdflist).reset_index(drop = True)
fulldf_mar.to_csv("/Users/james/Desktop/ADEC7430/SavedData/fulldf_mar.csv")

#%%
full_season_df = pd.concat([fulldf_oct, fulldf_nov, fulldf_dec, fulldf_jan, fulldf_feb, fulldf_mar],
                           axis = 0).reset_index(drop=True)
#%%
full_season_df.to_csv("/Users/james/Desktop/ADEC7430/SavedData/full_season_df.csv")
# =============================================================================
# #%% Read csv if program closes
# recovered_full_season_df = pd.read_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_season_df.csv").reset_index(drop = True)
# recovered_full_season_df.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/recovered_full_season_df.csv")
# recovered_full_season_df = recovered_full_season_df.reset_index(drop = True) 
# #resetting index didn't work when reading the df in.
# print(recovered_full_season_df.iloc[0,3]) #still says 4: will have to drop that column
# #drop column "Unnamed: 0"
# recovered_full_season_df = recovered_full_season_df.drop(["Unnamed: 0"], axis = 1)
# print(recovered_full_season_df.iloc[0,3]) #7. We're in business again. 
# full_season_df = recovered_full_season_df.copy()
# =============================================================================
#%% Remove rows with DNP
# =============================================================================
# full_season1 = full_season_df.copy()
# full_szn = full_season1[full_season1]
# full_szn.to_csv("C:/Users/mjlut/Documents/Grad_School/Big_Data_Econometrics/Assignments/SavedData/full_szn.csv")
# 
# =============================================================================
type(full_season_df.iloc[0,3]) #string
print(full_season_df.iloc[0,3]) #7

"""Because of the way this was created, every value in this dataframe is a string
Unfortunately, we will have to hardcode out any 'Did Not Play', 'Did Not Dress', etc.
Once that is done, we can then change the numbers to numbers
The things we need to remove are:
    Did Not Play
    Did Not Dress
    Not With Team"""
#%% Remove all rows containing the above listed strings
full_season1 = full_season_df.copy()
full_season1 = full_season1[full_season1.MP != "Did Not Play"]
full_season1 = full_season1[full_season1.MP != "Did Not Dress"]
full_season1 = full_season1[full_season1.MP != "Not With Team"]
full_season1.to_csv("/Users/james/Desktop/ADEC7430/SavedData")
#Looks good

#%% Convert numeric values to numbers so we can create calculated columns.
"""We have 19 columns that we need to convert, and fortunately they are all connected. 
Can we convert all columns in one swoop? Columns FG to +/-, or columns 3-21"""
full_szn = full_season1.copy()
full_szn.iloc[:,2:20] = full_szn.iloc[:,2:20].apply(pd.to_numeric)

print(full_szn.iloc[0,2]) #4.0
type(full_szn.iloc[0,2]) #float
print(full_szn.iloc[0,19]) #+9
type(full_szn.iloc[0,19]) #string - this is ok, we won't use this column anyways. 
#all set to move on with creating calculated columns

#%% Create column for fantasy points using DraftKings standard scoring
#Will be easier if I create columns for double-double and triple double first
def double_double(df):
    if df["PTS"] >= 10 and df["AST"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["TRB"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["TRB"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["TRB"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["TRB"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["BLK"] >= 10 and df["STL"] >= 10:
        return(1)
    else:
        return(0)
        
full_szn["dbl-dbl"] = full_szn.apply(double_double, axis = 1) 
full_szn.to_csv("/Users/james/Desktop/ADEC7430/SavedData")
#%% Triple double
def triple_double(df): 
    if df["PTS"] >= 10 and df["AST"] >= 10 and df["TRB"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["AST"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["AST"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["TRB"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["TRB"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["PTS"] >= 10 and df["STL"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["TRB"] >= 10 and df["STL"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["TRB"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["AST"] >= 10 and df["STL"] >= 10 and df["BLK"] >= 10:
        return(1)
    elif df["TRB"] >= 10 and df["STL"] >= 10 and df["BLK"] >= 10:
        return(1)
    else:
        return(0)
full_szn["trip-dbl"] = full_szn.apply(triple_double, axis = 1) 
full_szn.to_csv("/Users/james/Desktop/ADEC7430/SavedData/full_szn.csv")

#%%
def classic_scoring(df):
    fantasy_points = (0.5 * df["3P"] +
                      0.5 * df["3P"] +
                      1.25 * df["TRB"] +
                      1.5 * df["AST"] +
                      2 * df["BLK"] -
                      0.5 * df["TOV"] +
                      1.5 * df["dbl-dbl"] +
                      3 * df["trip-dbl"])
    return(fantasy_points)

full_szn["fantasy_points"] = full_szn.apply(classic_scoring, axis = 1)
full_szn.to_csv("/Users/james/Desktop/ADEC7430/SavedData")

