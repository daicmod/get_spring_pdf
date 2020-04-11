import pandas as pd
import urllib3
import requests, bs4
import time

pd.set_option("display.max_colwidth", 100)

df = pd.read_excel('./Free+English+textbooks.xlsx')
df_URL = df['DOI URL'].astype(str)
df_URL = df_URL.str.replace("http://doi.org/","HOGEHOGE")
df_URL = df_URL.str.replace('/','%2F')
df_URL = df_URL.str.replace('HOGEHOGE','https://link.springer.com/content/pdf/')
df_URL = df_URL + '.pdf'
download_url_list = df_URL.values.tolist()
df_TITLE = df['Book Title']
download_title_list = df_TITLE.values.tolist()

i = 0
for (download_url, download_title) in zip(download_url_list, download_title_list):
    title = str(download_title)
    title = title.replace('/', '')
    title = title.replace(':', '')
    title = title.replace('|', '')
    title = title.replace('"', '')
    title = title.replace('?', '')
    title = title.replace('<', '')
    title = title.replace('>', '')
    title = title.replace('\\', '')
    print('DOWNLOADING...: ' + title, end='\r')
    # 一秒スリープ
    time.sleep(1)
    r = requests.get(str(download_url))
    print('GET           : ' + title)
    # ファイルの保存
    if r.status_code == 200:
        with open(title + '.pdf', "wb") as f: 
            f.write(r.content)
            f.close()