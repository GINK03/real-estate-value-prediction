import pandas as pd

df = pd.read_csv('./lexical_parsed.csv')

df = df[df['country'] == '東京都']

# 方位
for val in list(df['houi'].unique()):
    df[f'houi:{val}'] = df['houi'].apply(lambda x: 1 if x == val else 0)
df.drop(['houi'], axis=1, inplace=True)

# 構造
for val in list(df['kouzou'].unique()):
    df[f'kouzou:{val}'] = df['kouzou'].apply(lambda x: 1 if x == val else 0)
df.drop(['kouzou'], axis=1, inplace=True)

# 階層
for val in list(df['kaisou'].unique()):
    if val in [1,2,3]:
        df[f'kaisou:{val}'] = df['kaisou'].apply(lambda x: 1 if x == val else 0)
    elif val.isdigit() and int(val) >= 3:
        df[f'kaisou:4階以上'] = df['kaisou'].apply(lambda x: 1 if str(x).isdigit() and int(x) >= 4 else 0  )
    else:
        df[f'kaisou:{val}'] = df['kaisou'].apply(lambda x: 1 if x == val else 0)
df.drop(['kaisou'], axis=1, inplace=True)

# 築年
for val in [val//5*5 for val in list(df['chikunen'].unique())]:
    df[f'chikunen:{val}'] = df['chikunen'].apply(lambda x: 1 if x//5*5 == val else 0)
df.drop(['chikunen'], axis=1, inplace=True)

# 詳細位置
for val in list(df['detail_position'].unique()):
    df[f'detail_position:{val}'] = df['detail_position'].apply(lambda x: 1 if x == val else 0)
df.drop(['detail_position'], axis=1, inplace=True)

# 広さ
'''
for val in [val//10*10 for val in list(df['menseki'].unique())]:
    df[f'menseki:{val}'] = df['menseki'].apply(lambda x: 1 if x//10*10 == val else 0)
'''
df.drop(['menseki'], axis=1, inplace=True)

df.drop(['country'], axis=1, inplace=True)
df.to_csv('encoded.csv', index=None)
