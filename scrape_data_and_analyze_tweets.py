import sys
import csv
import datetime
import logging
import re
import twint
from langdetect import DetectorFactory, detect

user_activity = {}

#######################################################################
########################## CUSTOM EXCEPTIONS ##########################
#######################################################################
class TweetlanguageNotEnglish(Exception):
    pass

#######################################################################
######################## FUNCTION DEFINITIONS #########################
#######################################################################

# TODO: add error handling?!
def get_follower_count_for_user(username):
    followers_if_existing = USER_FOLLOWERS.get(username)
    if followers_if_existing != None:
        return followers_if_existing
    else:
        # we need to scrape the information from twitter
        c = twint.Config()
        c.Username = username
        c.Store_object = True
        twint.run.Lookup(c)
        follower_count = twint.output.users_list[0].followers
        USER_FOLLOWERS[username] = follower_count
        return follower_count

def init_user_activity():
    for row in ALL_TWEETS_DATA:
        user_for_curr_tweet = row['username']
        curr_tweet_count_for_user = user_activity.get(user_for_curr_tweet)
        # first tweet we process from that user
        if curr_tweet_count_for_user is None:
            user_activity[user_for_curr_tweet] = 1
        # add one to current tweet count from the user
        else:
            user_activity[user_for_curr_tweet] += 1

def get_user_activity_for_user(username):
    return user_activity.get(username)

#TODO: implement
def clean_tweet(tweet):
    original_tweet = tweet
    # convert to lowercase

    # remove all email adresses
    tweet = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", '', tweet)
    return NotImplemented

#TODO: implement
def get_retweet_delay_for_tweet(row):
    return NotImplemented

#TODO: implement
def queue_output_for_row(data):
    return NotImplemented
#######################################################################
############################# MAIN SCRIPT #############################
#######################################################################

# Language detection algorithm is non-deterministic,
# which means that if you try to run it on a text which is either too short or too ambiguous,
# you might get different results everytime you run it.
DetectorFactory.seed = 0

INPUT_FILE = sys.argv[1]
OUTPUT_FILE_ALL = sys.argv[2]
OUTPUT_FILE_TWEETS = sys.argv[2]

logging.basicConfig(level=logging.DEBUG,
                    filename='finalize_data.log',
                    filemode='a',
                    format='%(asctime)s - %(levelname)s - %(message)s')

init_user_activity()

INPUT_FIELDNAMES = ['id',
                    'conversation_id',
                    'date',
                    'time',
                    'timezone',
                    'user_id',
                    'username',
                    'name',
                    'tweet',
                    'mentions',
                    'urls',
                    'photos',
                    'replies_count',
                    'retweets_count',
                    'likes_count',
                    'hashtags',
                    'link',
                    'quote_url',
                    'video',
                    'thumbnail',
                    'source',
                    'user_rt_id',
                    'user_rt',
                    'retweet_id',
                    'reply_to',
                    'retweet_date']

OUTPUT_FIELD_NAMES = ['tweet']
ALL_TWEETS_DATA = []
USER_FOLLOWERS = {}
OUTPUT_DATA_TWEETS = []
OUTPUT_DATA_ALL = []

with open(INPUT_FILE, 'r', newline='') as i:
    INPUT_READER = csv.DictReader(i, fieldnames=INPUT_FIELDNAMES, delimiter=',')

    # read everything into main memory for easier aggregation of user data
    for row in INPUT_READER:
        ALL_TWEETS_DATA.append(row)

    # process each tweet
    for row in ALL_TWEETS_DATA:
        curr_user = row['username']

        # a url is contained
        if row['urls'].strip() != '':
            urls = 1
        else:
            urls = 0

        # TODO: handle not english exception
        # TODO: gracefully handle other problems while cleaning
        cleaned_tweet = clean_tweet(row['tweet'])

        user_follower_count_for_row = get_follower_count_for_user(curr_user)
        user_activity_count_for_row = get_user_activity_for_user(curr_user)
        if int(row['retweets_count'].strip()) != 0:
            retweet_delay = get_retweet_delay_for_tweet(row)
        else:
            # convention
            retweet_delay = 0

        # TODO: give dict
        queue_output_for_row()

# write output with main data for later analysis
with open(OUTPUT_FILE_ALL, 'w', newline='') as o_all:
    ALL_WRITER = csv.DictWriter(o_all, fieldnames=output_all_fields, delimiter=',')
    ALL_WRITER.writerows(OUTPUT_DATA_ALL)

# write output with tweets to reuse in sentistrength
with open(OUTPUT_FILE_TWEETS, 'w', newline='') as o_tweets:
    TWEETS_WRITER = csv.DictWriter(o_tweets, fieldnames=OUTPUT_FIELD_NAMES, delimiter=',')
    TWEETS_WRITER.writerows(OUTPUT_DATA_TWEETS)
