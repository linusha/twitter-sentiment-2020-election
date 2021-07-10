# Small helper script that exports one row of data for analysis on another computer
setwd('~/twitter-sentiment-2020-election/')
tweet_data <- read.csv('complete_data.csv')
cleaned_tweets <- tweet_data$clean_tweet
write.csv(cleaned_tweets, 'clean_tweets.csv')