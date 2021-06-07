# Small helper script that exports one row of data for analysis on another computer
library('here')
here()
tweet_data <- read.csv(here('complete_data.csv'))
cleaned_tweets <- tweet_data$clean_tweet
write.csv(cleaned_tweets, here('clean_tweets.csv'))