import MeCab
import csv

m = MeCab.Tagger('-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd')

text = '''
アイドルマスターシンデレラガールズ佐久間まゆ荒木比奈堀裕子
'''

fi = open('mamayu_tweet.csv', 'r')
fo = open('split.txt', 'w')
for tweet in fi:
    # print(tweet)
    print(m.parse(tweet))
    sprit_tweet = m.parse(tweet)
    fo.write(sprit_tweet)
fi.close()
fo.close()
# print(type(text))
# print(type(f))

# print(m.parse(f))

# f = open('text.txt,'w')
# f.write()
# f.close()
