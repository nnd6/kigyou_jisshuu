import pandas as pd
import torch

# %%
def watcher_read_riyuu(watcher):
    def delete_unnecessary_lines(pd_data):
        subset = '業種・職種'                   # この列をキーに 削除する
        unnecessarys = ['－', '＊', subset]     # 上記の列にある 不要な行を抽出するキーワード

        pd_data_dropna = pd_data.dropna(subset=subset)  # まずは NaN列を削除

        unnecessary = None
        for un in unnecessarys:
            if unnecessary is None:
                unnecessary = (pd_data_dropna[subset] == un) #(pd_data.iloc[:,3] == un)
            else:
                unnecessary |= (pd_data_dropna[subset] == un) # (pd_data.iloc[:,3] == un)
        return pd_data_dropna.drop(pd_data_dropna.index[unnecessary])
    
    watcher_csv = pd.read_csv(watcher
                             , header=7
                             , encoding='cp932') # 'shift_jis')
    
    watcher_csv_necessary = delete_unnecessary_lines(watcher_csv)
    return watcher_csv_necessary

# %%
# データ読み込み
watcher_genjou = watcher_read_riyuu(r'D:\AUC\ITプログラミング科\kigyou_jisshuu\dist\watcher\景気判断理由集_現状=watcher4.csv')

# %%
# 評価指数 ⇔ 数値ラベル
watcher_handan = watcher_genjou['景気の現状判断']
def get_handan_dict(watcher_handan):
    watcher_handan_d_int, watcher_handan_d_str = pd.factorize(watcher_handan.unique())
    return dict(zip(watcher_handan_d_str, watcher_handan_d_int))

watcher_handan_dict = get_handan_dict(watcher_handan)

data_texts = watcher_genjou['追加説明及び具体的状況の説明']
data_labels = [watcher_handan_dict[wh] for wh in watcher_genjou['景気の現状判断']]

pass