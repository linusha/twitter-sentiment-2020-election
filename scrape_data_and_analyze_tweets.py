import sys
import csv
import datetime
import logging
import re
import string
from nltk.tokenize import TweetTokenizer
from nltk.stem import PorterStemmer

print('Script started.')

USER_ACTIVITY = {}
OUTPUT_FIELDS_ALL = ['hashtag',
                     'url',
                     'likes',
                     'retweets',
                     'replies',
                     'activity',
                    ]
ALL_TWEETS_DATA = []
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

# https://stackoverflow.com/a/49986645/4418325
def remove_emoji_from_text(text):
    regex = re.compile(pattern = "["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                           "]+", flags = re.UNICODE)
    return regrex_pattern.sub(r'',text)
    
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
    return tweet

def preprocess_tweet(tweet):
    tknzr = TweetTokenizer(strip_handles=True, reduce_len=True, preserve_case=False)
    stmmr = PorterStemmer()
    tweet_tokens = tknzr.tokenize(tweet)
    tweet_preprocesesed = []
    for token in tweet_tokens:
        stemmed_token = stmmr.stem(token)
        tweet_preprocesesed.append(stemmed_token)
    tweet_preprocesesed = ' '.join(tweet_preprocesesed)
    return tweet_preprocesesed

#######################################################################
############################# MAIN SCRIPT #############################
#######################################################################

INPUT_FILE = sys.argv[1]
OUTPUT_FILE_DATA = sys.argv[2]
OUTPUT_FILE_TWEETS_ORIG = sys.argv[3]
OUTPUT_FILE_TWEETS_CLEAN = sys.argv[4]
OUTPUT_FILE_TWEETS_CLEAN_NO_EMOJIS = sys.argv[5]
OUTPUT_FILE_TWEETS_PREPROCESSED = sys.argv[6]

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
print('Read data from input file. Read ' + str(len(ALL_TWEETS_DATA)) + ' entries.')

print('Begin to aggregate user activities.')
init_user_activity()
print('Finished to aggregate user activities.')

# process each tweet
while ALL_TWEETS_DATA:
    ROW = ALL_TWEETS_DATA.pop(0)
    CURR_USER = ROW['username']

    # a url is contained
    if ROW['urls'].strip() != '[]':
        URLS = 1
    else:
        URLS = 0

    # a hashtag is contained
    if ROW['hashtags'].strip() != '[]':
        HASHTAGS = 1
    else:
        HASHTAGS = 0

    CLEANED_TWEET = clean_tweet(ROW['tweet'])
    PEPROCESSED_TWEET = preprocess_tweet(CLEANED_TWEET)
    NO_EMOJI_TWEET = remove_emoji_from_text(CLEANED_TWEET)

    try:
        USER_ACTIVITY_COUNT_FOR_ROW = get_user_activity_for_user(CURR_USER)
    except InvalidUserActivityException:
        logging.fatal('Activity for user %s could not be retrieved!', CURR_USER)
        # this indicates a problem on our side, we need to investigate!
        sys.exit(1)

    data_for_row = ({
        'hashtag': HASHTAGS,
        'url': URLS,
        'likes': ROW['likes_count'],
        'retweets': ROW['retweets_count'],
        'replies': ROW['replies_count'],
        'activity': USER_ACTIVITY_COUNT_FOR_ROW,
    })

    original_tweet_for_row = ({
        'orig_tweet': ROW['tweet'],
    })

    cleaned_tweet_for_row = ({
       'clean_tweet': CLEANED_TWEET,
    })

    preprocessed_tweet_for_row = ({
       'preprocessed_tweet': PEPROCESSED_TWEET,
    })

    no_emoji_tweet_for_row = ({
       'no_emoji_tweet': NO_EMOJI_TWEET,
    })

    # write output with all data except tweet
    with open(OUTPUT_FILE_DATA, 'a', newline='') as o_data:
        DATA_WRITER = csv.DictWriter(o_data, fieldnames=OUTPUT_FIELDS_ALL, delimiter=',')
        DATA_WRITER.writerow(data_for_row)

    # write output with tweets in same order as the other data
    with open(OUTPUT_FILE_TWEETS_ORIG, 'a', newline='') as o_orig_tweets:
        TWEETS_WRITER = csv.DictWriter(o_orig_tweets, fieldnames=['orig_tweet'], delimiter=',')
        TWEETS_WRITER.writerow(original_tweet_for_row)

    with open(OUTPUT_FILE_TWEETS_CLEAN, 'a', newline='') as o_clean_tweets:
        TWEETS_WRITER = csv.DictWriter(o_clean_tweets, fieldnames=['clean_tweet'], delimiter=',')
        TWEETS_WRITER.writerow(cleaned_tweet_for_row)

    with open(OUTPUT_FILE_TWEETS_PREPROCESSED, 'a', newline='') as o_preprocessed_tweets:
        TWEETS_WRITER = csv.DictWriter(o_preprocessed_tweets, fieldnames=['preprocessed_tweet'], delimiter=',')
        TWEETS_WRITER.writerow(preprocessed_tweet_for_row)

    with open(OUTPUT_FILE_TWEETS_CLEAN_NO_EMOJIS, 'a', newline='') as o_no_emojis_tweets:
        TWEETS_WRITER = csv.DictWriter(o_no_emojis_tweets, fieldnames=['no_emoji_tweet'], delimiter=',')
        TWEETS_WRITER.writerow(no_emoji_tweet_for_row)

o_data.close()
o_orig_tweets.close()
o_clean_tweets.close()
o_preprocessed_tweets.close()
o_no_emojis_tweets.close()