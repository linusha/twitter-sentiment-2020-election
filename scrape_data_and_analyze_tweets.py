import sys
import csv
import datetime
import logging
import re
import string
import pdb
import twint
from langdetect import DetectorFactory, detect
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer

print('Script started.')
if (len(sys.argv) == 5):
    RESUME_MODE = True
    RESUME_COUNTER = sys.argv[5]
else:
    RESUME_MODE = False

USER_ACTIVITY = {}
OUTPUT_FIELDS_ALL = ['hashtag',
                     'url',
                     'likes',
                     'retweets',
                     'replies',
                     'activity',
                     'timedelay'
                    ]
ALL_TWEETS_DATA = []
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

def remove_urls_from_text(text):
    return re.sub(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]'
                  r'\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|'
                  r'https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]+\.[^\s]{2,}|www\.'
                  r'[a-zA-Z0-9]+\.[^\s]{2,})', '', text)
    
def init_user_activity():
    for entry in ALL_TWEETS_DATA:
        user_for_curr_tweet = entry['username']
        curr_tweet_count_for_user = USER_ACTIVITY.get(user_for_curr_tweet)
        # first tweet we process from that user
        if curr_tweet_count_for_user is None:
            USER_ACTIVITY[user_for_curr_tweet] = 1
        # add one to current tweet count from the user
        else:
            USER_ACTIVITY[user_for_curr_tweet] += 1

def get_user_activity_for_user(username):
    activity = USER_ACTIVITY.get(username)
    if activity >= 1:
        return activity
    else:
        # since this is only dependent on our already scraped data
        # this should never happen!
        raise InvalidUserActivityException

def clean_tweet(tweet):
    # convert to lowercase
    tweet = tweet.lower()
    # remove all email adresses
    tweet = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", '', tweet)
    #remove all urls
    tweet = remove_urls_from_text(tweet)
    # remove hashtags but preserve words
    tweet = tweet.replace('#', '')

    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
    stmmr = PorterStemmer()
    tweet_tokens = tknzr.tokenize(tweet)
    tweet_cleaned = []
    for token in tweet_tokens:
        stemmed_token = stmmr.stem(token)
        tweet_cleaned.append(stemmed_token)
    tweet_cleaned = ' '.join(tweet_cleaned)
    if detect(tweet_cleaned) != 'en':
        raise TweetLanguageNotEnglishException
    return tweet_cleaned

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
OUTPUT_FILE_DATA = sys.argv[2]
OUTPUT_FILE_TWEETS_ORIG = sys.argv[3]
OUTPUT_FILE_TWEETS_CLEAN = sys.argv[4]

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

print('Beginning to read data from input file.')
with open(INPUT_FILE, 'r', newline='') as i:
    INPUT_READER = csv.DictReader(i, fieldnames=INPUT_FIELDNAMES, delimiter=',')

    # read everything into main memory for easier aggregation of user data
    for row in INPUT_READER:
        ALL_TWEETS_DATA.append(
            {
                'date': row['date'],
                'time': row['time'],
                'username': row['username'],
                'tweet': row['tweet'],
                'urls': row['urls'],
                'retweets_count': row['retweets_count'],
                'likes_count': row['likes_count'],
                'replies_count': row['replies_count'],
                'hashtags': row['hashtags']
            }
        )
    i.close()
print('Read data from input file. Read %d entries.', len(ALL_TWEETS_DATA))

print('Begin to aggregate user activities.')
init_user_activity()
print('Finished to aggregate user activities.')

print('Begin scraping user data')
# process each tweet
while ALL_TWEETS_DATA:
    ROW = ALL_TWEETS_DATA.pop(0)
    CURR_USER = ROW['username']

    # a url is contained
    if ROW['urls'].strip() != '':
        URLS = 1
    else:
        URLS = 0

    # a hashtag is contained
    if ROW['hashtags'].strip() != '':
        HASHTAGS = 1
    else:
        HASHTAGS = 0

    try:
        CLEANED_TWEET = clean_tweet(ROW['tweet'])
    except TweetLanguageNotEnglishException:
        logging.error('Tweet: %s was not detected as english.', ROW['tweet'])
        print('Tweet discarded due to language.')
        continue

    try:
        USER_ACTIVITY_COUNT_FOR_ROW = get_user_activity_for_user(CURR_USER)
    except InvalidUserActivityException:
        logging.fatal('Activity for user %s could not be retrieved!', CURR_USER)
        # this indicates a problem on our side, we need to investigate!
        sys.exit(1)

    output_for_row = ({
        'orig_tweet': ROW['tweet'],
        'clean_tweet': CLEANED_TWEET,
        'hashtag': HASHTAGS,
        'url': URLS,
        'likes': ROW['likes_count'],
        'retweets': ROW['retweets_count'],
        'replies': ROW['replies_count'],
        'followers': USER_FOLLOWER_COUNT_FOR_ROW,
        'activity': USER_ACTIVITY_COUNT_FOR_ROW,
        'timedelay': RETWEET_DELAY,
        'all_tweets': USER_TWEET_COUNT_FOR_ROW,
    })

    # write output with all data except tweet
    with open(OUTPUT_FILE_ALL, 'a', newline='') as o_all:
        ALL_WRITER = csv.DictWriter(o_all, fieldnames=OUTPUT_FIELDS_ALL, delimiter=',')
        ALL_WRITER.writerow(output_for_row)

    # write output with tweets in same order as the other data
    with open(OUTPUT_FILE_TWEETS_ORIG, 'a', newline='') as o_tweets:
        TWEETS_WRITER = csv.DictWriter(o_tweets, fieldnames=['tweet'], delimiter=',')
        TWEETS_WRITER.writerow({'tweet': output_for_row['tweet']})

    with open(OUTPUT_FILE_TWEETS_CLEAN, 'a', newline='') as o_tweets:
        TWEETS_WRITER = csv.DictWriter(o_tweets, fieldnames=['tweet'], delimiter=',')
        TWEETS_WRITER.writerow({'tweet': output_for_row['clean_tweet']})

o_all.close()
o_tweets.close()