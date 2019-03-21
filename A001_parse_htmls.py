import glob
import bs4 

import gzip
import pickle
import re
import os
from concurrent.futures import ProcessPoolExecutor as PPE
import json
from pathlib import Path
from hashlib import sha256
import shutil
Path('json').mkdir(exist_ok=True)

def sanitize(text):
    text = re.sub(r'(\t|\n|\r)', '', text)
    text = re.sub(r'\xa0', '', text)
    text = re.sub(r'\\r', '', text)
    text = re.sub('地図で物件の周辺環境をチェック！', '', text)
    return text

def is_train(x):
    if '線' in x:
        return False
    else:
        return True

def pmap(arg):
    key, fns = arg
    SIZE = len(fns)
    for index, fn in enumerate(fns):
        try:
            print('now', key,index, 'size', SIZE, fn)
            html = gzip.decompress(open(fn, 'rb').read())
            soup = bs4.BeautifulSoup(html, 'lxml')
            if soup.find('link', {'rel':'canonical'}) is None:
                Path(fn).unlink()
                continue
            canonical = soup.find('link', {'rel':'canonical'})['href']
            if '/detail/' not in canonical:
                Path(fn).unlink()
                continue
            basic_table = soup.find('div', {'class':'detail_basicInfo'})
            if basic_table is None:
                Path(fn).unlink()
                continue
            basic_table = basic_table.find('table')
            # ズレの処理
            tds = list(basic_table.find_all('td'))
            tds.pop(0)
            #print(tds.pop(0).text)
            tds = [td for td in tds if is_train(td)]
            print(len(basic_table.find_all('th')), len(tds))
            if len(basic_table.find_all('th')) == 13 and len(tds) == 14:
                tds.pop(4)
                ...
            basic_obj = {sanitize(th.text):sanitize(td.text) for th, td in zip(basic_table.find_all('th'),tds)}

            detail_obj = {}
            for table in soup.find('div', {'class':'detail_specTable'}).find_all('table'):
                #print(table)
                for th, td in zip(table.find_all('th'), table.find_all('td')):
                    detail_obj[sanitize(th.text)] = sanitize(td.text)
            obj = {'basic':basic_obj, 'detail':detail_obj, 'canonical':canonical, 'title':soup.title.text}
            last_fn = fn.split('/')[-1]
            shutil.move(fn, f'parsed_htmls/{last_fn}' )
            with open(f'json/{last_fn}', 'w') as fp:
                fp.write(json.dumps(obj, indent=2, ensure_ascii=False))
        except Exception as ex:
            #Path(fn).unlink()
            print(ex)
        #detail_table = soup.find('table', {'class':'bukken_detail_table'})
        #detail_obj = {re.sub(r'\t', '', th.text):re.sub(r'(\t|\n)', '', td.text) for th, td in zip(detail_table.find_all('th'), detail_table.find_all('td'))}
        #print(detail_obj)
#urls = [sha256(bytes(v, 'utf8')).hexdigest() for v in json.load(fp=open('./hash_url.json')).values()]
#fns = [f'./htmls/{url}' for url in urls]
import random
files = glob.glob('./htmls/*')
random.shuffle(files)
args = {}
for index, fn in enumerate(files):
    key = index%8
    if args.get(key) is None:
        args[key] = []
    args[key].append(fn)
args = [(key,fns) for key,fns in args.items()]
#[pmap(arg) for arg in args]
with PPE(max_workers=8) as exe:
    exe.map(pmap, args)
