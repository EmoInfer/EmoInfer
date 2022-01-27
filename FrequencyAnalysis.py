#!/usr/bin/env python
# coding: utf-8

# In[163]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def FreqAnalysis(path):
# In[164]:
    df = pd.read_table(path, delimiter=',')
    df.fillna('', inplace=True)
    # print(df)
    emo_df = pd.read_table('~/Desktop/zurichproj/GUIEmotionAnalysis/au_to_emotion.csv', delimiter=',', names=('Emotion', 'Cor', 'Kel', 'Du', 'PhyDes'))
    emo_df = emo_df.iloc[1: , :]
    emos = pd.array(emo_df['Emotion'], dtype="string")


    # In[165]:


    # df2 = df.groupby('face_id')
    # print(df)
    # per_cor = [pd.DataFrame() for emo in emos]
    per = []
    # print(emos)
    # df['Cordaro'] == "Surprise"
    # df2.count()
    # emo = "Surprise"
    # print(df['Cordaro'].str.find(emo))
    i = 0
    for emo in emos:
    # emo = "Amusement"
        filter1 = df['Cordaro'].str.find(emo) != -1
        filter2 = df['Keltner'].str.find(emo) != -1
        filter3 = df['Du'].str.find(emo) != -1

        copy = df
        #     print(copy)
        #     print(df)
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
        # print(result)
        #     print(per_cor[i])
        #     .groupby('face_id').count()
        #     per_kel[i] = df.groupby('face_id').where(df['Keltner'].find(emo) != -1).count()
        #     per_du[i] = df.groupby('face_id').where(df['Du'].find(emo) != -1).count()
        i += 1
    # print(copy)


    # In[166]:


    import matplotlib.pyplot as plt

    plt.figure()
    i = 0
    for emo in emos:
        if i == 13:
            break
        plt.bar([i+1],[per[i]['Cordaro_'].sum()], label=emo)
        i += 1
    #     plt.bar()

    # plt.bar([2,4,6,8,10],[8,6,2,5,6], label="Example two", color='g')
    # plt.legend(loc = 7, bbox_to_anchor=(1.5, 0.5))
    plt.legend(loc='best')
    plt.ylabel('# of frames x # of faces')
    plt.xlabel('Emotion')

    plt.title('Cordaro et. al')

    plt.show()

    plt.figure()
    i = 0
    for emo in emos:
        if i == 15:
            break
        plt.bar([i+1],[per[i]['Keltner_'].sum()], label=emo)
        i += 1
    #     plt.bar()

    # plt.bar([2,4,6,8,10],[8,6,2,5,6], label="Example two", color='g')
    # plt.legend(loc = 7, bbox_to_anchor=(1.5, 0.5))
    plt.legend(loc='best')
    plt.ylabel('# of frames x # of faces')
    plt.xlabel('Emotion')

    plt.title('Keltner et. al')

    plt.show()

    plt.figure()
    i = 0
    for emo in emos:
        plt.bar([i+1],[per[i]['Du_'].sum()], label=emo)
        i += 1
    #     plt.bar()

    # plt.bar([2,4,6,8,10],[8,6,2,5,6], label="Example two", color='g')
    # plt.legend(loc = 7, bbox_to_anchor=(1.95, 0.5), ncol = 2)
    plt.legend(loc='best')
    plt.ylabel('# of frames x # of faces')
    plt.xlabel('Emotion')

    plt.title('Du et. al')

    plt.show()


# In[ ]:




