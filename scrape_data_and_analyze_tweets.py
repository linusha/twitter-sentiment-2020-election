import sys
import csv
import datetime
import logging
import re
import twint
import string
from langdetect import DetectorFactory, detect
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer

user_activity = {}
OUTPUT_FIELDS_TWEETS = ['tweet']
OUTPUT_FIELDS_ALL = ['orig_tweet',
                     'clean_tweet',
                     'hashtag',
                     'url',
                     'likes',
                     'retweets',
                     'followers',
                     'activity',
                     'timedelay']
ALL_TWEETS_DATA = []
USER_FOLLOWERS = {}
OUTPUT_DATA_TWEETS = []
OUTPUT_DATA_ALL = []
TRANSLATE_TABLE = dict((ord(char), None) for char in string.punctuation)

#######################################################################
########################## CUSTOM EXCEPTIONS ##########################
#######################################################################
class TweetLanguageNotEnglishException(Exception):
    pass

class NoRetweetsFoundException(Exception):
    pass

class UserInfoNotFoundException(Exception):
    pass

class InvalidUserActivityException(Exception):
    pass

#######################################################################
######################## FUNCTION DEFINITIONS #########################
#######################################################################

def remove_urls_from_string(string):
    return re.sub(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]'
                  r'\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|'
                  r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.'
                  r'[a-zA-Z0-9]+\.[^\s]{2,})', '', string)

def get_follower_count_for_user(username):
    followers_if_existing = USER_FOLLOWERS.get(username)
    if followers_if_existing != None:
        return followers_if_existing

    # we need to scrape the information from twitter
    c = twint.Config()
    c.Username = username
    c.Store_object = True
    twint.run.Lookup(c)
    follower_count = twint.output.users_list[0].followers
    if not follower_count:
        raise UserInfoNotFoundException
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
    activity = user_activity.get(username)
    if activity >= 1:
        return activity
    else:
        # since this is only dependent on our already scraped data
        # this should never happen!
        raise InvalidUserActivityException 

def clean_tweet(tweet):
    original_tweet = tweet
    # convert to lowercase
    tweet = tweet.lower()
    # remove all email adresses
    tweet = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", '', tweet)
    #remove all urls
    tweet = remove_urls_from_string(tweet)

    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
    stmmr = PorterStemmer()
    tweet_tokens = tknzr.tokenize(tweet)
    tweet_cleaned = []
    for token in tweet_tokens:
        stemmed_token = stmmr.stem(token)
        tweet_cleaned.append(stemmed_token)
    ' '.join(tweet_cleaned)
    if detect(tweet_cleaned) != 'en':
        raise TweetLanguageNotEnglishException
    return tweet_cleaned

# this functions returns the difference between the post time of a tweet
# and its first retweet in seconds
def get_retweet_delay_for_tweet(row):
    tweet = row['tweet']
    # remove emails, since they lead to emtpy twitter search results
    tweet_clean = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", '', tweet)
    # remove urls as well as a safety measure
    tweet_clean = remove_urls_from_string(tweet_clean)
    c = twint.Config()
    c.Search = tweet_clean
    c.Native_retweets = True
    c.Store_object = True
    retweets_of_row_tweet = []
    c.Store_object_tweets_list = retweets_of_row_tweet
    twint.run.Search(c)

    minimal_date = ''
    minimal_time = ''
    if not retweets_of_row_tweet:
        raise NoRetweetsFoundException

    for tweet in retweets_of_row_tweet:
        if minimal_date is None or minimal_date >= tweet['datestamp']:
            if minimal_time is None or minimal_time >= tweet['timestamp']:
                minimal_time = tweet['timestamp']
                minimal_date = tweet['datestamp']
    retweet_delay = convert_strs_to_time(minimal_date, minimal_time) - convert_strs_to_time(row['datestamp'], row['timestamp'])
    return retweet_delay.total_seconds()

# converts two strings into a single datetime object
def convert_strs_to_time(date_str, time_str):
    y = int(date_str[:4])
    m = int(date_str[5:7])
    d = int(date_str[8:])
    h = int(time_str[:2])
    mi = int(time_str[3:5])
    s = int(time_str[6:8])
    return datetime(year=y, month=m, day=d, hour=h, minute=mi, second=s)



def queue_output_for_row(data):
    OUTPUT_DATA_ALL.append({'tweet': data['clean_tweet']})
    OUTPUT_DATA_ALL.append(data)

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

        # a hashtag is contained
        if row['hashtags'].strip() != '':
            hashtags = 1
        else:
            hashtags = 0

        try:
            cleaned_tweet = clean_tweet(row['tweet'])
        except TweetLanguageNotEnglishException:
            logging.error('Tweet: \'{}\' was not detected as english.'.format(row['tweet']))
            continue

        try:
            user_follower_count_for_row = get_follower_count_for_user(curr_user)
        except UserInfoNotFoundException:
            logging.error('Follower Info for \'{}\' could not be scraped.'.format(curr_user))
        
        try:
            user_activity_count_for_row = get_user_activity_for_user(curr_user)
        except InvalidUserActivityException:
            logging.fatal('Activity for user \'{}\' could not be retrieved!'.format(curr_user))
            # this indicates a problem on our side, we need to investigate!
            sys.exit(1)

        if int(row['retweets_count'].strip()) != 0:
            try:
                retweet_delay = get_retweet_delay_for_tweet(row)
            except NoRetweetsFoundException:
                logging.error('Retweets for \'{}\' could not be scraped.'.format(row['tweet']))
                continue
        else:
            # convention
            retweet_delay = 0

        queue_output_for_row({
            'orig_tweet': row['tweet'],
            'clean_tweet': cleaned_tweet,
            'hashtag': hashtags,
            'url': urls,
            'likes':row['likes_count'],
            'retweets':row['retweets_count'],
            'followers': user_follower_count_for_row,
            'activity': user_activity_count_for_row,
            'timedelay': retweet_delay
            })

# write output with main data for later analysis
with open(OUTPUT_FILE_ALL, 'w', newline='') as o_all:
    ALL_WRITER = csv.DictWriter(o_all, fieldnames=OUTPUT_FIELDS_ALL, delimiter=',')
    ALL_WRITER.writerows(OUTPUT_DATA_ALL)

# write output with tweets to reuse in sentistrength
with open(OUTPUT_FILE_TWEETS, 'w', newline='') as o_tweets:
    TWEETS_WRITER = csv.DictWriter(o_tweets, fieldnames=OUTPUT_FIELDS_TWEETS, delimiter=',')
    TWEETS_WRITER.writerows(OUTPUT_DATA_TWEETS)
