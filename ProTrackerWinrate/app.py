import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd
import dataframe_image as dfi

url = "http://www.dota2protracker.com/hero/"

class WinrateCollect2():
    def __init__(self):
        self.file = "heroes_page_list.csv"
        cols = ['hero', 'g', 'wr', 'pos']
        self.stat = pd.DataFrame(columns=cols)

        cols = ['hero', 'matchup', 'w', 'l']
        self.matchups = pd.DataFrame(columns=cols)

    def role_to_nums(self, all_roles, role):
        f2 = all_roles.find("div", {"id": role})
        if f2:
            f3 = f2.find("div", {"class": "role_box_left"})
            nums = re.findall("\d+\.\d+", f3.text)
            return nums[0], nums[1]
        return None

    def add_to_stats(self, hero, nums, pos, matches):
        if nums:
            g1, wr1 = nums
            g = int(round(matches * float(g1) / 100))
            wr = float(wr1)
            row = {'hero': hero, 'g': g, 'wr': wr, 'pos': pos}
            self.stat = self.stat.append(row, ignore_index=True)

    def add_to_matchups(self, hero, matchup, w, l):
        try:
            if matchup:
                w = int(w)
                l = int(l)
                row = {'hero': hero, 'matchup': matchup, 'w': w, 'l': l}
                self.matchups = self.matchups.append(row, ignore_index=True)
        except:
            print('error: {} vs {}'.format(hero, matchup))

    def is_integer(self, v):
        try:
            int(v)
        except:
            return False
        return True

    def get_wr(self, hero):
        r = requests.get(url + hero, timeout = 10 ,verify=False).text
        #print(r)
        soup = BeautifulSoup(r, features="html.parser")

        # find matchups
        f1 = soup.find("div", {"id": "table-heroes"})
        matchups = re.split(r'\s{2,}', f1.text.strip())
        le = len(matchups)
        flag = True
        i = 0
        while i < len(matchups):
            matchup = matchups[i]
            if i + 2 < len(matchups) and self.is_integer(matchups[i + 2]):
                w = int(matchups[i + 1])
                l = int(matchups[i + 2])
                flag = w > l
            else:
                if flag:
                    w = int(matchups[i + 1])
                    l = 0
                else:
                    w = 0
                    l = int(matchups[i + 1])
                i -= 1
            self.add_to_matchups(hero, matchup, w, l)
            i += 3

        # find matches count
        f1 = soup.find("div", {"class": "hero-stats-descr"})
        matches = int(re.findall("\d+", f1.text)[0])

        # find winrate and games for each role
        f1 = soup.find("div", {"id": "all_roles"})

        nums1 = self.role_to_nums(f1, "role_Carry")
        self.add_to_stats(hero, nums1, 1, matches)

        nums2 = self.role_to_nums(f1, "role_Mid")
        self.add_to_stats(hero, nums2, 2, matches)

        nums3 = self.role_to_nums(f1, "role_Offlane")
        self.add_to_stats(hero, nums3, 3, matches)

        nums4 = self.role_to_nums(f1, "role_Support (4)")
        self.add_to_stats(hero, nums4, 4, matches)

        nums5 = self.role_to_nums(f1, "role_Support (5)")
        self.add_to_stats(hero, nums5, 5, matches)

        #print(self.stat.head(10))

    def print_sorted(self, d):
        a = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
        print(a)
        with open("res.csv", "a") as f:
            f.write(str(a) + "\n")

    def wr_pos(self):
        with open(self.file) as csvfile:
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                self.get_wr(row[0])

    def get_stat_by_pos(self, pos):
        df = self.stat.loc[(self.stat['pos'] == pos)]
        df = df.sort_values(by=['g', 'wr'],ascending=False)
        return df

    def df_fix_matchups(self):
        self.matchups['hero'] = self.matchups['hero'].str.replace('%20', ' ')
        self.matchups = self.matchups.astype({'w': 'int32'})
        self.matchups = self.matchups.astype({'l': 'int32'})

    def df_fix_positions(self):
        self.stat['hero'] = self.stat['hero'].str.replace('%20', ' ')
        self.stat = self.stat.astype({'g': 'int32'})

    def update_hero_main_position(self):
        df_tmp = self.stat.sort_values(['hero', 'g'], ascending=[True, False]).drop_duplicates(['hero']).set_index(
            'hero').pos
        df_tmp.to_pickle("main_heroes_position")

    def update_stat(self):
        self.wr_pos()
        self.df_fix_positions()
        self.df_fix_matchups()
        self.update_hero_main_position()

        self.stat.to_pickle("position_stats_data")
        self.matchups.to_pickle("matchup_stats_data")

#wc2 = WinrateCollect2("heroes.csv")
#wc2.wr_pos()
