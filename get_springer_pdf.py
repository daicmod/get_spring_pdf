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
# ダウンロードできなかったファイルのリストのインデックス
download_failure_list = list()

for (download_url, download_title, download_dir) in zip(download_url_list, download_title_list, download_dir_list):
    title = str(download_title)
    
    # 既にダウンロード済みのファイルであれば飛ばす
    if os.path.isfile('./' + download_dir + '/' + title + '.pdf'):
        print(str(i) + '/' + str(len(df)) + ':\t:' + 'PASS       ...: ' + title)
        i = i + 1
        continue
    
    print(str(i) + '/' + str(len(df)) + ':\t:' + 'DOWNLOADING...: ' + title, end='\r')
    # 実際にファイルをダウンロードしてくる。
    try:
        time.sleep(1)    # 連続でダウンロードし続けるのは申し訳ないのでスリープ
        r = requests.get(str(download_url),timeout = (6.0,5.0)) #timeout 接続待機[s], 応答時間[s]
    except requests.exceptions.Timeout:
        print('\t'+'== Timeout =='+'\r')
        download_failure_list.append(i)
    except:
        print('\t'+'== Any error =='+'\r')
        download_failure_list.append(i)
    else:        
        print('\t' + str(i) + '/' + str(len(df)) + ':\t:' + 'GET           : ' + title)
    
        # ファイルの保存
        if r.status_code == 200:
            # カテゴリ分類ごとにファイルを格納する。
            with open('./' + download_dir + '/' + title + '.pdf', "wb") as f: 
                f.write(r.content)
                f.close()

    i = i + 1
    

print('\n'+'---------------------------------- done ------------------------------------'+'\n')

if len(download_failure_list) > 0:
    print('-- '+str(len(download_failure_list))+ ' files are failed. Please retry or download following titles yourself.--'+'\r')
    for index in download_failure_list:
        print(str(index)+'\t:'+ download_title_list[index-1] + '\tdir:' + download_dir_list[index-1] + '\tURL:' + download_url_list[index-1] )