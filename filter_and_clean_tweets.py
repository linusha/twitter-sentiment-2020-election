import sys
import csv
import datetime
import logging
from langdetect import DetectorFactory, detect

# Language detection algorithm is non-deterministic,
# which means that if you try to run it on a text which is either too short or too ambiguous,
# you might get different results everytime you run it.
DetectorFactory.seed = 0

input_file = sys.argv[1]
output_file = sys.argv[2]

logging.basicConfig(level = logging.DEBUG, filename = 'cleaning.log', filemode = 'a', format = '%(asctime)s - %(levelname)s - %(message)s')

input_fieldnames = ['id', 
    'conversation_id',
    'created_at',
    'date',
    'time',
    'timezone',
    'user_id',
    'username',
    'name',
    'place',
    'tweet',
    'language',
    'mentions',
    'urls',
    'photos',
    'replies_count',
    'retweets_count',
    'likes_count',
    'hashtags',
    'cashtags',
    'link',
    'retweet',
    'quote_url',
    'video',
    'thumbnail',
    'near',
    'geo',
    'source',
    'user_rt_id',
    'user_rt',
    'retweet_id',
    'reply_to',
    'retweet_date',
    'translate',
    'trans_src',
    'trans_destid']

output_fieldnames = ['id', 
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
    input_reader = csv.DictReader(i, fieldnames = input_fieldnames, delimiter = '\t')
    with open(output_file, 'w', newline = '' ) as o:
        output_writer = csv.DictWriter(o, fieldnames = output_fieldnames, delimiter = ',')
        tweet_counter = 0
        qualifying_tweets_counter = 0
        # count how many tweets would be detected as english by langdetect
        lang_detect_counter = 0
        for row in input_reader:
            # skip header line with column names
            if (row['id'] == 'id'):
                continue
            tweet_counter += 1
            logging.info('Cleaning tweet {} in file {}.'.format(tweet_counter, output_file))
            # only process english tweets further
            if (row['language'] == 'en'):
                # due to time difference we want to discard everything later than 7am
                if (row['date'] == '2020-11-04'):
                    if (int(row['time'][:2])>=7):
                        logging.warning('Discarding tweet {} since it was made too late on 11-04.'.format(tweet_counter))
                        continue
                # due to time difference we want to discard everything earlier than 4am
                elif (row['date'] == '2020-11-03'):
                    if (int(row['time'][:2])<4):
                        logging.warning('Discarding tweet {} since it was made too early on 11-03.'.format(tweet_counter))
                        continue
                # do not process retweets
                if (row['retweet'] == 'False'):
                    # if we get here the tweets qualifies for the data set and will be written to the output
                    qualifying_tweets_counter += 1

                    detected_language = detect(row['tweet'])
                    if(detected_language == 'en'):
                        lang_detect_counter += 1
                    else:
                        logging.debug('Tweet: \'{}\' was not detected as english but as {}.'.format(row['tweet'], detected_language))

                    
                    output_writer.writerow({'id': row['id'],
                    'conversation_id': row['conversation_id'],
                    'date': row['date'],
                    'time': row['time'],
                    'timezone': row['timezone'],
                    'user_id': row['user_id'],
                    'username': row['username'],
                    'name': row['name'],
                    'tweet': row['tweet'],
                    'mentions': row['mentions'],
                    'urls': row['urls'],
                    'photos': row['photos'],
                    'replies_count': row['replies_count'],
                    'retweets_count': row['retweets_count'],
                    'likes_count': row['likes_count'],
                    'hashtags': row['hashtags'],
                    'link': row['link'],
                    'quote_url': row['quote_url'],
                    'video': row['video'],
                    'thumbnail': row['thumbnail'],
                    'source': row['source'],
                    'user_rt_id': row['user_rt_id'],
                    'user_rt': row['user_rt'],
                    'retweet_id': row['retweet_id'],
                    'reply_to': row['reply_to'],
                    'retweet_date': row['retweet_date']})
                else:
                    logging.warning('Discarding tweet {} since it is a retweet.'.format(tweet_counter))
            else:
                logging.warning('Discarding tweet {} since it is not english.'.format(tweet_counter))
        print('Of {} tweets in file {}, {} would have been detected as english by langdetect.'.format(tweet_counter, input_file, lang_detect_counter))
        
