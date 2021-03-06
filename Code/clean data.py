# -*- coding: utf-8 -*-
"""
Created on Thu Oct  5 12:59:10 2017

@author: spoonertaylor
"""

import pandas as pd

dt = pd.read_csv("C:/Users/Taylor/Documents/Projects/Data/si618_f17_hw5_batch_result_rxjiang_spoonert.csv")
#dt['count'] = 1
# We need rows as
## pagename, post_id, comment_id, comment, answer_1, answer_2, answer_3, answer_4, answer_5, answer_6

dt = dt[['Input.pagename', 'Input.post_id', 'Input.comment_id', 'Input.comment', 'Answer.Answer']]
dt.columns = ['pagename', 'post_id', 'comment_id', 'comment', 'answer']

df_temp = dt['answer'].str.split('|', expand=True).stack()
i = df_temp.index.get_level_values(0)
df_temp2 = dt.loc[i].copy()
df_temp2['answers'] = df_temp.values
del df_temp2['answer']
dt2 = df_temp2.groupby(['pagename', 'post_id', 'comment_id', 'comment', 'answers']).size().reset_index()
dt2.columns = ['pagename', 'post_id', 'comment_id', 'comment', 'answers', 'count']
dt_wide = pd.pivot_table(dt2, index=['pagename', 'post_id', 'comment_id', 'comment'], columns = 'answers', values = 'count')\
                        .reset_index()

dt_wide = dt_wide.fillna(0)
dt_wide['answer_3'] = 0
dt_wide = dt_wide[['pagename', 'post_id', 'comment_id', 'comment',\
                  'answer_1', 'answer_2', 'answer_3', 'answer_4', 'answer_5', 'answer_6']]
dt_wide.to_csv("clean_data.csv", index=False)