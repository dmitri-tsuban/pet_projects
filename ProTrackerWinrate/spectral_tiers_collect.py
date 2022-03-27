import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import dataframe_image as dfi


# depends only on main hero position from personal hero stats
class SpectralWinRateCollect():
    def __init__(self):
        self.url = "https://stats.spectral.gg/lrg2/?league=imm_ranked_meta_last_7&mod=heroes-positions-position_0.3"
        self.cols = ['hero', 'g', 'wr']
        #self.hero_pos = pd.read_pickle("main_heroes_position")

    def add_to_mainpage(self, hero, nums):
        try:
            if hero:
                g1, wr1 = nums.split()
                g = int(g1)
                wr = float(wr1[:-1])
                row = {'hero': hero, 'g': g, 'wr': wr}
                self.main_page = self.main_page.append(row, ignore_index=True)
        except:
            print('error: {} mainpage'.format(hero))

    def wr(self):
        r = requests.get(self.url, timeout=10, verify=False).text
        #print(r)
        soup = BeautifulSoup(r, features="html.parser")

        f1 = soup.find("table", {"id": "heroes-positions-0-3"})

        print(f1.text)
        self.main_page = pd.DataFrame(columns=self.cols)
        hero_info = re.split(r'\s{2,}', f1.text.strip().replace('\n', ' '))
        l = len(hero_info)
        i = 1
        while i < l:
            self.add_to_mainpage(hero_info[i], hero_info[i+1])
            i += 2

        self.main_page = self.main_page.set_index('hero')
        self.main_page = pd.concat([self.main_page, self.hero_pos], axis=1, join="inner")
        self.main_page.to_pickle("main_page_data")

    def update_main(self):
        self.wr()

    def do_ranking(self, df):
        center_g = 1
        center_wr = 1
        df = df.assign(g_qant=df['g'].rank(method='max', pct=True))
        df = df.assign(wr_qant=df['wr'].rank(method='max', pct=True))
        df = df.assign(
            qant_circle=(df['g_qant'] - center_g) ** 2 + (df['wr_qant'] - center_wr) ** 2)
        df = df.assign(rank=1 - df['qant_circle'])
        df_top = df.sort_values(by=['qant_circle'], ascending=True)[['g', 'wr', 'rank']]
        df_top = df_top.loc[df_top['rank'] > 0.49]
        return df_top

    def show_top(self):
        self.main_page = pd.read_pickle("main_page_data")
        p1 = self.main_page.loc[(self.main_page['pos'] == 1)]
        p3 = self.main_page.loc[(self.main_page['pos'] == 3)]
        p45 = self.main_page.loc[(self.main_page['pos'] == 4) | (self.main_page['pos'] == 5)]

        p1_rank = self.do_ranking(p1)
        p3_rank = self.do_ranking(p3)
        p45_rank = self.do_ranking(p45)

        p1_rank.dfi.export('C:/Users/HP17/Desktop/d2/main_page/pos1.png')
        p3_rank.dfi.export('C:/Users/HP17/Desktop/d2/main_page/pos3.png')
        p45_rank.dfi.export('C:/Users/HP17/Desktop/d2/main_page/pos45.png')


swc = SpectralWinRateCollect()
swc.update_main()
