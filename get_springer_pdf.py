import pandas as pd
import requests
import time
import os



df = pd.read_excel('./Free+English+textbooks.xlsx')
df = df.sort_values('Book Title')

# PDFダウンロード用のURLを拾ってくる。
df_URL = df['DOI URL'].astype(str)
df_URL = df_URL.str.replace("http://doi.org/","HOGEHOGE")
df_URL = df_URL.str.replace('/','%2F')
df_URL = df_URL.str.replace('HOGEHOGE','https://link.springer.com/content/pdf/')
df_URL = df_URL + '.pdf'
download_url_list = df_URL.values.tolist()

# PDF名に使う本のタイトルを拾ってくる。重複タイトルがあるので2つ目以降をナンバリングする。
df['dummy'] = df.groupby('Book Title').cumcount()
df_TITLE = df['Book Title'] + df['dummy'].astype(str).replace('0' , '')
df_TITLE = df_TITLE.str.replace('/', '')
df_TITLE = df_TITLE.str.replace(':', '')
df_TITLE = df_TITLE.str.replace('|', '')
df_TITLE = df_TITLE.str.replace('"', '')
df_TITLE = df_TITLE.str.replace('?', '')
df_TITLE = df_TITLE.str.replace('>', '')
df_TITLE = df_TITLE.str.replace('<', '')
df_TITLE = df_TITLE.str.replace('\\', '')
download_title_list = df_TITLE.values.tolist()

# 折角本のカテゴリ分類があるので分類するためのフォルダを事前に作成する。
df_DIR = df['English Package Name'].astype(str)
download_dir_list = df_DIR.values.tolist()
for folder in download_dir_list:
    try:
        os.makedirs('./' + folder)
    except FileExistsError:
        pass

# 雑にダウンロード済みのファイル数をカウントする。
i = 1
for (download_url, download_title, download_dir) in zip(download_url_list, download_title_list, download_dir_list):
    title = str(download_title)
    print(str(i) + '/' + str(len(df)) + ':\t:' + 'DOWNLOADING...: ' + title, end='\r')
    # 実際にファイルをダウンロードしてくる。
    r = requests.get(str(download_url))
    time.sleep(1)
    print(str(i) + '/' + str(len(df)) + ':\t:' + 'GET           : ' + title)

    # ファイルの保存
    if r.status_code == 200:
        # カテゴリ分類ごとにファイルを格納する。
        with open('./' + download_dir + '/' + title + '.pdf', "wb") as f: 
            f.write(r.content)
            f.close()
    i = i + 1