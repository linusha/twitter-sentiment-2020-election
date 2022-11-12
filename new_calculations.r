# This script assumes linewise execution in a "notebook" fashion.
# It is assumed, that your data set is loaded in the R environment (see other files).
# You will need to bring your own data set, as we cannot provide the full data (i.e., including tweet content) online.
# This script might not contain all relevant calculations, but enough context should be provided to reconstruct any missing calculation.
# In some cases, calculations for a specific subsample might be missing as well.

library(stringr)
library(here)
super_famous <- famous_tweet_data[famous_tweet_data$fameLevel == 3,]

media <- read.csv(here('relevant_accounts/media.csv'))
politicians <- read.csv(here('relevant_accounts/politiciancs.csv'))
calebrities <- read.csv(here('relevant_accounts/celebrities.csv'))
# lowercasing all usernames
media$handle <- tolower(media$handle)
politicians$handle <- tolower(politicians$handle)
calebrities$handle <- tolower(calebrities$handle)
famous_people <- rbind(media, politicians, calebrities)

# 1. Calculate Percentage of Singletons and @tweets (Table 3)
length(str_which(super_famous$clean_tweet, "@"))
length(str_which(famous_tweet_data$clean_tweet, "@"))

# Summarizing User Activity (Table 4) 
# `usernames.txt` contains the username of the author for each tweet in the sample.
names <- nroread.csv(here('usernames.txt'), header = FALSE)  
# Users fullfilling criteria
ranking <- names %>% filter(fameLevel == 1 | fameLevel == 2 | fameLevel == 3)
# Individual users fullfilling criteria with number of tweets
ranking <- summarize(group_by(ranking, V1), n = n()) 
# # Individual users fullfilling criteria based on number of tweets
ranking %>% filter (n > 20 & n < 51)
