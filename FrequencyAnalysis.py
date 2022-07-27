#!/usr/bin/env python
# coding: utf-8

import statistics as stats
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

def adjacent_values(vals, q1, q3):
    upper_adjacent_value = q3 + (q3 - q1) * 1.5
    upper_adjacent_value = np.clip(upper_adjacent_value, q3, vals[-1])

    lower_adjacent_value = q1 - (q3 - q1) * 1.5
    lower_adjacent_value = np.clip(lower_adjacent_value, vals[0], q1)
    return lower_adjacent_value, upper_adjacent_value


def FreqAnalysis(filename, path, paper, emotion):
# In[164]:
    df = pd.read_csv(path, delimiter=',')
    df.fillna('', inplace=True)
    # print(df)
    emo_df = pd.read_csv('au_to_emotion.csv', delimiter=',', names=('Emotion', 'Cor', 'Kel', 'Du', 'PhyDes'))
    emo_df = emo_df.iloc[1: , :]
    emos = pd.array(emo_df['Emotion'], dtype="string")
    emos_2 = list(emos)
    n_faces = df['face_id'].max() + 1

    per = []
    i = 0
    for emo in emos:
    # emo = "Amusement"
        filter1 = df['Cordaro'].str.find(emo) != -1
        filter2 = df['Keltner'].str.find(emo) != -1
        filter3 = df['Du'].str.find(emo) != -1

        copy = df
        cordf = copy.loc[filter1]
        foo1 = cordf.groupby('face_id').count()
    #     print(newdf)
        foo1 = foo1.add_suffix('_').reset_index()
        cordf1 = foo1[['face_id','Cordaro_']]
    #     print(cordf1)
        
        keldf = copy.loc[filter2]
        foo2 = keldf.groupby('face_id').count()
        foo2 = foo2.add_suffix('_').reset_index()
        keldf1 = foo2[['face_id','Keltner_']]
        
        dudf = copy.loc[filter3]
        foo3 = dudf.groupby('face_id').count()
        foo3 = foo3.add_suffix('_').reset_index()
        dudf1 = foo3[['face_id','Du_']]
        
        result = pd.merge(cordf1, keldf1,how="outer", on="face_id")
        result = pd.merge(result, dudf1,how="outer", on="face_id")
        per.append(result)
        i += 1

#### FROM HERE

##### TILL HERE


    # i = 0
    n_frames = df['frame'].max()

    ind = emos_2.index(emotion)
    if (per[ind].empty):
        c_ = [0 for n in range(n_faces)]
    else:
        c_ = [0 if math.isnan(n) else (n*100)/n_frames for n in per[ind][paper + "_"]]
    data_to_plot1 = [c_]
    quartile1, medians, quartile3 = np.percentile(data_to_plot1, [25, 50, 75], axis=1)
    whiskers = np.array([
        adjacent_values(sorted_array, q1, q3)
        for sorted_array, q1, q3 in zip(data_to_plot1, quartile1, quartile3)])
    whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

    inds = np.arange(1, len(medians) + 1)

    return [per, data_to_plot1, inds, medians, quartile1, quartile3, whiskers_min, whiskers_max]

