from pathlib import Path
import json
import MeCab
import re
import pandas as pd
import optuna
m = MeCab.Tagger('-Owakati')

type_cons = {}
for type, cons in [('communication', 'インターネット接続,BS,CATV,地上デジタル,光ファイバー'), 
    ('kitchen', 'ガスコンロ,洗面化粧台,衛生的,温水洗浄便座'),
    ('other', 'エアコン,フローリング,バルコニー,置き場,ベランダ'),
    ('secure', 'モニター,フォン,オートロック,インターホン,宅配ボックス'),
    ('shuunou', 'シューズボックス,クローゼット,ウォークインクローゼット,押入れ,ロフト'),
    ('position', '上階無し,最上階,角部屋,南向き'),
    ('madori','8LDK,2R,6DK,2SK,6LDK,4DK,7LDK,5DK,7DK,5K,6LDK,5LDK,1SR,6DK,2DK,3DK,1DK,4K,4LDK,5LDK,5DK,3LDK,1SK,1LDK,4DK,2LDK,3K,4LDK,2K,1DK,3DK,3LDK,1R,2DK,1LDK,2LDK,1K')
    ]:
    type_cons[type] = set(cons.split(','))

def filtering(type, x):
    if x  is None:
        return {f'{type}:{c}':0 for c in type_cons[type]}
    elif type in ['postion']:
        words = x.split('/')
        return {f'{type}:{c}': 1 if c in words else 0 for c in type_cons[type]}
    elif type in ['madori']:
        words = x
        return {f'{type}:{c}': 1 if c in words else 0 for c in type_cons[type]}
    else:
        words = m.parse(x).strip().split()
        return {f'{type}:{c}': 1 if c in words else 0 for c in type_cons[type]}


robjs = []
for path in Path('./json').glob('*'):
    #print(path)
    try:
        obj = json.load(path.open())
    except Exception as ex:
        path.unlink()
    try:
        basic = obj['basic']
        jusho = basic['住所']
        yachin = re.sub(r'(万|円|,)', '', basic['家賃'])
        yachin = float(yachin)
        menseki = re.sub(r'(,|m|.$)', '', basic['専有面積'])
        menseki = float(menseki)
        kouzou = basic['構造']
        houi = basic['方位']
        #print(basic['築年'])
        try:
            chikunen = re.search(r'築(\d{1,})年', basic['築年']).group(1)
        except:
            # 新築のときカッコがない
            chikunen = 0
        try:
            kaisou = re.search(r'^(B|)(\d{1,})', basic['物件階層']).group(0)
        except:
            kaisou = 1
            #print(basic['物件階層'])
        #print(kaisou)
        #print(jusho, yachin)
        try:
            country = re.search(r'(.+?[都道府県])(.+?[市区町村])(.+)', jusho).group(1)
            detail_position = re.search(r'(.+?[都道府県])(.+?[市区町村])(.+)', jusho).group(2)
        except:
            continue
        madori = re.sub(r'\(.*?\)', '', basic['間取り'])
        madori = re.sub(r'\+.?$', '', madori)
        madori = filtering('madori', madori)


        detail = obj['detail']
        communication = filtering('communication', detail.get("放送・通信"))
        shuunou = filtering('shuunou', detail.get('収納'))
        kitchen = filtering('kitchen', detail.get('キッチン/バス・トイレ'))
        secure = filtering('secure', detail.get('セキュリティ'))
        other = filtering('other', detail.get('その他'))
        position = filtering('position', detail.get('位置'))
         
        robj = {'country': country, 'yachin': yachin, 'menseki': menseki,
                'detail_position': detail_position, 
                'kouzou':kouzou, 'houi':houi, 'kaisou':kaisou, 'chikunen':chikunen, 
                }
        robj.update(communication)
        robj.update(kitchen)
        robj.update(secure)
        robj.update(other)
        robj.update(shuunou)
        robj.update(position)
        robj.update(madori)
        robjs.append(robj)

    except IndexError as ex:
        print(detail)
        print(ex)
    except KeyError as ex:
        if str(ex) in ["'家賃'", "'住所'"]:
            path.unlink()
            continue
        print(ex)

df = pd.DataFrame(robjs)

df.to_csv('lexical_parsed.csv', index=None)
