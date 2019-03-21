import seaborn as sns
import pandas as pd
from matplotlib import pyplot
pyplot.figure(figsize=(15*3, 15))
sns.set(style="whitegrid")
# exit()
def price_by_country():
    df = pd.read_csv('lexical_parsed.csv')
    countries = set()
    for country, subDf in df.groupby(by=['country']):
        if len(subDf) > 1000:
            print(country, subDf['yachin'].mean())
            countries.add(country)
    df = df.sort_values(by=['country'])
    df = df[df['country'].apply(lambda x:x in countries)]
    ax = sns.violinplot(x="country", y='yachin', data=df)
    pyplot.ylim(0, 20)
    ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=90)
    ax.figure.savefig('price_by_country.png')

def space_by_price_every_country():
    df = pd.read_csv('lexical_parsed.csv')
    countries = set()
    for country, subDf in df.groupby(by=['country']):
        if len(subDf) > 1000:
            countries.add(country)
    df = df.sort_values(by=['country'])
    df['space_by_price'] = df['menseki'] / df['yachin']
    df = df[df['country'].apply(lambda x:x in countries)]
    sns.set(font_scale=2)
    ax = sns.violinplot(x="country", y='space_by_price', data=df)
    pyplot.ylim(0, 15)
    ax.set_xticklabels(labels=ax.get_xticklabels(), rotation=90)
    ax.set(xlabel='都道府県', ylabel='m^2/家賃(万円)')

    ax.figure.savefig('space_by_price.png')

if __name__ == '__main__' :
    space_by_price_every_country()
