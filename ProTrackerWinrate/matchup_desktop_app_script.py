import dataframe_image as dfi
import pandas as pd

from tkinter import *
from ttkwidgets.autocomplete import AutocompleteEntry


df = pd.read_pickle("position_stats_data")
df_m = pd.read_pickle("matchup_stats_data")

def get_matchup(enemy_heroes):
    matchup = None
    for e in enemy_heroes:
        tmp = df_m.loc[(df_m['hero'] == e)][['matchup', 'w', 'l']].set_index('matchup') 
        if matchup is not None:
            matchup = matchup.add(tmp, fill_value=0)
        else:
            matchup = tmp
    matchup = matchup[~matchup.index.isin(enemy_heroes)]
    center_g = 1
    center_lr = 1
    matchup = matchup.assign(g = matchup['w'] + matchup['l'])
    matchup = matchup.assign(lr = matchup['l'] / (matchup['w'] + matchup['l']))
    matchup = matchup.assign(g_qant = matchup['g'].rank(method='max', pct=True))
    matchup = matchup.assign(lr_qant = matchup['lr'].rank(method='max', pct=True))
    matchup = matchup.assign(qant_circle = (matchup['g_qant']-center_g)**2 + (matchup['lr_qant']-center_lr)**2)
    matchup = matchup.assign(rank = 1 - matchup['qant_circle'])
    matchup = matchup.assign(r = 3 + ((matchup['g'] ** (2 / 3)) * (2 * matchup['lr'] - 1) / 10))
    df_top = matchup.loc[matchup['qant_circle'] <= 0.9]
    df_top = df_top.sort_values(by=['r','lr'],ascending=[False,False])[['g', 'lr','r']]
    df_top = df_top.loc[df_top['lr'] > 0.49]

    return df_top

df_tmp = pd.read_pickle("main_heroes_position")
#print(df_tmp.isin([1]))
p1 = df_tmp.index[df_tmp.isin([1])].tolist()
p2 = df_tmp.index[df_tmp.isin([2])].tolist()
p3 = df_tmp.index[df_tmp.isin([3])].tolist()
p4 = df_tmp.index[df_tmp.isin([4])].tolist()
p5 = df_tmp.index[df_tmp.isin([5])].tolist()

heroes_list = df_tmp.index.tolist()
p = 'C:/Users/HP17/Desktop/d2/matchup.png'

ws = Tk()
ws.title('Pick Enemy Heroes')
ws.geometry('500x250')
ws.config(bg='#f25252')

frame = Frame(ws, bg='#f25252')
frame.pack(expand=True)

Label(
    frame,
    bg='#f25252',
    font = ('Arial',21),
    text='1 Line - Insert hero press Enter\n2 Line - Insert position press Enter\npos = 0 -> all roles\npos = 45 -> 4 and 5 roles\nThen Matchup.png will be created'
    ).pack()

entry = AutocompleteEntry(
    frame,
    width=20,
    font=('Times', 18),
    completevalues=heroes_list
    )
entry.pack()

ent = Entry(
    frame,
    width=5,
    font=('Times', 18),
    )
ent.pack()

enemies = []

def on_change(e):
    enemies.append(e.widget.get())
    entry.delete(0, 20)

def start(e):
    pos = int(e.widget.get())
    if pos == 0:
        pos_list = heroes_list
    elif pos == 45:
        pos_list = df_tmp.index[df_tmp.isin([4,5])].tolist()
    else:
        pos_list = df_tmp.index[df_tmp.isin([pos])].tolist()

    m = get_matchup(enemies)
    m[m.index.isin(pos_list)].dfi.export(p)
    print('ok')
    ws.destroy()

entry.bind("<Return>", on_change)
ent.bind("<Return>", start)

ws.mainloop()


