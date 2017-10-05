#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 12:42:35 2017

@author: ruixin
"""

import sqlite3
import csv
import pandas as pd
       
reset = True

conn = sqlite3.connect('nytimes.db')
cur = conn.cursor()

if reset:
    cur.execute("DROP TABLE IF EXISTS Comments")

table_spec = 'CREATE TABLE IF NOT EXISTS '
table_spec += 'Comments (post_id TEXT, comment_id TEXT, answer TEXT)'
cur.execute(table_spec)

statement = 'INSERT INTO Comments VALUES (?, ?, ?)'

with open('/Users/ruixin/Desktop/SI 618/Lab/lab5/Facebook_API/Data/si618_f17_hw5_batch_result_rxjiang_spoonert.csv', 'r') as csvFile:
    batchFile = csv.reader(csvFile, lineterminator='\r\n')
    next(batchFile)
    for row in batchFile:
        if len(row[31].split('|')) == 1:
            t = (row[28], row[29], row[31])
            cur.execute(statement, t)
        else:
            for i in row[31].split('|'):
                t = (row[28], row[29], i)
                cur.execute(statement, t)
    
conn.commit()

# count the number of each answer for comments
q = 'SELECT post_id, comment_id, answer, COUNT(*) AS num FROM Comments GROUP BY comment_id, answer'
r = cur.execute(q)
res = []
data = []
for row in r:
    data.append([row[0], row[1], 0, 0, 0, 0, 0, 0])
    res.append(row)
    print(row)

# reshape dataframe from long format to wide format
df_long = pd.DataFrame(res, columns = ['post_id', 'comment_id', 'answer', 'count'])
df_wide = df_long.pivot(index='comment_id', columns='answer', values='count')
df_wide.fillna(0, inplace=True)

# set comment_id as index to update with values in df_wide 
df = pd.DataFrame(data, columns = ['post_id', 'comment_id', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5', 'answer_6']).drop_duplicates()
df.set_index('comment_id', inplace=True)
df.update(df_wide)
df.reset_index(level=0, inplace=True)

# add new columns to dataframe
df['pagename'] = 'nytimes'

# change the order of columns in dataframe
df = df[['pagename', 'post_id', 'comment_id', 'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5', 'answer_6']]
df.to_csv('si618_f17_hw5_cleaned_data_rxjiang_spoonert.csv', index=False)
