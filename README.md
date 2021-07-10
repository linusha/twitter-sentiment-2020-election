# twitter-sentiment-2020-election

This repository contains code and data used for a conceptual replication of "Emotions and Information Diffusion in Social Media - Sentiment of Microblogs and Sharing Behavior" (Stieglitz, Dang-Xuan. 2013).

All code is under MIT license. Please note that all data herein, figures and texts that are part of the data analysis are extempt to this.

## Process

The following paragraphs should give you a good overview of how to use the scripts in this repository given previous exposure to the command line, python and R. They are focused more on the how than the why. Please see the corresponding publication for further details.

### Collecting data

The relevant files are contained in the `/collection` directory.
The queries contained in the corresponding file in this repository were run using [`twint`](https://pypi.org/project/twint/) in version 2.1.22.
This produces two .csv files for each hashtag (they can be found separately in keywords.txt as well), one per day at which data was scraped.

Afterwards, run `filter_tweets.py` for all these files. This will discard tweets that are actually retweets and should not have been scraped as well as tweets that were not made on election day in any mainland US timezone. For each input file one output file will be produces, according to the arguments given when calling the script. A file named `cleaning.log` must exist in the same directory the script is run from.
Some unused rows are already omitted by this. A `tab` separated file is assumed as input. The output will be a `,` separated one.

For the six resulting `.csv` files, the following was executed in a shell:

```sh
awk '!a[$0]++' *.csv.clean > deduplicated_tweets.csv.clean
```

This results in a single file containing all collected tweets with exact data duplicates removed.

This file can now be used as input for the `clean_and_process_tweets.py` script. It will generate some of the features used in the later analysis, filter for non-english tweets and also output different versions of the original tweets. Please note, that we only used the so called *clean* tweets in the end.
For this step, the `process_tweets` step of the provided Makefile can be used.
