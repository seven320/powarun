# encoding utf-8
import os, sys
import datetime as dt
from dotenv import load_dotenv

import tweepy
import get_weather

class Powarun():
    def __init__(self):
        load_dotenv(".env")
        auth = tweepy.OAuthHandler(
            consumer_key = os.environ.get("CONSUMER_KEY"),
            consumer_secret = os.environ.get("CONSUMER_SECRET"))
        auth.set_access_token(
            key = os.environ.get("ACCESS_TOKEN"),
            secret = os.environ.get("TOKEN_SECRET"))

        self.api = tweepy.API(auth, wait_on_rate_limit = True)
        JST = dt.timezone(dt.timedelta(hours=+9), "JST")
        self.JST = dt.datetime.now(JST)

    def get_tweets(self):
        return self.api.home_timeline(count = 10, since_id = None)

    def tweet(self):
        status = "お天気観測してるポワ"
        self.api.update_statue(statue = status)
    
    def change_icon(self, form):
        if form == "normal":
            image = "../../normal.png"
        elif form == "rainy":
            image = "../../rainy.png"
        elif form == "sunny":
            image = "../../sunny.png"
        elif form == "snowy":
            image = "../../snowy.png"
        self.api.update_profile_image(image)

    # def description2japanese(self, description):
    #     trans = {
    #         "clear sky" : "快晴",
    #         "few clouds" : "晴れ",
    #         "scattered clouds" : "曇り",
    #         "broken clouds" : "曇り",
    #         "shower rain" : "小雨",
    #         "rain" :  "雨",
    #         "thunderstrom" : "雷雨",
    #         "snow" : "雪",
    #         "mist" : "霧"
    #     }
    #     return trans[description]

    def tweet_weather_forecast_morning(self, city = "kyoto"):
        data = get_weather.current_and_forecasts_weather_bycity(city)
        today_weather = {}
        for hourly_data in data["hourly"]:
            time = dt.datetime.fromtimestamp(hourly_data["dt"])
            if time.day == self.JST.day:
                today_weather[time.hour] = hourly_data["weather"][0]["description"]
        """
        朝は8:00 ~ 12:00まで
        夜は20:00 ~ 24:00に１時間に一回ずつ天気予報を呟く
        朝は今日の天気を
        夜は明日の天気を呟く
        """
        status = "{}年{}月{}日の京都のお天気をお伝えするポワ\n".format( \
            self.JST.year, \
            self.JST.month, \
            self.JST.day \
        ) + \
        "お昼頃は{}で,\n".format(today_weather[12]) + \
        "その後{}となる予定ですポワ\n".format(today_weather[15]) + \
        "また，夜には{}となりますポワ.".format(today_weather[18]) # 18時
        self.api.update_statue(status = status)
        
    def tweet_weather_forecast_night():
        pass
        # status = "明日の天気は"
        # 朝の天気
        # 昼の天気
        # 夜の天気

def main():
    powarun = Powarun()
    # public_tweet = powarun.get_tweets()
    powarun.tweet_weather_forecast_morning()
    # print(public_tweet)


if __name__ == "__main__":
    main()