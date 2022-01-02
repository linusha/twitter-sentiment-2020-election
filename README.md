# twitter-sentiment-2020-election


## Process Documentation

The following paragraphs should give you a good overview of how to use the scripts in this repository given previous exposure to the command line, `python` and `R`. Please see the corresponding publication for further details. This repository utilizes [Git Large File Storage](https://git-lfs.github.com/).

Following the steps outlined below should allow you to replicate our findings, beginning with the collection of tweets.
Please be aware that the availability of tweets might have changed since we collected the original data set.
For entry-point ready data-sets, please take a look at the "Data" section below.

Please note, that this code makes some assumptions about naming schemes, directory structures, ... that might be not documented.
Therefore, changes to the code will be necessary in order to run it successfully. We sincerely hope that this does not affect things other than paths and filenames.

Please reach out with any questions directly or open a ticket in this repository.

### Collecting Data

The relevant files are contained in the `/collection` directory.
The queries contained in the corresponding file in this repository were run using [`twint`](https://pypi.org/project/twint/) in version `2.1.22`.
This produces two .csv files for each hashtag (they can be found separately in keywords.txt as well), one per day at which data was scraped.

Afterwards, run `filter_tweets.py` for all these files. This will discard tweets that are actually retweets and should not have been scraped as well as tweets that were not made on election day in any mainland US timezone. For each input file one output file will be produced, according to the arguments given when calling the script. A file named `cleaning.log` must exist in the same directory the script is run from. For convenience, an empty one is already present after cloning the repository.
Some unused rows returned by `twint` will be omitted by this script. A tab-separated file is assumed as input. The output will be a comma-separated one.

For the six resulting `.csv` files, the following was executed in a shell:

```sh
awk '!a[$0]++' *.csv.clean > deduplicated_tweets.csv.clean
```

This results in a single file containing all collected tweets with exact data duplicates removed.

This file can now be used as input for the `clean_and_process_tweets.py` script. It will generate some of the features used in the later analysis, filter for non-english tweets and also output different versions of the original tweets. Please note, that we only used the so called *clean* tweets in the end.
For this step, the `process_tweets` target of the provided Makefile can be used.

### Sentiment Analysis Using SentiStrength

SentiStrength can be acquired from the [official website](http://sentistrength.wlv.ac.uk/). Then, the `sentiment` target of the Makefile can be executed.
Afterwards, the `process_sentiment` target of the Makefile will execute the `process_sentiment.py` script for all of the SentiStrength output files produced previously. There exists a `senti` target in the Makefile that combines both of these steps. The python script will execute some calculations and transformations to derive features used in the later analysis. The script can be found in the `/sentiment_senti-strength` directory.

### Analysis Using LIWC2015

LIWC can be acquired from the [official website](http://liwc.wpengine.com/).
Merge the data that resulted from the above steps using the interactive `merge_data.rmd` script located in `/liwc`. This will produce a single `.csv` file. The `clean_tweets` column of this file can now be exported as a single column. There is a helper script available called `export_clean_tweets.r`.
The clean_tweets can then be analyzed with LIWC. This will produce a separate `.csv` file.

### Dealing With Highly Relevant Accounts

To take into account the impact large amounts of followers have on subsequent engagement with tweets, we treated tweets from influential people specially.
For this, the `mark_famous_tweets.rmd` script can be used. All necessary files are already present in the `/relevant_accounts` directory. Otherwise they could be generated using the `socialbakers_conversion.rmd` script. Please note, that you need to extract the usernames of tweet authors from a previously generated file using `extract_names.rmd`, if you used the code as it is provided here. We assume extraction from the file produced by `awk` in the "Collecting Data" step.
Depending on your goal, it might be advisable to either keep the usernames longer or to prepone this step.

### Final Merging and Modelling

Scripts can be found in the `/analysis` directory. First, step through `feature_creation.rmd`.
Note, that not every step was used for the final pulication.
Step through `filtering.rmd`. Afterwards, the data processing has been completed.
Code for the models that we report on in our paper can be found in `modelling.rmd`.

## Data

We provide the data-set we used for modelling as `.RData` as well as the original tweet data-set we collected.
Please note, that the data we used for modelling is not easily matchable to the original tweets.

Both files can be found in the `data` directory. The `.RData` file can simply be loaded into an `R` environment and should allow you to start directly with the modelling step.

Because of the Twitter TOS, you need to hydrate the original data-set of tweets we collected yourself. For this you will need a Twitter API key. Suitable tools for hydrating the data are [`hydator`](https://github.com/DocNow/hydrator) (GUI) or [`twarc`](https://github.com/DocNow/twarc) (`python`).
In case you need additional data or help, please feel free to reach out.

The code used to provide this data in addition to the above described steps can be found in the `/export` directory.

## License

Copyright © 2021 Linus Hagemann, Olga Abramova.

All code is published under the MIT license.

Our data-sets are made available under the [Open Data Commons Attribution License](http://opendatacommons.org/licenses/by/1.0/)
