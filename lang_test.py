#%%
#####
# 言語処理 テスト
#####
import pandas as pd
import torch

# %%
import transformers
tokenizer = transformers.AutoTokenizer.from_pretrained("colorfulscoop/gpt2-small-ja")

#%%
sentence_index = tokenizer.encode("テキストのID化のテスト")

# %%
# Embedding - torch.nn
def embeds_torch_nn(sentence_index):
    VOCAB_SIZE = len(sentence_index) + 8000
    EMBEDDING_DIM = 6 # VOCAB_SIZE + 10

    sentence_inputs = torch.tensor(sentence_index).unsqueeze(dim=0)

    embeds = torch.nn.Embedding(VOCAB_SIZE, EMBEDDING_DIM)
    sentence_matrix = embeds(sentence_inputs)
    return sentence_matrix
sentence_matrix = embeds_torch_nn(sentence_index)
# %%
#sentence_inputs
sentence_index
sentence_matrix

# %%
tokenizer.decode([8582, 8, 6864, 193, 8, 2460])
# %%

####
# Thanks: https://colorfulscoop.github.io/lab/article/pytorch_language_model_pipeline/
####
class BlockDataset(torch.utils.data.IterableDataset):
    def __init__(self, tokenizer, generator, block_size, drop_last=True):
        super().__init__()
        self._block_size = block_size
        self._tokenizer = tokenizer
        self._generator = generator
        self._drop_last = drop_last

    @classmethod
    def from_texts(cls, tokenizer, texts, block_size):
        return cls(tokenizer=tokenizer, generator=lambda: texts, block_size=block_size)

    @classmethod
    def from_file(cls, tokenizer, filepath, block_size):
        return cls(tokenizer=tokenizer,
                   generator=lambda: (line.strip("\n") for line in open(filepath)),
                   block_size=block_size
                  )

    @classmethod
    def from_file(cls, tokenizer, filepath, block_size):
        return cls(tokenizer=tokenizer,
                   generator=lambda: (line.strip("\n") for line in open(filepath)),
                   block_size=block_size
                  )
    
    def __iter__(self):
        """
            Yields (List[int])
        """
        ids = []
        for text in self._generator():
            ids.extend(self._tokenizer.encode(text))
            while len(ids) >= self._block_size+1:
                yield {"input_ids": ids[:self._block_size], "labels": ids[1:self._block_size+1]}
                ids = ids[self._block_size:]
        if not self._drop_last:
            yield ids


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

watcher_genjou = watcher_read_riyuu(r'D:\AUC\ITプログラミング科\kigyou_jisshuu\dist\watcher\景気判断理由集_現状=watcher4.csv')
pass
# %%
watcher_genjou
# %%
# 評価指数
watcher_handan = watcher_genjou['景気の現状判断']
def get_handan_dict(watcher_handan):
    watcher_handan_d_int, watcher_handan_d_str = pd.factorize(watcher_handan.unique())
    return dict(zip(watcher_handan_d_str, watcher_handan_d_int))

watcher_handan_dict = get_handan_dict(watcher_handan)
watcher_handan.unique()   #watcher_genjou.iloc[:,2].unique()

# %%
watcher_riyuu = watcher_genjou['追加説明及び具体的状況の説明']   #watcher_genjou.iloc[:,2].unique()
watcher_riyuu[1]
# %%
tokenizer.encode(watcher_riyuu[0])



# %%
# MSE計算テスト
from torchmetrics.regression import MeanSquaredError
