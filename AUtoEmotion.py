#!/usr/bin/env python
# coding: utf-8

# In[11]:


# from asyncio.windows_events import None
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

def ExtractEmotion(arg, filename, auint, poserx, poserz):
# In[12]:

    df = pd.read_table(arg, delimiter=',')

    emo_df = pd.read_table('au_to_emotion.csv', delimiter=',', names=('Emotion', 'Cor', 'Kel', 'Du', 'PhyDes'))
    # print(df)
    # valid when <1000 ppl in video

    emo_df = emo_df.iloc[1: , :]

    if auint is not None:
        poserxthres = poserx
        poserzthres = poserz
    
    else:
        poserxthres = 0.25
        poserzthres = 0.25

    df['AU53_c'] = ""
    df['AU54_c'] = ""
    df['AU55_c'] = ""
    df['AU56_c'] = ""
    # df['AU53_c'] = [1 for item in df['pose_Rx'] if item < -0.25]
    i = 0
    for item in df['pose_Rx']:
    #     print(item)
        if item < -poserxthres:
            df['AU53_c'][i] = 1
            df['AU54_c'][i] = 0
        else:
            if item > poserxthres:
                df['AU54_c'][i] = 1
                df['AU53_c'][i] = 0
            else:
                df['AU54_c'][i] = 0
                df['AU53_c'][i] = 0
        i += 1

    i = 0
    for item in df['pose_Rz']:
    #     print(item)
        if item < -poserzthres:
            df['AU55_c'][i] = 1
            df['AU56_c'][i] = 0
        else:
            if item > poserzthres:
                df['AU56_c'][i] = 1
                df['AU55_c'][i] = 0
            else:
                df['AU55_c'][i] = 0
                df['AU56_c'][i] = 0
        i += 1
        

    df['unique_id'] = df['frame']*1000 + df['face_id']
    # print(df)
    # emo_df 


# # In[13]:

    # aus = ['AU01_c',"AU02_c","AU04_c","AU05_c","AU06_c","AU07_c","AU09_c","AU10_c","AU12_c","AU14_c","AU15_c","AU17_c","AU20_c","AU23_c","AU25_c","AU26_c","AU28_c","AU45_c"]
    aus = ['AU01_c',"AU02_c","AU04_c","AU05_c","AU06_c","AU07_c","AU09_c","AU10_c","AU12_c","AU14_c","AU15_c","AU17_c","AU20_c","AU23_c","AU25_c","AU26_c","AU28_c","AU45_c","AU53_c","AU54_c","AU55_c","AU56_c"]
    aus_r =  ['AU01_r',"AU02_r","AU04_r","AU05_r","AU06_r","AU07_r","AU09_r","AU10_r","AU12_r","AU14_r","AU15_r","AU17_r","AU20_r","AU23_r","AU25_r","AU26_r","AU28_r","AU45_r","AU53_c","AU54_c","AU55_c","AU56_c"]
    df['num_faces'] = df['frame'].map(df['frame'].value_counts())
    AUs = [ [] for _ in range(df.shape[0]) ]

    for i in range(df.shape[0]):
        for j in range(len(aus)):
    #         print(au)
    #         print(i)
    #         print(df2.iloc[i][au])
            if auint is None:
                if df.iloc[i][aus[j]] >= 1:
        #             print('here')
                    string = aus[j][2] + aus[j][3]
            #             print(string)
                    AUs[i] = np.append(AUs[i],str(int(string)))
            else:
                if (j >= len(aus) - 4) or aus[j] == "AU28_c":
                    if df.iloc[i][aus[j]] >= 1:
                        string = aus[j][2] + aus[j][3]
                        AUs[i] = np.append(AUs[i],str(int(string)))
                else:
                    if df.iloc[i][aus_r[j]] >= auint:
        #             print('here')
                        string = aus_r[j][2] + aus_r[j][3]
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
    newdf.to_csv("extracted/extracted_{}.csv".format(filename))
    path = "extracted/extracted_{}.csv".format(filename)
    # Emostrings
    print("Result saved to {}", path)
    return newdf, path


# In[ ]:




