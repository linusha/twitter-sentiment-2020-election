# process

1. Run `filter_tweets.py` for all files.
2. Remove duplicate tweets and merge all tweets in a single `.csv` file
3. Enrich tweets with additional data that needs to get scraped
4. analyze sentiment of all tweets

## `filter_and_clean_tweets.py`

Deletes tweets from a file that do not fulfill the following criteria:

- language is en in the twint collumn
- tweet was not made on 03.11 in mainland USA time
    - tweets scraped by twint are for GMT+0 (so GMT+0 the complete day is scraped) but GMT+1 is the time displayed
    - we want to keep tweets made between 03.11 04:00 GMT+1 and 04.11 07:00 GMT+1
- retweet = false, e.g., we only want to keep original tweets at this point

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

### Plausibility check: languages:

- check the rate for which `langdetect` classifies all remaining tweets as english

## remove duplicate tweets 

`awk '!a[$0]++' *.csv.clean > deduplicated_tweets.csv.clean`

## enrich data and prepare for analysis



