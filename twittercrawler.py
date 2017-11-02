from requests_oauthlib import OAuth1Session
import json
import setting
import csv
import urllib.request
import re
import sys
import time
#import cv2
#import numpy as np
twitter = OAuth1Session(setting.CONSUMER_KEY, setting.CONSUMER_SECRET, setting.ACCESS_TOKEN, setting.ACCESS_TOKEN_SECRET)

# timline上のidを獲得
def get_icon():
    params = {}
    req = twitter.get("https://api.twitter.com/1.1/statuses/home_timeline.json", params = params)

    timeline = json.loads(req.text)

    for i, tweet in enumerate(timeline):
        print(tweet["user"]["screen_name"])
        print(tweet["user"]['profile_image_url_https'])
        url = tweet["user"]['profile_image_url_https']
        url = url.replace("_normal", "")
        urllib.request.urlretrieve(url, "./face_list/face_{}.jpg".format(i))
        print("\n")

def tweet(word):
    # status key に 関連付けた単語をツイート
    req = twitter.post("https://api.twitter.com/1.1/statuses/update.json",params = params)


def follow(sc_name):
    # 指定したアカウントをフォローする
    params = {"screen_name": sc_name}
    twitter.post("https://api.twitter.com/1.1/friendships/create.json", params=params)

def get_timeline():
    url = "https://api.twitter.com/1.1/statuses/user_timeline.json"
    params ={'count' : 5}
    req = twitter.get(url, params = params)

    if req.status_code == 200:
        timeline = json.loads(req.text)
        for tweet in timeline:
            print(tweet['user']['name']+'::'+tweet['text'])
            print(tweet['created_at'])
            print('----------------------------------------------------')
    else:
        print("ERROR: %d" % req.status_code)

def search_word():
    url = "https://api.twitter.com/1.1/search/tweets.json"

    print("何を調べますか?")
    keyword = input('>> ')
    print('----------------------------------------------------')


    params = {'q' : keyword, 'count' : 5}

    req = twitter.get(url, params = params)

    if req.status_code == 200:
        search_timeline = json.loads(req.text)
        for tweet in search_timeline['statuses']:
            print(tweet['user']['name'] + '::' + tweet['text'])
            print(tweet['created_at'])
            print('----------------------------------------------------')
    else:
        print("ERROR: %d" % req.status_code)

def get_line():
    url = "https://api.twitter.com/1.1/statuses/home_timeline.json"
    params = {"count":200, #ツイートを最新から何件取得するか(最大200件)
          "include_entities" : 1, #エンティティ(画像のURL等)をツイートに含めるか
          "exclude_replies" : 1, #リプライを含めるか
          }

    req = twitter.get(url, params = params)
    timeline = json.loads(req.text)
    for tweet in timeline:
        print(tweet["text"])

def get_target_ward(ward):
    url = "https://api.twitter.com/1.1/search/tweets.json"
    params = {'q':ward,
              'count':100
          }
    req = twitter.get(url, params = params)
    timeline = json.loads(req.text)
    tweet_list = []
    for tweet in timeline['statuses']:
        tweet_list.append(tweet["text"])
        # print(tweet["text"])
    # print(tweet_list)
    tweet_list = list(set(tweet_list))
    for (i,tweet) in enumerate(tweet_list):
        print(str(i) + " : " + tweet)

    return tweet_list



# ツイートからURLを削除
def url_delete(tweet_list):
    url_delete_tweet_list = []
    for text in tweet_list:
        text=re.sub(r'https?://[\w/:%#\$&\?\(\)~\.=\+\-…]+', "", text)
        url_delete_tweet_list.append(text)
    return url_delete_tweet_list

# csvファイルを作成
def write_csv(tweet_list):
    with open("mamayu_tweet.csv","w") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(tweet_list)

# csvファイルに上書き
def write2_csv(tweet_list):
    with open("mamayu_tweet.csv","a") as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerow(tweet_list)

if __name__ == '__main__':
    # 検索対象の単語を選択
    all_list = []
    # ward = sys.argv[1]
    ward = "佐久間まゆ+OR+ままゆ"
    tweet_list = get_target_ward(ward)
    tweet_list = url_delete(tweet_list)
    write_csv(tweet_list)
    all_list.append(tweet_list)
    time.sleep(15)

    while True:
        tweet_list = get_target_ward(ward)
        tweet_list = url_delete(tweet_list)
        write2_csv(tweet_list)
        time.sleep(15)
