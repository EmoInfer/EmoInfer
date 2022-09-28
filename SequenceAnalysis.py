#!/usr/bin/env python
# coding: utf-8

# In[8]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math
import sys, os
import subprocess


def seq_analysis(filenames, n_videos, paper, hyp, time_gran):
    filename = "".join(filenames)
    dfs = []
    for i in range(n_videos):
        df = pd.read_csv('extracted/extracted_{}_{}.csv'.format(filenames[i], time_gran), delimiter=',', skipinitialspace=True)
        df.fillna('', inplace=True)
        # print(df)
        dfs.append(df)

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

    emos = [            'Amusement',             'Happiness',                   'Awe',
                    'Pride',              'Surprise',                 'Anger',
                'Confused',              'Contempt',               'Disgust',
            'Embarrassment',                  'Fear',                  'Pain',
                    'Shame',              'Interest',               'Sadness',
        'Happily Surprised',     'Happily Disgusted',         'Sadly Fearful',
            'Sadly Angry',       'Sadly Surprised',       'Sadly Disgusted',
        'Fearfully Angry',   'Fearfully Surprised',   'Fearfully Disgusted',
        'Angrily Surprised',     'Angrily Disgusted', 'Disgustedly Surprised',
        'Appalled/Hatred']

    for stri in reversed(emos):
        df = df.replace(regex=[stri], value = str(emos.index(stri) + 1))
        

    #print(df)

    # f1 = open("sequencing/Cordaro_raw_sequences_{time_gran}.txt", 'w+')
    # f2 = open("sequencing/Keltner_raw_sequences_{time_gran}.txt", 'w+')
    # f3 = open("sequencing/Du_raw_sequences_{time_gran}.txt", 'w+')

    if not os.path.exists(f"sequencing/{paper}/{filename}/"):
        os.makedirs(f"sequencing/{paper}/{filename}/")

    f_1 = open(f"sequencing/{paper}/{filename}/raw_sequences_{time_gran}.txt", 'w+')

    # COR, KEL,DU
    fcs = np.array(df.face_id)
    face_ids = np.unique(fcs)
    # #print(face_ids)

    for face in face_ids:
        df1 = df.loc[df['face_id'] == face]
        flag_a = 0
        for ind, row in df1.iterrows():
    #         #print(row['Cordaro'])
            if row[paper] is not "":
                f_1.write('<' + str(row['frame']) + '> ' + ' '.join(row[paper].split(", ")) + ' -1 ')
                flag_a = 1
        if flag_a:
            f_1.write('-2\n')
            
    f_1.close()

    os.system(f"java -jar spmf.jar run Fournier08-Closed+time \"sequencing/{paper}/{filename}/raw_sequences_{time_gran}.txt\" \"sequencing/{paper}/{filename}/temp_output_sequences_{time_gran}.txt\" {hyp[0]}% {hyp[1]} {hyp[2]} {hyp[3]} {hyp[4]}")

    # subprocess.run("java -jar ../spmf.jar run Fournier08-Closed+time sequencing/Cordaro_raw_sequences.txt sequencing/output_Cordaro_sequences.txt 75% 15 45 15 45", shell = True)
    # subprocess.run("java -jar ../spmf.jar run Fournier08-Closed+time sequencing/Keltner_raw_sequences.txt sequencing/output_Keltner_sequences.txt 75% 15 45 15 45", shell = True)
    # subprocess.run("java -jar ../spmf.jar run Fournier08-Closed+time sequencing/Du_raw_sequences.txt sequencing/output_Du_sequences.txt 75% 15 45 15 45", shell = True)


    file_a = open(f"sequencing/{paper}/{filename}/temp_output_sequences_{time_gran}.txt", 'r')

    # file1 = open('sequencing/output_Cordaro_sequences_{time_gran}.txt', 'r')
    # file2 = open('sequencing/output_Keltner_sequences_{time_gran}.txt', 'r')
    # file3 = open('sequencing/output_Du_sequences_{time_gran}.txt', 'r')


    set_of_seq = set()


    flag_gt = 1
    flag_sp = 0
    flag_sup = -1

    flag = 2
    flag_read = 100 #read now
    flag_stop = 404 #stop now

    list_l = []
    list_in = []
    while 1:
        # read by character
        char = file_a.read(1)
        if char == '>':
            flag = flag_gt
        if char == ' ' and flag == flag_gt:
            flag = flag_read
        if char == '#':
    #         list_l.append(list_in)
            set_of_seq.add(tuple(list_in))
            list_in = []
            flag = flag_stop
            
        if flag == flag_read:
            s = ""
    #         s = s + char
            while 1:
                char_r = file_a.read(1)
                if char_r == '-':
                    flag = 2
                    break
                if char_r == ' ':
                    list_in.append(s)
                    s = ""
                    continue
                s = s+char_r
    #         list_in.append(s)
        if not char:
            break

    #     #print(char)
    
    file_a.close()

    #print(set_of_seq)

    l = list(set_of_seq)

    # new_file = open(f"sequencing/final_sequences_{paper}_{filename}_{time_gran}.txt", 'w+')
    # new_mult_emos = open(f"sequencing/final_mult_sequences_{paper}_{filename}_{time_gran}.txt", 'w+')
    # new_uniq_emos = open(f"sequencing/final_uniq_sequences_{paper}_{filename}_{time_gran}.txt", 'w+')

    new_file = open(f"sequencing/{paper}/{filename}/final_sequences_{time_gran}.txt", 'w+')
    new_mult_emos = open(f"sequencing/{paper}/{filename}/final_mult_sequences_{time_gran}.txt", 'w+')
    new_uniq_emos = open(f"sequencing/{paper}/{filename}/final_uniq_sequences_{time_gran}.txt", 'w+')


    fin = []
    mult_emo_l = []
    for t in l:
        seqi = ""
        i = 0
        for num in t:
            seqi = seqi + emos[int(num)-1]
            if i < len(t)-1:
                seqi = seqi + " -> "
            i += 1
            
        fin.append(seqi)
        
        if (t.count(t[0]) != len(t)):
            mult_emo_l.append(seqi)
            new_mult_emos.write(seqi)
            new_mult_emos.write('\n')
            
        new_file.write(seqi)
        new_file.write('\n')
        
    new_file.close()
    new_mult_emos.close()

    #print(fin)
    #print(mult_emo_l)

    # removing subsequences
    combined_str = ''.join(fin)
    new_uniq_emos_l = []
    for seq in fin:
    #     #print(seq)
        if combined_str.count(seq) == 1:
    #         #print(seq)
            new_uniq_emos_l.append(seq)
            new_uniq_emos.write(seq)
            new_uniq_emos.write('\n')

    #print(new_uniq_emos_l)

    new_uniq_emos.close()

    new_uniq_emos_l = sorted(new_uniq_emos_l, key=len)
    fin = sorted(fin, key=len)
    mult_emo_l = sorted(mult_emo_l, key=len)

    uniq_str = '\n'.join(new_uniq_emos_l)
    mullen_str = '\n'.join(fin)
    mulemo_str = '\n'.join(mult_emo_l)
    return uniq_str, mullen_str, mulemo_str