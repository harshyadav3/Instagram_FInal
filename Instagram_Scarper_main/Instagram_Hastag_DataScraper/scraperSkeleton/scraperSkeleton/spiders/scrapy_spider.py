import scrapy
import time
import login
import parameter
from ..items import QuotesItem
import pandas as pd
import instaloader
class QuotesSpider(scrapy.Spider):
    # Enter your Scrapy Spider name
    name = "InstagramCrawler"
    AUTOTHROTTLE_ENABLED = True
    AUTOTHROTTLE_START_DELAY = 10
    # Enter the web domain which have to scrape
    allowed_domains = ["instagram.com"]
    handle_httpstatus_list = [999]
    # This function will call the login function and then parse function
    def start_requests(self):
        # login() calling function and returns CursorObject
        cursorObject = login.login()
        # Iterating over all the post avaiable on given Instagram Hashtag
        for post in cursorObject.get_hashtag_posts(parameter.Instagram_Hashtag):
            time.sleep(3)
            url1 = f"https://www.instagram.com/p/{post.shortcode}/"
            yield scrapy.Request(url1, callback=self.parse, cb_kwargs={'post': post})
    # data parsing function which will be scraped from the website.
    def parse(self, response, post):
        Data = []
        print(response.url)  # Print URL of the Post
        postLikes = post.get_likes()  # Extract no of likes in each Post
        postComment = post.get_comments()  # Extract no of comment in each Post
        items = QuotesItem()
        commentList = []  # in commentList variable we are getting name of the person who commented on post
        for comment in postComment:
            commentList.append(comment.owner.username)
        for profile in postLikes:
            var1 = 0
            for x in commentList:
                if (x == profile.username):
                    var1 = 1
                    print("Username:", profile.username)
            parsedData = {
                'Username': profile.username,
                'Fullname': profile.full_name,
                'Followers': profile.followers,
                'Following': profile.followees,
                'Biography': profile.biography,
                'Private': profile.is_private,
                'Verify': profile.is_verified,
                'Noposts': profile.mediacount,
                'Liked': "TRUE",
                'comment': bool(var1)
            }
            Data.append(parsedData)
            df = pd.DataFrame(Data)
            df.to_csv('hashtag1.csv', index=False)
            yield items
