import sys
import csv
import datetime
import logging
import twint
from langdetect import DetectorFactory, detect

# Language detection algorithm is non-deterministic,
# which means that if you try to run it on a text which is either too short or too ambiguous,
# you might get different results everytime you run it.
DetectorFactory.seed = 0

logging.basicConfig(level = logging.DEBUG, filename = 'finalize_data.log', filemode = 'a', format = '%(asctime)s - %(levelname)s - %(message)s')

input_fieldnames = ['id', 
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

with open(input_file, 'r', newline = '') as i:
    input_reader = csv.DictReader(i, fieldnames = input_fieldnames, delimiter = ',')
    with open(output_file_all, 'w', newline = '') as o_all:
        all_writer = csv.DictWriter()
        with open(output_file_tweets, 'w', newline = '') as o_tweets:
            tweets_writer = csv.DictWriter()
            

