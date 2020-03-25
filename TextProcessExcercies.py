#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 10:48:17 2019

@author: james
"""
#%% load some libraries
import sys
import os
import pandas as pd
import selenium
import time

#%%

from selenium import webdriver as webd

# launch the "drone" browser - commanded from Python
mydriver = webd.Chrome()
mydriver.get("https://www.amazon.com/dp/B003Q40V92")

#%% find the ratings link and click on it
customer_reviews_list = mydriver.find_elements_by_id('acrCustomerReviewLink')
[x.text for x in customer_reviews_list]
# choose the first one and click

elt = customer_reviews_list[0]
elt.click()

# find the page of reviews - start from the root of the "tree" (webpage)
reviews_list = mydriver.find_elements_by_id('cm-cr-dp-review-list')
reviews_list = reviews_list[0] # there is only one section / element with reviews

# identify all children of this element by class name
indiv_reviews_list = reviews_list.find_elements_by_class_name('review-text-content')

temp_reviews_page = pd.DataFrame([x.text for x in indiv_reviews_list])
#@@ for RV - figure out how much data came when the page at Amazon was "pulled" (get)


#%% better - start directly with all reviews for that given page
mydriver.get("https://www.amazon.com/product-reviews/B003Q40V92/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")

reviews_list = mydriver.find_elements_by_id('cm_cr-review_list')
reviews_list = reviews_list[0] # only one element

# find all visible children - these are individual reviews
reviews = reviews_list.find_elements_by_class_name('a-section.review') # see the link above, these are 2 classes that do not need to be next to each other
temp_page_reviews = pd.DataFrame({
        'id':[x.id for x in reviews],
        'text':[x.text for x in reviews],
        'date':[x.find_element_by_class_name('review-date').text for x in reviews]
        })


pages_scraped_list = [temp_page_reviews]
#%%
should_I_continue = True
last_elt = mydriver.find_elements_by_class_name('a-last')
if len(last_elt)==0:
    should_I_continue = False
    
cnt = 0
while ((should_I_continue) & (cnt < 10)):
    cnt += 1
    last_elt = last_elt[0]
    last_elt.click()
    time.sleep(2)

    reviews_list = mydriver.find_elements_by_id('cm_cr-review_list')
    reviews_list = reviews_list[0] # only one element
    
    # find all visible children - these are individual reviews
    reviews = reviews_list.find_elements_by_class_name('a-section.review') # see the link above, these are 2 classes that do not need to be next to each other
    temp_page_reviews = pd.DataFrame({
            'id':[x.id for x in reviews],
            'text':[x.text for x in reviews],
            'date':[x.find_element_by_class_name('review-date').text for x in reviews]
            })
    temp_page_reviews['page'] = cnt
    pages_scraped_list.append(temp_page_reviews.copy())    

    # now paginate if you can
    last_elt = mydriver.find_elements_by_class_name('a-last')
    if len(last_elt)==0:
        should_I_continue = False
    
#%%
all_reviews = pd.concat(pages_scraped_list)
#%%
import re
tbl1=pd.DataFrame()
tbl1['text_id']=all_reviews['id']
tbl1['text_raw']=all_reviews['text']
re_fluff = re.compile('(.*)\n[0-9]+ people found this helpful.*', re.DOTALL )



remove_punct = ['.',',','-',';',':',"'"]
def clean_punct(mystr):
    for tp in remove_punct:
        mystr = mystr.replace(tp, ' ')
    return(mystr)

def remove_fluff(my_str):
    try:
        str_no_fluff = re_fluff.match(my_str).groups()[0]
        return(str_no_fluff)
    except Exception as e:
        return(my_str)
        
tbl1['text_clean']=tbl1['text_raw'].apply(lambda x: remove_fluff(x))

tbl1['text_clean']=tbl1['text_clean'].apply(lambda x: clean_punct(x))      

tbl1=tbl1.reset_index()
tbl1

#%%
table2=pd.DataFrame()
table2['text_clean']=tbl1['text_clean']
table2['text_id']=tbl1['text_id']
df_try=pd.DataFrame(table2.text_clean.str.split('\n').tolist(), index= table2.text_id).stack()
df_try
#%%
table2=pd.DataFrame(df_try).reset_index()

table2.rename(columns={'level_1':'paragraph_id',
                       0:'par_text'}, inplace = True)
table2
#%%
from collections import Counter

def get_df_from_text(mystr):
#    Counter("this is a silly test with a silly text is this".split(' '))
#    mystr = "this is a silly test with a silly text is this"
    tdict = Counter(mystr.split(' '))
    xx = pd.DataFrame({'kwd':list(tdict.keys()), 'cnt':list(tdict.values())})
    return(xx)
#%%
get_df_from_text('this is a silly test of a silly text is it')
#%%
table3=table2.drop(columns=['text_id']).set_index(table2['paragraph_id'])
table3.drop(columns=['paragraph_id'])
#%%
yy=table3.par_text.apply(lambda x: get_df_from_text(x))

yy_list=pd.concat(list(yy))
#%%
index_tracker=0
par_list=[]

for x in yy_list.index:
    if x==0:
        index_tracker +=1
        par_list.append(index_tracker)
    else:
        index_tracker=index_tracker
        par_list.append(index_tracker)
        
yy_list['par_id']=par_list
#%%
table_3=yy_list
table_3









