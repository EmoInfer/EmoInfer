#!/usr/bin/env python
# coding: utf-8

# In[11]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def ExtractEmotion(arg):
# In[12]:

    df = pd.read_table(arg, delimiter=',')

    emo_df = pd.read_table('~/Desktop/zurichproj/GUIEmotionAnalysis/au_to_emotion.csv', delimiter=',', names=('Emotion', 'Cor', 'Kel', 'Du', 'PhyDes'))
    # print(df)
    # valid when <1000 ppl in video
    df['unique_id'] = df['frame']*1000 + df['face_id']
    # print(df)
    emo_df = emo_df.iloc[1: , :]
    # emo_df 


# # In[13]:

    aus = ['AU01_c',"AU02_c","AU04_c","AU05_c","AU06_c","AU07_c","AU09_c","AU10_c","AU12_c","AU14_c","AU15_c","AU17_c","AU20_c","AU23_c","AU25_c","AU26_c","AU28_c","AU45_c"]
    df['num_faces'] = df['frame'].map(df['frame'].value_counts())
    AUs = [ [] for _ in range(df.shape[0]) ]

    for i in range(df.shape[0]):
        for au in aus:
    #         print(au)
    #         print(i)
    #         print(df2.iloc[i][au])
            if df.iloc[i][au] >= 1:
    #             print('here')
                string = au[2] + au[3]
        #             print(string)
                AUs[i] = np.append(AUs[i],str(int(string)))
    #             print(AUs[i])
        
    for i in range(df.shape[0]):
        AUs[i] = ', '.join(map(str, AUs[i]))
    # print(AUs)

    Emos = [ [] for _ in range(df.shape[0])]
    Emostrings = [ [] for _ in range(df.shape[0])]
    Cor = [ [] for _ in range(df.shape[0])]
    Kel = [ [] for _ in range(df.shape[0])]
    Du = [ [] for _ in range(df.shape[0])]

    for i in range(df.shape[0]):
        tst = list(AUs[i].split(", "))
        for j in range(28):
            cor = list(emo_df.Cor[j+1].split(", "))
            kel = list(emo_df.Kel[j+1].split(", "))
            du = list(emo_df.Du[j+1].split(", "))
            if (set(tst) & set(cor) == set(cor)):
                Emos[i] = np.append(Emos[i],emo_df.Emotion[j+1] + ": Cordaro")
                Cor[i] = np.append(Cor[i],emo_df.Emotion[j+1])
            if (set(tst) & set(kel) == set(kel)):
                Emos[i] = np.append(Emos[i],emo_df.Emotion[j+1] + ": Keltner")
                Kel[i] = np.append(Kel[i],emo_df.Emotion[j+1])
            if (set(tst) & set(du) == set(du)):
                Emos[i] = np.append(Emos[i],emo_df.Emotion[j+1] + ": Du")
                Du[i] = np.append(Du[i],emo_df.Emotion[j+1])
    for i in range(df.shape[0]):
        Emostrings[i] = ", ".join(Emos[i])
        Cor[i] = ", ".join(Cor[i])
        Kel[i] = ", ".join(Kel[i])
        Du[i] = ", ".join(Du[i])
    # print(len(Emos))
    # print(df.shape[0])
    # Emostrings
    dat = zip(df.frame, df.face_id, Cor, Kel, Du)
    newdf = pd.DataFrame(dat, columns = ['frame', 'face_id','Cordaro', 'Keltner', 'Du'])
    # print(newdf)
    newdf.to_csv("~/Desktop/zurichproj/GUIEmotionAnalysis/extracted.csv")
    path = "~/Desktop/zurichproj/GUIEmotionAnalysis/extracted.csv"
    # Emostrings

    return newdf, path


# In[ ]:




