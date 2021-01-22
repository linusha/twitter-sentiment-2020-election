# process

1. For each **file** run: `sed -i $'s/\t/, /g' file` to convert the csv from `tab` style to being separated by `,` 
2. Run `filter_tweets.py` for all files.
3. Remove duplicate tweets and merge all tweets in a single `.csv` file
4. Enrich tweets with additional data that needs to get scraped
5. analyze sentiment of all tweets

## `filter_and_clean_tweets.py`

Deletes tweets from a file that do not fulfill the following criteria:

- language is en in the twint collumn
- language is not detected as english by `langdetect`
- tweet was not made on 03.11 in mainland USA time
    - tweets scraped by twint are for GMT+0
    - we want to keep tweets made between 03.11 05:00 GMT and 04.11 08:00 GMT

For tweets that remain in the sample the following columns are omitted:

- place
- language
- cashtag,
- near 
- geo
- translate
- trans_src
- trans_dest

## remove duplicate tweets 

`awk '!a[$0]++' file1.cvs file2.cvs`

