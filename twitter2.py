# -*- coding: utf-8 -*-
import tweepy
import sys, codecs
 
consumer_key = "XXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_token_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)

#自分のタイムラインを取得
"""
public_tweets = api.home_timeline()
for tweet in public_tweets:
    print(tweet.text)
"""

#リプライ先の情報
"""
search_result = api.get_status(000000000000000000)  #ツイートIDを入力
word=search_result.entities['user_mentions']
print(word)
"""

#キーワード検索
"""
search_result = api.search(q='XXXXXXXXX')
for result in search_result:
    status=result.text
    sys.stdout.buffer.write(status.encode('cp932', errors='replace'))
"""
#指定したユーザーの情報を取得
"""
user = api.get_user('XXXXXXX')
print(user.screen_name)
print(user.followers_count)
for friend in user.friends():
   print(friend.screen_name)
"""

#つぶやく
"""
api.update_status('test')
"""

#フォロワーに対してフォローを自動で返す
"""
for follower in tweepy.Cursor(api.followers).items():
    follower.follow()
"""

#フォロワーの表示
"""
def limit_handled(cursor):
    while True:
        try:
            yield cursor.next()
        except tweepy.RateLimitError:
            time.sleep(15 * 60)
for follower in limit_handled(tweepy.Cursor(api.followers).items()):
    if follower.friends_count < 300:
       print(follower.screen_name)
"""

#指定したユーザーのツイートを取得

page = 1
while True:
    statuses = api.user_timeline('XXXXXXX',page=page)
    if statuses:
        for status in statuses:
            #print(status)
            text=status.text
            if '@' in text and 'RT' not in text:     #リプライのみを取得
                sys.stdout.buffer.write(text.encode('cp932', errors='replace'))
                print("")
    else:
        break
    page += 1

#StreamingAPI
"""
class MyStreamListener(tweepy.StreamListener):
    def on_status(self, status):
        #print(status)
        text=status.text
        sys.stdout.buffer.write(text.encode('cp932', errors='replace'))
        return True
    def on_error(self, status_code):
        if status_code == 420:
          return False

myStreamListener = MyStreamListener()
Stream = tweepy.Stream(auth = api.auth, listener=MyStreamListener())
#Stream.filter(fllow=)   #ユーザーIDを指定
Stream.filter(track='')    #キーワード指定
#Stream.filter(locations=[XXXXXXXXXXX,XXXXXXXXXXXX])   #区域(経度・緯度)を指定
"""