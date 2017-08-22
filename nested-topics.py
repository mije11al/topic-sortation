#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Functions for reading a xls-file, iterate over it and construct a nested dictionary
@Author: Håvard Lundberg, with Modifications by Michael Jensen
@Date:   2017-08-22
@Email:  havard.lundberg@gmail.com, michael@nextwork.as

'''

import pandas as pd
from pprint import pprint
import numpy as np
import glob
import json
import os
import re


#Replace this with your own location for topic-sortation
path=r'C:/Users/micha/topic-sortation/'

#Reads in nested datafile
df = pd.read_excel\
    (path+'keys_for_nested_topics/nested.xlsx',
     sheetname='Sheet1', header=0,encoding='utf-8')

topics = {}

#creates empted dictionary with correct structure
for index, row in df.iterrows():
    #print row["niveau 1"], row["niveau 2"], row["niveau 3"]
    if row["niveau 1"] not in topics:
        topics[row["niveau 1"]] = {}
    if row["niveau 2"] not in topics[row["niveau 1"]]:
        topics[row["niveau 1"]][row["niveau 2"]] = {}
    else:
        topics[row["niveau 1"]][row["niveau 2"]][row["niveau 3"]]={}

print pprint(topics)


all_files = glob.glob(os.path.join(path, 'out/*.xlsx'))

#reads in all relevant data as dataframe
for f in all_files:
    name = os.path.basename(f)
    data = pd.read_excel(f)
    data = data.replace(np.nan, '', regex=True)

print data.columns

#Sorts data into nested structure
for column in data.columns:
    for k, v in topics.items():
        for k1, v1, in v.items():
            for k2, v2 in v1.items():
                if k2==column:
                    v1[k2]=v1[k2]= data['Message'].loc[data[column]==1].tolist()
                # else:
                #     v1[k2]=''

#Outputs topics into json file
with open("topics.json","w") as f:
    json.dump(topics,f)
