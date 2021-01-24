# process

1. For each **file** run: `sed -i $'s/\t/, /g' file` to convert the csv from `tab` style to being separated by `,` 
2. Run `filter_tweets.py` for all files.
3. Remove duplicate tweets and merge all tweets in a single `.csv` file
4. Enrich tweets with additional data that needs to get scraped
5. analyze sentiment of all tweets

## `filter_and_clean_tweets.py`

Deletes tweets from a file that do not fulfill the following criteria:

- language is en in the twint collumn
- tweet was not made on 03.11 in mainland USA time
    - tweets scraped by twint are for GMT+0 (so GMT+0 the complete day is scraped) but GMT+1 is the time displayed
    - we want to keep tweets made between 03.11 04:00 GMT+1 and 04.11 07:00 GMT+1

For tweets that remain in the sample the following columns are omitted:

- place
- language
- cashtag,
- near 
- geo
- translate
- trans_src
- trans_dest

### Plausibility check: languages:

- check the rate for which `langdetect` classifies all remaining tweets as english

## remove duplicate tweets 

`awk '!a[$0]++' file1.cvs file2.cvs`

