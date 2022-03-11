#!/usr/bin/env python
# coding: utf-8

# In[163]:


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

    i = 0
    n_frames = df['frame'].max()
    # per.replace(np.nan, 0)
    for emo in emos:
        c1 = [0 if math.isnan(n) else (n*100)/n_frames for n in per[i]["Cordaro_"]]
        c2 = [0 if math.isnan(n) else (n*100)/n_frames for n in per[i]["Keltner_"]]
        c3 = [0 if math.isnan(n) else (n*100)/n_frames for n in per[i]["Du_"]]
        ## combine these different collections into a list
        data_to_plot = [c1, c2, c3]

        # Create a figure instance
        fig = plt.figure()

        # Create an axes instance
        ax = fig.add_axes([0,0,1,1])

        # Create the boxplot
        parts = ax.violinplot(data_to_plot, showmeans=False, showmedians=False,
            showextrema=True)
    #     ax2.set_title('Customized violin plot')
    #     parts = ax2.violinplot(
    #             data, showmeans=False, showmedians=False,
    #             showextrema=False)

        for pc in parts['bodies']:
            pc.set_facecolor('#D43F3A')
            pc.set_edgecolor('black')
            pc.set_alpha(1)

        quartile1, medians, quartile3 = np.percentile(data_to_plot, [25, 50, 75], axis=1)
        whiskers = np.array([
            adjacent_values(sorted_array, q1, q3)
            for sorted_array, q1, q3 in zip(data_to_plot, quartile1, quartile3)])
        whiskers_min, whiskers_max = whiskers[:, 0], whiskers[:, 1]

        inds = np.arange(1, len(medians) + 1)
        ax.scatter(inds, medians, marker='o', color='white', s=30, zorder=3)
        ax.vlines(inds, quartile1, quartile3, color='k', linestyle='-', lw=5)
        ax.vlines(inds, whiskers_min, whiskers_max, color='k', linestyle='-', lw=1)
        plt.ylim(0, 100)
        plt.title(emo)
        # plt.xlabel("Cordaro, Keltner, Du")
        # plt.ylabel("percentage")
        plt.show()
        i += 1

# In[ ]:




