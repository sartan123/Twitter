# -*- coding:utf-8 -*-
import json
import time
from requests_oauthlib import OAuth1Session

api_count = 0


# API接続
def api_connect():
    consumer_key = "XXXXXXXXXXXXXXXXXXXXXXX"
    consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXX"
    access_token = "XXXXXXXXXXXXXXXXXXXXXXX"
    access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXX"
    twitter = OAuth1Session(consumer_key, consumer_secret, 
                            access_token, access_token_secret)
    return twitter


# 1ページ目のツイートを取得
def search_tweet(twitter, q):
    query = q
    url = 'https://api.twitter.com/1.1/search/tweets.json?'
    params = {
            "q": query,
            "lang": "ja",
            "result_type": "recent",
            "count": "100"
            }
    responce = twitter.get(url, params=params)
    tweets = json.loads(responce.text)
    view_tweets(tweets)
    next_id = tweets['statuses'][-1]['id']
    search_next_page(twitter, next_id, q)


# 2ページ目以降のツイートを取得
def search_next_page(twitter, start_id, q):
    query = q
    next_id = start_id-1
    global api_count
    for i in range(2, 1000):
        print('検索ページ:{}'.format(i))
        url = 'https://api.twitter.com/1.1/search/tweets.json?'
        params = {
                "q": query,
                "lang": "ja",
                "result_type": "recent",
                "count": "100",
                "max_id": next_id
                }
        responce = twitter.get(url, params=params)
        tweets = json.loads(responce.text)

        # APIの制限回数をチェックする
        api_count += 1
        if api_count == 170:
            print('API制限回数が近いため、16分停止')
            for i in range(16):
                print(i)
                time.sleep(60)
            print('再開')
            api_count = 0

        view_tweets(tweets)
        try:
            next_id = tweets['statuses'][-1]['id']-1
        except:
            print('検索できるツイートがなくなりました')
            break


# 取得したツイートを見る(ほぼデバッグ用)
def view_tweets(tweets):
    for tweet in tweets['statuses']:
        print(tweet['text'], file=file)


def main():
    twitter = api_connect()
    q = 'クエリを入力'
    search_tweet(twitter, q)

if __name__ == '__main__':
    file = open('output.txt', 'w')
    main()
