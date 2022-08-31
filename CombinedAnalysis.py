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


def CombFreqAnalysis(filenames, n_videos, paper, emotion, time_gran):
    filename = "".join(filenames)
    dfs = []
    for i in range(n_videos):
        df = pd.read_csv('extracted/extracted_{}.csv'.format(filenames[i]), delimiter=',', skipinitialspace=True)
        df.fillna('', inplace=True)
        # print(df)
        dfs.append(df)
    emo_df = pd.read_csv('au_to_emotion.csv', delimiter=',', skipinitialspace=True, names=('Emotion', 'Cor', 'Kel', 'Du', 'PhyDes'))
    emo_df = emo_df.iloc[1: , :]
    emos = pd.array(emo_df['Emotion'], dtype="str")
    emos_2 = list(emos)
    combined_df = pd.DataFrame()
    fac = 0
    for i in range(n_videos):
        fcs = dfs[i]['face_id'].max() + 1
        dfs[i]['face_id'] = dfs[i]['face_id'] + fac
        fac = fac + fcs
        # print(dfs[i])
        combined_df = combined_df.append(dfs[i])
        
    # print(combined_df)

    df = combined_df
    # In[165]:
    n_faces = df['face_id'].max() + 1
    n = time_gran

    per = []

#### FROM HERE
    i = 0
    for emo in emos:
        filter1 = df['Cordaro'].str.find(emo) != -1
        filter2 = df['Keltner'].str.find(emo) != -1
        filter3 = df['Du'].str.find(emo) != -1

        copy = df

        cordf = copy.loc[filter1]
        tem = cordf.groupby('face_id')
        cor_df1 = pd.DataFrame(columns = ['face_id', 'Cordaro_'])

        for name, group in tem:
            count_cor = 0
            i_cor = 0
            rows = group.shape[0]
            while i_cor < rows:
                f = group.iloc[i_cor, 1]
                f_prev = f
                rem = (f % n)
                if rem == 0:
                    rem = n
                left = n - rem
                temp = 1
                i_cor += 1
                while f <= (f_prev + left) and i_cor < rows:
                    f = group.iloc[i_cor, 1]
                    if f <= (f_prev + left):    
                        temp += 1
                    else:
                        break
                    i_cor += 1

                if temp >= (n/2 + n%2) and n >= 2:
                    count_cor += 1
                if n == 1:
                    count_cor += 1
            cor_df1 = cor_df1.append({'face_id' : name, 'Cordaro_' : count_cor},
                ignore_index = True)

        keldf = copy.loc[filter2]

        tem = keldf.groupby('face_id')
        kel_df1 = pd.DataFrame(columns = ['face_id', 'Keltner_'])

        for name, group in tem:
            count_kel = 0
            i_kel = 0
            rows = group.shape[0]
            while i_kel < rows:
                f = group.iloc[i_kel, 1]
                f_prev = f
                rem = (f % n)
                if rem == 0:
                    rem = n
                left = n - rem
                temp = 1
                i_kel += 1
                while f <= (f_prev + left) and i_kel < rows:
                    f = group.iloc[i_kel, 1]
                    if f <= (f_prev + left):    
                        temp += 1
                    else:
                        break
                    i_kel += 1

                if temp >= (n/2 + n%2) and n >= 2:
                    count_kel += 1
                if n == 1:
                    count_kel += 1

            kel_df1 = kel_df1.append({'face_id' : name, 'Keltner_' : count_kel},
                ignore_index = True)

        dudf = copy.loc[filter3]
        tem = dudf.groupby('face_id')
        du_df1 = pd.DataFrame(columns = ['face_id', 'Du_'])

        for name, group in tem:
            count_du = 0
            i_du = 0
            rows = group.shape[0]
            while i_du < rows:
                f = group.iloc[i_du, 1]
                f_prev = f
                rem = (f % n)
                if rem == 0:
                    rem = n
                left = n - rem
                temp = 1
                i_du += 1
                while f <= (f_prev + left) and i_du < rows:
                    f = group.iloc[i_du, 1]
                    if f <= (f_prev + left):    
                        temp += 1
                    else:
                        break
                    i_du += 1

                if temp >= (n/2 + n%2) and n >= 2:
                    count_du += 1
                if n == 1:
                    count_du += 1

            du_df1 = du_df1.append({'face_id' : name, 'Du_' : count_du},
                ignore_index = True)

        result = pd.merge(cor_df1, kel_df1,how="outer", on="face_id")
        result = pd.merge(result, du_df1,how="outer", on="face_id")
        per.append(result)
        i += 1
##### TILL HERE


    # i = 0
    n_frames = df['frame'].max()

    n_frames = (n_frames/n) + (n_frames%n > 0)
    
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

