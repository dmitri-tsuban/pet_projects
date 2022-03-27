import dataframe_image as dfi
import pandas as pd

def read_and_save(newfile, oldfile):
    i = 0
    with open(newfile, 'w') as outfile, open(oldfile, 'r', encoding='utf-8') as infile:
        for line in infile:
            if i % 5 == 0:
                line = line.replace('%','').strip()
                outfile.write(line + '\n')
            i += 1
read_and_save('pos15.txt', '1.txt')
read_and_save('pos2.txt', '2.txt')
read_and_save('pos34.txt', '3.txt')

def read_and_save_wr(newfile, oldfile):
    i = 0
    with open(newfile, 'w') as outfile, open(oldfile, 'r', encoding='utf-8') as infile:
        for line in infile:
            if i % 3 == 0:
                name = line.strip()
            if i % 3 == 1:
                wr = line.strip().split()[1].replace('%','')
            if i % 3 == 2:
                pickrate = line.strip().split()[1].replace('%', '')
                outfile.write(name + '\t' + wr + '\t' + pickrate + '\n')
            i += 1

read_and_save_wr('wr_clean.txt', 'wr.txt')
df_wr = pd.read_csv('wr_clean.txt', sep="\t", header=None)
df_wr.columns = ['name', 'wr', 'pick']
df_wr.pick = df_wr.pick
df_wr.wr = df_wr.wr / 100
df_wr['score'] = 1000 * df_wr.pick ** (2/3) * (2 * df_wr.wr - 1) / 10

df_mid = pd.read_csv('pos2.txt', sep="\t", header=None)
df_mid['pos'] = 2
df_easy = pd.read_csv('pos15.txt', sep="\t", header=None)
df_easy['pos'] = 15
df_off = pd.read_csv('pos34.txt', sep="\t", header=None)
df_off['pos'] = 34
df = pd.concat([df_easy, df_mid, df_off])
df.columns = ['name', 'pre', 'pos']
idx = df.groupby(['name'])['pre'].transform(max) == df['pre']
df = df[idx]
df = pd.merge(df, df_wr, on='name')

p15 = df[df.pos == 15].sort_values(by=['score'], ascending=False).head(30)
p15.dfi.export('C:/Users/HP17/Desktop/d2/dotabuff/pos15.png')
p34 = df[df.pos == 34].sort_values(by=['score'], ascending=False).head(30)
p34.dfi.export('C:/Users/HP17/Desktop/d2/dotabuff/pos34.png')
p2 = df[df.pos == 2].sort_values(by=['score'], ascending=False).head(20)
p2.dfi.export('C:/Users/HP17/Desktop/d2/dotabuff/pos2.png')


#df[idx].to_csv('result.txt')
#print(df.dtypes)