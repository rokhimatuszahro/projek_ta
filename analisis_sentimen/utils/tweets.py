from django.conf import settings
import tweepy

class TweetManager:
    def _get_api_handle(self):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        api = tweepy.API(auth, wait_on_rate_limit=True)
        return api
    def crawling_tweet(self, keyword, jumlah_tweet, result_type, lang):
        keyword = keyword + " -filter:retweets"
        api = self._get_api_handle()
        tweets = tweepy.Cursor(api.search,
                                q=keyword,
                                full_text=True,
                                result_type=result_type,
                                tweet_mode='extended',
                                lang=lang).items(jumlah_tweet)
        # Looping data Twitter
        datatweet = [[tweet.user.name, '@'+tweet.user.screen_name, tweet.created_at, tweet.full_text] for tweet in tweets]
        return datatweet