import pandas as pd
from app import WinrateCollect2

df = pd.read_pickle("position_stats_data")
df_m = pd.read_pickle("matchup_stats_data")

center_g = 1
center_wr = 1


# .style.hide_index()
def tierS(pos):
    # 5% - outliers
    min_g = df.loc[(df['pos'] == pos)]['g'].max() / 10
    df1 = df.loc[(df['pos'] == pos) & (df['g'] >= min_g)]
    df1['r'] = 3 + ((df1.g ** (2 / 3)) * (2 * df1.wr / 100 - 1) / 10)
    #df1 = df1.assign(g_qant=df1['g'].rank(method='max', pct=True))
    #df1 = df1.assign(wr_qant=df1['wr'].rank(method='max', pct=True))
    #df1 = df1.assign(qant_circle=(df1['g_qant'] - center_g) ** 2 + (df1['wr_qant'] - center_wr) ** 2)
    #df1 = df1.assign(rank=1 - df1['qant_circle'])

    #df2 = df1.loc[df1['qant_circle'] <= 0.0625]
    #df_top = df2.sort_values(by=['qant_circle'], ascending=True)[['hero', 'g', 'wr', 'rank']]

    df_top3 = df1.sort_values(by=['r'], ascending=False)
    return df_top3[:20]


def tierA(pos):
    # 5% - outliers
    min_g = df.loc[(df['pos'] == pos)]['g'].max() / 20
    df1 = df.loc[(df['pos'] == pos) & (df['g'] >= min_g)]

    df1 = df1.assign(g_qant=df1['g'].rank(method='max', pct=True))
    df1 = df1.assign(wr_qant=df1['wr'].rank(method='max', pct=True))
    df1 = df1.assign(qant_circle=(df1['g_qant'] - center_g) ** 2 + (df1['wr_qant'] - center_wr) ** 2)
    df1 = df1.assign(rank=1 - df1['qant_circle'])

    df2 = df1.loc[(df1['qant_circle'] <= 0.25) & (df1['qant_circle'] > 0.0625)]
    df_top = df2.sort_values(by=['qant_circle'], ascending=True)[['hero', 'g', 'wr', 'rank']]
    return df_top


def tierB_plus(pos):
    # 5% - outliers
    min_g = df.loc[(df['pos'] == pos)]['g'].max() / 20
    df1 = df.loc[(df['pos'] == pos) & (df['g'] >= min_g)]

    df1 = df1.assign(g_qant=df1['g'].rank(method='max', pct=True))
    df1 = df1.assign(wr_qant=df1['wr'].rank(method='max', pct=True))
    df1 = df1.assign(qant_circle=(df1['g_qant'] - center_g) ** 2 + (df1['wr_qant'] - center_wr) ** 2)
    df1 = df1.assign(rank=1 - df1['qant_circle'])

    df2 = df1.loc[(df1['qant_circle'] > 0.25)]
    df_top = df2.sort_values(by=['qant_circle'], ascending=True)[['hero', 'g', 'wr', 'rank']]
    return df_top


def topWR_lowpick():
    df_top3 = df.sort_values(by=['wr', 'g'], ascending=[False, False])
    return df_top3.loc[df_top3['wr'] > 60]

def topWR_score():
    df1 = df.copy()
    df1['r'] = 3 + ((df1.g ** (2 / 3)) * (2 * df1.wr / 100 - 1) / 10)
    df_top3 = df1.sort_values(by=['r'], ascending=False)
    return df_top3.loc[df_top3['r'] > 3.5]

def topHiddenImba_pos(pos):
    # 5% - outliers
    min_g = df.loc[(df['pos'] == pos)]['g'].max() / 20
    df1 = df.loc[(df['pos'] == pos) & (df['g'] >= min_g)]

    df1 = df1.assign(g_qant=df1['g'].rank(method='max', pct=True))
    df1 = df1.assign(wr_qant=df1['wr'].rank(method='max', pct=True))
    df1 = df1.assign(qant_circle=(df1['g_qant'] - center_g / 2) ** 2 + (df1['wr_qant'] - center_wr) ** 2)
    df1 = df1.assign(rank=1 - df1['qant_circle'])

    df2 = df1.loc[df1['qant_circle'] <= 0.25]
    df_top = df2.sort_values(by=['qant_circle'], ascending=True)[['hero', 'g', 'wr', 'rank']]
    return df_top.loc[df_top['wr'] >= 53.5]


def topWinrateOverallTiers():
    min_g = df['g'].max() / 10
    df1 = df.loc[(df['g'] > min_g) & (df['wr'] >= 49)]
    df_top3 = df1.sort_values(by=['wr', 'g'], ascending=[False, False])
    return df_top3.loc[df_top3['wr'] >= 53.5]

import os
from datetime import datetime
fold = 'C:/Users/HP17/Desktop/d2/tiers'
import dataframe_image as dfi

tierS(1).dfi.export(fold + '/1_Tiers.png')
topWinrateOverallTiers().dfi.export(fold + '/topWinrate.png')
topWR_lowpick().dfi.export(fold + '/topLowpick.png')
topWR_score().dfi.export(fold + '/Meta.png')
tierS(2).dfi.export(fold + '/2_Tiers.png')
tierS(3).dfi.export(fold + '/3_Tiers.png')
tierS(4).dfi.export(fold + '/4_Tiers.png')
tierS(5).dfi.export(fold + '/5_Tiers.png')

import time
time.sleep(2)