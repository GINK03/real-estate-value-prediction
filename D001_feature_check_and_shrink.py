import MeCab
import pandas as pd


df = pd.read_csv('./lexical_parsed.csv')


m = MeCab.Tagger('-Owakati')
m.parse("")
feat_freq = {}
for obj in df.to_dict('record'):
    # print(obj)
    com = obj['madori']
    try:
        for feat in set(com.split('/')):
            if feat_freq.get(feat) is None:
                feat_freq[feat] = 0
            feat_freq[feat] += 1
    except:
        ...
for feat, freq in sorted(feat_freq.items(), key=lambda x: x[1]):
    print(feat, freq)


('communication', 'インターネット接続,BS,CATV,地上デジタル,無料,光ファイバー')
('kitchen', '別,ガスコンロ,洗面化粧台,衛生的,温水洗浄便座')
('other', 'エアコン,フローリング,バルコニー,置き場,ベランダ')
('secure', 'モニター,フォン,オートロック,インターホン,宅配ボックス')
('position', '上階無し,最上階,角部屋,南向き')
('madori', '8LDK,2R,6DK,2SK,6LDK,4DK,7LDK,5DK,7DK,5K,6LDK,5LDK,1SR,6DK,2DK,3DK,1DK,4K,4LDK,5LDK,5DK,3LDK,1SK,1LDK,4DK,2LDK,3K,4LDK,2K,1DK,3DK,3LDK,1R,2DK,1LDK,2LDK,1K')
