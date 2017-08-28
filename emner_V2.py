# -*- coding: latin-1 -*-
"""
spyder editor

updated 14-03-2017
"""

import pandas as pd
import os, re
import glob
import numpy as np

# ==============================================================================
import sys

reload(sys)
sys.setdefaultencoding('latin-1')


# ==============================================================================


path = r'/Users/nextwork/Dropbox/PycharmProjects/topics/'

def dagsordener(self):
    df = pd.read_excel(r'/Users/nextwork/Dropbox/PycharmProjects/topics/topic_index.xlsx',
                       sheetname='keywords')
    df = df.replace(np.nan, "{}", regex=True)
    for column in df.columns:
        self[column] = self['Message'].str.contains('|'.join
        (map(re.escape, df[column].values, )))
        return self





# ==============================================================================




def kval_analyzer(path):
    all_files = glob.glob(os.path.join(path, 'input/dansk_erhverv/*.xlsx'))
    for f in all_files:
        name = os.path.basename(f)
        result = []
        df = pd.read_excel(f)  # doesn't create a list, nor does it append to one
        dagsordener(df)
        # converts bools to numbers
        df_num = df.loc[:, 'aeldre':'yderomraader'].applymap(lambda x: 1 if x else 0)
        nozero = df_num.replace(0, "")
        df_label = nozero.loc[:, 'aeldre':'yderomraader'].replace\
        (1, pd.Series(df_num.columns, df_num.columns))
        temp = []
        temp = df_label.combine_first(df)
        temp['Emner'] = temp.loc[:, 'aeldre':'yderomraader'].apply\
        (lambda x: ','.join(x.dropna()), axis=1)
        temp.to_excel(path+'output/' + name)


def quant_analyzer(path):
    all_files = glob.glob(os.path.join
    (path,"input/dansk_erhverv/*.xlsx"))  # advisable to use os.path.join as this makes concatenation OS independent
    for f in all_files:
        name = os.path.basename(f)
        df = pd.read_excel(f)  # doesn't create a list, nor does it append to one
        dagsordener(df)
        # converts bools to numbers
        df_num = df.loc[:, 'aeldre':'yderomraader'].applymap\
            (lambda x: 1 if x else 0)
        temp = df_num.combine_first(df)
        # temp.loc['Total']= temp.sum()
        # temp=temp.dropna()
        return temp.to_excel(path + "output/dansk_erhverv/out_" + name)


quant_analyzer(path)



