# twitter-sentiment-2020-election

This repository contains code and data used for a conceptual replication of "Emotions and Information Diffusion in Social Media - Sentiment of Microblogs and Sharing Behavior" (Stieglitz, Dang-Xuan. 2013).

All code is under MIT license. Please note that all data herein, figures and texts that are part of the data analysis are extempt to this.

## Process

### Collecting data

The queries contained in the corresponding file in this repository were run using `twint` in version 2.1.22.

1. Run `filter__and_clean_tweets.py` for all files.
2. Remove duplicate tweets and merge all tweets in a single `.csv` file

## `filter_and_clean_tweets.py`

Deletes tweets from a file that do not fulfill the following criteria:

- language is en in the twint collumn
- tweet was made on 03.11 in mainland USA time
    - tweets scraped by twint are for GMT+0 (so GMT+0 the complete day is scraped) but GMT+1 is the time displayed
    - we want to keep tweets made between 03.11 04:00 GMT+1 and 04.11 07:00 GMT+1
- retweet = false, i.e., we only want to keep original tweets at this point

For tweets that remain in the sample the following columns are omitted:

- place
- language
- cashtag,
- retweet
- near 
- geo
- translate
- trans_src
- trans_dest

To run the script cleaning.log must exist. The script will convert from a `tab` separated input file to an output file separated by `,`.

## remove duplicate tweets 

`awk '!a[$0]++' *.csv.clean > deduplicated_tweets.csv.clean`



