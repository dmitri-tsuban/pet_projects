import requests
from bs4 import BeautifulSoup
import re
import csv
import pandas as pd

url = "http://www.dota2protracker.com/hero/"

class WinrateCollect():
    def __init__(self, pos, file):
        self.pos = pos
        self.file = file

    def get_wr(self, hero):
        r = requests.get(url + hero, timeout = 10 ,verify=False).text
        #print(r)
        soup = BeautifulSoup(r)

        if self.pos == 1:
            id = "role_Carry"
        elif self.pos == 3:
            id = "role_Offlane"
        elif self.pos == 5:
            id = "role_Support (5)"
        else:
            raise IndexError
        f1 = soup.find("div", {"id": id})
        f2 = f1.find("div", {"class": "role_box_left"})
        text = f2.text
        nums = re.findall("\d+\.\d+", text)
        if float(nums[0]) > 30:
            wr = float(nums[1])
        else:
            wr = 0
        return wr

    def print_sorted(self, d):
        a = dict(sorted(d.items(), key=lambda item: item[1], reverse=True))
        print(a)
        with open("res.csv", "a") as f:
            f.write(str(a) + "\n")

    def wr_pos(self):
        with open(self.file) as csvfile:
            playable = dict()
            unplayable = dict()
            readCSV = csv.reader(csvfile, delimiter=',')
            for row in readCSV:
                wr = self.get_wr(row[0])
                if row[1] == '1':
                    playable[row[0]] = wr
                else:
                    unplayable[row[0]] = wr
            self.print_sorted(playable)
            self.print_sorted(unplayable)

class WinrateCollect2():
    def __init__(self, file):
        self.file = file
        cols = ['hero', 'g', 'wr', 'pos']
        self.stat = pd.DataFrame(columns=cols)


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


    def get_wr(self, hero):
        r = requests.get(url + hero, timeout = 10 ,verify=False).text
        #print(r)
        soup = BeautifulSoup(r)
        f1 = soup.find("div", {"class": "hero-stats-descr"})
        matches = int(re.findall("\d+", f1.text)[0])

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

    def update_stat(self):
        self.wr_pos()
        self.stat.to_pickle("data")
        #self.stat = pd.read_pickle("data")



#pos1 = WinrateCollect(pos=1, file="pos1.csv")
#pos1.wr_pos()

#pos5 = WinrateCollect(pos=5, file="pos5.csv")
#pos5.wr_pos()

#pos3 = WinrateCollect(pos=3, file="pos3.csv")
#pos3.wr_pos()