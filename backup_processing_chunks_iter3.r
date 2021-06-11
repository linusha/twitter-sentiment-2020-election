```{r include=FALSE, eval=FALSE}
tweet_data <- read.csv('final_data.csv')
# mistake in a function, we will use the correct famous levels
tweet_data$isFamous <- NULL
tweet_data$fameLevel <- NULL
tweet_data <- cbind(tweet_data, tweet_famous_level)
# preparing subsample of famous tweets
famous_tweet_data <- tweet_data[tweet_data$isFamous == 1,]
```
```{r include=FALSE, eval=FALSE}
#make the data frame easier to work with
tweet_data <- tweet_data[,c('hashtags',
                            'url',
                            'likes',
                            'retweets',
                            'replies',
                            "user_activity",
                            "clean_tweet",
                            "ct_positiveScore",
                            "ct_negativeScore",
                            "ct_polarity",
                            "ct_sentiment",
                            "ct_isNegative",
                            "ct_interactionTerm",
                            "log_user_activity",
                            "cleanLIWC_WC",
                            "cleanLIWC_i",
                            "cleanLIWC_we",
                            "cleanLIWC_they",
                            "cleanLIWC_posemo",
                            "cleanLIWC_negemo",
                            "cleanLIWC_insight",
                            "cleanLIWC_cause",
                            "cleanLIWC_discrep",
                            "cleanLIWC_certain",
                            "hashtagCount",
                            "charLength",
                            "ct_negative_interaction",
                            "ct_positive_interaction",
                            "ct_negativeScoreToUse",
                            "sentences",
                            "syllables",
                            "flesch",
                            "isFamous",
                            "fameLevel")]
tweet_data <- complete.cases(tweet_data)
tweet_data$liked <- ifelse(tweet_data$likes != 0, TRUE, FALSE)
tweet_data$retweeted <- ifelse(tweet_data$retweets != 0, TRUE, FALSE)
tweet_data$repliedTo <- ifelse(tweet_data$replies != 0, TRUE, FALSE)
tweet_data$ct_polarity <- tweet_data$ct_polarity + 4
tweet_data <- na.omit(tweet_data)
tweet_data$syllables <- NULL
tweet_data$fameLevel <- as.factor(tweet_data$fameLevel)
famous_tweet_data <- tweet_data[tweet_data$isFamous == 1,]
```